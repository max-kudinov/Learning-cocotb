import cocotb
from scoreboard import Scoreboard
from random_tester import RandomTester
from max_tester import MaxTester
import sys
sys.path.insert(0, "..")
from tinyalu_utils import TinyAluBfm  # noqa: E402


async def execute_test(tester_class):
    bfm = TinyAluBfm()
    scoreboard = Scoreboard()
    await bfm.reset()

    # Parallel like fork join because we don't await
    # BFM starts interration with the DUT (drive/monitor)
    bfm.start_tasks()
    # Scoreboard gets values from BFM queues
    scoreboard.start_tasks()
    # ----------------------

    tester = tester_class()

    # Sends stimulus to the DUT
    await tester.execute()

    # Check monitored commands and results with a model
    passed = scoreboard.check_results()
    return passed


@cocotb.test()
async def random_test(_):
    """Random operands"""
    passed = await execute_test(RandomTester)
    assert passed


@cocotb.test()
async def max_test(_):
    """Maximum operands"""
    passed = await execute_test(MaxTester)
    assert passed
