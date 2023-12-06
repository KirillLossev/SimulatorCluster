import pika

import sys
from pathlib import Path
sys.path.append(f'{Path(__file__).parent.parent}/resources')

from environments import mq_host, mq_port
from environments import cc_speed

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

speed_queue = channel.queue_declare(queue='', exclusive=True)
channel.queue_bind(exchange='speed', queue=speed_queue.method.queue)
channel.confirm_delivery()

channel.basic_consume(queue=speed_queue.method.queue,
                      auto_ack=True,
                      on_message_callback=process_message)
channel.start_consuming()