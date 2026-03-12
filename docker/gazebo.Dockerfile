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

# Install Gazebo as requested
RUN apt-get update && apt-get install -y \
    gazebo \
    libgazebo-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /plugins

# Clone and build the Betaflight Gazebo plugin from mkschreder/gazebo-betaflight
# This is one of the few specific to Gazebo Classic
RUN git clone https://github.com/mkschreder/gazebo-betaflight.git /plugins/gazebo-betaflight

WORKDIR /plugins/gazebo-betaflight
RUN mkdir build && cd build && cmake .. && make -j$(nproc)

WORKDIR /gazebo_ws

# Setup env variables for Gazebo to find models and world
ENV GAZEBO_PLUGIN_PATH=${GAZEBO_PLUGIN_PATH}:/plugins/gazebo-betaflight/build
ENV GAZEBO_MODEL_PATH=${GAZEBO_MODEL_PATH}:/plugins/gazebo-betaflight/models

CMD ["gazebo", "--verbose", "/gazebo_ws/worlds/drone_world.world"]
