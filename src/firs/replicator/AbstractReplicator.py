from ..utils import Logger

'''
An replicator is a structure which contains replicates of the experiments.
An experiment is a pair <system, topic>. Replicates might be, for example, reformulations or shards.

Notice that replicators contains only replicates of the experiments, not replicated measures. For example,
replicators should not be used to store data from RWBM or APsplitting (since they are replicates of the measure for
a ``simulated'' experiment, and not a real experiment replication).
'''


class AbstractReplicator:

    def __init__(self, collection, *args, **kwargs):
        self.logger = Logger().logger
        self.collection = collection
        self.experiment = self.get_replicates(*args, **kwargs)


    def get_replicates(self, *args, **kwargs):
        raise NotImplementedError