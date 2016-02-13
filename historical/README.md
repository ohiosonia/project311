# Historical Data

This folder contains all the information related to the historical load of the NYC 311 data.

## Table of Contents
- <a href= "https://github.com/smehta930/project311/blob/master/historical/README.md#dataset">Dataset</a>
- <a href= "https://github.com/smehta930/project311/blob/master/historical/README.md#processing-the-dataset">Processing the dataset</a>
- <a href= "https://github.com/smehta930/project311/blob/master/historical/README.md#dataset#migrating-the-data-to-ubuntu">Migrating the data to Ubuntu</a>
- <a href= "https://github.com/smehta930/project311/blob/master/historical/README.md#create-the-table-in-cassandra">Create the table in Cassandra</a>
- <a href= "https://github.com/smehta930/project311/blob/master/historical/README.md#processing-the-data-on-pyspark-and-dumping-into-cassandra">Processing the data on Pyspark and dumping into Cassandra</a>
- <a href= "https://github.com/smehta930/project311/blob/master/historical/README.md#querying-the-data-from-cassandra">Querying the data from Cassandra</a>

## Dataset
The full dataset is available [here] (https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9/). As of February 2016, the file was around 6.5 GB. There are several formats you can use to download the data, I chose csv.

## Processing the dataset
I modified the csv before migrating the data onto Ubuntu. Specifically, I removed the capital letters and spaces from the header of the file. To do this, I did the following:
 
1. `tail -n +2 311_old_header.csv > 311_no_header.csv` ##Removes the header from the file

2. `echo "unique_key,created_date,closed_date,agency,agency_name,complaint_type,descriptor,location_type,incident_zip,incident_address,street_name,cross_street_1,cross_street_2,intersection_street_1,intersection_street_2,address_type,city,landmark,facility_type,status,due_date,resolution_description,resolution_action_updated_date,community_board,borough,x_coordinate_state_plane,y_coordinate_state_plane,park_facility_name,park_borough,school_name,school_number,school_region,school_code,school_phone_number,school_address,school_city,school_state,school_zip,school_not_found,school_or_citywide_complaint,vehicle_type,taxi_company_borough,taxi_pick_up_location,bridge_highway_name,bridge_highway_direction,road_ramp,bridge_highway_segment,garage_lot_name,ferry_direction,ferry_terminal_name,latitude,longitude,location" > 311_full.csv ##Creates a separate file with the header only as the row`

3. `cat 311_no_header.csv >> 311_full.csv ##Combines the header only file and the non-header data file`


## Migrating the data to Ubuntu
After downloading the data to my local machine, I copied the data to my Ubuntu machine using the following code:

`scp <FILE LOCATION/311_full.csv> ubuntu@<PUBLIC DNS NAME>:/<FILE LOCATION ON UBUNTU>`

## Copying the data from Ubuntu to HDFS
Once the data was loaded onto my local machine, I transferred the data to HDFS.I executed the following command to migrate the data from my local Ubuntu folder to HDFS. I elected to use HDFS so that the processing could be done in a distributed manner.

`hdfs dfs -copyFromLocal ~/311data/311_full.csv /311data/311_full.csv`

## Create the table in Cassandra
For the historical data, I created three tables within Cassandra:
1. Distinct Complaints (complaint_types)
2. Types of Calls (types_of_calls)
3. Neighborhood Awards (awards)

#### Distinct Complaints (complaint_types)
This table was created for exploratory purposes -- to understand the various types of complaints made by residents.

`CREATE TABLE playground.complaint_types (
    complaint_type text,
    PRIMARY KEY (complaint_type)
)
;`

#### Types of Calls (types_of_calls)
This table feeds the following page on the front-end. It captures all the complaints from a particular zip code.

![alt text](https://raw.githubusercontent.com/smehta930/project311/master/img/types_of_calls.png "Types of Calls")
 
`CREATE TABLE playground.types_of_calls (
    incident_zip int,
    total int,
    complaint_type text,
    PRIMARY KEY (incident_zip, total)
) WITH CLUSTERING ORDER BY (total DESC);`

#### Neighborhood Awards (awards)
This table feeds the following page on the front-end. It captures which zip codes have had the highest complaints in various topics.

![alt text](https://raw.githubusercontent.com/smehta930/project311/master/img/awards.png "Neighborhood Awards")

`CREATE TABLE playground.awards (
    incident_zip int,
    total int,
    complaint_type text,
    PRIMARY KEY (complaint_type, total)
) WITH CLUSTERING ORDER BY (total DESC)
;`


## Processing the data on Pyspark and dumping into Cassandra
This was done using the SQL Context within PySpark. Using the tables created above, the following scripts processes the data in Spark and outputs it into Cassandra.

#### Distinct Complaints
Please see the `distinct_complaints.py` file

#### Types of Calls
Please see the `types_of_calls.py` file

#### Neighborhood Awards
Please see the `awards_batch.py` file

## Querying the data from Cassandra
Once the Spark jobs are complete, the data can be queried from Cassandra using CQL.
