FROM nvidia/cudagl:10.2-devel-ubuntu18.04
# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES \
    ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

ARG UBUNTU_RELEASE_YEAR=18
ARG CUDA_MAJOR=10
ARG CUDA_MINOR=0

ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}compute,video,utility,graphics
ARG DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND=noninteractive

RUN echo "Europe/Paris" > /etc/localtime ; echo "CUDA Version 10.2.0" > /usr/local/cuda/version.txt

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && apt-get upgrade -y && apt-get autoremove -y && \
    apt-get install --no-install-recommends lsb-release wget less udev sudo -y && \
    wget -q -O ZED_SDK_Linux_Ubuntu18.run https://download.stereolabs.com/zedsdk/3.7/cu102/ubuntu18 && \
    chmod +x ZED_SDK_Linux_Ubuntu18.run ; ./ZED_SDK_Linux_Ubuntu18.run -- silent runtime_only && \
    rm ZED_SDK_Linux_Ubuntu18.run && \
    rm -rf /var/lib/apt/lists/*

RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN sudo apt -y install curl 
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
RUN apt update
RUN apt -y install ros-melodic-desktop-full

RUN apt-get update
RUN apt-get install -y cmake git libgtk2.0-dev pkg-config libavcodec-dev \
libavformat-dev libswscale-dev python-dev python-numpy libtbb2 libtbb-dev \
libjpeg-dev libpng-dev libtiff-dev  libdc1394-22-dev unzip

RUN apt-get install -y wget

# Just get a simple editor for convienience (you could just cancel this line)
RUN apt-get install -y vim 

RUN apt-get install -y libglew-dev

RUN echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
RUN ["/bin/bash"]

USER $USERNAME
# terminal colors with xterm
ENV TERM xterm
RUN mkdir /ws
WORKDIR /ws
CMD ["bash"]
