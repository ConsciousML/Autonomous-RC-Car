# Autonomous Remote Controlled Car
![title](data/images/smartcar.jpg)

## Objective
The goal of this project was to build an autonomous remote controlled car using deep learning.
The car is embedded with a Raspberry Pi and a Convolutional Neural Network (CNN) to predict in real-time the speed and the steering angle. We used an ultrasonic sensor to stop the car when encountering obstacles and another CNN for detecting stop signs.

## Championships
We participated to two competition. We got 3rd at [Iron Car Summer 2018](http://www.mylanderpages.com/ironcar2018/ironcar2018) and 
1st at [RobotCars Winter 2018](https://www.meetup.com/DIY-Robocars-France/). Check out our best performance [here](https://github.com/ConsciousML/Autonomous-RC-Car/raw/master/data/demo/v2.0/competition_03.mp4).

## Version 1.0: SunFounder
We used the [SunFounder PiCar-S Kit V2.0 for Raspberry Pi with Raspberry Pi 4B and TF card](https://www.sunfounder.com/picars-kit-with-raspberrypi.html) for the hardware. It costs around 180$ and can be built in an hour or two.
The final presentation of this project can be found as a [pdf](https://github.com/ConsciousML/Autonomous-RC-Car/blob/master/data/slides/SmartCar.pdf) or a [powerpoint](https://github.com/ConsciousML/Autonomous-RC-Car/blob/master/data/slides/SmartCar.pptx) file.
You can find some videos of the car's performance [here](https://github.com/ConsciousML/Autonomous-RC-Car/raw/master/data/demo/v1.0/driving.mp4).

## Version 2.0: DonkeyCar 
For the second version of this project we used the [DonkeyCar kit](https://www.donkeycar.com/) to build a faster and steadier car model. We generated some data using PIL by drawing lane lines on floor pictures. You can find the code of the data generator in `smartcar\simulator`. The version 2.0 is much better than the first version as you can see in this [video](https://github.com/ConsciousML/Autonomous-RC-Car/raw/master/data/demo/v2.0/driving_01.mp4).

## Installation
Run the following line to create the appropriate conda environment:
```bash
conda env create -f environment.yml
```

## Caution
This repository aims at giving a sample project for building a self driving rc car.
The logic for the client-server is only working with the hardware used for this experiment.
We highly advise you to understand the `smartcar\learn` module for knowing how to train the model
and the `smartcar\server\auto_drive.py` file for the autonomous driving logic.

## Generate your own data
You can use our script to generate your own data. Get many pictures of the floor, put them in a directory and run the following command:
```bash 
python scripts/generate.py -i image_dir -n 10 -p output_dir
```
where `-i` option is for specifying the input data, `-p` the output directory and `-n` the number of images to generate.

## Train your own model
If you have your own data i.e (image, steering_angle, speed), we created a script that allows you to train you own model.
In a given directory, the images should a the form `unique_id.jpg` and the label as the json file `unique_id.jpg`.
The json file should have the following format:
```json
{
  "angle" : 0.0,
  "velocity": 0.0
}
```

Then cd at the root of the project and run the training script:
```bash
python scripts/train_pilot.py --help
```
You will get the following output:
```bash
  -h, --help            show this help message and exit
  --data_dir [DATA_DIR]
                        The directory containing the training data.
  --out_dir [OUT_DIR]   The output directory to store best model and training
                        curves.
  --lr [LR]             The learning rate.
  --batch_size [BATCH_SIZE]
                        The batch size.
  --epochs [EPOCHS]     The number of epochs.
```
Fill these arguments according to your configuration, here is an examples:
```bash
python scripts/train_pilot.py --data_dir=data/tracks --out_dir=tmp --lr=1e-4 --batch_size=128 --epochs=20
```
