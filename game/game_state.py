"""Game state management"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Set

from game.challenge import Challenge
from interpreter.lambda_interpreter import Expr, LambdaSyntaxError, Parser


class ProgressLoadError(RuntimeError):
    """The saved progress file is invalid or could not be read."""


class ProgressSaveError(RuntimeError):
    """The saved progress file could not be written or removed."""


class GameState:
    """Manages the game session state."""

    PROGRESS_VERSION = 1

    def __init__(
        self,
        progress_path: Optional[Path] = None,
        challenges_data: Optional[List[Mapping[str, Any]]] = None,
        auto_save: bool = True,
    ):
        self.completed_challenges: Set[str] = set()
        self.aliases: Dict[str, Expr] = {}
        self.challenges_data: list[Challenge] = []
        self.auto_save = auto_save
        self.progress_path = progress_path or (
            Path.home() / ".lambda-calculus-game" / "progress.json"
        )
        if challenges_data is None:
            self._load_challenges()
        else:
            self.challenges_data = [
                Challenge.from_dict(challenge) for challenge in challenges_data
            ]
        if self.auto_save:
            self._load_progress()

    def _load_challenges(self):
        """Load challenges from JSON as typed challenge objects."""
        challenges_path = Path(__file__).parent.parent / "challenges" / "challenges.json"
        with open(challenges_path, 'r', encoding='utf-8') as file:
            raw_challenges = json.load(file)
        self.challenges_data = [Challenge.from_dict(challenge) for challenge in raw_challenges]

    def get_challenge(self, challenge_id: str) -> Optional[Challenge]:
        """Get challenge by ID."""
        for challenge in self.challenges_data:
            if challenge.id == challenge_id:
                return challenge
        return None

    def get_available_challenges(self) -> list[Challenge]:
        """Get list of available (unlocked) challenges."""
        available = []
        for challenge in self.challenges_data:
            if self._is_unlocked(challenge.id):
                available.append(challenge)
        return available

    def _is_unlocked(self, challenge_id: str) -> bool:
        """Check if a challenge is unlocked."""
        challenge = self.get_challenge(challenge_id)
        if not challenge:
            return False

        requirements = challenge.requirements
        return all(req in self.completed_challenges for req in requirements)

    def is_completed(self, challenge_id: str) -> bool:
        """Check if a challenge is completed."""
        return challenge_id in self.completed_challenges

    def complete_challenge(self, challenge_id: str, solution: Expr):
        """Mark a challenge as completed and add its alias."""
        if challenge_id not in self.completed_challenges:
            self.completed_challenges.add(challenge_id)
            self.aliases[challenge_id] = solution
            if self.auto_save:
                try:
                    self._save_progress()
                except ProgressSaveError:
                    self.completed_challenges.remove(challenge_id)
                    self.aliases.pop(challenge_id, None)
                    raise

    def reset_progress(self):
        """Clear saved and in-memory challenge progress."""
        if self.auto_save:
            try:
                self.progress_path.unlink(missing_ok=True)
            except OSError as exc:
                raise ProgressSaveError(
                    f"Could not remove saved progress at {self.progress_path}: {exc}"
                ) from exc

        self.completed_challenges.clear()
        self.aliases.clear()

    def get_progress_data(self) -> Dict[str, Any]:
        """Return the current progress in the versioned save-file format."""
        return {
            "version": self.PROGRESS_VERSION,
            "completed_challenges": sorted(self.completed_challenges),
            "aliases": {
                challenge_id: str(self.aliases[challenge_id])
                for challenge_id in sorted(self.completed_challenges)
            },
        }

    def restore_progress_data(self, data: Any):
        """Validate and restore progress supplied by a non-file storage layer."""
        try:
            completed, aliases = self._parse_progress(data)
        except (KeyError, TypeError, ValueError, LambdaSyntaxError) as exc:
            raise ProgressLoadError(f"Invalid saved progress: {exc}") from exc

        self.completed_challenges = completed
        self.aliases = aliases

    def _load_progress(self):
        """Restore challenge completion and aliases from the save file."""
        try:
            contents = self.progress_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return
        except OSError as exc:
            raise ProgressLoadError(
                f"Could not read saved progress at {self.progress_path}: {exc}"
            ) from exc

        try:
            data = json.loads(contents)
            completed, aliases = self._parse_progress(data)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError, LambdaSyntaxError) as exc:
            raise ProgressLoadError(
                f"Invalid saved progress at {self.progress_path}: {exc}"
            ) from exc

        self.completed_challenges = completed
        self.aliases = aliases

    def _parse_progress(self, data: Any) -> tuple[Set[str], Dict[str, Expr]]:
        if not isinstance(data, dict):
            raise ValueError("save data must be a JSON object")
        if (
            type(data.get("version")) is not int
            or data["version"] != self.PROGRESS_VERSION
        ):
            raise ValueError(f"unsupported save version: {data.get('version')!r}")

        completed_data = data.get("completed_challenges")
        aliases_data = data.get("aliases")
        if not isinstance(completed_data, list) or not all(
            isinstance(challenge_id, str) for challenge_id in completed_data
        ):
            raise ValueError("'completed_challenges' must be a list of challenge IDs")
        if not isinstance(aliases_data, dict) or not all(
            isinstance(challenge_id, str) and isinstance(expression, str)
            for challenge_id, expression in aliases_data.items()
        ):
            raise ValueError("'aliases' must map challenge IDs to expressions")

        completed = set(completed_data)
        if len(completed) != len(completed_data):
            raise ValueError("'completed_challenges' contains duplicate IDs")

        known_ids = {challenge.id for challenge in self.challenges_data}
        if not completed.issubset(known_ids):
            unknown = sorted(completed - known_ids)
            raise ValueError(f"unknown completed challenge IDs: {', '.join(unknown)}")
        if set(aliases_data) != completed:
            raise ValueError("saved aliases must match the completed challenge IDs")
        for challenge_id in completed:
            challenge = self.get_challenge(challenge_id)
            if challenge is not None and not set(challenge.requirements).issubset(completed):
                raise ValueError(
                    f"completed challenge {challenge_id} is missing prerequisites"
                )

        aliases = {
            challenge_id: Parser(expression).parse()
            for challenge_id, expression in aliases_data.items()
        }
        return completed, aliases

    def _save_progress(self):
        """Write current progress as a readable JSON text file."""
        data = self.get_progress_data()

        try:
            self.progress_path.parent.mkdir(parents=True, exist_ok=True)
            self.progress_path.write_text(
                json.dumps(data, indent=2) + "\n",
                encoding="utf-8",
            )
        except OSError as exc:
            raise ProgressSaveError(
                f"Could not save progress at {self.progress_path}: {exc}"
            ) from exc

    def get_alias(self, alias_id: str) -> Expr:
        """Get alias expression."""
        return self.aliases.get(alias_id)

    def get_all_aliases(self) -> Dict[str, Expr]:
        """Get all available aliases."""
        return self.aliases.copy()
