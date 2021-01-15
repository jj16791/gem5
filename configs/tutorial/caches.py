import m5
from m5.objects import Cache


# L1 cache class inheiting from BaseCache class in src/mem/cache/Cache.py defining most non-default attributes
class L1Cache(Cache):
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20


# I and D caches inheriting from above class
class L1ICache(L1Cache):
    size = '16kB'


class L1DCache(L1Cache):
    size = '64kB'


# L2 cache class inheiting from BaseCache class
class L2Cache(Cache):
    size = '256kB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12