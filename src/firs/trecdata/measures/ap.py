from .abstractMeasure import abstractMeasure
import pandas as pd
import pytrec_eval


class _ap(abstractMeasure):

    def __init__(self, cutoff=1000):
        super().__init__(cutoff)

    def __str__(self):
        return f"ap at {self.cutoff}"

    def __repr__(self):
        return f"ap@{self.cutoff}"

    def __call__(self, qrels, runs):

        te = {tID: pytrec_eval.RelevanceEvaluator({tID: qrels[tID]}, {f'map'}) for tID in qrels}
        n = f'map'

        measures = []
        for rID in runs:
            for tID in te:
                if len(runs[rID][tID]) <= self.cutoff:
                    pointMeasure = te[tID].evaluate({tID: runs[rID][tID]})
                else:

                    filtered_run = dict(sorted(runs[rID][tID].items(), key=lambda x: x[1], reverse=True)[:self.cutoff])
                    pointMeasure = te[tID].evaluate({tID: filtered_run})
                pointMeasure = pointMeasure[tID][n]
                measures.append([rID, tID, pointMeasure])

        return self.pandize(measures)
