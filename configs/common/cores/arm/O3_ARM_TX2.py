from __future__ import print_function
from __future__ import absolute_import

from m5.objects import *


# Port 0 of TX2
class O3_ARM_TX2_Port0(FUDesc):
    opList = [
        OpDesc(opClass='IntAlu', opLat=1),
        OpDesc(opClass='SimdAdd', opLat=7),
        OpDesc(opClass='SimdAddAcc', opLat=7),
        OpDesc(opClass='SimdAlu', opLat=7),
        OpDesc(opClass='SimdCmp', opLat=7),
        OpDesc(opClass='SimdCvt', opLat=7),
        OpDesc(opClass='SimdMisc', opLat=5),
        OpDesc(opClass='SimdMult', opLat=7),
        OpDesc(opClass='SimdMultAcc', opLat=7),
        OpDesc(opClass='SimdShift', opLat=7),
        OpDesc(opClass='SimdShiftAcc', opLat=7),
        OpDesc(opClass='SimdSqrt', opLat=6),
        OpDesc(opClass='SimdFloatAdd', opLat=6),
        OpDesc(opClass='SimdFloatAlu', opLat=6),
        OpDesc(opClass='SimdFloatCmp', opLat=5),
        OpDesc(opClass='SimdFloatCvt', opLat=7),
        OpDesc(opClass='SimdFloatDiv', opLat=16),
        OpDesc(opClass='SimdFloatMisc', opLat=5),
        OpDesc(opClass='SimdFloatMult', opLat=6),
        OpDesc(opClass='SimdFloatMultAcc', opLat=6),
        OpDesc(opClass='SimdFloatSqrt', opLat=23),
        OpDesc(opClass='FloatAdd', opLat=6),
        OpDesc(opClass='FloatCmp', opLat=5),
        OpDesc(opClass='FloatCvt', opLat=7),
        OpDesc(opClass='FloatDiv', opLat=23, pipelined=False),
        OpDesc(opClass='FloatSqrt', opLat=23, pipelined=False),
        OpDesc(opClass='FloatMult', opLat=6),
        OpDesc(opClass='FloatMultAcc', opLat=6),
        OpDesc(opClass='FloatMisc', opLat=5)
    ]
    count = 1


# Port 1 of TX2
class O3_ARM_TX2_Port1(FUDesc):
    opList = [
        OpDesc(opClass='IntAlu', opLat=1),
        OpDesc(opClass='IntMult', opLat=5),
        OpDesc(opClass='IntDiv', opLat=13, pipelined=False),
        OpDesc(opClass='SimdAdd', opLat=7),
        OpDesc(opClass='SimdAddAcc', opLat=7),
        OpDesc(opClass='SimdAlu', opLat=7),
        OpDesc(opClass='SimdCmp', opLat=7),
        OpDesc(opClass='SimdCvt', opLat=7),
        OpDesc(opClass='SimdMisc', opLat=5),
        OpDesc(opClass='SimdMult', opLat=7),
        OpDesc(opClass='SimdMultAcc', opLat=7),
        OpDesc(opClass='SimdShift', opLat=7),
        OpDesc(opClass='SimdShiftAcc', opLat=7),
        OpDesc(opClass='SimdSqrt', opLat=6),
        OpDesc(opClass='SimdFloatAdd', opLat=6),
        OpDesc(opClass='SimdFloatAlu', opLat=6),
        OpDesc(opClass='SimdFloatCmp', opLat=5),
        OpDesc(opClass='SimdFloatCvt', opLat=7),
        OpDesc(opClass='SimdFloatDiv', opLat=16),
        OpDesc(opClass='SimdFloatMisc', opLat=5),
        OpDesc(opClass='SimdFloatMult', opLat=6),
        OpDesc(opClass='SimdFloatMultAcc', opLat=6),
        OpDesc(opClass='SimdFloatSqrt', opLat=23),
        OpDesc(opClass='FloatAdd', opLat=6),
        OpDesc(opClass='FloatCmp', opLat=5),
        OpDesc(opClass='FloatCvt', opLat=7),
        OpDesc(opClass='FloatDiv', opLat=23, pipelined=False),
        OpDesc(opClass='FloatSqrt', opLat=23, pipelined=False),
        OpDesc(opClass='FloatMult', opLat=6),
        OpDesc(opClass='FloatMultAcc', opLat=6),
        OpDesc(opClass='FloatMisc', opLat=5)
    ]
    count = 1


# Port 2 of TX2
class O3_ARM_TX2_Port2(FUDesc):
    opList = [OpDesc(opClass='IntAlu', opLat=1)]
    count = 1


# Port 3 of TX2
class O3_ARM_TX2_Port3(FUDesc):
    opList = [
        OpDesc(opClass='MemWrite', opLat=4),
        OpDesc(opClass='FloatMemWrite', opLat=4)
    ]
    count = 1


# Port 4 of TX2
class O3_ARM_TX2_Port4(FUDesc):
    opList = [
        OpDesc(opClass='MemRead', opLat=4),
        OpDesc(opClass='FloatMemRead', opLat=4)
    ]
    count = 1


# Port 5 of TX2
class O3_ARM_TX2_Port5(FUDesc):
    opList = [
        OpDesc(opClass='MemRead', opLat=4),
        OpDesc(opClass='FloatMemRead', opLat=4)
    ]
    count = 1


# Execute Units
class O3_ARM_TX2_FUP(FUPool):
    FUList = [
        O3_ARM_TX2_Port0(),
        O3_ARM_TX2_Port1(),
        O3_ARM_TX2_Port2(),
        O3_ARM_TX2_Port3(),
        O3_ARM_TX2_Port4(),
        O3_ARM_TX2_Port5()
    ]


# BTB Branch Predictor
class O3_ARM_TX2_BP(LocalBP):
    BTBEntries = 65536
    BTBTagSize = 16
    RASSize = 1
    instShiftAmt = 0
    localPredictorSize = 65536
    localCtrBits = 1


# Core
class O3_ARM_TX2_3(DerivO3CPU):
    fetchWidth = 8
    fetchBufferSize = 16
    fetchToDecodeDelay = 1
    decodeWidth = 4
    decodeToRenameDelay = 1
    renameWidth = 4
    renameToIEWDelay = 1
    dispatchWidth = 4
    issueWidth = 6
    wbWidth = 8
    fuPool = O3_ARM_TX2_FUP()
    commitWidth = 4
    squashWidth = 4
    backComSize = 5
    forwardComSize = 5

    # LQEntries = 16
    LQEntries = 64
    # SQEntries = 16
    SQEntries = 36
    LSQDepCheckShift = 0

    numPhysIntRegs = 154
    numPhysFloatRegs = 90
    numPhysVecRegs = 90
    # numPhysVecPredRegs = 48
    # numPhysCCRegs = 128
    numIQEntries = 60
    numROBEntries = 180

    branchPred = O3_ARM_TX2_BP()


# Base L1 cache
class O3_ARM_TX2_L1Cache(Cache):
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 4
    tgts_per_mshr = 8


# Instruction Cache
class O3_ARM_TX2_ICache(O3_ARM_TX2_L1Cache):
    assoc = 8
    size = '32kB'
    mshrs = 2
    is_read_only = True
    # Writeback clean lines as well
    writeback_clean = True


# Data Cache
class O3_ARM_TX2_DCache(O3_ARM_TX2_L1Cache):
    assoc = 8
    size = '32kB'
    mshrs = 6
    tgts_per_mshr = 8
    write_buffers = 16
    # Writeback clean lines as well
    writeback_clean = True