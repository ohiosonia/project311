# (Near) Real Time Data

This folder contains all the information related to the near real-time  load of the NYC 311 data.

## Table of Contents
- <a href= "https://github.com/smehta930/project311/blob/master/kafka/README.md#producer-script">Producer Script</a>
- <a href= "https://github.com/smehta930/project311/blob/master/kafka/README.md#consumer-script">Consumer Script</a>
- <a href= "https://github.com/smehta930/project311/blob/master/kafka/README.md#create-table-in-cassandra">Create Table in Cassandra</a>


## Producer Script

The `kafka_producer.py` script creates a `source, timestamp, zipcode, complaint_type`.

To kick off the producer script execute `bash spawn_kafka_streams.sh <PUBLIC IP> 8 k1` where `8` is the number of producers to spawn and `k1` is the name of the session.

##Consumer Script

The `spark_streaming.py` script consumes the data created from the producer script and performs a mapReduce function on the event data, to aggregate all the events by zipcode and timestamp and insert it into Cassandra.

## Create Table in Cassandra
This table feeds the following page on the front-end. It captures the total number of complaints recieved by zipcode, every 30 seconds.

![alt text](https://raw.githubusercontent.com/smehta930/project311/master/img/current_trends.png "Current Trends")




