from pyuvm import uvm_env
from scoreboard import Scoreboard


class BaseEnv(uvm_env):
    """Instantiate the scoreboard"""

    def build_phase(self):
        self.scoreboard = Scoreboard("scoreboard", self)
