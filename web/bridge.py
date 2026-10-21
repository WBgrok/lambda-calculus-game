"""JSON-in/JSON-out API for the static browser frontend."""

from __future__ import annotations

import json
from typing import Any, Optional

from game.game_state import GameState
from interpreter.lambda_interpreter import Parser, parse_and_eval


_game_state: Optional[GameState] = None


def initialize(challenges_json: str, progress_json: Optional[str] = None) -> str:
    """Initialize a browser session from fetched challenge and save JSON."""
    global _game_state

    challenge_data = json.loads(challenges_json)
    _game_state = GameState(challenges_data=challenge_data, auto_save=False)
    if progress_json:
        _game_state.restore_progress_data(json.loads(progress_json))
    return get_state()


def get_state() -> str:
    """Return challenge metadata and progress as JSON."""
    state = _require_state()
    available_challenges = state.get_available_challenges()
    challenges = [
        {
            "id": challenge.id,
            "name": challenge.name,
            "description": challenge.description,
            "requirements": list(challenge.requirements),
            "completed": state.is_completed(challenge.id),
            "unlocked": True,
        }
        for challenge in available_challenges
    ]
    return json.dumps({
        "challenges": challenges,
        "total_challenges": len(state.challenges_data),
        "completed_count": len(state.completed_challenges),
        "progress": state.get_progress_data(),
    })


def submit_solution(challenge_id: str, source: str) -> str:
    """Run a challenge solution and return its tests and updated game state."""
    state = _require_state()
    challenge = state.get_challenge(challenge_id)
    if challenge is None:
        raise ValueError(f"Unknown challenge: {challenge_id}")
    if challenge_id not in {
        available.id for available in state.get_available_challenges()
    }:
        raise ValueError(f"Challenge is locked: {challenge_id}")

    all_passed, results = challenge.test_solution(source, state.get_all_aliases())
    for result in results:
        result["steps"] = [
            {
                "expression": str(step.expression),
                "description": step.description,
            }
            for step in result.get("steps", [])
        ]

    progress = state.get_progress_data()
    if all_passed:
        solution = Parser(source, state.get_all_aliases()).parse()
        state.complete_challenge(challenge_id, solution)
        progress = state.get_progress_data()

    return json.dumps({
        "all_passed": all_passed,
        "results": results,
        "progress": progress,
        "state": json.loads(get_state()),
    })


def evaluate_expression(source: str) -> str:
    """Evaluate a free-form expression and return its reduction trace."""
    evaluation = parse_and_eval(source, _require_state().get_all_aliases())
    return json.dumps({
        "initial_expression": str(evaluation.initial_expression),
        "final_expression": str(evaluation.final_expression),
        "steps": [
            {
                "expression": str(step.expression),
                "description": step.description,
            }
            for step in evaluation.steps
        ],
    })


def new_game() -> str:
    """Clear in-memory browser progress and return the empty game state."""
    _require_state().reset_progress()
    return get_state()


def _require_state() -> GameState:
    if _game_state is None:
        raise RuntimeError("The browser game has not been initialized")
    return _game_state
