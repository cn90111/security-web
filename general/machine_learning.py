from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn import svm
import pandas as pd

class MachineLearning():
    SUPPORT_LIST = ['decision_trees', 'svm', 'random_forest']
    
    def __init__(self, method):
        self.method = method

    def fit(self, file_path):
        feature, label = self.getDataset(file_path)
        print(feature)
        print(label)
        
    def getDataset(self, file_path):
        dataframe = pd.read_csv(file_path)
        feature = dataframe.iloc[:, 0:-1]
        label = dataframe.iloc[:, -1]
        return feature, label