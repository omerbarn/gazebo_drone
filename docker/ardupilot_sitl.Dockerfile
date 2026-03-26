FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    python3-pip \
    sudo \
    lsb-release \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN git clone --recursive https://github.com/ArduPilot/ardupilot.git /ardupilot

WORKDIR /ardupilot

RUN ./tools/environment_install/install-prereqs-ubuntu.sh -y

RUN ./modules/waf/waf-light configure --board sitl
RUN ./modules/waf/waf-light build --targets bin/arducopter

# Create a symlink for easier access
RUN ln -s /ardupilot/build/sitl/bin/arducopter /usr/local/bin/arducopter

WORKDIR /workspace

CMD ["arducopter", "-S", "-I0", "--model", "gazebo-iris", "--speedup", "1", "--home", "0,0,0,0"]
