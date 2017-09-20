import numpy as np

labels = np.load("labels.npy")
dataset = np.load("dataset.npy")
u, c = np.unique(labels, return_counts=True)
p = zip(u, c)
print p

maxe = 283

r = np.ones((3, 283), dtype=np.int)

for k, v in p:
    index = np.where(labels == k)[0]
    if v > 283:
        index = np.random.choice(index, 283, False)
    print index
    r[int(k)] = index

r = r.reshape(r.size)
print r
print r.shape
print dataset.shape
dataset = dataset[r,:]
labels = labels[r]
np.save("dataset_same_nb", dataset)
np.save("labels_same_nb", dataset)
