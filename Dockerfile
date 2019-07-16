FROM debian:stretch

RUN apt-get update && apt-get install -y --no-install-recommends \
    libsm6 libxext6 libxrender-dev udev build-essential libc6-dev\
    libjpeg-dev libtiff5-dev  \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
    libxvidcore-dev libx264-dev \
    libusb-1.0-0-dev \
    cmake \
    git \
    wget \
    unzip \
    pkg-config \
    python python-pip libczmq-dev \
    python-dev python-setuptools \
    python-numpy python-imaging libopencv-dev python-opencv \
    && rm -rf /var/lib/apt/lists/*

RUN cd /tmp && mkdir opencv && cd opencv && \
    wget -O opencv.zip https://downloads.sourceforge.net/project/opencvlibrary/opencv-unix/2.4.13/opencv-2.4.13.zip && \
    unzip opencv.zip && ls -al && cd opencv-2.4.13 && mkdir release && cd release && \
    cmake -D ENABLE_PRECOMPILED_HEADERS=OFF -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local .. && \
    make && make install && ldconfig

RUN cd /tmp && \
    git clone -b v1.12.1 https://github.com/IntelRealSense/librealsense.git

WORKDIR /tmp/librealsense
RUN mkdir build && cd build && pwd && \
    cmake .. && make && make install


RUN python --version && \
    pip install pyzmq --no-cache-dir && \
    pip install pyserial --no-cache-dir && \
    pip install cython --no-cache-dir && \
    pip install pyrealsense==2.0 --no-cache-dir

WORKDIR /work/

ENTRYPOINT ["./docker-entrypoint.sh"]