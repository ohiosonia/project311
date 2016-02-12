# The 411 on the 311
This project was a proof of concept to create a data pipeline for my Insight Data Engineering project. Specifically, I elected to base this project off of NYC 311 data. For the purposes of this project, the data has been either modified or self-engineered, so the results are fictious.

## Project Overview
I have two streams of data: historical and (near) real-time. After ingesting this data and performing some processing in Spark and Spark Streaming (for historical and real-time, respectively), I use Cassandra as my key-value store. A full diagram of my pipeline is below:



## Front-End Results
I have a created a simple Flask app that displays the results from my data pipeline. The app is available at www.sonia.nyc

## How to use this repo



