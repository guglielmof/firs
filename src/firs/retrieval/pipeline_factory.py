


def _module_factory(pt, index, module, stopandstem):
    if module in ["BM25", "QLM", "DFR", "PL2", "InL2", "DLH", "DPH", "DFRee", "DFI0", "DirichletLM", "DFIC", "DFIZ",
                  "InB2", "InL2"]:
                  
        return pt.BatchRetrieve(index, wmodel=module, verbose=False, properties={"termpipelines" : stopandstem})

    elif module == "HiemstraLM":
        return pt.BatchRetrieve(index, wmodel="Hiemstra_LM", verbose=False, properties={"termpipelines" : stopandstem})

    elif module == "InexpB2":
        return pt.BatchRetrieve(index, wmodel="In_expB2", verbose=False, properties={"termpipelines" : stopandstem})

    elif module == "InexpC2":
        return pt.BatchRetrieve(index, wmodel="In_expC2", verbose=False, properties={"termpipelines" : stopandstem})
    elif module == "JsKLs":
        return pt.BatchRetrieve(index, wmodel="Js_KLs", verbose=False, properties={"termpipelines" : stopandstem})

    elif module == "TFIDF":
        return pt.BatchRetrieve(index, wmodel="TF_IDF", verbose=False, properties={"termpipelines" : stopandstem})

    elif module in ["Bo1QueryExpansion", "RM3", "AxiomaticQE", "KLQueryExpansion"]:
        return getattr(pt.rewrite, module)(index, verbose=False, properties={"termpipelines" : stopandstem})


def get_pipeline(pt, index, config):
    components = config.split("_")
    stopandstem = config_mapper("_".join(components[:2]))
    retriever = _module_factory(pt, index, components[2], stopandstem)

    if components[3] == 'none':

        return retriever

    else:

        return retriever >> _module_factory(pt, index, components[3], stopandstem) >> retriever



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