import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
from sklearn.externals import joblib
# home coded
import scoring
# classifiers
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.multiclass import OneVsRestClassifier

CLF_FOLDER = "tmp/"
CLF_NAME = "onevsrest"
DEBUG = True

dataset = np.load("dataset.npy")
labels = np.load("labels.npy")
if DEBUG:
    print("Dataset loaded.")
X_train, X_test, y_train, y_test = train_test_split(dataset, labels, test_size=0.3, random_state=42)

# Different classifiers
'''
clf = svm.SVC(kernel='linear', C = 1.0)
clf = GaussianNB()
'''
clf = OneVsRestClassifier(svm.SVC(kernel='linear', probability=True))
if DEBUG:
    print("Learning phase done.")

clf = clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
scoring.show_confusion_matrix(y_test, y_pred)

_ = joblib.dump(clf, CLF_FOLDER + CLF_NAME + ".joblib.pkl")
