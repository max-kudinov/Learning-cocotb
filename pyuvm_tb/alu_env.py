from pyuvm import uvm_env, uvm_sequencer, uvm_tlm_fifo, ConfigDB
from driver import Driver
from coverage import Coverage
from monitor import Monitor
from scoreboard import Scoreboard
from base_tester import BaseTester


class AluEnv(uvm_env):

    def build_phase(self):
        self.seqr = uvm_sequencer("seqr", self)
        ConfigDB().set(None, "*", "SEQR", self.seqr)
        self.driver = Driver("driver", self)
        self.scoreboard = Scoreboard("scoreboard", self)
        self.coverage = Coverage("coverage", self)
        self.cmd_mon = Monitor("cmd_monitor", self, "get_cmd")
        self.result_mon = Monitor("result_monitor", self, "get_result")

    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)
        self.cmd_mon.ap.connect(self.coverage)
        self.cmd_mon.ap.connect(self.scoreboard.cmd_export)
        self.result_mon.ap.connect(self.scoreboard.result_export)
