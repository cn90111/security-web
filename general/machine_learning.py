from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.metrics import mean_squared_error
import pandas as pd

class MachineLearning():
    SUPPORT_LIST = ['decision_trees', 'svm', 'random_forest']
    train_percent = 80
    train_feature = None
    test_feature = None
    train_label = None
    test_label = None
    
    def __init__(self, method, file_path):
        if method == 'decision_trees':
            self.method_object = tree.DecisionTreeClassifier()
        elif method == 'svm':
            self.method_object = svm.SVC()
        elif method == 'random_forest':
            self.method_object = RandomForestClassifier(max_depth=20, random_state=0)
        else:
            raise AttributeError("無此method：" + method)
        self.preprocessing(file_path)

    def preprocessing(self, file_path):
        feature, label = self.getDataset(file_path)
        self.train_feature, self.test_feature = \
            self.percentage_split(feature, self.train_percent)
        self.train_label, self.test_label = \
            self.percentage_split(label, self.train_percent)
            
    def fit(self):
        self.method_object.fit(self.train_feature, self.train_label)
        
    def predict(self, feature):
        return self.method_object.predict(feature)
        
    def score(self):
        accuracy = self.method_object.score(self.test_feature, self.test_label)
        return accuracy
        
    def get_mse(self):
        predict_label = self.method_object.predict(self.test_feature)
        return mean_squared_error(self.test_label, predict_label)
    
    def getDataset(self, file_path):
        dataframe = pd.read_csv(file_path)
        feature = dataframe.iloc[:, 0:-1]
        feature = pd.get_dummies(feature).values.tolist()
        label = dataframe.iloc[:, -1]
        if type(label) is str or type(label) is chr:
            label = pd.get_dummies(label).values.tolist()
        else:
            label = label.values.tolist()
        return feature, label
        
    def percentage_split(self, data, percent):
        split_point = len(data)*percent//100
        return data[0:split_point], data[split_point:]
        