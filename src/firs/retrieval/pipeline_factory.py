from ..configuration import configuration
import importlib
import sys


def get_pipeline(pt, index, conf):
    stop, stem, model, qryexp = conf

    models_dict = dict(configuration().get_config().items(f'models'))
    qryexp_dict = dict(configuration().get_config().items(f'queryexpansions'))

    stopandstem, stopfile = get_stopandstem(stop, stem)
    if stopfile is not None:
        properties = {"termpipelines": stopandstem, "stopwords.filename": stopfile}
    else:
        properties = {"termpipelines": stopandstem}

    mdclass = models_dict[f'model.{model.lower()}.class']
    mdtype = models_dict[f'model.{model.lower()}.type']

    if mdtype == 'terrier':
        model = pt.BatchRetrieve(index, wmodel=mdclass, verbose=False, properties=properties)
        pipeline = model
    else:
        # TODO: implement the case when we have a python file
        pass

    if qryexp != 'none':
        qeclass = qryexp_dict[f'queryexpansions.{qryexp.lower()}.class']
        qetype = qryexp_dict[f'queryexpansions.{qryexp.lower()}.type']

        if qetype == 'terrier':
            rewriter = getattr(pt.rewrite, qeclass)(index, verbose=False, properties=properties)
            pipeline = model >> rewriter >> model
        else:
            # TODO: implement the case when we have a python file
            pass

    return pipeline


def get_stopandstem(stop, stem):
    stopfile = None
    if stop == "none":
        stopFinal = "NoOp"
    else:
        stopFinal = "Stopwords"
        if stop != "default":
            stop_dict = dict(configuration().get_config().items(f'stoplists'))
            stopfile = stop_dict['stop']

    if stem == "none":
        stemFinal = "NoOp"
    else:
        stemFinal = stem

    return f"{stopFinal},{stemFinal}", stopfile
