import time
import os
from ...utils import chunk_based_on_number, Logger
import pandas as pd
from multiprocessing import Pool
import pytrec_eval


def parallel_evaluate(self, nThreads=1, measure="map"):


    self.logger.info("\t*importing the qrels...")
    stime = time.time()
    self._import_qrels()
    self.logger.info(f"\tdone in {time.time() - stime:.2f} seconds")

    run_paths = [self.cpaths['runs_path'] + p for p in os.listdir(self.cpaths['runs_path'])][:10]
    runs_chunks = chunk_based_on_number(run_paths, nThreads)

    with Pool(processes=nThreads) as pool:

        futureMeasures = [pool.apply_async(_evaluate_chunk, [measure, chunk, self.qrel]) for chunk in runs_chunks]

        measures = pd.concat([fm.get() for fm in futureMeasures])

    return measures


def _evaluate_chunk(measure, runs_paths, qrels):
    logger = Logger().logger

    topic_evaluators = {tID: pytrec_eval.RelevanceEvaluator({tID: qrels[tID]}, {measure}) for tID in qrels}

    measures = []


    for run_file in runs_paths:
        rname = ".".join(run_file.split("/")[-1].split(".")[:-1])
        with open(run_file, "r") as F:

            run = pytrec_eval.parse_run(F)

            for tID in topic_evaluators:
                pointMeasure = topic_evaluators[tID].evaluate({tID: run[tID]})
                pointMeasure = pointMeasure[tID]['map']
                measures.append([rname, tID, pointMeasure])


    measures = pd.DataFrame(measures, columns=['system', 'topic', 'measure'])

    return measures