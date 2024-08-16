import pyuvm
from pyuvm import *


@pyuvm.test()
class HelloWorldTest(uvm_test):
    async def run_phase(self):
        self.raise_objection()
        self.logger.info("Hello, world!")
        self.drop_objection()
