import asyncio
import os
from pathlib import Path

from websockets.asyncio.server import serve

from .adapters.gemini import live
from .adapters.knowledge import FixtureKnowledge
from .adapters.orders import SQLiteOrders
from .dispatch import Session
from .protocol import emit
from .rehearsal import rehearsal

PAGE = Path(__file__).resolve().parent / "web" / "index.html"
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-native-audio-preview-12-2025")
KNOWLEDGE = FixtureKnowledge()
ORDERS = SQLiteOrders(Path(os.getenv("FIELDDESK_DB", "orders.sqlite3")))


async def handler(ws):
    session = Session(KNOWLEDGE, ORDERS)
    if ws.request.path == "/rehearse":
        await rehearsal(ws, session)
        return
    if ws.request.path != "/live":
        await ws.close(1008)
        return
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        await emit(ws, error="Set GEMINI_API_KEY on the server to start live voice.")
        return
    try:
        await live(ws, session, key, MODEL)
    except Exception as exc:
        print("Gemini session ended:", type(exc).__name__, flush=True)
        await emit(ws, error="Gemini disconnected. Check the API key, configured model and network, then reconnect.")

async def serve_page(connection, request):
    if request.path in {"/live", "/rehearse"}:
        origin = request.headers.get("Origin", "")
        host = request.headers.get("Host", "")
        if origin not in {"http://"+host, "https://"+host}:
            return connection.respond(403, "Same-origin browser session required.")
        return None
    if request.path == "/":
        response = connection.respond(200, PAGE.read_text(encoding="utf-8"))
        response.headers["Content-Type"] = "text/html; charset=utf-8"
        return response
    return connection.respond(404, "Not found")

async def run():
    port = int(os.getenv("PORT", "8765"))
    async with serve(handler, "127.0.0.1", port, process_request=serve_page):
        print(f"FieldDesk is running at http://localhost:{port}", flush=True)
        await asyncio.Future()


def main():
    asyncio.run(run())
