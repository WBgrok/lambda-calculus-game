"""Game state management"""

import json
from pathlib import Path
from typing import Set, Dict
from interpreter.lambda_interpreter import Expr


class GameState:
    """Manages the game session state"""
    
    def __init__(self):
        self.completed_challenges: Set[str] = set()
        self.aliases: Dict[str, Expr] = {}
        self.challenges_data: list = []
        self._load_challenges()
    
    def _load_challenges(self):
        """Load challenges from JSON"""
        challenges_path = Path(__file__).parent.parent / "challenges" / "challenges.json"
        with open(challenges_path, 'r') as f:
            self.challenges_data = json.load(f)
    
    def get_challenge(self, challenge_id: str) -> Dict:
        """Get challenge by ID"""
        for ch in self.challenges_data:
            if ch['id'] == challenge_id:
                return ch
        return None
    
    def get_available_challenges(self) -> list:
        """Get list of available (unlocked) challenges"""
        available = []
        for ch in self.challenges_data:
            if self._is_unlocked(ch['id']):
                available.append(ch)
        return available
    
    def _is_unlocked(self, challenge_id: str) -> bool:
        """Check if a challenge is unlocked"""
        ch = self.get_challenge(challenge_id)
        if not ch:
            return False
        
        # Challenge is unlocked if all requirements are completed
        requirements = ch.get('requirements', [])
        return all(req in self.completed_challenges for req in requirements)
    
    def is_completed(self, challenge_id: str) -> bool:
        """Check if a challenge is completed"""
        return challenge_id in self.completed_challenges
    
    def complete_challenge(self, challenge_id: str, solution: Expr):
        """Mark a challenge as completed and add its alias"""
        if challenge_id not in self.completed_challenges:
            self.completed_challenges.add(challenge_id)
            self.aliases[challenge_id] = solution
    
    def get_alias(self, alias_id: str) -> Expr:
        """Get alias expression"""
        return self.aliases.get(alias_id)
    
    def get_all_aliases(self) -> Dict[str, Expr]:
        """Get all available aliases"""
        return self.aliases.copy()
