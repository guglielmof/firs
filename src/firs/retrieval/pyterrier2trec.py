def pyterrier2trec(run, name):
    run['useless'] = ['Q0'] * len(run.index)
    run['name'] = [name] * len(run.index)

    return run