"""Game state management"""

import json
from pathlib import Path
from typing import Dict, Set

from game.challenge import Challenge
from interpreter.lambda_interpreter import Expr


class GameState:
    """Manages the game session state."""

    def __init__(self):
        self.completed_challenges: Set[str] = set()
        self.aliases: Dict[str, Expr] = {}
        self.challenges_data: list[Challenge] = []
        self._load_challenges()

    def _load_challenges(self):
        """Load challenges from JSON as typed challenge objects."""
        challenges_path = Path(__file__).parent.parent / "challenges" / "challenges.json"
        with open(challenges_path, 'r', encoding='utf-8') as file:
            raw_challenges = json.load(file)
        self.challenges_data = [Challenge.from_dict(challenge) for challenge in raw_challenges]

    def get_challenge(self, challenge_id: str) -> Challenge | None:
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

    def get_alias(self, alias_id: str) -> Expr:
        """Get alias expression."""
        return self.aliases.get(alias_id)

    def get_all_aliases(self) -> Dict[str, Expr]:
        """Get all available aliases."""
        return self.aliases.copy()
