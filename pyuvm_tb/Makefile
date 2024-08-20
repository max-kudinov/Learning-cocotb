SIM ?= icarus

TOPLEVEL_LANG ?= verilog
VERILOG_SOURCES += $(PWD)/../tinyalu.sv
TOPLEVEL = tinyalu
MODULE = max_test

COCOTB_HDL_TIMEUNIT = 1ns
COCOTB_HDL_TIMEPRECISION = 1ps

include $(shell cocotb-config --makefiles)/Makefile.sim
