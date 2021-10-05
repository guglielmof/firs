import json
import pytrec_eval
from ..utils import chunk_based_on_number, Logger
from multiprocessing import Pool
import os
import time
import pandas as pd

import numpy as np

from .. import configuration


class TrecCollection:
    config_file_path = os.path.dirname(os.path.abspath(__file__)) + "/../configs/collections.json"
    base_path = configuration().get_configs()['PATHS']['WDIR']

    def __init__(self, **kwargs):
        self.logger = Logger().logger

        # the name of the collection is one of the predefined; it can be imported directly
        if 'collectionName' in kwargs:
            self._import_paths(kwargs['collectionName'])
            self.collection_name = kwargs['collectionName']
        # paths to qrel file and runs directory have been directly passed
        else:
            self.collection_name = ".".join(kwargs['qrel_path'].split("/")[-1].split(".")[:-1])
            self.cpaths = {k: self.base_path+v for k, v in kwargs.items() if k[-5:] == "_path"}



    def get_name(self):
        return self.collection_name

    def import_collection(self, **kwargs):

        self._import_collection(**kwargs)
        return self

    def __str__(self):
        return f"collection: {self.collection_name}\n\t* topics: {len(self.qrel)}\n\t* runs: {len(self.runs)}"

    def remove_shorter_runs(self):
        """
        this method allows to remove runs that have ranked lists (for even one topic) shorter than the maximum length
        allowed
        """
        mlen = max([len(trun) for _, run in self.runs.items() for _, trun in run.items()])
        self.runs = {rId: run for rId, run in self.runs.items() if
                     np.all([len(trun) == mlen for _, trun in run.items()])}
        self.systems = list(self.runs.keys())

        return self

    def _import_collection(self, **kwargs):
        self.logger.info("started importing the collection...")
        self.logger.info("\t*importing the qrels...")
        stime = time.time()
        self._import_qrels()
        self.logger.info(f"\tdone in {time.time() - stime:.2f} seconds")

        self.logger.info("\t*importing the runs...")
        stime = time.time()
        if 'threads' in kwargs and type(kwargs['threads']) is int and kwargs['threads'] > 1:
            self._import_runs(kwargs['threads'])
        else:
            self._import_runs(1)
        self.logger.info(f"\tdone in {time.time() - stime:.2f} seconds")
        self.logger.info(f"Imported {len(self.qrel)} topics and {len(self.runs)} runs")

    def _import_runs(self, nThreads):

        run_paths = [self.cpaths['runs_path'] + p for p in os.listdir(self.cpaths['runs_path'])][:10]
        runs_chunks = chunk_based_on_number(run_paths, nThreads)
        with Pool(processes=nThreads) as pool:
            futureRuns = [pool.apply_async(_import_runs_list, [chunk]) for chunk in runs_chunks]

            runs = [fr.get() for fr in futureRuns]
        self.runs = {rId: run for rl in runs for rId, run in rl.items()}
        self.systems = list(self.runs.keys())

    def _import_qrels(self):
        with open(self.cpaths['qrel_path'], "r") as F:
            self.qrel = pytrec_eval.parse_qrel(F)
        self.topics = list(self.qrel.keys())

    def _import_paths(self, collectionName):

        # load the internal json file containing the position of the principal collections
        cpaths = json.load(open(self.config_file_path, "r"))

        if collectionName not in cpaths:
            raise ValueError(
                f"collection {collectionName} not available in configuration file \"{self.config_file_path}\".")

        self.cpaths = {k: self.base_path+v for k, v in cpaths[collectionName].items()}

    def evaluate(self, measure="map", precomputedPath=None):

        if precomputedPath is not None:
            pd.read_csv(precomputedPath)
            return measure

        # very ugly way to make pytrec_eval works with our data collection
        topic_evaluators = {tID: pytrec_eval.RelevanceEvaluator({tID: self.qrel[tID]}, {measure}) for tID in self.qrel}

        # again, a very ugly solution to compute the measure and put it in a dataframe
        measures = []
        for rID in self.runs:
            for tID in topic_evaluators:
                pointMeasure = topic_evaluators[tID].evaluate({tID: self.runs[rID][tID]})
                pointMeasure = pointMeasure[tID][measure]
                measures.append([rID, tID, pointMeasure])

        measures = pd.DataFrame(measures, columns=['system', 'topic', 'measure'])
        return measures

    def import_measures(self):
        measures = pd.read_csv(self.cpaths['msrs_path'], index_col=False)
        measures = measures.drop("Unnamed: 0", axis=1)
        if self.collection_name == 'robust04qv':
            measures = measures[measures['replicate'] == "0-0"].reset_index()
            measures = measures.drop('index', axis=1).drop('replicate', axis=1)

        return measures


def _import_runs_list(paths_list):
    runs = {}
    for run_filename in paths_list:
        with open(run_filename, "r") as F:
            try:
                rname = ".".join(run_filename.split("/")[-1].split(".")[:-1])
                runs[rname] = pytrec_eval.parse_run(F)
            except Exception as e:
                print(e)
                print(run_filename)

    return runs
