from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer


client = KafkaClient("52.71.164.204:9092")

consumer = SimpleConsumer(client, "xx", "complaints")

for x in consumer:
    print x

