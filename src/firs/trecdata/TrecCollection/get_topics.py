from .topic_parsers import *

from ... import configuration


def get_topics(self):

    if self.topics is None:
        self._import_topics()

    return self.topics


def _import_topics(self):


    tpath = self.cpaths['tpcs_path']

    tpname = dict(self.configs.items(f'collections.{self.collection_name}'))['topic_parser']

    self.topics = eval(tpname)(tpath)