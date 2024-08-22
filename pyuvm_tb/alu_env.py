from pyuvm import uvm_env, uvm_tlm_fifo
from driver import Driver
from coverage import Coverage
from monitor import Monitor
from scoreboard import Scoreboard
from base_tester import BaseTester


class AluEnv(uvm_env):

    def build_phase(self):
        self.tester = BaseTester.create("tester", self)
        self.driver = Driver("driver", self)
        self.cmd_fifo = uvm_tlm_fifo("cmd_fifo", self)
        self.scoreboard = Scoreboard("scoreboard", self)
        self.coverage = Coverage("coverage", self)
        self.cmd_mon = Monitor("cmd_monitor", self, "get_cmd")
        self.result_mon = Monitor("result_monitor", self, "get_result")

    def connect_phase(self):
        self.tester.pp.connect(self.cmd_fifo.put_export)
        self.driver.gp.connect(self.cmd_fifo.get_export)
        self.cmd_mon.ap.connect(self.coverage)
        self.cmd_mon.ap.connect(self.scoreboard.cmd_export)
        self.result_mon.ap.connect(self.scoreboard.result_export)
