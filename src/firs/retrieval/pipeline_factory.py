from ..configuration import configuration
import importlib
import sys


def get_pipeline(pt, index, conf):
    stop, stem, model, qryexp = conf

    models_dict = dict(configuration().get_config().items(f'models'))
    qryexp_dict = dict(configuration().get_config().items(f'queryexpansions'))

    stopandstem = get_stopandstem(stop, stem)

    mdclass = models_dict[f'model.{model}.class']
    mdtype = models_dict[f'model.{model}.type']

    if mdtype == 'terrier':
        pipeline = pt.BatchRetrieve(index, wmodel=mdclass, verbose=False, properties={"termpipelines": stopandstem})
    else:
        pass

    if qryexp != 'none':
        qeclass = qryexp_dict[f'queryexpansions.{qryexp}.class']
        qetype = qryexp_dict[f'queryexpansions.{qryexp}.type']

        if qetype == 'terrier':
            rewriter = getattr(pt.rewrite, qeclass)(index, verbose=False, properties={"termpipelines": stopandstem})
            pipeline = pipeline >> rewriter >> pipeline
        else:
            pass

    return pipeline


def get_stopandstem(stop, stem):
    if stop == "none":
        stopFinal = "NoOp"
    else:
        stopFinal = stop

    if stem == "none":
        stemFinal = "NoOp"
    else:
        stemFinal = stem

    return f"{stopFinal},{stemFinal}"
