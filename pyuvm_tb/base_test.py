from pyuvm import *  # noqa: F403
from scoreboard import Scoreboard
import sys
sys.path.insert(0, "..")
from tinyalu_utils import TinyAluBfm  # noqa: E402


class BaseTest(uvm_test):
    async def run_phase(self):
        self.raise_objection()
        bfm = TinyAluBfm()
        scoreboard = Scoreboard()
        await bfm.reset()

        bfm.start_tasks()
        scoreboard.start_tasks()

        await self.tester.execute()
        passed = scoreboard.check_results()
        assert passed
        self.drop_objection()
