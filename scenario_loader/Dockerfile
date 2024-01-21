FROM python:3.8-slim-buster AS carlabase
RUN pip3 install carla==0.9.14

FROM carlabase
COPY host_util.py carla_util.py scenario_loader/run_scenario_loader.py ./
CMD ["python3", "run_scenario_loader.py"]