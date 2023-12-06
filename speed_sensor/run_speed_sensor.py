import math
import os
import threading
import carla
import pika

from main import carla_host, carla_port
from main import mq_host, mq_port

from main import select_hero_actor

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
hero_actor = select_hero_actor(world)

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

print("end")
print("*" * 20)