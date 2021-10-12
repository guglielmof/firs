import pandas as pd
import pytrec_eval

def evaluate(self, measure="map"):
    # very ugly way to make pytrec_eval works with our data collection
    topic_evaluators = {tID: {sID: pytrec_eval.RelevanceEvaluator({tID: self.replicated_qrel[tID][sID]}, {measure})
                              for sID in self.replicated_qrel[tID]} for tID in self.replicated_qrel}

    # again, a very ugly solution to compute the measure
    measures = []
    for rID in self.replicated_runs:
        for tID in topic_evaluators:
            for sID in self.replicated_runs[rID][tID]:
                pointMeasure = topic_evaluators[tID][sID].evaluate({tID: self.replicated_runs[rID][tID][sID]})
                pointMeasure = pointMeasure[tID][measure]
                measures.append([rID, tID, sID, pointMeasure])

    measures = pd.DataFrame(measures, columns=['system', 'topic', 'replicate', 'measure'])
    return measures