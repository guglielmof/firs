import numpy as np
import os


def _get_documents_list(collection):
    docs = []

    for t in collection.topics:
        docs += list(collection.qrel[t].keys())
        for s in collection.systems:
            docs += list(collection.runs[s][t].keys())

    return list(set(docs))


def _relevant_documents(collection):
    relDocsByTopic = {}
    relDocs = set()

    for t in collection.qrel:
        rdt = [d for d, r in collection.qrel[t].items() if r > 0]
        relDocsByTopic[t] = set(rdt)
        relDocs = relDocs.union(relDocsByTopic[t])

    return list(relDocs), relDocsByTopic


def checkShardingValidity(relDocsByShard, relDocsByTopic):
    if not relDocsByShard:
        return False

    found = True
    for t, t2rdocs in relDocsByTopic.items():
        for s, s2rdocs in relDocsByShard.items():
            if len(s2rdocs.intersection(t2rdocs)) == 0:
                found = False
                break
        if not found:
            break
    return found


def is_shardable(nShards, relDocsByTopic):
    return np.all([len(rd) >= nShards for _, rd in relDocsByTopic.items()])


def _shards_available(shutteringId, sharding_path):
    """
    Determine whether the shard has been precomputed and is available in the system

    :return: True if the shard is precomputed, False else
    """
    return shutteringId in os.listdir(sharding_path)
