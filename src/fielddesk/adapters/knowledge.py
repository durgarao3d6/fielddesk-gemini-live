import json
from pathlib import Path

RECORDS = Path(__file__).resolve().parents[1] / "fixtures" / "records.json"


class FixtureKnowledge:
    def __init__(self, path=RECORDS):
        self.records = json.loads(path.read_text(encoding="utf-8"))

    def lookup(self, asset):
        return [
            {"id": record["id"], "title": record["title"], "excerpt": record["excerpt"]}
            for record in self.records
            if record["asset"] == asset
        ]
