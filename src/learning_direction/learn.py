import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

dataset = np.load("dataset.npy")
labels = np.load("labels.npy")

X_train, X_test, y_train, y_test = train_test_split(dataset, labels, test_size=0.3, random_state=42)

clf = svm.SVC(kernel='linear', C = 1.0)
clf.fit(X_train, y_train)

#f = open("clf")
#s = pickle.dump(clf, f)
#f.close()

y_pred = clf.predict(X_test)
print accuracy_score(y_test, y_pred)
