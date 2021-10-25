import pyterrier as pt
import os
from ..utils import Logger
import time
import json
from multiprocessing import Pool
from ..configuration import configuration


def index_collection(collection, nThreads=1):
    configs = configuration().get_config()
    os.environ['JAVA_HOME'] = dict(configs.items('paths'))['java_home']
    gop = dict(configs.items('GoP'))

    logger = Logger().logger


    stoplists = gop['stoplists'].split(",")
    stemmers = gop['stemmers'].split(",")

    idx_conf = [(stop, stem) for stop in stoplists for stem in stemmers]

    logger.info(f"started indexing the collection {collection.get_name()}. found {len(idx_conf)} configurations...")
    s = time.time()

    print(idx_conf)

    '''
    with Pool(processes=nThreads) as pool:
        futureIndexes = [pool.apply_async(_parallel_indexing, [collection, config]) for ic in idx_conf]
        _ = [fi.get() for fi in futureIndexes]
    '''

    logger.info(f"complete indexing done in {time.time()-s:.2f} seconds.")


def config_mapper(configuration):
    configs = configuration().get_config()

    stemmer_classes = dict(configs.items('stemmers'))
    stoplist_classes = dict(configs.items('stoplists'))

    stop, stem = configuration


    if stop=="none":
        if stem=="none":
            return None,"NoOp,NoOp"
        else:
            return f"NoOp,{stem}"
    else:
        if stem=="none":
            return f"{stop}"

        return f"{stop},{stem}"


def _parallel_indexing(collection, configuration):
    if not pt.started():
        pt.init()

    logger = Logger().logger


    coll_id = collection.get_name()
    cpaths = collection.get_paths()
    coll_path = cpaths['coll_path']
    indx_path = cpaths['indx_path']

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

