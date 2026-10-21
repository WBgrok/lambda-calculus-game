const PYODIDE_VERSION = "v314.0.7";
const SAVE_KEY = "lambda-calculus-game.progress";
const sourceAssets = [
  "game/__init__.py",
  "game/challenge.py",
  "game/game_state.py",
  "interpreter/__init__.py",
  "interpreter/lambda_interpreter.py",
  "web/__init__.py",
  "web/bridge.py",
];

const statusElement = document.querySelector("#status");
const challengeList = document.querySelector("#challenge-list");
const challengeTitle = document.querySelector("#challenge-title");
const challengeRequirements = document.querySelector("#challenge-requirements");
const challengeDescription = document.querySelector("#challenge-description");
const solutionForm = document.querySelector("#solution-form");
const solutionInput = document.querySelector("#solution-input");
const submitButton = document.querySelector("#submit-solution");
const challengeResults = document.querySelector("#challenge-results");
const interpreterForm = document.querySelector("#interpreter-form");
const expressionInput = document.querySelector("#expression-input");
const evaluateButton = document.querySelector("#evaluate-expression");
const interpreterResults = document.querySelector("#interpreter-results");
const newGameButton = document.querySelector("#new-game");
const progressCount = document.querySelector("#progress-count");

let pyodide;
let gameState;
let selectedChallengeId;

function showError(error) {
  statusElement.textContent = error instanceof Error ? error.message : String(error);
  statusElement.hidden = false;
}

function clearError() {
  statusElement.textContent = "";
  statusElement.hidden = true;
}

async function fetchText(url) {
  const response = await fetch(url, { cache: "no-cache" });
  if (!response.ok) {
    throw new Error(`Could not load ${url.pathname} (HTTP ${response.status}).`);
  }
  return response.text();
}

function loadPyodideScript() {
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = `https://cdn.jsdelivr.net/pyodide/${PYODIDE_VERSION}/full/pyodide.js`;
    script.onload = resolve;
    script.onerror = () => reject(new Error(
      `Could not load Pyodide ${PYODIDE_VERSION} from its CDN. Check your network connection.`
    ));
    document.head.append(script);
  });
}

async function loadPythonFiles() {
  const files = await Promise.all(sourceAssets.map(async (path) => ({
    path,
    source: await fetchText(new URL(`../${path}`, import.meta.url)),
  })));

  for (const { path, source } of files) {
    const destination = `/${path}`;
    const parent = destination.slice(0, destination.lastIndexOf("/"));
    pyodide.FS.mkdirTree(parent);
    pyodide.FS.writeFile(destination, source);
  }

  pyodide.runPython(
    "import sys, importlib; sys.path.insert(0, '/'); importlib.invalidate_caches()"
  );
}

function callBridge(code) {
  const rawResult = pyodide.runPython(code);
  return JSON.parse(rawResult);
}

function renderDescription(description) {
  challengeDescription.textContent = description;
}

function renderState(state) {
  gameState = state;
  progressCount.textContent =
    `${state.completed_count} of ${state.challenges.length} complete`;
  newGameButton.disabled = state.completed_count === 0;

  challengeList.replaceChildren();
  for (const challenge of state.challenges) {
    const item = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.disabled = !challenge.unlocked;
    button.dataset.challengeId = challenge.id;
    button.setAttribute(
      "aria-current",
      String(challenge.id === selectedChallengeId)
    );

    const mark = document.createElement("span");
    mark.className = "challenge-mark";
    if (challenge.completed) {
      mark.classList.add("complete");
      mark.textContent = "✓";
      mark.setAttribute("aria-label", "Completed");
    } else if (!challenge.unlocked) {
      mark.classList.add("locked");
      mark.textContent = "·";
      mark.setAttribute("aria-label", "Locked");
    } else {
      mark.textContent = challenge.id;
      mark.setAttribute("aria-label", "Available");
    }

    const name = document.createElement("span");
    name.textContent = challenge.name;
    button.append(mark, name);
    item.append(button);
    challengeList.append(item);
  }

  const selected = state.challenges.find(
    (challenge) => challenge.id === selectedChallengeId
  );
  if (!selected || !selected.unlocked) {
    const nextChallenge = state.challenges.find(
      (challenge) => challenge.unlocked && !challenge.completed
    ) || state.challenges.find((challenge) => challenge.unlocked);
    selectedChallengeId = nextChallenge?.id;
    if (selectedChallengeId) {
      renderState(state);
      return;
    }
  }

  const challenge = state.challenges.find(
    (item) => item.id === selectedChallengeId
  );
  if (challenge) {
    challengeTitle.textContent = `${challenge.id}: ${challenge.name}`;
    challengeRequirements.textContent = challenge.requirements.length
      ? `Requires: ${challenge.requirements.join(", ")}`
      : "No prerequisites";
    renderDescription(challenge.description);
    submitButton.disabled = false;
    solutionInput.disabled = false;
  } else {
    challengeTitle.textContent = "No challenges available";
    challengeRequirements.textContent = "";
    challengeDescription.textContent =
      "The challenge catalog is empty or has no unlocked challenges.";
    submitButton.disabled = true;
    solutionInput.disabled = true;
  }
}

function appendSteps(parent, steps, label = "Reduction steps") {
  if (!steps || steps.length === 0) {
    return;
  }
  const details = document.createElement("details");
  const summary = document.createElement("summary");
  summary.textContent = `${label} (${steps.length})`;
  const list = document.createElement("ol");
  list.className = "steps";
  for (const step of steps) {
    const item = document.createElement("li");
    item.textContent = step.description;
    const expression = document.createElement("span");
    expression.className = "expression";
    expression.textContent = step.expression;
    item.append(expression);
    list.append(item);
  }
  details.append(summary, list);
  parent.append(details);
}

function renderTestResults(result) {
  challengeResults.replaceChildren();
  const heading = document.createElement("p");
  heading.className = result.all_passed ? "passed" : "failed";
  heading.textContent = result.all_passed
    ? "All tests passed. Challenge completed!"
    : "Not quite — review the results and try again.";
  challengeResults.append(heading);

  for (const test of result.results) {
    const card = document.createElement("article");
    card.className = `result-card ${test.passed ? "pass" : "fail"}`;
    const title = document.createElement("div");
    title.className = "result-heading";
    title.textContent = test.passed ? "Passed" : "Failed";
    card.append(title);
    addExpression(card, "Input", test.input);
    addExpression(card, "Expected", test.expected_result ?? test.expected);
    if (test.actual !== null) {
      addExpression(card, "Actual", test.actual);
    }
    if (test.error) {
      addExpression(card, "Error", test.error);
    }
    appendSteps(card, test.steps);
    challengeResults.append(card);
  }
}

function addExpression(parent, label, value) {
  const paragraph = document.createElement("p");
  paragraph.textContent = `${label}: `;
  const expression = document.createElement("span");
  expression.className = "expression";
  expression.textContent = value ?? "—";
  paragraph.append(expression);
  parent.append(paragraph);
}

function setBusy(isBusy) {
  submitButton.disabled = isBusy || !gameState;
  evaluateButton.disabled = isBusy || !gameState;
  newGameButton.disabled = isBusy || !gameState || gameState.completed_count === 0;
}

async function initializeGame(challengeJson, savedProgressJson) {
  pyodide.globals.set("browser_challenge_json", challengeJson);
  pyodide.globals.set("browser_progress_json", savedProgressJson);
  return callBridge(
    "import web.bridge as browser_bridge; " +
    "browser_bridge.initialize(browser_challenge_json, browser_progress_json)"
  );
}

async function start() {
  try {
    await loadPyodideScript();
    pyodide = await loadPyodide();
    const [challengeJson,] = await Promise.all([
      fetchText(new URL("../challenges/challenges.json", import.meta.url)),
      loadPythonFiles(),
    ]);

    let savedProgress = localStorage.getItem(SAVE_KEY);
    let state;
    try {
      state = await initializeGame(challengeJson, savedProgress);
    } catch (error) {
      if (!savedProgress) {
        throw error;
      }
      const clearSave = window.confirm(
        `Saved progress could not be loaded:\n${error.message}\n\n` +
        "Clear the invalid browser save and start a fresh game?"
      );
      if (!clearSave) {
        throw error;
      }
      localStorage.removeItem(SAVE_KEY);
      savedProgress = null;
      state = await initializeGame(challengeJson, savedProgress);
    }
    clearError();
    renderState(state);
    evaluateButton.disabled = false;
  } catch (error) {
    showError(error);
  }
}

challengeList.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-challenge-id]");
  if (!button || button.disabled) {
    return;
  }
  selectedChallengeId = button.dataset.challengeId;
  challengeResults.replaceChildren();
  solutionInput.value = "";
  renderState(gameState);
});

solutionForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearError();
  if (!solutionInput.value.trim()) {
    expressionInput.focus();
    expressionInput.scrollIntoView({ behavior: "smooth", block: "center" });
    return;
  }

  setBusy(true);
  challengeResults.replaceChildren();
  try {
    pyodide.globals.set("browser_challenge_id", selectedChallengeId);
    pyodide.globals.set("browser_solution", solutionInput.value);
    const result = callBridge(
      "browser_bridge.submit_solution(browser_challenge_id, browser_solution)"
    );
    if (result.all_passed) {
      localStorage.setItem(SAVE_KEY, JSON.stringify(result.progress));
    }
    renderState(result.state);
    renderTestResults(result);
  } catch (error) {
    showError(error);
  } finally {
    setBusy(false);
  }
});

interpreterForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearError();
  if (!expressionInput.value.trim()) {
    expressionInput.focus();
    return;
  }

  setBusy(true);
  interpreterResults.replaceChildren();
  try {
    pyodide.globals.set("browser_expression", expressionInput.value);
    const result = callBridge(
      "browser_bridge.evaluate_expression(browser_expression)"
    );
    const card = document.createElement("article");
    card.className = "trace-card";
    addExpression(card, "Final result", result.final_expression);
    appendSteps(card, result.steps);
    interpreterResults.append(card);
  } catch (error) {
    showError(error);
  } finally {
    setBusy(false);
  }
});

newGameButton.addEventListener("click", () => {
  if (!window.confirm("Start a new game and remove this browser's saved progress?")) {
    return;
  }
  clearError();
  try {
    localStorage.removeItem(SAVE_KEY);
    selectedChallengeId = undefined;
    challengeResults.replaceChildren();
    interpreterResults.replaceChildren();
    solutionInput.value = "";
    renderState(callBridge("browser_bridge.new_game()"));
  } catch (error) {
    showError(error);
  }
});

start();
