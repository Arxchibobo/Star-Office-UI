# Star-Office-UI

A real-time AI assistant status visualization system that renders your AI's work state as an animated pixel-art office scene, accessible via Telegram WebApp or any web browser.

> Forked and deeply customized from [ringhyacinth/Star-Office-UI](https://github.com/ringhyacinth/Star-Office-UI)

---

## Overview

Star-Office-UI bridges your AI assistant's operational state with a visual, game-like interface. As the AI transitions between idle, writing, researching, executing, or error states, an animated lobster character moves through an AI-generated pixel office — sitting at a desk when working, relaxing in the breakroom when idle, and surfacing contextual speech bubbles throughout.

The system integrates natively with Telegram via WebApp, giving you a live view of your AI's status directly from your phone with no extra app required.

---

## Features

- **Real-time state visualization** — Polls the AI state every 2 seconds and animates the character accordingly, with <3 second end-to-end latency
- **Phaser 3.85 game engine** — Full pixel-art scene with walking animations, eye blinking, speech bubbles, and typewriter status text
- **Telegram WebApp integration** — One-tap access via bot menu button; HTTPS delivery via Cloudflare Tunnel
- **AI-generated assets** — Office background and lobster character sprite generated with Gemini 3 Pro Image
- **Multi-source state sync** — Reads from OpenClaw Gateway (journalctl) or Agent Swarm (active-tasks.json)
- **Configurable state mapping** — Maps AI states to office zones via `office-config.json`
- **Automated screenshot push** — Optionally captures and sends office screenshots to Telegram on a schedule
- **Manual state control** — `set_state.py` lets you test any state directly

---

## Requirements

- Python 3.10+
- `cloudflared` CLI (for public HTTPS access via Cloudflare Tunnel)
- A Telegram Bot token (from [@BotFather](https://t.me/BotFather))
- Modern web browser (Chrome, Firefox, or Safari)
- Playwright Chromium (only if using the screenshot-to-Telegram feature)

**Python packages:**
```
flask
flask-cors
requests
playwright
pillow
numpy
```

---

## Installation

```bash
git clone https://github.com/Arxchibobo/Star-Office-UI.git
cd Star-Office-UI
python -m venv venv
source venv/bin/activate
pip install flask flask-cors requests playwright pillow numpy
playwright install chromium  # only needed for screenshot feature
```

---

## Usage

### Start the backend and state sync

```bash
./start_office.sh
```

This launches:
- The Flask backend on port `18793`
- The state synchronization service

The office is then accessible at `http://localhost:18793`.

### Enable public access for Telegram WebApp

Telegram WebApp requires HTTPS. Use the provided Cloudflare Tunnel script:

```bash
./setup_telegram_public.sh
```

This starts a `cloudflared` tunnel, prints the public URL, and configures your Telegram bot's menu button to open the office.

### Register the Telegram bot menu button manually

```bash
python setup_telegram_webapp.py
```

### Update AI state manually (for testing)

```bash
python set_state.py writing "Drafting response..."
python set_state.py idle
python set_state.py error "Tool call failed"
```

---

## Configuration

### `office-config.json`

The main configuration file. Key sections:

| Section | Description |
|---|---|
| `telegram` | WebApp URL, button label, description |
| `state_sync` | Source (`openclaw` or `agent_swarm`), poll interval, auto-idle timeout |
| `screenshot` | Enable/disable automated screenshots and Telegram push interval |
| `state_mapping` | Maps AI states to office states, emojis, and work areas |
| `office_areas` | Pixel coordinates for `desk`, `breakroom`, and `alert` zones |

### `state.json` (runtime)

Written automatically by the sync service. Structure:

```json
{
  "state": "writing",
  "detail": "Drafting the response...",
  "progress": 42,
  "updated_at": "2026-03-26T10:00:00Z",
  "ttl_seconds": 30
}
```

If the state is not updated within `ttl_seconds`, the character automatically returns to the breakroom.

Copy `state.sample.json` to `state.json` to bootstrap manually.

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Serve the full Phaser game (`index.html`) |
| `/debug` | GET | Serve the simplified debug view |
| `/status` | GET | Return current state as JSON |
| `/health` | GET | Health check |
| `/update` | POST | Push a new state (JSON body) |
| `/static/*` | GET | Serve static assets |

---

## State Mapping

| AI State | Office Location | Character Behavior |
|---|---|---|
| `idle` | Breakroom (休息区) | Sitting, occasional speech bubbles |
| `writing` | Work desk (办公桌) | Typing animation, status text |
| `researching` | Work desk (办公桌) | Searching animation |
| `executing` | Work desk (办公桌) | Active tool-use animation |
| `error` | Alert area | Visual alert indicator |

---

## Project Structure

```
Star-Office-UI/
├── frontend/
│   ├── index.html                # Phaser 3.85 game (main UI)
│   ├── debug.html                # Lightweight debug view
│   ├── office_bg.png             # AI-generated office background
│   └── lobster_bright_clean.png  # Transparent lobster character sprite
├── backend/
│   ├── app_telegram.py           # Main backend (CORS-enabled, port 18793)
│   └── app.py                    # Legacy backend (port 18791)
├── scripts/
│   └── remove_white_bg.py        # Strip background from character sprites
├── sync_openclaw_state.py        # Sync state from OpenClaw Gateway logs
├── sync_agent_state.py           # Sync state from Agent Swarm task files
├── set_state.py                  # Manual state update tool
├── screenshot_to_telegram.py     # Automated screenshot pusher (Playwright)
├── office-config.json            # Main configuration
├── state.sample.json             # Sample runtime state
├── start_office.sh               # Launch backend + sync
├── start_sync.sh                 # Launch sync only
├── deploy.sh                     # One-click dependency setup
├── setup_telegram_public.sh      # Configure Cloudflare Tunnel + bot
└── setup_telegram_webapp.py      # Register Telegram WebApp button
```

---

## OpenClaw Integration

This project integrates directly with the [OpenClaw](https://github.com/Arxchibobo/OpenClaw) AI agent system. `sync_openclaw_state.py` monitors OpenClaw Gateway logs via `journalctl` and maps agent activity to the office state in real time.

To use with Agent Swarm instead, run `sync_agent_state.py`, which reads from `active-tasks.json`.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
