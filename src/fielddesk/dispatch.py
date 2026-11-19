import uuid

CONFIRM = {
    "confirm work order", "वर्क ऑर्डर कन्फर्म करो", "वर्क ऑर्डर कंफर्म करो",
    "वर्क ऑर्डर कन्फ़र्म करो", "work order confirm karo",
}

def normalize(value):
    return " ".join(value.lower().strip().strip(".!?।").split())


class Session:
    def __init__(self, knowledge, orders):
        self.knowledge = knowledge
        self.orders = orders
        self.records = []
        self.order = None
        self.transcript = ""
        self.readback_complete = False

    def call(self, name, args):
        if name == "lookup_asset":
            asset = str(args.get("asset", "")).upper().replace(" ", "")
            self.records = self.knowledge.lookup(asset)
            return {"records": self.records}
        if name == "stage_order":
            symptom = str(args.get("symptom", "")).strip()
            if not self.records or args.get("asset") != "P-204" or not 1 <= len(symptom) <= 240:
                return {"error": "Retrieve the asset and supply its observed symptom."}
            self.order = {"id": "WO-" + uuid.uuid4().hex[:8].upper(), "asset": "P-204", "symptom": symptom}
            self.transcript = ""
            self.readback_complete = False
            return {"pending": self.order}
        if name == "commit_order":
            if not self.order or not self.readback_complete or normalize(self.transcript) not in CONFIRM:
                return {"error": "No pending order with explicit spoken confirmation."}
            result = self.orders.save(self.order)
            self.order = None
            self.transcript = ""
            return result
        return {"error":"Unknown tool."}
