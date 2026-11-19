# FieldDesk

FieldDesk is a Gemini Live voice-to-voice maintenance dispatcher for technicians reporting a fault on a plant floor. It retrieves English records for a demo pump, answers in the language the technician uses, and writes an inspection work order to a local SQLite database after an explicit confirmation.

## Run locally

With Python 3.10+ and Chrome:

```bash
python -m pip install -r requirements.txt
python app.py
```

Open http://localhost:8765 and choose **Start rehearsal** for a scripted walkthrough with optional browser speech synthesis. The rehearsal writes to the same local backend. Each session requires a new draft and confirmation.

For native live audio, set an API key issued by Google AI Studio in the terminal before launching the server. The key stays on the server. Use `GEMINI_MODEL` if your account exposes a different native-audio Live model.

```bash
read -rs -p "Gemini API key: " GEMINI_API_KEY
export GEMINI_API_KEY
python app.py
```

Choose **Start Gemini Live**, grant microphone access, and use headphones where possible. The server binds to localhost. Use synthetic records for the demo.

## Two-minute judge demo

1. Say “P-204 ke seal se leak ho raha hai. Pichle ticket mein kya tha, aur spare kit stock mein hai kya?”
2. While FieldDesk is speaking, interrupt with “Ek minute, kit ka bin batao.” Show the interrupted playback and the English source cards.
3. Say “Mechanical inspection ka work order bana do.” Show the pending read-back.
4. After it finishes, say “Confirm work order.” Show the saved work order ID. For a confirmation negative test, say “Don't confirm work order” before giving approval and verify the draft remains pending.
5. Repeat with moderate recorded plant ambience in the room. Record successes, failures and the visible latency.

## Architecture and evaluation

Chrome streams 16 kHz microphone PCM through the local WebSocket relay to Gemini's native audio Live API. Gemini streams spoken output back, emits transcripts for the console and requests tools for retrieval, drafting and saving. Gemini's interruption event flushes scheduled browser audio. Staging and saving are separate calls. The server requires a pending draft, completion of its proposal turn and an exact match against the incoming confirmation transcript. A successful commit persists a receipt in `orders.sqlite3`. The confirmation gate is for a local demo, with no employee identity or role integration.

The three source types are fixture data keyed by asset ID. Gemini interprets the spoken question and looks up the relevant English records through a structured tool. This demo measures approximate response latency from the last above-threshold microphone frame to scheduled playback of the first audio. Noise and browser audio buffering can affect this estimate.

Measure task completion and citation accuracy on a set of English, Hinglish and Hindi queries with and without noise. Record p50 and p95 latency, how often interruption works, and baseline manual completion time on the same tasks. Calculate cost per successful resolution using actual API charges divided by successful resolutions. For a slide illustration only, 5,000 successful orders a month × 4 minutes saved × ₹300/hour gives ₹100,000/month in labor capacity. If the actual per-order variable cost were ₹3, that would leave ₹85,000/month before fixed costs. Validate the assumptions with a timed pilot and billed usage.
