FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    lsb-release \
    git \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install Gazebo Sim Harmonic
RUN curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null \
    && apt-get update && apt-get install -y \
    gz-harmonic \
    && rm -rf /var/lib/apt/lists/*

# Install ArduPilot Gazebo Plugin for Gazebo Sim
WORKDIR /plugins
RUN git clone https://github.com/ArduPilot/ardupilot_gazebo.git

WORKDIR /plugins/ardupilot_gazebo
RUN mkdir build && cd build && cmake .. && make -j$(nproc) && make install

WORKDIR /gazebo_ws

# Copy models from the plugin repo to our workspace
RUN cp -r /plugins/ardupilot_gazebo/models/* /gazebo_ws/models/ || true

ENV GZ_SIM_RESOURCE_PATH=/gazebo_ws/models:/gazebo_ws/worlds
ENV GZ_SIM_SYSTEM_PLUGIN_PATH=/usr/local/lib

CMD ["gz", "sim", "-v4", "default.sdf"]
