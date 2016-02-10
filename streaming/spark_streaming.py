import sys, re, json
from datetime import datetime, timedelta
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark_cassandra import streaming

def convert(source, info):
    info_all = info.split(';')
    return info_all
   
if __name__ == "__main__":

   # arguments
   kafka_ip = "52.71.164.204"
   # configure spark instance
   conf = (SparkConf().setMaster("spark://ip-172-31-0-134:7077")\
           .setAppName("get_topics_in_stream")\
           .set("spark.executor.memory", "1g")\
           .set("spark.cores.max", "3"))
   sc = SparkContext(conf = conf)

   # get broadcast variables from cassandra
   count = sc.accumulator(0)
   # stream every 5 seconds
   ssc = StreamingContext(sc, 1)

   print "-----\n",ssc, count 
   try:
       data = KafkaUtils.createStream(ssc, "%s:2181"%kafka_ip, "complaints",{"complaints":1})
   except Exception as e:
       print "--- exception----", e
   print "--- data --", data, data.pprint()
   print "test"
   parsed = data.map(lambda (in_tuple): convert(in_tuple[0], in_tuple[1]))
   parsed.pprint()
   my_row = parsed.map(lambda x: {
   "source": x[0],
   "time": x[1],
   "zipcode": x[2],
   "complaint": x[3]
    })
   my_row.saveToCassandra("playground", "live_complaints2" )# save RDD to cassandra
   ssc.start() # start the process
   ssc.awaitTermination()

