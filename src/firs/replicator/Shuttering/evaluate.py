import pandas as pd
import pytrec_eval

def evaluate(self, measure):

    topicsIDs = list(self.replicated_qrel.keys())
    shardsIDs = list(self.replicated_qrel[topicsIDs[0]].keys())
    runsIDs   = list(self.replicated_runs.keys())

    newQrels = {sID: {tID: self.replicated_qrel[tID][sID] for tID in topicsIDs} for sID in shardsIDs}
    newRuns  = {sID: {rID: {tID:  self.replicated_runs[rID][tID][sID] for tID in topicsIDs} for rID in runsIDs} for sID in shardsIDs}


    # again, a very ugly solution to compute the measure
    measures = []

    for sID in shardsIDs:
        measures.append(measure(newQrels[sID], newRuns[sID]))
        measures[-1]['replicate'] = pd.Series([sID]*len(measures[-1].index), index=measures[-1].index)

    measures = pd.concat(measures)

    return measures