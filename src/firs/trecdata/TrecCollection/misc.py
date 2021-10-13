import numpy as np


def remove_shorter_runs(self):
    """
    this method allows to remove runs that have ranked lists (for even one topic) shorter than the maximum length
    allowed
    """
    mlen = max([len(trun) for _, run in self.runs.items() for _, trun in run.items()])
    self.runs = {rId: run for rId, run in self.runs.items() if
                 np.all([len(trun) == mlen for _, trun in run.items()])}
    self.systems = list(self.runs.keys())

    return self
