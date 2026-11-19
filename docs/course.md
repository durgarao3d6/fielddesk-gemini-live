# Voice AI Engineering with FieldDesk

**Audience.** Working software, data and product professionals who want to understand how a voice AI feature moves from model output to an application decision.

**Prerequisites.** Basic Python and JavaScript, the ability to run a local server, and familiarity with JSON over HTTP. A Gemini key is optional for the live voice exercises.

Start FieldDesk and open `http://localhost:8765/learn`. Work through one lesson at a time. For each lab, capture one observation, the code that explains it, and a test that could falsify your interpretation.

| Session | Learning objective | Evidence to submit |
| --- | --- | --- |
| LLMs and context | Identify instruction, evidence, response and state in a single turn | Annotated event trace |
| Voice streaming | Explain native vs. cascaded audio and measure interruption behavior | PCM calculation and playback observation |
| Retrieval | Distinguish retrieval quality from answer grounding | Source-to-claim table |
| Tool calling | Enforce approval before a durable write | Passing test for an unauthorized action |
| Evaluation | Quantify behavior and estimate usage cost | Test set, measurement definitions, observed or simulated results clearly labeled |
| Capstone | Extend the dispatcher while preserving the retrieval-to-action boundary | Proposed change, tests and decision record |

## Capstone rubric

- **Grounding (30%)**. The second asset has traceable evidence, and unknown assets produce an explicit fallback.
- **Action correctness (35%)**. Tests cover staging, explicit confirmation and a rejected mismatch between the retrieved asset and the requested action.
- **Evaluation (25%)**. Report your cases, observations and failure modes. Label scripted results and live Gemini results.
- **Communication (10%)**. Explain the design and point reviewers to one runnable example.

One capstone submission can be a practice-branch diff with a short README and output from the test suite. Completion of a browser quiz records progress locally. Grade capstone work using the rubric.

## Further reading

- [Gemini Live API](https://ai.google.dev/gemini-api/docs/live-api)
- [Function calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [AudioWorklet](https://developer.mozilla.org/en-US/docs/Web/API/AudioWorklet)
- [Gemini Live best practices and billing](https://ai.google.dev/gemini-api/docs/live-api/best-practices)
