from pyuvm import uvm_analysis_port, uvm_monitor
import sys
sys.path.insert(0, "..")
from tinyalu_utils import TinyAluBfm  # noqa: E402


class Monitor(uvm_monitor):
    def __init__(self, name, parent, method_name):
        super().__init__(name, parent)
        self.method_name = method_name

    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)
        self.bfm = TinyAluBfm()
        self.get_method = getattr(self.bfm, self.method_name)

    async def run_phase(self):
        while True:
            datum = await self.get_method()
            self.ap.write(datum)
