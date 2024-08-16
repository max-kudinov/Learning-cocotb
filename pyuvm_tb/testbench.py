import pyuvm
from pyuvm import uvm_test


@pyuvm.test()
class HelloWorldTest(uvm_test):
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Hello, world :)")
        self.drop_objection()
