from pyuvm import uvm_sequence_item


class AluResultItem(uvm_sequence_item):
    def __init__(self, name, result):
        super().__init__(name)
        self.result = result

    def __str__(self):
        return f"RESULT: {self.result}"
