import pandas as pd

class abstractMeasure:


    def __init__(self, cutoff):
        self.cutoff = cutoff


    def __matmul__(self, other):
        return self.__class__(other)


    def pandize(self, measures):
        return pd.DataFrame(measures, columns=['system', 'topic', self.__repr__()])

