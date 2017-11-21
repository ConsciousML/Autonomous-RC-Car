from build_models import *
from processing.build_dataset_angle import *

BATCH = 10
f_dataset = "a_dataset.npy"
f_labels = "a_labels.npy"
generator = gen_data(f_dataset, f_labels, BATCH)

model = RecurrentMobileNet()

for i in range(1):
    data, labels = next(generator)
    print(data.shape)
    print(labels.shape)

    model.fit(data, labels)

model.save("output/mobileNet2.h5")

