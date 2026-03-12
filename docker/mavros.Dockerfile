FROM osrf/ros:humble-desktop

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    ros-humble-mavros \
    ros-humble-mavros-extras \
    && rm -rf /var/lib/apt/lists/*

# Install MAVLink datasets
RUN wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh \
    && chmod +x install_geographiclib_datasets.sh \
    && ./install_geographiclib_datasets.sh \
    && rm install_geographiclib_datasets.sh

CMD ["ros2", "launch", "mavros", "apm.launch", "fcu_url:=udp://127.0.0.1:14550@14555"]
