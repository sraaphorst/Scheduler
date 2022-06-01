from components.optimizer.base import BaseOptimizer, Selection
from common.minimodel import Plan
from typing import List
import random


class DummyOptimizer(BaseOptimizer):

    def __init__(self, seed=42):
        # Set seed for replication
        random.seed(seed)

    def _run(self, plans: List[Plan]):
        """
        Gives a random group/observation to add to plan
        """
        while all(plan.is_full() for plan in plans):

            ran_group = random.choice(list(self.selection.values()))
            for observation in ran_group[0].observations():
                # TODO: This should be constant not lineal time
                for plan in plans:
                    if not plan.is_full and plan.site == observation.site:
                        obs_len = plan.time2slots(observation.total_used())
                        if (plan.time_left() >= obs_len):
                            plan.add(observation, obs_len)
                            break
                        else:
                            # TODO: DO a partial insert
                            # Splitting groups is not yet implemented
                            # Right now we are just going to finish the plan
                            plan.is_full = True
        
    def add(self, selection: Selection):
        # Preparation for the optimizer i.e create chromosomes, etc.
        self.selection = selection
        return self
