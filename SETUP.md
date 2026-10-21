# Development Setup

## Requirements

- Python 3.9 or later
- No third-party packages are needed.

## Optional virtual environment

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

The game and tests use the Python standard library. From the project root:

```bash
python main.py
python -m unittest discover -v
```

## Browser edition

The static browser version uses Pyodide and the repository's existing Python
game logic. From the repository root, serve the files over HTTP:

```bash
python -m http.server 8000
```

Open `http://localhost:8000/web/`. The browser fetches Python modules and
`challenges/challenges.json` from the repository root, so do not open the page
as a `file://` URL. Static deployments must include `web/`, `game/`,
`interpreter/`, and `challenges/` in their existing relative locations. The
Pyodide runtime is fetched from its pinned CDN release and needs network access
on first load.

The browser version stores progress in `localStorage`, separately from the
console save file. Challenge JSON is fetched at runtime and can be updated as a
static asset independently of the frontend.

## Progress save

The game automatically saves completed challenges and their aliases to
`Path.home() / ".lambda-calculus-game" / "progress.json"`. Tests pass a
temporary path to `GameState`, so they do not access or modify the real save.

## Project layout

```
main.py
requirements.txt
game/
    challenge.py       Challenge definitions and solution tests
    controller.py      Game navigation and actions
    game_state.py      Challenge state and save/load
    menu.py            Console prompts and presentation
interpreter/
    lambda_interpreter.py
challenges/
    challenges.json    Challenge catalog and test cases
web/
    index.html         Static browser UI
    app.js             Pyodide loader and frontend
    bridge.py          Browser-facing Python API
    style.css          Browser presentation
test_aliases.py
test_challenge_fix.py
test_interpreter.py
test_new_challenges.py
test_progress.py
test_web_bridge.py
```
