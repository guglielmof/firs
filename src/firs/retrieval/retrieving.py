import pyterrier as pt
import os
from ..utils import Logger
import time
import json
from multiprocessing import Pool

from .pipeline_factory import get_pipeline
from .pyterrier2trec import pyterrier2trec

from ..configuration import configuration


def retrieve_collection(collection, nThreads=1):
    logger = Logger().logger


    topics = collection.get_topics()

    configs = configuration().get_config()
    os.environ['JAVA_HOME'] = dict(configs.items('paths'))['java_home']
    gopoptions = dict(configs.items('GoP'))

    logger = Logger().logger

    gop = [(stop, stem, model, qe)
                            for qe in gopoptions["queryexpansions"].split(",")
                        for stop in gopoptions["stoplists"].split(",")
                    for stem in gopoptions["stemmers"].split(",")
               for model in gopoptions["models"].split(",")]

    logger.info(f"started retrieving the collection {collection.get_name()}. found {len(gop)} configurations...")

    s = time.time()

    with Pool(processes=nThreads) as pool:
        futureRuns = [pool.apply_async(_parallel_retrieving, [topics, collection, g]) for g in gop]
        runs = [fr.get() for fr in futureRuns]


    logger.info(f"complete indexing done in {time.time() - s:.2f} seconds.")


def _parallel_retrieving(topics, collection, cnfg):
    runs_path = collection.get_paths()['runs_path']
    index_path = collection.get_paths()['indx_path']

    stime = time.time()
    if not pt.started():
        pt.init(boot_packages=["com.github.terrierteam:terrier-prf:-SNAPSHOT"], logging='ERROR')

    logger = Logger().logger

    text_cnfg = "_".join(list(cnfg))
    logger.info(f"retrieving documents for {len(topics.index)} queries, with system {text_cnfg}")

    stoplist, stemmer, model, qe = cnfg


    index = pt.IndexFactory.of(f"{index_path}/{stoplist}_{stemmer}/data.properties")


    pipeline = get_pipeline(pt, index, cnfg)

    run = pipeline(topics)

    run = pyterrier2trec(run, text_cnfg)
    run = run[['qid', 'useless', 'docno', 'rank', 'score', 'name']]
    run.to_csv(f"{runs_path}{text_cnfg}.txt", index=False, header=False, sep="\t")

    logger.info(f"documents for configuration: {text_cnfg} retrieved in {time.time() - stime:.2f}")
