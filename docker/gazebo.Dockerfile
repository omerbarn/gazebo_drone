FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    lsb-release \
    wget \
    gnupg \
    curl \
    git \
    build-essential \
    cmake \
    mesa-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Gazebo 11 from official OSRF repository
RUN sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list' \
    && curl -sSL http://packages.osrfoundation.org/gazebo.key | apt-key add - \
    && apt-get update && apt-get install -y \
    gazebo11 \
    libgazebo11-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /plugins

# ArduPilot plugin (ArduCopterPlugin)
RUN git clone https://github.com/ArduPilot/ardupilot_gazebo.git /plugins/ardupilot_gazebo

WORKDIR /plugins/ardupilot_gazebo
RUN mkdir build && cd build && cmake .. && make -j$(nproc) && make install

WORKDIR /gazebo_ws

# Setup env variables for Gazebo to find models and world
ENV GAZEBO_PLUGIN_PATH=${GAZEBO_PLUGIN_PATH}:/usr/local/lib
ENV GAZEBO_MODEL_PATH=${GAZEBO_MODEL_PATH}:/plugins/ardupilot_gazebo/models

CMD ["gazebo", "--verbose", "/gazebo_ws/worlds/drone_world.world"]
