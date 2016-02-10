'''
    kafka_consumer.py
    A module that consumers from kafka topics subscribed to
'''
from kafka import KafkaConsumer
from kafka import SimpleProducer, create_message
from kafka.client import KafkaClient
from kafka.consumer import KafkaConsumer
import datetime
client = KafkaClient('52.70.92.128')
consumer = KafkaConsumer('complaints', group_id=0, bootstrap_servers=['localhost:9092'])
#date1 = datetime.datetime.now()

for message in consumer:
     print "{}:{}:{}: key={} value={}".format(message.topic, message.partition, message.offset, message.key, message.value)
 #    if currentdate - date1 = 1 minute:
#	print 

