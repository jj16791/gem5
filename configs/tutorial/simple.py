# Import the m5 library and all SimObjects that have been compiled
import m5
from m5.objects import *

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

# Connect CPU cache ports direct to memory bus (No caches so connect straight to membus)
# Memory systems have a 'mem_side_ports' and 'cpu_side_ports' port where a 'mem_side_ports' ports send requests and 'cpu_side_ports' ports return requests
system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports

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
