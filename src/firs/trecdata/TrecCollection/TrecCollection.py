import pandas as pd


from ... import configuration
from ...utils import Logger


class TrecCollection:
    

    def __init__(self, **kwargs):
        self.configs = configuration().get_config()
        self.logger = Logger().logger
        self.topics = None

        # the name of the collection is one of the predefined; it can be imported directly
        if 'collectionName' in kwargs and f"collections.{kwargs['collectionName']}" in self.configs.sections():
            self._import_paths(kwargs['collectionName'])
            self.collection_name = kwargs['collectionName']
        

    def get_name(self):
        return self.collection_name

    def get_paths(self):
        return self.cpaths

    def __str__(self):
        return f"collection: {self.collection_name}\n\t* topics: {len(self.qrel)}\n\t* runs: {len(self.runs)}"


    from .import_collection import import_collection, _import_collection, _import_runs, _import_qrels, _import_runs_list
    from .evaluate import evaluate, import_measures
    from .parallel_evaluate import parallel_evaluate
    from .misc import remove_shorter_runs
    from .get_topics import get_topics, _import_topics


    def _import_paths(self, collectionName):
        self.cpaths = dict(self.configs.items(f'collections.{collectionName}'))

