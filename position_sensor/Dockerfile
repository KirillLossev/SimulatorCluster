FROM python:3.8-slim-buster AS carlabase
RUN pip3 install carla==0.9.14

FROM carlabase AS mqbase
RUN pip3 install pika
COPY host_util.py position_sensor/run_position_sensor.py ./
CMD ["python3", "run_position_sensor.py"]