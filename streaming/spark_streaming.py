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
   ssc = StreamingContext(sc, 10)

   #print "-----\n",ssc, count 
   try:
       data = KafkaUtils.createStream(ssc, "%s:2181"%kafka_ip, "complaints",{"complaints":1})
   except Exception as e:
       print "--- exception----", e
   #print "--- data --", data, data.pprint()
   
   parsed = data.map(lambda (in_tuple): convert(in_tuple[0], in_tuple[1]))
   #print "--- map ---\n"
   #parsed.pprint()
   my_row = parsed.map(lambda x: (x[1]+'_'+x[2],1))
   #my_row.pprint()
   my = my_row.reduceByKey(lambda a, b: a + b)
   my.pprint()
   my_new = my.map(lambda x:  (x[0].split('_')[0], x[0].split('_')[1], x[1]))
   #my_new.pprint()
   my_new.saveToCassandra("playground", "live_complaints2" )# save RDD to cassandra
   ssc.start() # start the process
   ssc.awaitTermination()

