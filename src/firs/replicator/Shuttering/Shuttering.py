'''
A Shuttering object represents a division into shards of a collection. If a shuttering is already available in the
system, the shuttering will be directly loaded. Else, the collection will be imported and shuttered.

A shuttering is represented by the following elements:
 - the collection on which it is based
 - the number of shards considered (integer)
 - the sampling used to build the shards (RNDM - EVEN)
 - whether shards without relevant documents are allowed (NE - E)

i.e. the shuttering robust04_5_RND_NE indicates the shuttering built for the robust 04 collection, on 5 shards
which does not allow some shards to not have relevant documents for any topic.

A single shard, has additionally the shard identifier.
Each shard is identified by robust04_5_RND_NE_001


The shuttering includes both the qrels and runs
'''
from ..AbstractReplicator import AbstractReplicator


class Shuttering(AbstractReplicator):

    def __init__(self, collection, *args, **kwargs):

        self._check_inputs(**kwargs)
        self.collection_name = collection.get_name()
        self.shutteringId = self._get_shuttering_id()
        super().__init__(collection, *args, **kwargs)


    def __str__(self):
        return f"sharding with identifier: {self.shutteringId}"


    from .get_replicates import get_replicates
    from .evaluate import evaluate
    from .build_shards import build_shards
    from ._get_shuttering_id import _get_shuttering_id
    from ._check_inputs import _check_inputs