# This is a blueprint for the project
# AI-generated

import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ActionType(Enum):
    UPVOTE = 1       # Positive signal injection
    DOWNVOTE = -1    # Negative signal suppression
    HOVER_ONLY = 0   # Weak signal / passive observation
    SKIP = -2        # Avoid reinforcement


@dataclass
class ItemMetadata:
    item_id: str
    tags: Dict[str, float]  # e.g., {"cooking": 0.8, "tech": 0.2}
    length_sec: float


@dataclass
class ActionInstruction:
    item_id: str
    action: ActionType
    watch_duration_sec: float
    reasoning: str


class TagProfileManager:
    """Tracks observed tag weights and measures profile state entropy [4, 5]."""

    def __init__(self):
        self.profile_weights: Dict[str, float] = {}

    def update_profile(self, item_tags: Dict[str, float], action_multiplier: float):
        """Updates internal profile representation based on executed interactions [4, 5]."""
        for tag, weight in item_tags.items():
            current = self.profile_weights.get(tag, 0.0)
            # Add or reduce tag weight depending on upvote (+1) or downvote (-1)
            self.profile_weights[tag] = max(0.0, current + (weight * action_multiplier))

    def get_normalized_distribution(self) -> Dict[str, float]:
        """Returns softmax or normalized probability distribution over all tags."""
        total = sum(self.profile_weights.values())
        if total == 0:
            return {}
        return {k: v / total for k, v in self.profile_weights.items()}

    def compute_shannon_entropy(self) -> float:
        """Calculates global tag entropy. Max entropy = uniform distribution (full obfuscation) [6]."""
        probs = np.array(list(self.get_normalized_distribution().values()))
        probs = probs[probs > 0]
        if len(probs) <= 1:
            return 0.0
        entropy = -np.sum(probs * np.log2(probs))
        max_entropy = np.log2(len(probs))
        return float(entropy / max_entropy)  # Normalized [3]


class PivotingObfuscationEngine:
    """
    Generalized 'Pivoting Additions' Algorithm [1].
    Calculates adversarial noise vectors to flatten tag dominance.
    """

    def __init__(self, target_entropy: float = 0.95):
        self.target_entropy = target_entropy

    def calculate_ideal_perturbation_vector(self, current_dist: Dict[str, float]) -> Dict[str, float]:
        """
        Determines which tags need positive reinforcement (pivoting additions)
        and which need suppression to achieve max tag entropy [1, 6].
        """
        if not current_dist:
            return {}

        num_tags = len(current_dist)
        uniform_target = 1.0 / num_tags

        # Calculate Delta_w = Target_Distribution - Current_Distribution
        tag_deltas = {}
        for tag, prob in current_dist.items():
            tag_deltas[tag] = uniform_target - prob

        return tag_deltas


class ActionDecisionPlanner:
    """Maps ideal perturbation vectors into concrete Upvote/Downvote actions [4, 5]."""

    def __init__(self, engine: PivotingObfuscationEngine):
        self.engine = engine

    def evaluate_candidates(
        self, candidates: List[ItemMetadata], profile_mgr: TagProfileManager
    ) -> List[ActionInstruction]:
        current_dist = profile_mgr.get_normalized_distribution()
        ideal_deltas = self.engine.calculate_ideal_perturbation_vector(current_dist)

        instructions = []
        for item in candidates:
            # Score item based on alignment with ideal perturbation delta
            alignment_score = sum(
                item.tags.get(tag, 0.0) * delta for tag, delta in ideal_deltas.items()
            )

            # Assign pivoting action based on alignment score
            if alignment_score > 0.15:
                # Item contains under-represented tags -> UPVOTE (Pivoting Addition) [1, 4]
                action = ActionType.UPVOTE
                watch_time = min(item.length_sec * 0.3, 15.0)  # Minimize total execution time [6]
                reason = "Injecting pivoting tags to boost profile entropy"
            elif alignment_score < -0.15:
                # Item contains over-represented tags -> DOWNVOTE / Signal Suppression [4]
                action = ActionType.DOWNVOTE
                watch_time = 2.0  # Skip quickly
                reason = "Suppressing dominant tags to reduce homogenization"
            else:
                action = ActionType.HOVER_ONLY
                watch_time = 5.0
                reason = "Neutral impact on tag entropy"

            instructions.append(
                ActionInstruction(
                    item_id=item.item_id,
                    action=action,
                    watch_duration_sec=watch_time,
                    reasoning=reason,
                )
            )

        return instructions


class CountermeasureController:
    """Main orchestration loop connecting Backend logic to Frontend scraper [3, 5]."""

    def __init__(self):
        self.profile_mgr = TagProfileManager()
        self.engine = PivotingObfuscationEngine()
        self.planner = ActionDecisionPlanner(self.engine)

    def process_recommendation_batch(self, raw_feed: List[ItemMetadata]) -> List[ActionInstruction]:
        """Executes one cycle of metadata extraction, evaluation, and profile updating [5]."""
        # 1. Plan actions for current feed candidates
        instructions = self.planner.evaluate_candidates(raw_feed, self.profile_mgr)

        # 2. Simulate feedback updating internal profile weights [5]
        for item, inst in zip(raw_feed, instructions):
            multiplier = inst.action.value
            self.profile_mgr.update_profile(item.tags, action_multiplier=multiplier)

        # 3. Log updated privacy/entropy metrics [5, 6]
        current_entropy = self.profile_mgr.compute_shannon_entropy()
        print(f"[Entropy Monitor] Profile Tag Entropy: {current_entropy:.4f} / 1.0000")

        return instructions