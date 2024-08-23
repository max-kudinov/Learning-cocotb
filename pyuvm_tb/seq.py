import random
from base_seq import BaseSeq


class RandomSeq(BaseSeq):
    def set_operands(self, tr):
        tr.A = random.randint(0, 255)
        tr.B = random.randint(0, 255)


class MaxSeq(BaseSeq):
    def set_operands(self, tr):
        tr.A = 0xFF
        tr.B = 0xFF
