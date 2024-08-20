from base_env import BaseEnv
from max_tester import MaxTester


class MaxEnv(BaseEnv):
    """Generate maximum operands"""

    def build_phase(self):
        super().build_phase()
        self.tester = MaxTester("tester", self)
