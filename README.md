# The 411 on the 311
This project was a proof of concept to create a data pipeline for my Insight Data Engineering project. Specifically, I elected to base this project off of NYC 311 data. For the purposes of this project, the data has been either modified or self-engineered, so the results are fictious.

## Project Overview
I have two streams of data: historical and (near) real-time. After ingesting this data and performing some processing in Spark and Spark Streaming (for historical and real-time, respectively), I use Cassandra as my key-value store. A full diagram of my pipeline is below:

#### Historical Data: 
![alt text](https://raw.githubusercontent.com/smehta930/project311/master/historical/historical.png "Historical Data")

#### (Near) Real Time Data:
![alt text](https://raw.githubusercontent.com/smehta930/project311/master/kafka/real_time.png "Near Real Time Data")

## Front-End Results
I have a created a simple Flask app that displays the results from my data pipeline. The app is available at www.sonia.nyc and a video demonstration of the site is available [here] (https://youtu.be/pQgADLRgwkE).

## How to Use this Repo
* The full details of the historical stream is documented in the [historical] (https://github.com/smehta930/project311/tree/master/historical) folder.
* The full details of the data I randomly generated is available in the [kafka] (https://github.com/smehta930/project311/tree/master/kafka) folder. The Spark Submission processing job is also available in this folder.
* I also tested submitting my live data in Spark via Scala. This is available in the [streaming] (https://github.com/smehta930/project311/tree/master/streaming) folder.
