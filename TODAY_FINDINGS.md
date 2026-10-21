# Project Findings — 2026-10-13

## Current state

The project is a working Python console game for learning lambda calculus.
Challenge definitions live in JSON; the parser and evaluator are kept separate
from the game controller and console view.

## Implemented improvements

- Challenge and challenge-test definitions use dataclasses.
- The console presentation is separated from game flow.
- Evaluation returns a structured result with an immutable reduction trace.
- Parser errors and reduction-limit errors have named exception types; expected
  input errors are handled without swallowing unexpected programming errors.
- Completed challenges and their aliases are saved to
  `Path.home() / ".lambda-calculus-game" / "progress.json"`.
- The main menu resumes saved progress by default and requires confirmation
  before starting a new game and deleting the save.
- Automated tests use Python's built-in `unittest` and require no extra
  dependencies.

## Test coverage

The test suite covers interpreter reduction and syntax errors, aliases, every
challenge in the JSON catalog, prerequisite references, controller navigation,
and progress loading, saving, validation, and reset. Persistence tests use
temporary directories and do not touch a real user save.

## Static browser edition

- Planning and prioritization are recorded in [WEB_PORT_PLAN.md](WEB_PORT_PLAN.md).
- The static Pyodide frontend lives in `web/` and calls a JSON-facing Python
  bridge; parser, evaluator, challenge logic, and challenge definitions remain
  reusable and separate from presentation.
- Challenge JSON is loaded as a runtime asset. Browser progress uses
  `localStorage`, separate from the console save file, and the **New game**
  action confirms before clearing it.
- Local browser testing requires HTTP: run `python -m http.server 8000` from
  the repository root and open `http://localhost:8000/web/`.

## Follow-up

- Run and manually exercise the page in a browser with network access to the
  pinned Pyodide CDN; Python unit tests validate the bridge, not browser/CDN
  behavior.
- Consider import/export of browser progress only if save portability is
  requested. Accounts, synchronization, a backend, and offline/PWA support
  remain out of scope.
