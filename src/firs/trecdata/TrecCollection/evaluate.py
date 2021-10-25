import pandas as pd
import pytrec_eval

def evaluate(self, measure, savePath=None):
    '''
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

    if savePath is not None:
        measures.to_csv(self.cpaths['msrs_path'])
    '''



    return measure(self.qrel, self.runs)


def import_measures(self):
    measures = pd.read_csv(self.cpaths['msrs_path'], index_col=False)
    measures = measures.drop("Unnamed: 0", axis=1)
    if self.collection_name == 'robust04qv':
        measures = measures[measures['replicate'] == "0-0"].reset_index()
        measures = measures.drop('index', axis=1).drop('replicate', axis=1)

    return measures


