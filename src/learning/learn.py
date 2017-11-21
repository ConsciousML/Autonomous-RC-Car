import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
from sklearn.externals import joblib

# home coded
import scoring

# classifiers
from sklearn.model_selection import GridSearchCV
'''
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import GradientBoostingClassifier
'''
from sklearn.ensemble import RandomForestClassifier

DATASET_NAME = "recurent_same_nb"
CLF_FOLDER = "./"
CLF_NAME = "forest_" + DATASET_NAME
DEBUG = False

#DATASET_NAME = "same_nb"
#DATASET_NAME = ""

dataset = np.load("dataset_" + DATASET_NAME + ".npy")
labels = np.load("labels_" + DATASET_NAME + ".npy")
print(dataset[1].sum)
print("***")
print("Result for classifier: %s" % CLF_NAME)
if DEBUG:
    print("Dataset loaded.")
X_train, X_test, y_train, y_test = train_test_split(dataset, labels, test_size=0.001, random_state=None)

print("Training samples: %d\tTesting samples: %d" % (len(X_train), len(X_test)))
# Different classifiers
'''
clf = svm.SVC(kernel='linear', C = 1.0)
clf = GaussianNB()
clf = OneVsRestClassifier(svm.SVC(kernel='linear', probability=True))
'''
clf = RandomForestClassifier(random_state=None, criterion='gini', n_estimators=48)


clf = clf.fit(X_train, y_train)
if DEBUG:
    print("Learning phase done.")

y_pred = clf.predict(X_test)
scoring.get_confusion_matrix(y_test, y_pred)

_ = joblib.dump(clf, CLF_FOLDER + CLF_NAME + "" +".joblib.pkl")

# Searching parameters
search_parameters = None
"""
search_parameters = {
        'criterion': ['gini', 'entropy'],
        'n_estimators': [45, 46, 47, 48, 49, 50, 52]
        }

if search_parameters is not None:
    clf = GridSearchCV(clf, search_parameters)

clf = clf.fit(X_train, y_train)
if DEBUG:
    print("Learning phase done.")

y_pred = clf.predict(X_test)

if search_parameters:
    print(clf.best_score_)
    print(clf.best_params_)
    print(clf.best_estimator_)
else:
    scoring.get_confusion_matrix(y_test, y_pred)
    _ = joblib.dump(clf, CLF_FOLDER + CLF_NAME + ".joblib.pkl")
"""
