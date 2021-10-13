from .AbstractReplicator import AbstractReplicator
import pandas as pd

class Reformulations(AbstractReplicator):

    def __init__(self, collection, *args, **kwargs):
        super().__init__(collection, *args, **kwargs)

    def get_replicates(self, *args, **kwargs):
        return None

    def evaluate(self, measure="map"):
        measures = None
        if self.collection.collection_name == "robust04qv":
            measures = pd.read_csv(self.collection.cpaths['msrs_path']).drop("Unnamed: 0", axis=1)
            measures = measures[measures['replicate'] != "0-0"]
            
        return measures