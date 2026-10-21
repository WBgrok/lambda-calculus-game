# Lambda Calculus Game

A small game for learning lambda calculus by writing expressions, watching them
reduce, and solving progressive challenges. Play in a terminal or in your
browser.

## Play in your browser

The browser edition runs as a static site. It uses Pyodide to run the project's
Python parser, evaluator, and challenge logic; it does not need a backend,
database, frontend build, or installed Python runtime.

The browser game is published at
<https://wbgrok.github.io/lambda-calculus-game/web/>. Its deployment requires
the GitHub Actions workflow described below to complete successfully.

### Run locally

Install Python 3.9 or later, then serve the repository root over HTTP:

```bash
python -m http.server 8000
```

Open <http://localhost:8000/web/>. Do not open `web/index.html` directly with a
`file://` URL: the app fetches Python modules and challenge data from the site.

### Deploy with GitHub Pages

1. Push the project to GitHub.
2. Open the repository's **Settings → Pages**.
3. Under **Build and deployment**, set **Source** to **GitHub Actions**.
4. Push to `master` or manually run **Deploy game to GitHub Pages** from the
   **Actions** tab.
5. Wait for the workflow run to succeed, then open the published site at
   <https://wbgrok.github.io/lambda-calculus-game/web/>.

The workflow assembles and publishes the static files needed by the game:
`web/`, `game/`, `interpreter/`, and `challenges/`. Keep these assets at their
relative paths in the published artifact; the browser fetches Python modules
and challenge JSON from beside the web UI. A custom domain can use the same
`/web/` path.

If the game reports that a Python module or challenge JSON returns HTTP 404,
check that the latest **Deploy game to GitHub Pages** workflow run succeeded
and that Pages is configured to use **GitHub Actions** as its source. Verify
that
<https://wbgrok.github.io/lambda-calculus-game/game/__init__.py> returns the
module contents. If it returns 404, Pages is still serving an artifact that
does not include the Python files; the browser cannot initialize until a
correct artifact is deployed.

The Pyodide runtime is fetched from its pinned CDN release, so the browser needs
network access to that CDN when starting the game. Challenge data is fetched
from `challenges/challenges.json` at runtime. When publishing challenge
changes, ensure the host or CDN revalidates that JSON asset.

## Play in the terminal

Python 3.9 or later is required. The console game uses only the Python standard
library.

```bash
python main.py
```

Completed challenges save automatically to
`Path.home() / ".lambda-calculus-game" / "progress.json"`. Choose **New Game**
from the main menu and confirm to clear the save.

## Progress and game behavior

The game includes fifteen challenges with prerequisite-based unlocking.
Completed challenge solutions can be reused by their challenge IDs as aliases.
The free interpreter shows a reduction trace for any valid expression.

Browser progress is saved in that browser profile's `localStorage`. It is
separate from the console save and is not synchronized between browsers or
devices. The browser's **New game** action confirms before clearing local
progress.

## Lambda syntax

- `\x.body` defines a function.
- `function argument` applies a function to an argument; application is
  left-associative.
- Parentheses group expressions.
- Multiple parameters are nested lambdas, for example `\x.\y.x`.
- Completed challenge IDs such as `ID` can be used as aliases.

## Challenges

Challenge definitions live in [`challenges/challenges.json`](challenges/challenges.json).
Each entry contains an `id`, `name`, `description`, a list of tests (`input`
and `expected` expressions), and optional prerequisite IDs in `requirements`.
Set `validation_only` to `true` for a challenge that accepts any well-formed
expression without evaluating it against test cases.
The browser fetches this JSON at runtime, so challenge content can be updated
independently from the frontend.

## Run the tests

The test suite uses the standard library and temporary save files:

```bash
python -m unittest discover -v
```

Tests cover parsing and reduction, aliases, all challenge definitions,
controller flows, progress persistence, and the browser-facing Python bridge.

## Project structure

- `interpreter/` — parser, evaluator, and reduction results
- `game/` — challenge models, game state, console controller and view
- `challenges/challenges.json` — editable challenge catalog
- `web/` — static browser UI and Pyodide bridge
- `test_*.py` — standard-library automated tests
