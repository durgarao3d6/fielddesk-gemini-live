import json

from .protocol import emit


async def rehearsal(ws, session):
    async for raw in ws:
        event = json.loads(raw)
        if event.get("step") == "ask":
            result = session.call("lookup_asset", {"asset":"P-204"})
            await emit(ws, tool="lookup_asset", result=result)
            await emit(ws, sample="P-204 के लिए Store B, bin 07 में दो compatible seal kits हैं। पिछले ticket में भी seal leak था। क्या inspection work order बनाऊँ?")
        elif event.get("step") == "stage":
            result = session.call("stage_order", {"asset":"P-204","symptom":"Reported seal leakage"})
            await emit(ws, tool="stage_order", result=result)
            if "pending" in result:
                session.readback_complete = True
                await emit(ws, sample="P-204 के reported seal leak के लिए mechanical inspection। To approve, say confirm work order.")
        elif event.get("step") == "confirm":
            session.transcript = "confirm work order"
            result = session.call("commit_order", {})
            await emit(ws, tool="commit_order", result=result)
            if result.get("created"):
                await emit(ws, sample=f"Work order {result['id']} created.")
        elif event.get("step") == "interrupt":
            await emit(ws, interrupted=True)
