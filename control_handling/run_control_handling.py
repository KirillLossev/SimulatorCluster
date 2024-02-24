import json
import os
import pika
from host_util import parse_hostport

if not os.environ["MQ_SERVER"]:
    print("The address of the Message Queue server is not specified. Set the MQ_SERVER environment variable.")
    exit()

(mq_host, mq_port) = parse_hostport(os.environ["MQ_SERVER"])

cc_throttle_active = False
obstacle_detected = False

def process_cc_message(channel, method, properties, body):
    global cc_throttle_active
    cc_throttle_active = (body == b'True')

def process_obstacle_message(channel, method, properties, body):
    global obstacle_detected
    obstacle_detected = (body == b'True')

def process_control_message(channel, method, properties, body):
    driver_control = json.loads(body)
    applied_control = calculate_applied_control(driver_control)
    channel.basic_publish(exchange='throttle',
                          routing_key='',
                          body=str(json.dumps(applied_control)))

def calculate_applied_control(driver_control):
    # Braking takes priority
    if obstacle_detected:
        driver_control['throttle'] = '0'
        driver_control['brake'] = '1'
        return driver_control
    elif cc_throttle_active and (float(driver_control['throttle']) == 0):
        driver_control['throttle'] = '1'
    
    return driver_control

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=mq_host,
    port=mq_port))
channel = connection.channel()
channel.exchange_declare(exchange='throttle', exchange_type='fanout')
channel.exchange_declare(exchange='control', exchange_type='fanout')
channel.exchange_declare(exchange='cruisecontrol', exchange_type='fanout')
channel.exchange_declare(exchange='obstacle_detected', exchange_type='fanout')

control_queue = channel.queue_declare(queue='', exclusive=True)
channel.queue_bind(exchange='control', queue=control_queue.method.queue)
channel.confirm_delivery()

cc_queue = channel.queue_declare(queue='', exclusive=True)
channel.queue_bind(exchange='cruisecontrol', queue=cc_queue.method.queue)

obstacle_queue = channel.queue_declare(queue='', exclusive=True)
channel.queue_bind(exchange='obstacle_detected', queue=obstacle_queue.method.queue)


channel.confirm_delivery()

channel.basic_consume(queue=control_queue.method.queue,
                      auto_ack=True,
                      on_message_callback=process_control_message)
channel.basic_consume(queue=cc_queue.method.queue,
                      auto_ack=True,
                      on_message_callback=process_cc_message)
channel.basic_consume(queue=obstacle_queue.method.queue,
                      auto_ack=True,
                      on_message_callback=process_obstacle_message)
channel.start_consuming()