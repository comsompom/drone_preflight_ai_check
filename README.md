# ArduPilot Preflight AI Check

![ArduPilot Preflight Inspector](drone_preflight_logo.jpg)

AI-powered preflight configuration and mission checker for ArduPilot (ArduCopter, ArduPlane), built for the **DigitalOcean Gradient™ AI Hackathon**. The agent guides you through parameter checks and mission verification using a multi-phase workflow.

## Demo

- **[Plane preflight check & flight (3.2 m wingspan, 18 kg)](https://www.youtube.com/watch?v=PhpToEW_G1I)** — Video: fixed-wing (3.2 m wingspan, 18 kg) through the preflight agent check, then flight.
- **[Flask web app demo](https://www.youtube.com/watch?v=U-wCpUDEEk0)** — Video: upload parameter file and chat with the agent in the military-style UI.

## Architecture

- **Agent (DigitalOcean Gradient):** Expert ArduPilot Flight Engineer agent with a knowledge base (ArduPilot docs). You send config + param/mission data; it returns safety reports and suggested changes.
- **This repo:** Python client and scripts that call the agent via its API (OpenAI-compatible endpoint).

## Setup

### 1. Clone and install

```bash
cd drone_preflight_ai_check
pip install -r requirements.txt
```

### 2. Environment variables

Copy the example env and add your agent URL and API key:

```bash
cp .env.example .env
```

Edit `.env`:

- **AGENT_URL** — Your agent endpoint (e.g. `https://xxxxxxxx.agents.do-ai.run`). Find it in DigitalOcean: Agent → Overview or Settings.
- **AGENT_API_KEY** — Your endpoint access key. Create one in the agent’s **Settings → Endpoint Access Keys**, then paste the **secret** into `.env`.

Do not commit `.env`; it is listed in `.gitignore`.

### 3. Verify

```bash
python run_demo.py
```

You should see the agent’s reply to the sample plane preflight message.

## Web app (Flask)

The Flask UI lives in the **`webapp/`** folder. Run it from the **project root** so it can find `.env` and `agent_client.py`:

```bash
python webapp/app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). Enter your message (e.g. drone type, specs, param list) and click **SEND** to get the agent’s preflight report.

To use a different port: `PORT=8080 python webapp/app.py`.

## Scripts

| Script | Description |
|--------|-------------|
| **run_demo.py** | Sends the hackathon demo message (plane, 18 kg, catapult). Use to verify the agent and knowledge base. |
| **chat.py** | Send one message to the agent. `python chat.py "Your message"` or pipe/stdin. |
| **send_params.py** | Send a `.param` or mission file to the agent, with optional intro (drone type, takeoff method). |

### Examples

```bash
# Demo (plane, 18 kg, catapult)
python run_demo.py

# Single message
python chat.py "I have a quad, 2 kg, manual flight, land takeoff. Are these params safe?"

# Param file with intro
python send_params.py sample_params.param --intro "Plane, 18 kg, 3.2m wingspan, catapult, land takeoff"

# Mission file
python send_params.py my_waypoints.txt --intro "Quad, mission flight"
```

## Agent workflow (summary)

1. **Phase 1:** You provide drone type, specs, takeoff method, and full parameter list. Agent returns SAFE / NEEDS CHANGE and recommended values.
2. **Phase 2:** If you use a mission, the agent explains how to create it in Mission Planner / QGroundControl and asks you to upload the waypoint file + updated params.
3. **Phase 3:** Agent verifies updated params and mission and gives final GO or lists remaining fixes.

## Files

- **`webapp/`** — Flask app (military-style UI):
  - `webapp/app.py` — Web server and `/api/chat` endpoint.
  - `webapp/templates/` — HTML (base + index).
  - `webapp/static/css/style.css` — Military theme (dark green, olive, monospace).
  - `webapp/static/js/app.js` — Chat form and API calls.
- `agent_client.py` — Client that loads `.env` and calls the agent (OpenAI SDK).
- `.env` (project root) — Used by both CLI scripts and `webapp/app.py`; do not commit.
- `.env.example` — Template for `AGENT_URL` and `AGENT_API_KEY`.
- `tests/` — Unit tests (pytest).

## Testing

Run the test suite from the project root:

```bash
pip install -r requirements.txt
pytest
```

With coverage:

```bash
pytest --cov=. --cov-report=term-missing --ignore=webapp
```

Tests cover: `agent_client` (get_client validation, send_message with mocked API), Flask app (index, `/api/chat` validation and responses), `send_params` (message building, file handling), and `run_demo` (demo message and send_message call). No real API calls are made; the agent is mocked in tests.

## License

Use as needed for the hackathon and learning.
