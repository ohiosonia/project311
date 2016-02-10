from pyspark import SparkContext
from pyspark.streaming.kafka import KafkaUtils, TopicAndPartition
from pyspark.streaming import StreamingContext

sc = SparkContext(appName='ExStreamlyCheapDeals')
ssc = StreamingContext(sc, 1)
start = 0
partition = 0
topic = 'complaints'
topicPartion = TopicAndPartition(topic,partition)
fromOffset = {topicPartion: long(start)}

directKafkaStream = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": '52.71.164.204:9092'}, fromOffsets\
=fromOffset)
lines = directKafkaStream.map(lambda x: x[1])
counts = lines.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)
counts.pprint()

ssc.start()
ssc.awaitTermination()
