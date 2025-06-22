import os
from pathlib import Path

from rs_fec import rs_enc

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

    for i in range(64):
        dut.msg_in[i] = 0
    dut.msg_valid.value = 0

    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 10)


async def input_driver(dut):
    """Drive the slave side of DUT"""
    await RisingEdge(dut.clk)
    for _ in range(TEST_SYMBOLS):
        symbol = rng.integers(0, 256, size=64, dtype=int)
        for i in range(64):
            dut.msg_in[i].value = int(symbol[i])
        dut.msg_valid.value = 1
        await RisingEdge(dut.clk)
    dut.msg_valid.value = 0


async def input_monitor(dut):
    """Monitor the slave side of DUT"""
    while True:
        await RisingEdge(dut.clk)

        if dut.msg_valid.value:
            input_data = np.zeros(64, dtype=int)
            for i in range(64):
                input_data[i] = dut.msg_in[i].value.integer
            input_queue.put_nowait(input_data)


async def output_monitor(dut):
    """Monitor the master side of DUT"""
    while True:
        await RisingEdge(dut.clk)

        if dut.parity_valid.value:
            output_data = np.zeros(4, dtype=int)
            for i in range(4):
                output_data[i] = dut.parity_out[i].value.integer
            output_queue.put_nowait(output_data)


async def checker():
    """Check the output of DUT"""
    n = 0
    while True:
        input_data = await input_queue.get()
        output_data = await output_queue.get()
        expected_data = rs_enc(input_data)
        n += 1
        cocotb.log.info("# %d / %d", n, TEST_SYMBOLS)
        assert np.array_equal(expected_data, output_data), (
            f"Input data: {input_data}\nExpected: {expected_data}got: {output_data}"
        )


# MARK: Tests


@cocotb.test
async def test_rs_encoder(dut):
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


def test_rs_encoder_runner():
    """Run the test for RS Encoder"""
    sim = "questa"

    hdl_toplevel = "rs_encoder"
    hdl_toplevel_lang = "verilog"

    verilog_sources = [
        prj_path / "rs_encoder.sv",
    ]

    test_args = [
        # f"-gSOME_PARAMETER={SOME_PARAMETER}",
    ]

    runner = get_runner(sim)
    runner.build(
        hdl_toplevel=hdl_toplevel,
        verilog_sources=verilog_sources,
        always=True,
    )

    runner.test(
        hdl_toplevel=hdl_toplevel,
        hdl_toplevel_lang=hdl_toplevel_lang,
        test_args=test_args,
        test_module="test_rs_encoder",
        waves=True,
        gui=GUI,
    )


if __name__ == "__main__":
    test_rs_encoder_runner()
