import cocotb
from pyuvm import uvm_component, uvm_get_port, uvm_tlm_analysis_fifo
import sys
sys.path.insert(0, "..")
from tinyalu_utils import TinyAluBfm, Ops, alu_prediction   # noqa: E402


class Scoreboard(uvm_component):
    def build_phase(self):
        self.cmd_mon_fifo = uvm_tlm_analysis_fifo("cmd_mon_fifo", self)
        self.result_mon_fifo = uvm_tlm_analysis_fifo("result_mon_fifo", self)
        self.cmd_gp = uvm_get_port("cmd_gp", self)
        self.result_gp = uvm_get_port("result_gp", self)

    def connect_phase(self):
        self.cmd_gp.connect(self.cmd_mon_fifo.get_export)
        self.result_gp.connect(self.result_mon_fifo.get_export)
        self.cmd_export = self.cmd_mon_fifo.analysis_export
        self.result_export = self.result_mon_fifo.analysis_export

    def check_phase(self):
        passed = True
        while True:
            got_next_cmd, cmd = self.cmd_gp.try_get()

            if not got_next_cmd:
                break

            result_exists, actual = self.result_gp.try_get()

            if not result_exists:
                raise RuntimeError(f"Missing result for command {cmd}")

            a, b, op = cmd
            op = Ops(op)
            prediction = alu_prediction(a, b, op)

            if actual == prediction:
                self.logger.info(f"PASSED: {a:02x} {op.name} {b:02x} = "
                                 f"{actual:04x}")
            else:
                self.logger.error(
                    f"FAILED: {a:02x} {op.name} {b:02x} = {actual:04x}"
                    f" - predicted {prediction:04x}")
                passed = False

        assert passed
