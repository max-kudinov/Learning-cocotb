from pyuvm import uvm_sequence_item
import sys

sys.path.insert(0, "..")
from tinyalu_utils import Ops  # noqa: E402


class AluSeqItem(uvm_sequence_item):
    def __init__(self, name, a, b, op):
        super().__init__(name)
        self.A = a
        self.B = b
        self.op = Ops(op)

    def __eq__(self, other):
        same = self.A == other.A and self.B == other.B and self.op == other.op
        return same

    def __str__(self):
        return f"{self.get_name()}: A 0x{self.A:02x} \
                 OP: {self.op.name} ({self.op.value}) B: 0x{self.B:02x}"
