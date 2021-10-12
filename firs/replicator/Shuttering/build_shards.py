import os
from .shuttering_utils import _get_documents_list,_relevant_documents,is_shardable

def build_shards(self, **kwargs):
    # fetch the list of all documents
    docsList = _get_documents_list(self.collection)

    # get, for each topic, all of its relevant documents
    rDocsList, rDocsByTopic = _relevant_documents(self.collection)
    nrDocsList = list(set(docsList) - set(rDocsList))

    if self.emptyShards == 'NE':
        if not is_shardable(self.nShards, rDocsByTopic):
            raise Exception(f"Impossible to build {self.nShards} shards, all with relevant docs: "
                            f"one or more topics has less relevant documents than shards")

    if self.sampling == "RNDM":
        shards = self._random_sharding(self.nShards, rDocsByTopic, rDocsList, nrDocsList, self.emptyShards)
    elif self.sampling == "EVEN":
        raise NotImplementedError
    else:
        raise ValueError(f"{self.sampling} is not a valid sampling process")

    # if necessary save the shard
    if kwargs['sharding.save']:
        self.logger.info("saving the sharded collection")
        sharding_path = self.collection['cpaths']['shrd_path']

        os.mkdir(f"{sharding_path}{self.shutteringId}")
        # shard IDs: collection_nShards_rep
        for sId in shards:
            shrdID = f"{self.shutteringId}_{sId:03d}"

            with open(f"{sharding_path}{self.shutteringId}/{shrdID}.txt", "w") as F:
                F.write("\n".join(shards[sId]))

    return shards
