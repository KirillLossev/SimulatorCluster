import pika

import sys
from pathlib import Path
sys.path.append(f'{Path(__file__).parent.parent}/resources')

from environments import mq_host, mq_port
from environments import version

def is_distance_safe_v1(distance: float):
    return distance >= 50 or distance == 0 # in metres

def is_distance_safe_v2(distance: float):
    return distance >= 75 or distance == 0 # in metres

is_distance_safe = None
if version == "1":
    is_distance_safe = is_distance_safe_v1
elif version == "2":
    is_distance_safe = is_distance_safe_v2
else:
    print("Invalid version.")
    exit()

def process_message(channel, method, properties, body):
    distance = float(body)
    channel.basic_publish(exchange='',
                          routing_key='obstacle_detected',
                          body=str(is_distance_safe(distance)))

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=mq_host,
    port=mq_port))
channel = connection.channel()
channel.queue_declare(queue='obstacle_distance')
channel.queue_declare(queue='obstacle_detected')
channel.confirm_delivery()

channel.basic_consume(queue="obstacle_distance",
                      auto_ack=True,
                      on_message_callback=process_message)
channel.start_consuming()