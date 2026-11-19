import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

from websockets.asyncio.client import connect
from websockets.asyncio.server import serve

from fielddesk import server
from fielddesk.adapters.knowledge import FixtureKnowledge
from fielddesk.adapters.orders import SQLiteOrders
from fielddesk.dispatch import Session


class DispatchTest(unittest.TestCase):
    def test_work_order_requires_readback_and_positive_confirmation(self):
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "orders.sqlite3"
            session = Session(FixtureKnowledge(), SQLiteOrders(db_path))
            self.assertIn("error", session.call("stage_order", {"asset": "P-204", "symptom": "Leak"}))
            self.assertEqual(len(session.call("lookup_asset", {"asset": "p-204"})["records"]), 3)
            pending = session.call("stage_order", {"asset": "P-204", "symptom": "Leak"})["pending"]
            session.transcript = "confirm work order"
            self.assertIn("error", session.call("commit_order", {}))
            session.readback_complete = True
            session.transcript = "don't confirm work order"
            self.assertIn("error", session.call("commit_order", {}))
            self.assertFalse(db_path.exists())
            session.transcript = "वर्क ऑर्डर कन्फर्म करो।"
            receipt = session.call("commit_order", {})
            self.assertEqual(receipt["id"], pending["id"])
            self.assertIn("error", session.call("commit_order", {}))
            with closing(sqlite3.connect(db_path)) as db:
                self.assertEqual(db.execute("SELECT id FROM orders").fetchall(), [(pending["id"],)])


class RehearsalTest(unittest.IsolatedAsyncioTestCase):
    async def test_rehearsal_websocket(self):
        with tempfile.TemporaryDirectory() as directory:
            orders = SQLiteOrders(Path(directory) / "orders.sqlite3")
            with patch.object(server, "ORDERS", orders):
                async with serve(server.handler, "127.0.0.1", 0, process_request=server.serve_page) as listener:
                    address = f"127.0.0.1:{listener.sockets[0].getsockname()[1]}"
                    async with connect(f"ws://{address}/rehearse", origin=f"http://{address}") as socket:
                        for step, expected in (
                            ("confirm", "error"),
                            ("ask", "records"),
                            ("stage", "pending"),
                            ("confirm", "created"),
                        ):
                            await socket.send(json.dumps({"step": step}))
                            self.assertIn(expected, json.loads(await socket.recv())["result"])
                            if expected != "error":
                                self.assertIn("sample", json.loads(await socket.recv()))
                        await socket.send('{"step":"interrupt"}')
                        self.assertTrue(json.loads(await socket.recv())["interrupted"])
