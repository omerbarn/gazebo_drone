FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    cmake \
    gcc \
    g++ \
    python3 \
    python3-pip \
    make \
    wget \
    curl \
    ca-certificates \
    python-is-python3 \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/betaflight/betaflight.git

WORKDIR /betaflight

RUN make arm_sdk_install
RUN make configs

RUN make TARGET=SITL

# Add a script to run SITL with initial configuration
COPY betaflight_ws/init.cli /betaflight/init.cli

CMD ["/bin/bash", "-c", "./obj/main/betaflight_SITL.elf < /betaflight/init.cli"]
