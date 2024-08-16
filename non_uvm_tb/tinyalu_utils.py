import cocotb
from cocotb.triggers import FallingEdge
from cocotb.queue import QueueEmpty, Queue
import enum
import logging
import pyuvm


# #### The OPS enumeration

# Figure 4: The operation enumeration
@enum.unique
class Ops(enum.IntEnum):
    """Legal ops for the TinyALU"""
    ADD = 1
    AND = 2
    XOR = 3
    MUL = 4


# #### The alu_prediction function

# Figure 5: The prediction function for the scoreboard
def alu_prediction(A, B, op):
    """Python model of the TinyALU"""
    assert isinstance(op, Ops), "The tinyalu op must be of type Ops"
    if op == Ops.ADD:
        result = A + B
    elif op == Ops.AND:
        result = A & B
    elif op == Ops.XOR:
        result = A ^ B
    elif op == Ops.MUL:
        result = A * B
    return result


# #### The logger

# Figure 6: Setting up logging using the logger variable
logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# ### Reading a signal value
# Figure 6: get_int() converts a bus to an integer
# turning a value of x or z to 0
def get_int(signal):
    try:
        int_val = int(signal.value)
    except ValueError:
        int_val = 0
    return int_val


# ## The TinyAluBfm singleton
# ### Initializing the TinyAluBfm object

class TinyAluBfm(metaclass=pyuvm.Singleton):
    def __init__(self):
        """Initialize the BFM"""
        self.dut = cocotb.top
        self.cmd_driver_queue = Queue(maxsize=1)
        self.cmd_mon_queue = Queue(maxsize=0)
        self.result_mon_queue = Queue(maxsize=0)

    async def reset(self):
        """Reset the design"""
        await FallingEdge(self.dut.clk)
        self.dut.reset_n.value = 0
        self.dut.A.value = 0
        self.dut.B.value = 0
        self.dut.op.value = 0
        await FallingEdge(self.dut.clk)
        self.dut.reset_n.value = 1
        await FallingEdge(self.dut.clk)

    async def result_mon(self):
        """Monitor results from DUT"""
        prev_done = 0
        while True:
            await FallingEdge(self.dut.clk)
            done = get_int(self.dut.done)
            if prev_done == 0 and done == 1:
                result = get_int(self.dut.result)
                self.result_mon_queue.put_nowait(result)
            prev_done = done

    async def cmd_mon(self):
        """Monitor stimuli from TB to DUT"""
        prev_start = 0
        while True:
            await FallingEdge(self.dut.clk)
            start = get_int(self.dut.start)
            if prev_start == 0 and start == 1:
                cmd_tupple = (get_int(self.dut.A),
                              get_int(self.dut.B),
                              get_int(self.dut.op))
                self.cmd_mon_queue.put_nowait(cmd_tupple)
            prev_start = start

    async def cmd_driver(self):
        """Drive the DUT lol"""
        self.dut.start.value = 0
        self.dut.A.value = 0
        self.dut.B.value = 0
        self.dut.op.value = 0
        while True:
            await FallingEdge(self.dut.clk)
            start = get_int(self.dut.start)
            done = get_int(self.dut.done)

            if start == 0 and done == 0:
                try:
                    (a, b, op) = self.cmd_driver_queue.get_nowait()
                    self.dut.A.value = a
                    self.dut.B.value = b
                    self.dut.op.value = op
                    self.dut.start.value = 1
                except QueueEmpty:
                    continue
            elif start == 1 and done == 1:
                self.dut.start.value = 0

    def start_tasks(self):
        """Start all three BFMs"""
        cocotb.start_soon(self.cmd_driver())
        cocotb.start_soon(self.cmd_mon())
        cocotb.start_soon(self.result_mon())

    async def get_cmd(self):
        """Get the next command"""
        cmd = await self.cmd_mon_queue.get()
        return cmd

    async def get_result(self):
        """Get result from the queue"""
        result = await self.result_mon_queue.get()
        return result

    async def send_op(self, a, b, op):
        """Send data to the queue"""
        cmd_tupple = (a, b, op)
        await self.cmd_driver_queue.put(cmd_tupple)
