import argparse

# Import the m5 library and all SimObjects that have been compiled
import m5
from m5.objects import *

# Import custom cache config
from caches import *

parser = argparse.ArgumentParser()
parser.add_argument('--l1i_size', help="L1 instruction cache size")
parser.add_argument('--l1d_size', help="L1 data cache size")
parser.add_argument('--l2_size', help="Unified L2 cache size")

args = parser.parse_args()

# System objects are the parent of all the other objects in the simulated system
system = System()

# Clock domain
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Memory system (timing mode used except for special-cases)
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# Timing CPU is similar to SimEng's Emulation mode but memory requests have latency
system.cpu = TimingSimpleCPU()

# System-wide memory bus
system.membus = SystemXBar()

# Create caches defined in caches.py
system.cpu.icache = L1ICache(args)
system.cpu.dcache = L1DCache(args)

# Connect caces to CPU ports using defined helper functions
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# L2 cache only expects one connection port so create a bus to connect both L1's to it
system.l2bus = L2XBar()
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# Create and connect L2 cache to L1-L2 bus
system.l2cache = L2Cache(args)
system.l2cache.connectCPUSideBus(system.l2bus)
system.l2cache.connectMemSideBus(system.membus)

# ...
system.cpu.createInterruptController()
system.system_port = system.membus.cpu_side_ports

# DDR3 memory controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Create process
process = Process()
process.cmd = ['tests/test-progs/hello/bin/arm/linux/hello']
system.cpu.workload = process
system.cpu.createThreads()

# Create Root object and instantiate simulation
root = Root(full_system=False, system=system)
m5.instantiate()

# Simulate
print("Beginning simulation!")
exit_event = m5.simulate()

# Print final state of simulation
print('Exiting @ tick {} because {}'.format(m5.curTick(),
                                            exit_event.getCause()))
