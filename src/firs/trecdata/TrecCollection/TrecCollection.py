import pandas as pd


from ... import configuration
from ...utils import Logger


class TrecCollection:
    

    def __init__(self, **kwargs):
        self.configs = configuration().get_config()
        self.logger = Logger().logger

        # the name of the collection is one of the predefined; it can be imported directly
        if 'collectionName' in kwargs and f"collections.{kwargs['collectionName']}" in self.configs.sections():
            self._import_paths(kwargs['collectionName'])
            self.collection_name = kwargs['collectionName']
        

    def get_name(self):
        return self.collection_name

    def __str__(self):
        return f"collection: {self.collection_name}\n\t* topics: {len(self.qrel)}\n\t* runs: {len(self.runs)}"


    from .import_collection import import_collection, _import_collection, _import_runs, _import_qrels, _import_runs_list
    from .evaluate import evaluate
    from .parallel_evaluate import parallel_evaluate
    from .misc import remove_shorter_runs


    def _import_paths(self, collectionName):
        self.cpaths = dict(self.configs.items(f'collections.{collectionName}'))


    def import_measures(self):
        measures = pd.read_csv(self.cpaths['msrs_path'], index_col=False)
        measures = measures.drop("Unnamed: 0", axis=1)
        if self.collection_name == 'robust04qv':
            measures = measures[measures['replicate'] == "0-0"].reset_index()
            measures = measures.drop('index', axis=1).drop('replicate', axis=1)

        return measures
