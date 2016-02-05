from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
from pyspark.sql import Row
import sys
import pyspark_cassandra

Conf = SparkConf()#.setMaster("local[*]")
sc = SparkContext(conf=Conf)
sqlContext = SQLContext(sc)

raw_data = sc.textFile('hdfs://ec2-52-71-164-204.compute-1.amazonaws.com:9000/311data/311_full.csv')
csv_data = raw_data.map(lambda x: x.split(","))

row_data = csv_data.map(lambda p: Row(
    unique_key=p[0], 
    created_date=p[1],
    closed_date=p[2],
    agency=p[3],
    agency_name=p[4],
    complaint_type=p[5],
    descriptor=p[6], 
    location_type=p[7], 
    incident_zip=p[8],
    incident_address=p[9], 
    street_name=p[10],
    cross_street_1=p[11], 
    cross_street_2=p[12], 
    intersection_street_1=p[13], 
    intersection_street_2=p[14], 
    address_type=p[15], 
    city=p[16], 
    landmark=p[17], 
    facility_type=p[18], 
    status=p[19], 
    due_date=p[20],
    resolution_description=p[21], 
    resolution_action_updated_date=p[22], 
    community_board=p[23], 
    borough=p[24], 
    x_coordinate_state_plane=p[25], 
    y_coordinate_state_plane=p[26], 
    park_facility_name=p[27],
    park_borough=p[28], 
    school_name=p[29], 
    school_number=p[30], 
    school_region=p[31], 
    school_code=p[32], 
    school_phone_number=p[33], 
    school_address=p[34], 
    school_city=p[35], 
    school_state=p[36], 
    school_zip=p[37],
    school_not_found=p[38], 
    school_or_citywide_complaint=p[39], 
    vehicle_type=p[40], 
    taxi_company_borough=p[41], 
    taxi_pick_up_location=p[42], 
    bridge_highway_name=p[43], 
    bridge_highway_direction=p[44],
    road_ramp=p[45], 
    bridge_highway_segment=p[46], 
    garage_lot_name=p[47], 
    ferry_direction=p[48], 
    ferry_terminal_name=p[49], 
    latitude=p[50], 
    longitude=p[51], 
    location=p[52]
    )
)

interactions_df = sqlContext.createDataFrame(row_data)
interactions_df.registerTempTable("tmp_1")
##interactions_df.registerTempTable("zipcode_complaints")

##complaints = sqlContext.sql("""
  ##  SELECT complaint_type, incident_zip, count(*) total FROM zipcode_complaints group by complaint_type, incident_zip
##""")

complaints = sqlContext.sql("""
    SELECT count(*) total FROM tmp_1
""")

complaints.show()

#complaints.write.format("org.apache.spark.sql.cassandra").options(table ="zipcode_complaints", keyspace = "playground").save(mode='append')


complaints.write.format("org.apache.spark.sql.cassandra").options(table ="tmp_1", keyspace = "playground").save(mode='append')

