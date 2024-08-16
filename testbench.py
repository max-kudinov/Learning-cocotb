import cocotb
from scoreboard import Scoreboard
from random_tester import RandomTester
from max_tester import MaxTester
from tinyalu_utils import TinyAluBfm


async def execute_test(tester_class):
    bfm = TinyAluBfm()
    scoreboard = Scoreboard()
    await bfm.reset()
    bfm.start_tasks()
    scoreboard.start_tasks()
    tester = tester_class()
    await tester.execute()
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
