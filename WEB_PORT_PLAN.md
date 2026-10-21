# Static Web Port Plan

## Decision

Use **Pyodide directly** with a small HTML/CSS/JavaScript frontend. Host the
repository as static files. Do not add a Python server, database, frontend
framework, or PyScript layer for the first port.

The browser UI owns presentation and interaction. The existing Python parser,
evaluator, challenge model, and progression rules remain the source of game
behavior. JavaScript is a thin bridge for loading Pyodide, retrieving static
Python/JSON files, calling the Python API, and storing progress in
`localStorage`.

## Prioritised implementation

1. **Reuse Python game logic in-browser.** Load the interpreter, challenge
   model, game state, and a small browser bridge into Pyodide's virtual
   filesystem. Load the challenge catalog over HTTP at runtime so an updated
   JSON catalog can be published independently of the page code.
2. **Ship the essential play loop.** Provide challenge selection, prerequisite
   and completion status, solution submission with pass/fail details and
   reduction steps, and the free interpreter.
3. **Persist per-browser progress.** Store the existing versioned progress
   document in `localStorage`; restore it at startup. Starting a new game must
   ask before clearing the local save.
4. **Keep static deployment and failure modes clear.** Pin the Pyodide runtime,
   document local HTTP serving and static-host deployment, and surface failures
   loading the runtime, Python modules, challenge JSON, or browser storage.
5. **Validate parity.** Add standard-library tests for the Python/browser
   bridge and retain the existing console-game test suite.

## Boundaries and data flow

- `interpreter/` stays independent of either UI.
- `game/challenge.py` and `game/game_state.py` provide reusable game rules and
  serializable progress.
- `web/bridge.py` exposes JSON-in/JSON-out browser operations; it does not
  manipulate the DOM.
- `web/` HTML, CSS, and JavaScript render the game and call the bridge.
- `challenges/challenges.json` remains the editable, runtime-loaded content
  source.
- Console progress remains a JSON file under the user's home directory.
  Browser progress is separate and remains in that browser profile's
  `localStorage`; it is not synchronized across browsers or devices.

## Deployment notes

Serve the repository root (including `web/`, `game/`, `interpreter/`, and
`challenges/`) from a static host. For local testing, run
`python -m http.server 8000` from the repository root and open
`http://localhost:8000/web/`. Do not open the HTML as a `file://` URL: browser
fetches and Pyodide require HTTP(S).

The Pyodide runtime is loaded from its pinned official CDN URL, so initial
startup needs network access to that CDN. Python and challenge updates are
fetched as separate static assets. Publish all assets together; configure the
host/CDN to revalidate or invalidate cached `challenges.json` when updating
challenge content.

## Later, only if needed

- Add offline/PWA support if offline play becomes a requirement.
- Add import/export of browser progress if players need to move saves between
  browsers.
- Consider a typed challenge result object if result payloads continue to grow.
- Consider accounts or remote progress only if cross-device synchronization is
  requested; those features require a backend and are deliberately out of scope.
