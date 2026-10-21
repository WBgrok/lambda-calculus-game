# Lambda Calculus Game

A game for learning lambda calculus through progressive challenges. Play in the
Python console or in a static browser build. Write lambda expressions, see each
reduction step, and reuse completed solutions as aliases.

## Features

- Backslash lambda notation, for example `\x.x` for identity
- Step-by-step beta reduction and a free interpreter
- Thirteen challenges with prerequisite-based unlocking
- Automatic progress saving and resume between runs
- A confirmation-protected **New Game** option
- Static browser edition powered by Pyodide, with progress saved in browser
  storage

## Requirements and installation

- Python 3.9 or later for the console game and tests
- No third-party Python packages are required

From the project directory, run the game:

```bash
python main.py
```

## Browser edition

The browser edition uses the same Python parser, evaluator, challenge logic,
and challenge JSON catalog. Its HTML/CSS/JavaScript frontend is in `web/`; it
does not require a server-side Python process or backend.

From the repository root, serve the files over HTTP:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/web/`. Do not open `web/index.html` directly
with a `file://` URL; the browser must fetch Python source files and the
challenge catalog. For static hosting, publish the repository root or otherwise
include `web/`, `game/`, `interpreter/`, and `challenges/` at the same relative
paths. The Pyodide runtime is loaded from its pinned CDN release, so first use
requires network access to that CDN.

Browser progress is stored separately in the browser's `localStorage` and is
not synchronized with the console save or other devices. Challenge definitions
are fetched from `challenges/challenges.json` at runtime, so that catalog can
be updated without changing the frontend.

Progress is saved as JSON at
`Path.home() / ".lambda-calculus-game" / "progress.json"` (under the current
user's home directory). Completing a challenge saves automatically. Select
**New Game** in the main menu to remove the save; the game asks for confirmation
first.

## Tests

Run the complete standard-library test suite from the project directory:

```bash
python -m unittest discover -v
```

Tests cover parsing and reduction, aliases, all challenge definitions,
controller flows, save/load/reset behavior, and the browser bridge. They use
temporary progress files and do not change the user's console-game save.

## Lambda syntax

- `\x.body` defines a function.
- `function argument` applies a function to an argument; application is
  left-associative.
- Parentheses group expressions.
- Multiple parameters are written as nested lambdas, e.g. `\x.\y.x`.
- A completed challenge ID, such as `ID`, can be used as an alias.

## Evaluation API

`parse_and_eval(source, aliases=None)` returns an `EvaluationResult`:

- `initial_expression`: parsed input expression
- `final_expression`: expression after reduction
- `steps`: immutable tuple of `ReductionStep` objects, each with `expression`
  and `description`

Malformed source raises `LambdaSyntaxError` (a `SyntaxError` subclass);
reduction-limit exhaustion raises `EvaluationLimitError` (a `RuntimeError`
subclass).

## Challenge definitions

Challenges are defined in `challenges/challenges.json`. Each entry has an
`id`, `name`, `description`, a list of `tests` (`input` and `expected` source
expressions), and optional prerequisite challenge IDs in `requirements`.

## Project layout

```
main.py                 Game entry point
game/controller.py      Game flow
game/menu.py            Console presentation
game/game_state.py      Challenge state and progress persistence
game/challenge.py       Challenge models and solution testing
interpreter/             Parser and lambda evaluator
challenges/challenges.json Challenge catalog
web/                      Static HTML/CSS/JavaScript and Python bridge
test_*.py                 Standard-library automated tests
```
