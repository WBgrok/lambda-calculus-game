# Lambda Calculus Game

A small game for learning lambda calculus by writing expressions, watching them
reduce, and solving progressive challenges. Play in a terminal or in your
browser.

## Play in your browser

The browser edition runs as a static site. It uses Pyodide to run the project's
Python parser, evaluator, and challenge logic; it does not need a backend,
database, frontend build, or installed Python runtime.

Once GitHub Pages is enabled, open the published repository URL with `/web/`
appended.

### Run locally

Install Python 3.9 or later, then serve the repository root over HTTP:

```bash
python -m http.server 8000
```

Open <http://localhost:8000/web/>. Do not open `web/index.html` directly with a
`file://` URL: the app fetches Python modules and challenge data from the site.

### Deploy with GitHub Pages

1. Open the repository's **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**.
3. Select the branch containing the published version of the game and choose
   `/(root)` as the folder.
4. Save the settings and wait for Pages to finish publishing.
5. Open the published site URL with `/web/` appended, for example:
   `https://OWNER.github.io/REPOSITORY/web/`.

Publish the repository root, not only the `web/` directory. The browser loads
`game/`, `interpreter/`, and `challenges/` from sibling paths. A custom domain
can point to the same `/web/` path.

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

The game includes thirteen challenges with prerequisite-based unlocking.
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
