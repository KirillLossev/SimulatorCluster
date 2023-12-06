import carla
import json
import pika

import sys
from pathlib import Path
sys.path.append(f'{Path(__file__).parent.parent}/resources')

from environments import carla_host, carla_port
from environments import mq_host, mq_port

import carla_util

def load_control(control_json):
    props = json.loads(control_json)
    return carla.VehicleControl(
        throttle=float(props['throttle']),
        steer=float(props['steer']),
        brake=float(props['brake']),
        hand_brake=bool(props['hand_brake']),
        reverse=bool(props['reverse']),
        manual_gear_shift=bool(props['manual_gear_shift']),
        gear=int(props['gear'])
    )

def process_message(channel, method, properties, body):
    control = load_control(body)
    hero_actor.apply_control(control)


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
cc_queue = channel.queue_declare(queue='', exclusive=True)
channel.queue_bind(exchange='throttle', queue=cc_queue.method.queue)
channel.confirm_delivery()

channel.basic_consume(queue=cc_queue.method.queue,
                      auto_ack=True,
                      on_message_callback=process_message)
channel.start_consuming()
