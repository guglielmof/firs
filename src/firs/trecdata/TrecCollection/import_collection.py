import time
from multiprocessing import Pool
import os
import pytrec_eval

from ...utils import chunk_based_on_number




def import_collection(self, **kwargs):
    self._import_collection(**kwargs)
    return self


def _import_collection(self, **kwargs):
    self.logger.info("started importing the collection...")

    self.logger.info("\t*importing the qrels...")
    stime = time.time()
    self._import_qrels()
    self.logger.info(f"\tdone in {time.time() - stime:.2f} seconds")

    self.logger.info("\t*importing the runs...")
    stime = time.time()
    if 'nThreads' in kwargs and type(kwargs['nThreads']) is int and kwargs['nThreads'] > 1:
        nthreads = kwargs['nThreads']
    else:
        nthreads = 1
    self._import_runs(nthreads)
    self.logger.info(f"\tdone in {time.time() - stime:.2f} seconds")
    self.logger.info(f"Imported {len(self.qrel)} topics and {len(self.runs)} runs")


def _import_runs(self, nThreads):
    run_paths = [self.cpaths['runs_path'] + p for p in os.listdir(self.cpaths['runs_path'])]
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
