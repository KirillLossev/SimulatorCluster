import math
import os
import threading
import carla
import carla_util
import pika

import urllib.parse

from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values('.env')

try:
    env_vars["CARLA_SERVER"]
except KeyError:
    print("The address of the CARLA server is not specified. Set the CARLA_SERVER environment variable.")
    exit()

try:
    env_vars["MQ_SERVER"]
except KeyError:
    print("The address of the Message Queue server is not specified. Set the MQ_SERVER environment variable.")
    exit()
    

# https://stackoverflow.com/a/53172593
def parse_hostport(hp):
    # urlparse() and urlsplit() insists on absolute URLs starting with "//"
    result = urllib.parse.urlsplit('//' + hp)
    return result.hostname, result.port

(mq_host, mq_port) = parse_hostport(env_vars["MQ_SERVER"])
(carla_host, carla_port) = parse_hostport(os.environ["CARLA_SERVER"])
(mq_host, mq_port) = parse_hostport(os.environ["MQ_SERVER"])

def push_data(speed, channel):
    channel.basic_publish(exchange='speed', routing_key='', body=str(speed))

def get_speed(actor):
    speed_vec = actor.get_velocity()
    # km/h
    abs_speed = 3.6 * math.sqrt(speed_vec.x ** 2 + speed_vec.y ** 2 + speed_vec.z ** 2)
    return abs_speed

def on_tick(actor, channel):
    speed = get_speed(actor)
    push_data(speed, channel)

# Connect to CARLA server
client = carla.Client(carla_host, carla_port)
world = client.get_world()
world.wait_for_tick()
hero_actor = carla_util.select_hero_actor(world)

# Connect to the message queue
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=mq_host,
    port=mq_port))
channel = connection.channel()
channel.exchange_declare(exchange='speed', exchange_type='fanout')
channel.confirm_delivery()

# Set up the sensors
world.on_tick(lambda _: on_tick(hero_actor, channel))

# Run until stopped
forever = threading.Event()
forever.wait()
