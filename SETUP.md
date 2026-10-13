# Development Setup

## Requirements

- Python 3.8 or later
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
test_aliases.py
test_challenge_fix.py
test_interpreter.py
test_new_challenges.py
test_progress.py
```
