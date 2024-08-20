from base_env import BaseEnv
from random_tester import RandomTester


class RandomEnv(BaseEnv):
    """Generate random operands"""

    def build_phase(self):
        super().build_phase()
        self.tester = RandomTester("tester", self)
