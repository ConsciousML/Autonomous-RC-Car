import numpy as np

labels = np.load("labels.npy")
dataset = np.load("dataset.npy")
u, c = np.unique(labels, return_counts=True)
p = zip(u, c)
print p


def min(a, b) : return a if a < b else b

maxe = -1
for k, v in p:
    if maxe == -1:
        maxe = v
    maxe = min(maxe, v)

r = np.ones((3, maxe), dtype=np.int)

for k, v in p:
    index = np.where(labels == k)[0]
    if v > maxe:
        index = np.random.choice(index, maxe, False)
    print index
    r[int(k)] = index

r = r.reshape(r.size)
dataset = dataset[r,:]
labels = labels[r]
np.save("dataset_same_nb", dataset)
np.save("labels_same_nb", labels)
