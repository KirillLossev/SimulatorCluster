FROM python:3.8-slim-buster AS carlabase
RUN pip3 install carla==0.9.14

FROM carlabase
RUN apt update && apt install -y libsdl2-dev fontconfig
RUN fc-cache -f -v
RUN pip3 install pygame numpy
COPY host_util.py drive/run_drive.py ./
CMD ["python3", "run_drive.py"]