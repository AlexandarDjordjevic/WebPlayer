FROM ubuntu:16.04

RUN apt-get update
RUN apt-get -y install software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get -y install vlc vim git
RUN apt-get -y install python3.6
RUN apt-get -y install python3-pip
RUN pip3 install flask
RUN pip3 install sqlalchemy
RUN pip3 install python-vlc
CMD ["/usr/bin/python3", "web_app.py"]