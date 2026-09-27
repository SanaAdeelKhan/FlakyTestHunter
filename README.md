# 🔍 FlakyTestHunter

**AI-powered flaky test detection, diagnosis, and fix — built on IBM Bob 2.0**

Built by **Team GREEN** for the IBM Bob 2.0 Hackathon (lablab.ai), September 2026.

🌐 **Live app:** [flakytesthunter.netlify.app](https://flakytesthunter.netlify.app)
🔧 **Live API:** [flakytesthunter.onrender.com](https://flakytesthunter.onrender.com)
📸 **Session screenshots:** [`bob_sessions/`](./bob_sessions)

---

## The problem

Flaky tests — tests that pass or fail inconsistently with no code change — are one of the most expensive, least-glamorous problems in software engineering. They erode trust in CI, get silently skipped or retried, and hide real bugs behind "just rerun it." Diagnosing *why* a test is flaky usually means a developer manually re-running it dozens of times and reading tea leaves in stack traces.

## The solution

FlakyTestHunter hands that whole workflow to a 3-stage IBM Bob 2.0 subagent pipeline:

| Stage | What it does |
|---|---|
| **1. Detector** | Runs the target test suite 10 times in a row and reports the raw pass/fail pattern |
| **2. Diagnosis** | Reads the source code and explains, in plain English, the exact root cause of the non-determinism |
| **3. Fix & Proof** | Applies a deterministic fix (mocking the source of randomness), re-runs the suite 10 more times, and confirms 100% pass rate |

Every stage is a real, live Bob Shell task — not a canned script. The pipeline is triggered via a plain FastAPI backend that calls Bob in headless mode (`bob run --accept-license`), so it runs unattended with zero approval prompts.

## What you can do on the live site

- **Run Pipeline (Cached Demo)** — instantly see a real, previously-captured Bob run against our sample flaky app
- **Run Live** — trigger a genuine live Bob Shell run against our deployed backend (~1–2 min, real Bobcoins spent)
- **Upload your own file** — upload any Python file containing a test, and Bob will diagnose and fix it live, with the corrected file available to download
- **Gallery** — browse real, unedited screenshots from actual Bob Shell sessions

## Proven results

Run against our seeded sample app (`process_order()`, with an intentional ~33% failure rate from an unseeded `random.uniform` call):

- **Flaky test correctly detected** every run, with the exact failure pattern reported
- **Root cause correctly diagnosed** every run — Bob identified the exact line, the exact probability math, and the exact decision boundary
- **Fix applied and verified**: 10/10 deterministic passes after the fix, with zero changes to production code
- **Average cost per full pipeline run**: ~0.3–0.7 Bobcoins (well within the 40-Bobcoin free trial budget)
- Also validated against a **second, unseen flaky pattern** (time/latency-based instead of pure-random) via the upload feature — proving the approach generalizes beyond the one sample app

## Architecture

```
┌─────────────────┐      ┌──────────────────────┐      ┌─────────────────┐
│  Frontend        │─────▶│  FastAPI Backend      │─────▶│  IBM Bob 2.0    │
│  (HTML/CSS/JS)   │      │  (Python, headless    │      │  Shell (subprocess,
│  Netlify         │◀─────│  Bob subprocess calls)│◀─────│  --accept-license) │
└─────────────────┘      └──────────────────────┘      └─────────────────┘
                                    │
                                    ▼
                          Docker container on Render
                          (Node 22 + Python 3 + Bob Shell CLI)
```

## Tech stack

- **Backend**: FastAPI (Python), deployed on Render as a Docker service
- **Bob integration**: Bob Shell CLI, installed via a non-interactive install flag (`--pm npm`) inside a `node:22-slim` base image, invoked headlessly via subprocess
- **Frontend**: Vanilla HTML/CSS/JS (no framework, no build step), deployed on Netlify
- **Auth**: `BOB_API_KEY` scoped credential, injected as a Render environment variable

## Project structure

```
FlakyTestHunter/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app, CORS, router wiring
│   │   ├── bob/bob_shell.py     # Bob subprocess wrapper + flaky-test reset logic
│   │   └── routes/
│   │       ├── pipeline.py      # /api/run-pipeline — runs the 3-stage demo pipeline
│   │       └── upload.py        # /api/upload-and-fix — runs the pipeline against a user-uploaded file
│   └── requirements.txt
├── sample-target/                # Seeded flaky Python app used for the demo pipeline
├── frontend/
│   ├── index.html                # Home page — cached demo, live run, upload & fix
│   ├── gallery.html               # Real Bob Shell session screenshots
│   └── gallery/                   # Screenshot assets
├── bob_sessions/                  # Raw screenshots of real Bob Shell tasks
├── Dockerfile                     # Node + Python + Bob Shell, single-image deploy
└── AGENTS.md                      # Bob-facing project context
```

## Running locally

```bash
# Backend
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
echo "BOB_API_KEY=your_key_here" > .env
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
python3 -m http.server 5500
# open http://localhost:5500
```

## What's next

- Accept a full repository (not just a single file) as pipeline input
- Persist run history so users can compare pipeline runs over time
- Expand beyond pytest to other test frameworks

## License

MIT — see [`LICENSE`](./LICENSE)

---

Built with ❤️ by **Team GREEN** for the IBM Bob 2.0 Hackathon.
