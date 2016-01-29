import random
import sys
import six
from datetime import datetime
from kafka.client import KafkaClient
from kafka.producer import KeyedProducer

class Producer(object):

  def __init__(self, addr):
    self.client = KafkaClient(addr)
    self.producer = KeyedProducer(self.client)
    self.zipcode = []
    self.complaint = []

  def load_ids(self):
    zipcode_path = "/home/ubuntu/repos/project311/kafka/zipcodes.txt"
    complaint_path = "/home/ubuntu/repos/project311/kafka/complaint_type.txt"
    with open(zipcode_path, 'r') as f1:
      for line in f1:
        if line != "":
            self.zipcode.append(line.strip())
    with open(complaint_path) as f2:
      for line in f2:
        if line != "":
          self.complaint.append(line.strip())

  def produce_msgs(self, source_symbol):
    msg_cnt = 0
    while True:
      time_field = datetime.now().strftime("%Y%m%d %H%M%S")
      zipcode_field = random.choice(self.zipcode)
      complaint_field = random.choice(self.complaint)
      str_fmt = "{};{};{};{}"
      message_info = str_fmt.format(source_symbol, time_field, zipcode_field, complaint_field)
      # print message_info
      self.producer.send_messages('complaint', source_symbol, message_info)
      msg_cnt += 1


if __name__ == "__main__":
  args = sys.argv
  ip_addr = str(args[1])
  partition_key = str(args[2])
  prod = Producer(ip_addr)
  prod.load_ids()
  prod.produce_msgs(partition_key)