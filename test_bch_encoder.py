import os
from pathlib import Path

from bch_fec import bch_enc

import cocotb
import numpy as np
from cocotb.clock import Clock
from cocotb.queue import Queue
from cocotb.runner import get_runner
from cocotb.triggers import ClockCycles, RisingEdge


# MARK: Env


prj_path = Path(__file__).resolve().parent
rng = np.random.default_rng(1234567890)

GUI = os.environ.get("GUI", "false").lower() == "true"

TEST_SYMBOLS = 1000

# MARK: Helper


input_queue = Queue()
output_queue = Queue()


async def reset(dut):
    """Reset the DUT"""
    dut.rst_n.value = 0

    dut.data_in.value = 0
    dut.vld_in.value = 0

    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 10)


async def input_driver(dut):
    """Drive the slave side of DUT"""
    await RisingEdge(dut.clk)
    for _ in range(TEST_SYMBOLS):
        symbol = rng.integers(0, 2, size=512, dtype=int)
        data_in = 0
        for i in range(512):
            data_in <<= 1
            data_in |= int(symbol[i])
        dut.data_in.value = data_in
        dut.vld_in.value = 1
        await RisingEdge(dut.clk)
    dut.vld_in.value = 0


async def input_monitor(dut):
    """Monitor the slave side of DUT"""
    while True:
        await RisingEdge(dut.clk)

        if dut.vld_in.value:
            input_data = np.zeros(512, dtype=int)
            for i in range(512):
                input_data[i] = (dut.data_in.value >> i) & 0x1
            input_data = np.flip(input_data)
            input_queue.put_nowait(input_data)


async def output_monitor(dut):
    """Monitor the master side of DUT"""
    while True:
        await RisingEdge(dut.clk)

        if dut.vld_out.value:
            output_data = np.zeros(20, dtype=int)
            for i in range(20):
                output_data[i] = (dut.parity_out.value >> i) & 0x1
            output_data = np.flip(output_data)
            output_queue.put_nowait(output_data)


async def checker():
    """Check the output of DUT"""
    n = 0
    while True:
        input_data = await input_queue.get()
        output_data = await output_queue.get()
        expected_data = bch_enc(input_data)
        n += 1
        cocotb.log.info("# %d / %d", n, TEST_SYMBOLS)
        assert np.array_equal(expected_data, output_data), (
            f"Input data: {input_data}\nExpected: {expected_data}\nGot: {output_data}"
        )


# MARK: Tests


@cocotb.test
async def test_bch_encoder(dut):
    """Test case for RS Encoder"""
    cocotb.log.info("Simulation started")

    # Create clock and start it
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start(start_high=False))

    # Reset the DUT
    await reset(dut)

    # Run test multiple times
    cocotb.start_soon(output_monitor(dut))
    cocotb.start_soon(input_monitor(dut))
    cocotb.start_soon(checker())

    await input_driver(dut)

    await ClockCycles(dut.clk, 100)
    cocotb.log.info("Simulation finished")


def test_bch_encoder_runner():
    """Run the test for RS Encoder"""
    sim = "verilator"

    hdl_toplevel = "bch_encoder"
    hdl_toplevel_lang = "verilog"

    verilog_sources = [
        prj_path / "rtl/bch_encoder.sv",
    ]

    extra_args = [
        "--trace",
        "--trace-fst",
        "--trace-structs",
    ]

    test_args = [
        # f"-gSOME_PARAMETER={SOME_PARAMETER}",
    ]

    runner = get_runner(sim)
    runner.build(
        hdl_toplevel=hdl_toplevel,
        verilog_sources=verilog_sources,
        build_args=extra_args,
        clean=True,
        always=True,
        waves=True,
    )

    runner.test(
        hdl_toplevel=hdl_toplevel,
        hdl_toplevel_lang=hdl_toplevel_lang,
        test_args=test_args,
        test_module="test_bch_encoder",
        waves=True,
        gui=GUI,
    )


if __name__ == "__main__":
    test_bch_encoder_runner()
