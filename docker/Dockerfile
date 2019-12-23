# set the base image
FROM ubuntu:18.04

# author
MAINTAINER Hany Hamed

# extra metadata
LABEL version="0.1"
LABEL description="First image with Dockerfile."

# update sources list
RUN apt-get update -y

# Install the required dependencies
RUN apt install -qy git nano g++ libglib2.0-dev curl frRUN apt install -qyeeglut3 freeglut3-dev cmake build-essential unzip g++-4.8 python python3-pip xvfb
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.8
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 40 --slave /usr/bin/g++ g++ /usr/bin/g++-7
RUN pip3 install gym
RUN pip3 install tqdm

RUN mkdir ~/hany606
RUN git clone https://github.com/hany606/Tensegrity-Robotics.git ~/hany606
RUN git -C ~/Tensegrity-Robotics/ checkout headless_server

RUN ~/hany606/Tensegrity-Robotics/bin/build.sh
RUN ~/hany606/Tensegrity-Robotics/bin/build.sh
RUN ~/hany606/Tensegrity-Robotics/bin/build.sh

RUN pip3 install -e ~/hany606/Tensegrity-Robotics/src/dev/gym-tensegrity/gym_tensegrity/

RUN Xvfb :3 -screen 0 1024x768x24 -ac +extension GLX +render -noreset &> xvfb.log &
RUN export DISPLAY=:3
