from random import randint
import statistics
import pyuvm
from pyuvm import uvm_analysis_export, uvm_analysis_port, uvm_component, uvm_nonblocking_get_port, uvm_subscriber, uvm_test, uvm_tlm_analysis_fifo


class NumberGenerator(uvm_component):
    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)

    async def run_phase(self):
        self.raise_objection()
        for _ in range(9):
            n = randint(1, 10)
            print(n, end=" ")
            self.ap.write(n)
        print()
        self.drop_objection()


class Adder(uvm_analysis_export):
    def start_of_simulation_phase(self):
        self.sum = 0

    def write(self, n):
        self.sum += n

    def report_phase(self):
        self.logger.info(f"Sum: {self.sum}")


class Median(uvm_subscriber):
    def start_of_simulation_phase(self):
        self.numb_list = list()

    def write(self, n):
        self.numb_list.append(n)

    def report_phase(self):
        median = statistics.median(self.numb_list)
        self.logger.info(f"Median: {median}")


class Mult(uvm_analysis_export):
    def start_of_simulation_phase(self):
        self.product = 1

    def write(self, n):
        self.product *= n

    def report_phase(self):
        self.logger.info(f"Product: {self.product}")


class AdderTest(uvm_test):
    def build_phase(self):
        self.num_gen = NumberGenerator("num_gen", self)
        self.adder_export = Adder("adder", self)
        self.mult_export = Mult("mult", self)

    def connect_phase(self):
        self.num_gen.ap.connect(self.adder_export)
        self.num_gen.ap.connect(self.mult_export)


class Average(uvm_component):
    def build_phase(self):
        self.fifo = uvm_tlm_analysis_fifo("fifo", self)
        self.nbgp = uvm_nonblocking_get_port("nbgp", self)

    def connect_phase(self):
        self.nbgp.connect(self.fifo.get_export)
        self.analysis_export = self.fifo.analysis_export

    def report_phase(self):
        success = True
        sum = 0
        count = 0

        while success:
            success, n = self.nbgp.try_get()
            if success:
                sum += n
                count += 1

        self.logger.info(f"Average: {sum/count:0.2f}")


@pyuvm.test()
class AverageTest(uvm_test):
    def build_phase(self):
        self.num_gen = NumberGenerator("num_gen", self)
        self.sum_export = Adder("sum", self)
        self.median = Median("median", self)
        self.avg = Average("avg", self)

    def connect_phase(self):
        self.num_gen.ap.connect(self.sum_export)
        self.num_gen.ap.connect(self.median.analysis_export)
        self.num_gen.ap.connect(self.avg.analysis_export)


class MedianTest(uvm_test):
    def build_phase(self):
        self.num_gen = NumberGenerator("num_gen", self)
        self.sum_export = Adder("sum", self)
        self.median = Median("median", self)

    def connect_phase(self):
        self.num_gen.ap.connect(self.sum_export)
        self.num_gen.ap.connect(self.median.analysis_export)
