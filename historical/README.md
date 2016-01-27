# Historical Data

This folder contains all the information related to the historical load of the NYC 311 data.

## Dataset
The full dataset is available [here] [https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9]. As of January 2016, the file was around 6.5 GB. There are several formats you can use to download the data, I chose csv.

## Processing the dataset
Remove headers

## Migrating the data to Ubuntu
After downloading the data to my local machine, I copied the data to my Ubuntu machine using the following code:
`scp <FILE LOCATION/311_full.csv> ubuntu@<PUBLIC DNS NAME>:/<FILE LOCATION ON UBUNTU>`

## Copying the data from Ubuntu to HDFS


## Processing the data on Pyspark
