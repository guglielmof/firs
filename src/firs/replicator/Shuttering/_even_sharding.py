import numpy as np
import random

from .shuttering_utils import checkShardingValidity

def _even_sharding(nShards, rDocsByTopic, rDocsList, nrDocsList, emptyShards):
    allowed_empty = (emptyShards == 'E')

    nRelDocs = len(rDocsList)
    nNRelDocs = len(nrDocsList)
    nDocs = nRelDocs + nNRelDocs
    shardsList = np.arange(nShards)

    l = np.array([s for s in shardsList]*int(nDocs/len(shardsList))+[s for s in shardsList][:nDocs%len(shardsList)])
    lp = l
    rDocsByShard = {}
    found = False
    # TODO - a very bad sharding apporach: we should do a stratified sampling. This is very slow... but works
    while not found:


        lp = l[np.random.permutation(nDocs)]
        rShards = lp[:nRelDocs]
        rDocsByShard = {i: set([d for e, d in enumerate(rDocsList) if rShards[e] == i]) for i in shardsList}
        found = (allowed_empty or checkShardingValidity(rDocsByShard, rDocsByTopic))


    nrShards = lp[nRelDocs:]
    nrDocsByShard = {i: [d for e, d in enumerate(nrDocsList) if nrShards[e] == i] for i in shardsList}

    shards = {i: set(list(rDocsByShard[i]) + nrDocsByShard[i]) for i in shardsList}

    return shards
