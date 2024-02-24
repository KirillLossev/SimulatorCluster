import os
import pika
from host_util import parse_hostport

if not os.environ["MQ_SERVER"]:
    print("The address of the Message Queue server is not specified. Set the MQ_SERVER environment variable.")
    exit()

if not os.environ["VERSION"]:
    print("The component version to run is not specified. Set the VERSION environment variable.")
    exit()

buffer_distance = 10 # m
# Assumption, can be changed based on the vehicle
braking_factor = 5 # m/s²

speed = 0

(mq_host, mq_port) = parse_hostport(os.environ["MQ_SERVER"])

def is_distance_safe_v1(distance: float):
    return distance >= 50 or distance == 0 # in metres

def is_distance_safe_v2(distance: float):
    return distance >= 75 or distance == 0 # in metres

def is_distance_safe_v3(distance: float):
    # Assumes that the vehicle in front is stopped completely,
    # i.e. its velocity is 0
    # Also assumes that braking delay time is 0
    safe_distance = (speed**2 / braking_factor) / 2 + buffer_distance
    return distance >= safe_distance

is_distance_safe = None
if os.environ["VERSION"] == "1":
    is_distance_safe = is_distance_safe_v1
elif os.environ["VERSION"] == "2":
    is_distance_safe = is_distance_safe_v2
elif os.environ["VERSION"] == "3":
    is_distance_safe = is_distance_safe_v3
else:
    print("Invalid version.")
    exit()

def process_obstacle_distance_message(channel, method, properties, body):
    distance = float(body)
    result = is_distance_safe(distance)
    channel.basic_publish(exchange='obstacle_detected',
                          routing_key='',
                          # the value of the bool is true if the distance *is* safe
                          body=str(not result))
    
def process_speed_message(channel, method, properties, body):
    global speed
    speed = float(body)

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=mq_host,
    port=mq_port))
channel = connection.channel()
channel.exchange_declare(exchange='speed', exchange_type='fanout')
channel.exchange_declare(exchange='obstacle_distance', exchange_type='fanout')
channel.exchange_declare(exchange='obstacle_detected', exchange_type='fanout')

speed_queue = channel.queue_declare(queue='', exclusive=True)
channel.queue_bind(exchange='speed', queue=speed_queue.method.queue)
obstacle_distance_queue = channel.queue_declare(queue='', exclusive=True)
channel.queue_bind(exchange='obstacle_distance', queue=obstacle_distance_queue.method.queue)

channel.confirm_delivery()

channel.basic_consume(queue=speed_queue.method.queue,
                      auto_ack=True,
                      on_message_callback=process_speed_message)
channel.basic_consume(queue=obstacle_distance_queue.method.queue,
                      auto_ack=True,
                      on_message_callback=process_obstacle_distance_message)
channel.start_consuming()