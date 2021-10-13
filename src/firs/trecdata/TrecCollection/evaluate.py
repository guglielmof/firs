import pandas as pd
import pytrec_eval

def evaluate(self, measure="map"):
    # very ugly way to make pytrec_eval works with our data collection
    topic_evaluators = {tID: pytrec_eval.RelevanceEvaluator({tID: self.qrel[tID]}, {measure}) for tID in self.qrel}

    # again, a very ugly solution to compute the measure and put it in a dataframe
    measures = []
    for rID in self.runs:
        for tID in topic_evaluators:
            pointMeasure = topic_evaluators[tID].evaluate({tID: self.runs[rID][tID]})
            pointMeasure = pointMeasure[tID][measure]
            measures.append([rID, tID, pointMeasure])

    measures = pd.DataFrame(measures, columns=['system', 'topic', 'measure'])
    return measures