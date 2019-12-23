# set the base image
FROM ubuntu:18.04

# author
MAINTAINER Hany Hamed

# extra metadata
LABEL version="0.2"
LABEL description="First image with Dockerfile."

# update sources list
RUN apt-get update -y

# Install the required dependencies
RUN apt-get install -qy git nano g++ libglib2.0-dev curl freeglut3 freeglut3-dev cmake build-essential unzip g++-4.8 python python3-pip xvfb
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.8 60 --slave /usr/bin/g++ g++ /usr/bin/g++-4.8
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 40 --slave /usr/bin/g++ g++ /usr/bin/g++-7
RUN pip3 install gym
RUN pip3 install tqdm

RUN mkdir -p /home/hany606 \
    cd /home/hany606

WORKDIR /home/hany606
RUN git clone https://github.com/hany606/Tensegrity-Robotics.git --branch headless_server

CMD [ "/home/hany606/Tensegirty-Robotics/bin/setup_helper.sh" ]

# RUN ["/home/hany606/Tensegrity-Robotics/bin/build.sh"] || true
# RUN ["/home/hany606/Tensegrity-Robotics/bin/build.sh"]
# RUN ["/home/hany606/Tensegrity-Robotics/bin/build.sh"]

# RUN ["/home/hany606/Tensegrity-Robotics/bin/setup_gym_env.sh"]

RUN Xvfb :3 -screen 0 1024x768x24 -ac +extension GLX +render -noreset &> xvfb.log &
RUN export DISPLAY=:3