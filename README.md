# The 411 on the 311
This project was a proof of concept to create a data pipeline for my Insight Data Engineering project. Specifically, I elected to base this project off of NYC 311 data. For the purposes of this project, the data has been either modified or self-engineered, so the results are fictious.

![alt text](https://raw.githubusercontent.com/smehta930/project311/master/img/homepage.png "Historical Data")

## Table of Contents
- <a href= "https://github.com/smehta930/project311/blob/master/README.md#project-overview">Project Overview</a>
- <a href= "https://github.com/smehta930/project311/blob/master/README.md#data-architecture">Data Architecture</a>
- <a href= "https://github.com/smehta930/project311/blob/master/README.md#how-to-use-this-repo">How to Use this Repo</a>
- <a href= "https://github.com/smehta930/project311/blob/master/README.md#front-end-results">Front End Results</a>

## Project Overview
I have two streams of data: historical and (near) real-time. After ingesting this data and performing some processing in Spark and Spark Streaming (for historical and real-time, respectively), I use Cassandra as my key-value store. A full diagram of my pipeline is below.

## Data Architecture
The following tools were used for this project:
* Zookeeper
* Kafka
* HDFS
* Spark
* Spark Streaming
* Cassandra

The data and processing were done on four AWS EC2 m4 xlarge machines. The ingestion, storage, and processing were setup to run in a distributed manner, with 1 master node and 3 worker nodes. The master node had 8GB of memory and 50GB of storage. The worker nodes each had 8GB of memory and 1TB of storage.

#### Historical Data: 
![alt text](https://raw.githubusercontent.com/smehta930/project311/master/img/historical.png "Historical Data")

#### Near Real Time Data:
![alt text](https://raw.githubusercontent.com/smehta930/project311/master/img/real_time.png "Near Real Time Data")

## How to Use this Repo
* The full details of the historical stream is documented in the [historical] (https://github.com/smehta930/project311/tree/master/historical) folder.
* The full details of the data I randomly generated is available in the [kafka] (https://github.com/smehta930/project311/tree/master/kafka) folder. The Spark Submission processing job is also available in this folder.
* I also tested submitting my live data in Spark via Scala. This is available in the [streaming] (https://github.com/smehta930/project311/tree/master/streaming) folder.

## Front End Results
I have a created a simple Flask app that displays the results from my data pipeline. The app is available at www.sonia.nyc and a video demonstration of the site is available [here] (https://youtu.be/pQgADLRgwkE).





