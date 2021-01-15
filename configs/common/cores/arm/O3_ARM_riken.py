# Copyright (c) 2012 The Regents of The University of Michigan
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Ron Dreslinski

from __future__ import print_function
from __future__ import absolute_import

from m5.objects import *


# Simple ALU Instructions have a latency of 1
class O3_ARM_riken_Simple_Int(FUDesc):
    opList = [OpDesc(opClass='IntAlu', opLat=1)]
    count = 2


# Complex ALU instructions have a variable latencies
class O3_ARM_riken_Complex_Int(FUDesc):
    opList = [
        OpDesc(opClass='IntMult', opLat=4, pipelined=True),
        OpDesc(opClass='IntDiv', opLat=13, pipelined=True),
        OpDesc(opClass='IprAccess', opLat=3, pipelined=True)
    ]
    count = 1


# Floating point and SIMD instructions
class O3_ARM_riken_FP(FUDesc):
    opList = [
        OpDesc(opClass='SimdAdd', opLat=7),
        OpDesc(opClass='SimdAddAcc', opLat=7),
        OpDesc(opClass='SimdAlu', opLat=7),
        OpDesc(opClass='SimdCmp', opLat=5),
        OpDesc(opClass='SimdCvt', opLat=6),
        OpDesc(opClass='SimdMisc', opLat=5),
        OpDesc(opClass='SimdMult', opLat=7),
        OpDesc(opClass='SimdMultAcc', opLat=7),
        OpDesc(opClass='SimdShift', opLat=5),
        OpDesc(opClass='SimdShiftAcc', opLat=5),
        OpDesc(opClass='SimdSqrt', opLat=7),
        OpDesc(opClass='SimdFloatAdd', opLat=6),
        OpDesc(opClass='SimdFloatAlu', opLat=5),
        OpDesc(opClass='SimdFloatCmp', opLat=5),
        OpDesc(opClass='SimdFloatCvt', opLat=5),
        OpDesc(opClass='SimdFloatDiv', opLat=16),
        OpDesc(opClass='SimdFloatMisc', opLat=5),
        OpDesc(opClass='SimdFloatMult', opLat=6),
        OpDesc(opClass='SimdFloatMultAcc', opLat=6),
        OpDesc(opClass='SimdFloatSqrt', opLat=16),
        OpDesc(opClass='FloatAdd', opLat=6),
        OpDesc(opClass='FloatCmp', opLat=5),
        OpDesc(opClass='FloatCvt', opLat=7),
        OpDesc(opClass='FloatDiv', opLat=16, pipelined=True),
        OpDesc(opClass='FloatSqrt', opLat=16, pipelined=True),
        OpDesc(opClass='FloatMult', opLat=6),
        OpDesc(opClass='FloatMultAcc', opLat=6),
        OpDesc(opClass='FloatMisc', opLat=5)
    ]
    count = 2


# Load/Store Units
class O3_ARM_riken_Load(FUDesc):
    opList = [
        OpDesc(opClass='MemRead', opLat=4),
        OpDesc(opClass='FloatMemRead', opLat=4)
    ]
    count = 2


class O3_ARM_riken_Store(FUDesc):
    opList = [
        OpDesc(opClass='MemWrite', opLat=2),
        OpDesc(opClass='FloatMemWrite', opLat=2)
    ]
    count = 1


# Functional Units for this CPU
class O3_ARM_riken_FUP(FUPool):
    FUList = [
        O3_ARM_riken_Simple_Int(),
        O3_ARM_riken_Complex_Int(),
        O3_ARM_riken_Load(),
        O3_ARM_riken_Store(),
        O3_ARM_riken_FP()
    ]


# Bi-Mode Branch Predictor
class O3_ARM_riken_BP(BiModeBP):
    globalPredictorSize = 8192
    globalCtrBits = 2
    choicePredictorSize = 8192
    choiceCtrBits = 2
    BTBEntries = 2048
    BTBTagSize = 18
    RASSize = 16
    instShiftAmt = 2


class O3_ARM_riken_3(DerivO3CPU):
    LQEntries = 16
    SQEntries = 16
    LSQDepCheckShift = 0
    LFSTSize = 1024
    SSITSize = 1024
    decodeToFetchDelay = 1
    renameToFetchDelay = 1
    iewToFetchDelay = 1
    commitToFetchDelay = 1
    renameToDecodeDelay = 1
    iewToDecodeDelay = 1
    commitToDecodeDelay = 1
    iewToRenameDelay = 1
    commitToRenameDelay = 1
    commitToIEWDelay = 1
    fetchWidth = 8
    fetchBufferSize = 16
    fetchToDecodeDelay = 3
    decodeWidth = 4
    decodeToRenameDelay = 2
    renameWidth = 4
    renameToIEWDelay = 1
    issueToExecuteDelay = 1
    dispatchWidth = 6
    issueWidth = 8
    wbWidth = 8
    fuPool = O3_ARM_riken_FUP()
    iewToCommitDelay = 1
    renameToROBDelay = 1
    commitWidth = 4
    squashWidth = 8
    trapLatency = 13
    backComSize = 5
    forwardComSize = 5
    numPhysIntRegs = 128
    numPhysFloatRegs = 512
    numPhysVecRegs = 128
    numIQEntries = 60
    numROBEntries = 180

    switched_out = False
    branchPred = O3_ARM_riken_BP()


# Instruction Cache
class O3_ARM_riken_ICache(Cache):
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 2
    tgts_per_mshr = 8
    size = '32kB'
    assoc = 8
    is_read_only = True
    # Writeback clean lines as well
    writeback_clean = True


# Data Cache
class O3_ARM_riken_DCache(Cache):
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 16
    tgts_per_mshr = 8
    size = '32kB'
    assoc = 8
    write_buffers = 16
    # Consider the L2 a victim cache also for clean lines
    writeback_clean = True


# TLB Cache
# Use a cache as a L2 TLB
class O3_ARM_riken_WalkCache(Cache):
    tag_latency = 4
    data_latency = 4
    response_latency = 4
    mshrs = 6
    tgts_per_mshr = 8
    size = '1kB'
    assoc = 8
    write_buffers = 16
    is_read_only = True
    # Writeback clean lines as well
    writeback_clean = True


# L2 Cache
class O3_ARM_riken_L2(Cache):
    tag_latency = 11
    data_latency = 11
    response_latency = 11
    mshrs = 16
    tgts_per_mshr = 8
    size = '256kB'
    assoc = 8
    write_buffers = 8
    prefetch_on_access = True
    clusivity = 'mostly_excl'
    # Simple stride prefetcher
    prefetcher = StridePrefetcher(degree=8, latency=1)
    # tags = RandomRepl()
