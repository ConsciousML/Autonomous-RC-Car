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

CLF_FOLDER = "tmp/"
CLF_NAME = "gaussian"

dataset = np.load("dataset.npy")
labels = np.load("labels.npy")

X_train, X_test, y_train, y_test = train_test_split(dataset, labels, test_size=0.3, random_state=42)

#clf = svm.SVC(kernel='linear', C = 1.0)
clf = GaussianNB()

clf = clf.fit(X_train, y_train)

#f = open("clf")
#s = pickle.dump(clf, f)
#f.close()

y_pred = clf.predict(X_test)
scoring.show_confusion_matrix(y_test, y_pred)

_ = joblib.dump(clf, CLF_FOLDER + CLF_NAME + ".joblib.pkl")
