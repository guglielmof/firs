from .abstractMeasure import abstractMeasure
import pandas as pd
import pytrec_eval

class _nDCG(abstractMeasure):

    def __init__(self, cutoff = 1000):
        super().__init__(cutoff)

    def __str__(self):
        return f"nDCG at {self.cutoff}"

    def __repr__(self):
        return f"nDCG@{self.cutoff}"

    def __call__(self, qrels, runs):

        te = {tID: pytrec_eval.RelevanceEvaluator({tID: qrels[tID]}, {f'ndcg_cut.{self.cutoff}'}) for tID in qrels}
        n = f'ndcg_cut_{self.cutoff}'

        measures = []
        for rID in runs:
            for tID in te:
                pointMeasure = te[tID].evaluate({tID: runs[rID][tID]})

                pointMeasure = pointMeasure[tID][n]
                measures.append([rID, tID, pointMeasure])

        return self.pandize(measures)