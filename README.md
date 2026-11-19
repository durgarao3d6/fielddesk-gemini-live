# FieldDesk · Gemini Live

FieldDesk is a native voice-to-voice maintenance dispatcher for technicians on a plant floor. It lets a technician describe a fault in Hinglish, search English knowledge and inventory records, and confirm a mechanical inspection work order without switching systems.

## Run the demo

Requires Python 3.10+ and a recent Chrome browser.

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
fielddesk
```

Open http://localhost:8765. **Start rehearsal** runs the scripted workflow without credentials and persists a real local work order.

For microphone input and Gemini's native audio, configure a Google AI Studio API key before starting the server.

```sh
read -rsp 'Gemini API key: ' GEMINI_API_KEY
export GEMINI_API_KEY
fielddesk
```

Choose **Start Gemini Live** and grant microphone access. Set `GEMINI_MODEL` if your account provides a different native-audio Live model. `PORT` defaults to 8765 and `FIELDDESK_DB` defaults to `orders.sqlite3`.

## Learn with FieldDesk

After starting the server, open [Voice AI Engineering](http://localhost:8765/learn) for six guided lessons, exercises, knowledge checks and a capstone. The guide tracks quiz progress in your browser. Rehearsal exercises require no Gemini credentials. Optional live exercises use the configured Gemini key.

Budget 25–35 minutes per lesson, with extra time for the capstone. The [course syllabus](docs/course.md) lists objectives, assessment criteria and documentation for further study.

## Repository map

| Path | Responsibility |
| --- | --- |
| `src/fielddesk/server.py` | Local HTTP and WebSocket entry points |
| `src/fielddesk/dispatch.py` | Per-session retrieval, draft and confirmation rules |
| `src/fielddesk/adapters/` | Gemini Live relay, knowledge lookup and SQLite persistence |
| `src/fielddesk/fixtures/` | Synthetic maintenance, ticket and inventory records |
| `src/fielddesk/web/` | Technician voice console, source cards and latency indicator |
| `tests/` | Dispatch and rehearsal integration tests |
| `docs/` | Architecture, judge script and evaluation plan |
| `.github/workflows/` | Automated checks on pushes and pull requests |

Run the checks with `python -m unittest discover -s tests -v`.

## Submission materials

- [Architecture and trust boundaries](docs/architecture.md)
- [Judge walkthrough and evaluation plan](docs/demo-and-evaluation.md)

The demo uses synthetic records for one asset and a local SQLite work-order store. Live voice latency, noisy-environment recognition and language coverage require measurement with a configured Gemini session.
