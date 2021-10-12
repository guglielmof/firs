import pyterrier as pt
import os
from ..utils import Logger
import time
import json
from multiprocessing import Pool
from ..configuration import configuration


os.environ['JAVA_HOME'] = configuration().get_configs()['PATHS']['JAVAHOME']

def index_collection(coll_id, coll_path, indx_path, nThreads=1):

    logger = Logger().logger

    with open(configuration().get_configs()['PATHS']['GOP_CONFIG'], "r") as F:
        gp = json.load(F)


    configs = [f"{stop}_{stem}"  for stop in gp["stopwords"] for stem in gp["stemmers"]]

    logger.info(f"started indexing the collection {coll_id}. found {len(configs)} configurations...")
    s = time.time()
    with Pool(processes=nThreads) as pool:
        futureRuns = [pool.apply_async(_parallel_indexing, [coll_id, coll_path, indx_path, config]) for config in configs]
        runs = [fr.get() for fr in futureRuns]


    logger.info(f"complete indexing done in {time.time()-s:.2f} seconds.")


def config_mapper(configuration):
    stop, stem = configuration.split("_")
    if stop=="none":
        if stem=="none":
            return "NoOp"
        else:
            return f"{stem}"
    else:
        if stem=="none":
            return f"{stop}"
        return f"{stop},{stem}"


def _parallel_indexing(coll_id, coll_path, indx_path, configuration):
    if not pt.started():
        pt.init()

    logger = Logger().logger

    files = pt.io.find_files(coll_path)

    logger.info(f"started indexing the collection {coll_id} with configuration {configuration}...")
    stime = time.time()
    if configuration not in os.listdir(indx_path):
        os.mkdir(f"{indx_path}/{configuration}")
    indexer = pt.TRECCollectionIndexer(f"{indx_path}/{configuration}", verbose=False)
    indexer.setProperty("termpipelines", config_mapper(configuration))
    indexref = indexer.index(files)
    logger.info(f"indexing {coll_id} with configuration {configuration} done in {time.time() - stime:.2f}s.")
    index = pt.IndexFactory.of(indexref)
    logger.info(index.getCollectionStatistics().toString())

