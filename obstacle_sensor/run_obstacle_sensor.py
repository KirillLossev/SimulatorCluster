import os
import threading
import carla
import carla_util
import pika

from host_util import parse_hostport

if not os.environ["CARLA_SERVER"]:
    print("The address of the CARLA server is not specified. Set the CARLA_SERVER environment variable.")
    exit()

if not os.environ["MQ_SERVER"]:
    print("The address of the Message Queue server is not specified. Set the MQ_SERVER environment variable.")
    exit()
    
(carla_host, carla_port) = parse_hostport(os.environ["CARLA_SERVER"])
(mq_host, mq_port) = parse_hostport(os.environ["MQ_SERVER"])

def push_data(data, channel):
    channel.basic_publish(exchange='obstacle_distance', routing_key='', body=str(data.distance))

# Connect to CARLA server
client = carla.Client(carla_host, carla_port)
world = client.get_world()
world.wait_for_tick()

# Connect to the message queue
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=mq_host,
    port=mq_port))
channel = connection.channel()
channel.exchange_declare(exchange='obstacle_distance', exchange_type='fanout')
channel.confirm_delivery()

# Set up the sensors
hero_actor = carla_util.select_hero_actor(world)
blueprint = world.get_blueprint_library().find('sensor.other.obstacle')
blueprint.set_attribute("distance", "50")
blueprint.set_attribute("only_dynamics", "True")
transform = carla.Transform(carla.Location(x=0, y=0, z=0))
sensor = world.spawn_actor(blueprint, transform, attach_to=hero_actor)
sensor.listen(lambda data: push_data(data, channel))

# Run until stopped
forever = threading.Event()
forever.wait()
