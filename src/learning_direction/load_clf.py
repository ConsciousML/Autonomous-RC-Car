from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
import numpy as np
# home coded
import scoring

CLF_FOLDER = "tmp/"
CLF_NAME = "gaussian"

clf = joblib.load(CLF_FOLDER + CLF_NAME + ".joblib.pkl")

dataset = np.load("dataset.npy")
labels = np.load("labels.npy")
X_train, X_test, y_train, y_test = train_test_split(dataset, labels, test_size=0.3, random_state=42)
y_pred = clf.predict(X_test)
scoring.show_confusion_matrix(y_test, y_pred)
