from pyuvm import UVMConfigItemNotFound, uvm_analysis_export, ConfigDB
import sys

sys.path.insert(0, "..")
from tinyalu_utils import Ops  # noqa: E402


class Coverage(uvm_analysis_export):
    def start_of_simulation_phase(self):
        self.cvg = set()
        try:
            self.disable_errors = ConfigDB().get(self, "", "DISABLE_COVERAGE_ERRORS")
        except UVMConfigItemNotFound:
            self.disable_errors = False

    def write(self, cmd):
        _, _, op = cmd
        self.cvg.add(Ops(op))

    def check_phase(self):
        if not self.disable_errors:
            if len(set(Ops) - self.cvg) > 0:
                self.logger.error(
                    f"Functional coverage error. Missed {set(Ops) - self.cvg}"
                )
                assert False
            else:
                self.logger.info("Covered all operations")
