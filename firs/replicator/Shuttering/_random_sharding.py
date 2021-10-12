import numpy as np
import random

from .shuttering_utils import checkShardingValidity

def _random_sharding(nShards, rDocsByTopic, rDocsList, nrDocsList, emptyShards):
    allowed_empty = (emptyShards == 'E')

    nRelDocs = len(rDocsList)
    nNRelDocs = len(nrDocsList)
    shardsList = np.arange(nShards)
    for b in range(nShards):
        found = False
        while not found:
            rShards = random.choices(shardsList, k=nRelDocs)
            rDocsByShard = {i: set([d for e, d in enumerate(rDocsList) if rShards[e] == i]) for i in shardsList}
            found = allowed_empty or checkShardingValidity(rDocsByShard, rDocsByTopic)

        nrShards = random.choices(shardsList, k=nNRelDocs)
        nrDocsByShard = {i: [d for e, d in enumerate(nrDocsList) if nrShards[e] == i] for i in shardsList}

    shards = {i: set(list(rDocsByShard[i]) + nrDocsByShard[i]) for i in shardsList}

    return shards
