FROM nvidia/cuda:11.8.0-devel-ubuntu20.04
# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES \
    ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

ARG UBUNTU_RELEASE_YEAR=20
ARG CUDA_MAJOR=11
ARG CUDA_MINOR=0

ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}compute,video,utility,graphics
ARG DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_FRONTEND=noninteractive

RUN echo "Europe/Paris" > /etc/localtime ; echo "CUDA Version 11.8.0" > /usr/local/cuda/version.txt

RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && apt-get upgrade -y && apt-get autoremove -y && \
    apt-get install --no-install-recommends lsb-release zstd wget less udev sudo -y && \
    wget -q -O ZED_SDK_Ubuntu20_cuda11.8_v4.zstd.run https://download.stereolabs.com/zedsdk/4.0/cu118/ubuntu20 && \
    chmod +x ZED_SDK_Ubuntu20_cuda11.8_v4.zstd.run ; ./ZED_SDK_Ubuntu20_cuda11.8_v4.zstd.run -- silent runtime_only && \
    rm ZED_SDK_Ubuntu20_cuda11.8_v4.zstd.run && \
    rm -rf /var/lib/apt/lists/*

RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN sudo apt -y install curl 
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
RUN apt update
RUN apt -y install ros-noetic-desktop-full

RUN apt-get update
RUN apt-get install -y cmake git libgtk2.0-dev pkg-config libavcodec-dev \
libavformat-dev libswscale-dev python-dev python-numpy libtbb2 libtbb-dev \
libjpeg-dev libpng-dev libtiff-dev  libdc1394-22-dev unzip

RUN apt-get install -y wget

# Just get a simple editor for convienience (you could just cancel this line)
RUN apt-get install -y neovim 

RUN apt-get install -y libglew-dev

RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
RUN echo "source /ws/devel/setup.bash" >> ~/.bashrc
RUN ["/bin/bash"]

# Install Catkin Build
RUN sudo apt-get install python3-catkin-tools -y

# Install YOLOv7 Requirements
RUN pip3 install torch torchvision torchaudio
RUN pip3 install opencv-contrib-python
RUN pip3 install opencv-python
RUN pip3 install seaborn
RUN pip3 install thop
RUN pip3 install requests
RUN pip3 install tqdm
RUN pip3 install pyyaml
RUN pip3 install scipy

# Install OctoMap Requirements
RUN apt-get install ros-noetic-octomap -y
RUN apt-get install ros-noetic-octomap-mapping -y

USER $USERNAME
# terminal colors with xterm
ENV TERM xterm
RUN mkdir /ws
WORKDIR /ws
CMD ["bash"]
