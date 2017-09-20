import numpy as np
from sklearn.decomposition import PCA

dataset = np.load("dataset.npy")
pca = PCA()
pca.n_components=9296
pca_dataset = pca.fit_transform(dataset)
pca_dataset = pca.transform(dataset)
np.save("pca_dataset", pca_dataset)
