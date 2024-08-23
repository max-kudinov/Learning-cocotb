import pyuvm
import copy
from pyuvm import uvm_object, uvm_test


class PersonRecord(uvm_object):
    def __init__(self, name="", id_number=None):
        super().__init__(name)
        self.id_number = id_number

    def __str__(self):
        return f"Name: {self.get_name()}, ID: {self.id_number}"

    def __eq__(self, other):
        return self.id_number == other.id_number

    def do_copy(self, other):
        super().do_copy(other)
        self.id_number = other.id_number


class StudentRecord(PersonRecord):
    def __init__(self, name="", id_number=None, grades=[]):
        super().__init__(name, id_number)
        self.grades = grades

    def __str__(self):
        return super().__str__() + f" Grades: {self.grades}"

    def do_copy(self, other):
        super().do_copy(other)
        self.grades = list(other.grades)


@pyuvm.test()
class CopyTest(uvm_test):
    async def run_phase(self):
        self.raise_objection()
        mary = StudentRecord("Mary", 33, [97, 82])
        mary_copy = StudentRecord()
        mary_copy.copy(mary)
        print("mary:", mary)
        print("mary_copy:", mary_copy)
        print("-----grades-------")
        print("mary id:", id(mary.grades))
        print("mary_copy id", id(mary_copy.grades))
        self.drop_objection()


@pyuvm.test()
class CloneTest(uvm_test):
    async def run_phase(self):
        self.raise_objection()
        mary = StudentRecord("Mary", 33, [97, 82])
        mary_copy = mary.clone()
        print("mary:", mary)
        print("mary_copy:", mary_copy)
        print("-----grades-------")
        print("mary id:", id(mary.grades))
        print("mary_copy id", id(mary_copy.grades))
        self.drop_objection()
