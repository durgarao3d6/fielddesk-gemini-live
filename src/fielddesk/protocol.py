import json


async def emit(ws, **payload):
    await ws.send(json.dumps(payload, ensure_ascii=False))
