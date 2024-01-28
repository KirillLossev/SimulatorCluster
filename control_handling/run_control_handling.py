import json
import os
import pika
from host_util import parse_hostport

if not os.environ["MQ_SERVER"]:
    print("The address of the Message Queue server is not specified. Set the MQ_SERVER environment variable.")
    exit()

(mq_host, mq_port) = parse_hostport(os.environ["MQ_SERVER"])

cc_throttle_active = False

def process_cc_message(channel, method, properties, body):
    global cc_throttle_active
    cc_throttle_active = (body == b'True')

def process_control_message(channel, method, properties, body):
    drive_control = json.loads(body)
    if cc_throttle_active and (float(drive_control['throttle']) == 0):
        drive_control['throttle'] = '1'
    channel.basic_publish(exchange='throttle',
                          routing_key='',
                          body=str(json.dumps(drive_control)))

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=mq_host,
    port=mq_port))
channel = connection.channel()
channel.exchange_declare(exchange='throttle', exchange_type='fanout')
channel.exchange_declare(exchange='control', exchange_type='fanout')
channel.exchange_declare(exchange='cruisecontrol', exchange_type='fanout')

control_queue = channel.queue_declare(queue='', exclusive=True)
channel.queue_bind(exchange='control', queue=control_queue.method.queue)
channel.confirm_delivery()

cc_queue = channel.queue_declare(queue='', exclusive=True)
channel.queue_bind(exchange='cruisecontrol', queue=cc_queue.method.queue)
channel.confirm_delivery()

channel.basic_consume(queue=control_queue.method.queue,
                      auto_ack=True,
                      on_message_callback=process_control_message)
channel.basic_consume(queue=cc_queue.method.queue,
                      auto_ack=True,
                      on_message_callback=process_cc_message)
channel.start_consuming()