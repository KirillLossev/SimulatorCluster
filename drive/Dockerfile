FROM jlesage/baseimage-gui:debian-10-v4.5.3 as vnc

RUN apt update && apt install -y ca-certificates

ADD --chmod=655 https://people.debian.org/~paravoid/python-all/unofficial-python-all.asc /etc/apt/trusted.gpg.d/unofficial-python-all.asc 
RUN echo "deb http://people.debian.org/~paravoid/python-all buster main" | tee /etc/apt/sources.list.d/python-all.list

RUN apt update && apt install -y libsdl2-dev fontconfig python3.8

ADD https://bootstrap.pypa.io/get-pip.py get-pip.py
RUN python3.8 get-pip.py

RUN python3.8 -m pip install pygame numpy pika carla==0.9.14

RUN fc-cache -f -v

COPY host_util.py carla_util.py drive/run_drive.py /

COPY drive/startapp.sh /startapp.sh

RUN chmod +x /startapp.sh

ENV USER_ID=0

RUN set-cont-env APP_NAME "Simulation Viewer"
