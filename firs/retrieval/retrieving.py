import pyterrier as pt
import os
from ..utils import Logger
import time
import json
from multiprocessing import Pool

from .pipeline_factory import get_pipeline
from .pyterrier2trec import pyterrier2trec

from ..configuration import configuration


os.environ['JAVA_HOME'] = '/mnt/SOFTWARE/jdk-11.0.11'


def retrieve(coll_id, topics, runs_path, index_path, nThreads=1):

    logger = Logger().logger

    with open("retrieval/gop_properties.json", "r") as F:
        gp = json.load(F)


    configs = [f"{stop}_{stem}_{model}_{qe}"
               for qe in gp["rewritings"]
               for stop in gp["stopwords"]
               for stem in gp["stemmers"]
               for model in gp["models"]]

    logger.info(f"started retrieving the collection {coll_id}. found {len(configs)} configurations...")
    s = time.time()
    with Pool(processes=nThreads) as pool:
        futureRuns = [pool.apply_async(_parallel_retrieving, [topics, runs_path, index_path, config]) for config in configs]
        runs = [fr.get() for fr in futureRuns]


    logger.info(f"complete indexing done in {time.time()-s:.2f} seconds.")


def _parallel_retrieving(topics, runs_path, index_path, config):
    stime = time.time()
    if not pt.started():
        pt.init(boot_packages=["com.github.terrierteam:terrier-prf:-SNAPSHOT"], logging='ERROR')

    logger = Logger().logger

    logger.info(f"retrieving documents for {len(topics.index)} queries, with system {config}")

    stoplist, stemmer, _, _ = config.split("_")


    logger.info(config)
    index = pt.IndexFactory.of(f"{index_path}/{stoplist}_{stemmer}/data.properties")
    pipeline = get_pipeline(pt, index, config)

    run = pipeline(topics)

    run = pyterrier2trec(run, config)
    run = run[['qid', 'useless', 'docno', 'rank', 'score', 'name']]
    run.to_csv(f"{runs_path}/{config}.txt", index=False, header=False, sep="\t")



    logger.info(f"documents for configuration: {config} retrieved in {time.time() - stime:.2f}")



