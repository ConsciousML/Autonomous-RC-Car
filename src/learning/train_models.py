from build_models import *
from processing.build_dataset import *

BATCH = 10
f_dataset = "dataset.npy"
f_labels = "labels.npy"
generator = gen_data(f_dataset, f_labels, BATCH)

model = RecurrentMobileNet()

for i in range(1):
    data, labels = next(generator)
    print(data.shape)
    print(labels.shape)

    model.fit(data, labels)

model.save("output/mobileNet.h5")

