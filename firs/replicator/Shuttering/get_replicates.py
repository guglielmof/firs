import time
from .shuttering_utils import _shards_available
from ._import_precomputed_shards import _import_precomputed_shards


def get_replicates(self, *args, **kwargs):
    self.logger.info(f"Getting the shuttering with id: {self.shutteringId}")
    # check if the data is already available
    sharding_path = self.collection.cpaths['shrd_path']

    if not _shards_available(self.shutteringId, sharding_path):

        # if not, check if the user desires to build the shards
        if 'sharding.pipeline' in kwargs and kwargs['sharding.pipeline']:
            self.logger.info("\tshuttering not found. computing it.")
            shards = self.build_shards(self.collection, **kwargs)

        else:
            raise Exception(
                f"data for sharding {self.shutteringId} is not available "
                f"and sharding.pipeline is not set to 'true' in the property file")

    else:
        shards = _import_precomputed_shards(self.shutteringId, sharding_path)

    self.logger.info("splitting the collection according to required sharding")
    stime = time.time()

    self.replicated_runs = {rID:
                                {tID:
                                     {sID:
                                          {dID: self.collection.runs[rID][tID][dID]
                                           for dID in self.collection.runs[rID][tID] if dID in shards[sID]}
                                      for sID in shards}
                                 for tID in self.collection.runs[rID]}
                            for rID in self.collection.runs}

    self.replicated_qrel = {tID:
                                {sID:
                                     {dID: self.collection.qrel[tID][dID]
                                      for dID in self.collection.qrel[tID] if dID in shards[sID]}
                                 for sID in shards}
                            for tID in self.collection.qrel}

    self.logger.info(f"collection splitted in {time.time() - stime:.2f}s")
