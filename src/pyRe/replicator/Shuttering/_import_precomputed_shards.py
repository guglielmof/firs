import os

def _import_precomputed_shards(shutteringId, sharding_path):
    sharding_dir = sharding_path + shutteringId
    shards = {}
    for shard in os.listdir(sharding_dir):
        with open(sharding_dir + "/" + shard, "r") as F:
            shards[shard.split(".")[0].split("_")[-1]] = set([did.strip() for did in F.readlines()])

    return shards
