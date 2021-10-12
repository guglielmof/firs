import os
from .shuttering_utils import _get_documents_list,_relevant_documents,is_shardable
from ._random_sharding import _random_sharding

def build_shards(self, save=False):
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
        shards = _random_sharding(self.nShards, rDocsByTopic, rDocsList, nrDocsList, self.emptyShards)
    elif self.sampling == "EVEN":
        raise NotImplementedError
    else:
        raise ValueError(f"{self.sampling} is not a valid sampling process")


    sharding_path = f"{self.collection.cpaths['shrd_path']}{self.shutteringId}"

    if save:

        if not os.path.exists(sharding_path):
            os.mkdir(sharding_path)

        if save=='force':
            for f in os.listdir(sharding_path):
                os.remove(f"{sharding_path}/{f}")


        if len(os.listdir(sharding_path))==0:
            self.logger.info("saving the sharded collection")

            # shard IDs: collection_nShards_rep
            for sId in shards:
                shrdID = f"{self.shutteringId}_{sId:03d}"

                with open(f"{sharding_path}/{shrdID}.txt", "w") as F:
                    F.write("\n".join(shards[sId]))

    return shards
