# CS5287_Cloud_Computing_Team6_Homework1
Manual Deployment of a Cloud-based IoT Data Analytics Pipeline using Virtual Machines

## Goals

The goal of this assignment is to deploy a data analytics pipeline in the cloud using a cluster of distributed virtual machines. The scenario we are emulating is an IoT application where some surveillance cameras periodically send data via Kafka publish/subscribe brokers to a cloud-based analytics engine that attempts to infer the incoming image and then stores the input and output to a database so that eventually additional analytics can be conducted on the stored data. Since the Kafka brokers represent a publish/subscribe system, our emulated IoT sources serve as the producers of information. Our system will support two types of consumers. One type of consumer in our system pulls the data from the Kafka broker and stores it in a database. The other kind of consumer pulls the same sample from the Broker and sends it to a machine learning (ML) trained model that provides inference decisions. The inference decision is then added to the entry that was inserted previously in the database. In a later assignment, we will run Map Reduce on such stored data.

<img width="427" alt="image" src="https://github.com/user-attachments/assets/99647e47-b5b6-44f1-923f-e6ca48292f2e">

## About Members

#### Young-jae Moon
* M.Sc. in computer science and Engineering Graduate Fellowship recipient at Vanderbilt University.
* Incoming Online Master in computer science student at Georgia Tech.
* Email: youngjae.moon@Vanderbilt.Edu

#### Robert Sheng
* M.Sc. in computer science student at Vanderbilt University
* Email: robert.sheng@Vanderbilt.Edu

#### Lisa Liu
* B.Sc. in computer science student at Vanderbilt University
* Email: chuci.liu@Vanderbilt.Edu

## Course Instructor

#### Professor Aniruddha Gokhale
* Professor in the Computer Science at Vanderbilt University
* Email: a.gokhale@Vanderbilt.edu

# Technologies Used
1. Python 3
2. Apache Kafka
3. MongoDB
4. Chameleon Cloud with Ubuntu Linux version 22.04 image (CC-Ubuntu22.04 on Chameleon)
5. CIFAR-10 image data set used by the IoT source.

## Instructions for setting up the technologies used

* To be added

## Instructions for testing the assignment

* To be added

## Bug tracking

* All users can view and report a bug in the "GitHub Issues" of our repository.
* Here is the URL for viewing and reporting a list of bugs: https://github.com/Pingumaniac/CS5287_Cloud_Computing_Team6_Homework1/issues

