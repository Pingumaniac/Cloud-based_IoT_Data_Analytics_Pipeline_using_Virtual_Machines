# Manual Deployment of a Cloud-based IoT Data Analytics Pipeline using Virtual Machines

CS 5287 Programming Assignment 1

## Goals

The goal of this assignment is to deploy a data analytics pipeline in the cloud using a cluster of distributed virtual machines. The scenario we are emulating is an IoT application where some surveillance cameras periodically send data via Kafka publish/subscribe brokers to a cloud-based analytics engine that attempts to infer the incoming image and then stores the input and output to a database so that eventually additional analytics can be conducted on the stored data. Since the Kafka brokers represent a publish/subscribe system, our emulated IoT sources serve as the producers of information. Our system will support two types of consumers. One type of consumer in our system pulls the data from the Kafka broker and stores it in a database. The other kind of consumer pulls the same sample from the Broker and sends it to a machine learning (ML) trained model that provides inference decisions. The inference decision is then added to the entry that was inserted previously in the database. In a later assignment, we will run Map Reduce on such stored data.

<img width="427" alt="image" src="https://github.com/user-attachments/assets/99647e47-b5b6-44f1-923f-e6ca48292f2e">

## Overview
To reproduce our project, follow installation steps below. Then, on VMs 1 and 3, start Zookeeper and the Kafka server. Start and log into the database on VM4 with
```
sudo systemctl start mongod
mongosh --authenticationDatabase admin -u adminuser -p
```
Once mongodb is up and running, run the following:
```
use image_database
db.createCollection("image_data")
```

You can later check results of our model by running 
```
db.image_data.aggregate([ { $group: { _id: null, total: { $sum: 1 }, correct: { $sum: { $cond: [{ $eq: ["$InferredValue", "$GroundTruth"] }, 1, 0] } } } }, { $project: { _id: 0, total: 1, correct: 1, accuracy: { $divide: ["$correct", "$total"] } } }] )
```
On VM2, run
```
wget https://github.com/chenyaofo/pytorch-cifar-models/releases/download/resnet/cifar10_resnet20-4118986f.pt -O cifar10_resnet20.pt
```
to download the weights from the Resnet-20 model for CIFAR10.

Next, start the consumers with 
```
python3 inference_consumer.py # on VM2
python3 db_consumer.py # on VM3
```
and the producer on VM1 with
```
python3 producer.py
```

### Components
#### VM1: Kafka Broker and Image Producer

* Runs Apache Kafka and Zookeeper
* Produces CIFAR-10 images to the "image_data" Kafka topic
* Adds noise to images to simulate real-world conditions

producer.py: Generates and sends image data

#### VM2: Inference Consumer

* Consumes image data from VM1
* Performs image classification using the pretrained CIFAR20
* Produces inference results to VM3

inference_consumer.py: Processes images and generates predictions

cifar100_resnet18.pth: Pre-trained model weights

#### VM3: Database Consumer and Kafka Broker

* Runs a second Kafka broker
* Consumes image data from VM1 and inference results from VM2
* Stores all data in MongoDB on VM4

db_consumer.py: Receives data and manages database operations

#### VM4: MongoDB Server

* Runs MongoDB database
* Stores all image data and inference results

### Communication

VM1 to VM2: Kafka topic "image_data" (bootstrap server: VM1:9092)

VM2 to VM3: Kafka topic "inference_results" (bootstrap server: VM3:9092)

VM1 to VM3: Kafka topic "image_data" (bootstrap server: VM1:9092)

VM3 to VM4: MongoDB connection

## Technologies Used
1. Python 3
2. Apache Kafka
3. MongoDB
4. Chameleon Cloud with Ubuntu Linux version 22.04 image (CC-Ubuntu22.04 on Chameleon)
5. CIFAR-10 image data set used by the IoT source.

## Instructions for setting up the technologies used

1. Install the following Python packages through your chosen CLI.

```
pip3 install kafka-python
pip3 install torch torchvision
pip3 install pymongo
```

2. Install Docker Image for Apache Kafka.

```
docker pull apache/kafka
```

3. Download Apache Kafka on your chosen directory using wget or curl -0 command.

```
wget https://downloads.apache.org/kafka/3.8.0/kafka_2.13-3.8.0.tgz
```

```
curl -O https://downloads.apache.org/kafka/3.8.0/kafka_2.13-3.8.0.tgz
```

Then, unzip the file, and move to the kafka directory.

```
tar -xzf kafka_2.13-3.8.0.tgz
cd kafka_2.13-3.8.0
```

## Effort Required

Setting up this distributed system required significant effort, as well as the following:

Infrastructure: Provisioning and configuring four separate VMs as well as ensuring network connectivity between them.

Distributed Systems: Installing and configuring Kafka and Zookeeper on multiple machines and ensuring proper communication.

Database Management: Setting up and securing a MongoDB instance.

Machine Learning: Preparing a pre-trained model for inference, potentially including model training or fine-tuning, albeit with the help of LLMs.

System Integration: Ensuring all components work together seamlessly, including proper data serialization and deserialization.

Monitoring and Maintenance: Setting up logging, monitoring, and maintenance procedures for the entire system.

## How work was split

* Robert Sheng primarily worked on getting milestone 1 set up, as well as putting the finishing touches on the project (as well as the README, video, etc.)
* Youngjae Moon primarily worked on logic for the ML models and ensured proper serialization/deserialization, and trying to get high accuracy.
* Lisa Liu primarily worked on getting the database and communication set up between the VMs for proper connectivity.

## Team Members

* Young-jae Moon (MS, youngjae.moon@vanderbilt.edu
* Robert Sheng (BS/MS, robert.sheng@vanderbilt.edu
* Lisa Liu (BS, chuci.liu@vanderbilt.edu

under Professor Aniruddha Gokhale, a.gokhale@vanderbilt.edu
