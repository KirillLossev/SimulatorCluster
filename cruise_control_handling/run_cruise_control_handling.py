import os
import pika
from host_util import parse_hostport

if not os.environ["MQ_SERVER"]:
    print("The address of the Message Queue server is not specified. Set the MQ_SERVER environment variable.")
    exit()

if not os.environ["CC_SPEED"]:
    print("The cruise control speed is not specified. Set the CC_SPEED environment variable.")
    exit()


(mq_host, mq_port) = parse_hostport(os.environ["MQ_SERVER"])

cc_speed = float(os.environ["CC_SPEED"])

def vehicle_speed_below_set(curr_speed):
    return (curr_speed < cc_speed)

def process_message(channel, method, properties, body):
    curr_speed = float(body)
    channel.basic_publish(exchange='cruisecontrol',
                          routing_key='',
                          body=str(vehicle_speed_below_set(curr_speed)))

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=mq_host,
    port=mq_port))
channel = connection.channel()
channel.exchange_declare(exchange='cruisecontrol', exchange_type='fanout')
channel.exchange_declare(exchange='speed', exchange_type='fanout')

speed_queue = channel.queue_declare(queue='', exclusive=True)
channel.queue_bind(exchange='speed', queue=speed_queue.method.queue)
channel.confirm_delivery()

channel.basic_consume(queue=speed_queue.method.queue,
                      auto_ack=True,
                      on_message_callback=process_message)
channel.start_consuming()