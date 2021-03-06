FROM nvidia/cuda:11.0-devel-ubuntu18.04

MAINTAINER Tobias Winchen "twinchen@mpifr-bonn.mpg.de"

# Suppress debconf warnings
ENV DEBIAN_FRONTEND noninteractive

USER root

# Software sources go to /src

# basic setup of installed packages and Melanox drivers
RUN mkdir /src && \
    cd /src && \
    apt-get -y check && \
    apt-get -y update && \
    apt-get install -y apt-utils apt-transport-https software-properties-common locales && \
    apt-get -y update --fix-missing && \
    apt-get -y upgrade && \
    echo en_US.UTF-8 UTF-8 > /etc/locale.gen && \
    echo LANG=en_US.UTF-8 > /etc/default/locale && \
    locale-gen  && \
    # Install dependencies \
    apt-get --no-install-recommends -y install \
      build-essential \
      autoconf \
      iputils-ping \
      autotools-dev \
      automake \
      autogen \
      libtool \
      csh \
      gcc \
      gfortran \
      wget \
      cmake \
      git \
      less \
      cvs \
      expect \
      libcfitsio-dev \
      libltdl-dev \
      gsl-bin \
      libgsl-dev \
      libgsl23 \
      hwloc \
      libhwloc-dev \
      pkg-config \
      net-tools \
      vim-gtk \
      iproute2 \
      htop \
      kmod \
      ethtool \
      lsof \
      pciutils \
      numactl && \
    \
    # Download and install Mellanox OFED 4.1.1 for Ubuntu 16.04 \
    wget http://content.mellanox.com/ofed/MLNX_OFED-4.7-1.0.0.1/MLNX_OFED_LINUX-4.7-1.0.0.1-ubuntu18.04-x86_64.tgz &&\ 
    tar -xzvf MLNX_OFED_LINUX-4.7-1.0.0.1-ubuntu18.04-x86_64.tgz &&\ 
    MLNX_OFED_LINUX-4.7-1.0.0.1-ubuntu18.04-x86_64/mlnxofedinstall --user-space-only --without-fw-update --all -q && \
    rm -rf /src/MLNX_OFED_LINUX* &&\
    # boost all dev conflicts with MEllanox stuff thus install only here\
    apt-get --no-install-recommends -y install libboost-all-dev


### PSRDADA
RUN cd /src && \
    git clone git://git.code.sf.net/p/psrdada/code psrdada && \
    cd psrdada && \
    git checkout 10513fff767ce9922c3423eb7199c64f9301d1c8 && \
    # Version from  Wed Feb 12 07:46:37 2020 +0200 \
    ./bootstrap && \
    ./configure --with-cuda-dir=yes --with-cuda-include-dir=/usr/local/cuda/include/ --with-cuda-lib-dir=/usr/local/cuda/lib64/ && \
    make -j4 && \
    make install

### PSRDADACPP 2 \
RUN cd /src && \
    git clone https://github.com/MPIfR-BDG/psrdada_cpp.git && \
    cd psrdada_cpp/ &&\
    ### Could be lib for lib layout in VLBI mode \
    git checkout devel &&\
    git submodule init &&\
    git submodule update &&\
    mkdir build/ &&\
    cd build/ &&\
    cmake -DENABLE_CUDA=True .. &&\ 
    make -j 8 &&\
    make test;\
		make install

### SPEAD 2 \
 RUN  cd /src && \
    git clone https://github.com/ska-sa/spead2.git && \
    cd spead2 && \
    git checkout v1.8.0  && \
    # v1.8.0 or later is required by mksend \
    # v1.9.2 does not work with the ibverbs version MLNX_OFED-4.1-1.0.2.0 used above \
    ./bootstrap.sh --no-python && \
    ./configure && \
    make -j8 &&\
    make install

### MKRECV \ 
RUN  cd /src && \
    git clone https://gitlab.mpifr-bonn.mpg.de/mhein/mkrecv.git && \
    cd mkrecv &&\
    mkdir build &&\
    cd build && \
    # TODO: AVOID LOCAL PATHS
    cmake .. -DENABLE_CUDA=TRUE -DPSRDADA_CPP_INCLUDE_DIR=/src/psrdada_cpp/ -DPSRDADA_CPP_LIBRARIES=/src/psrdada_cpp/build/psrdada_cpp/libpsrdada_cpp.a && \
    make -j8 &&\
    make install

### MKSEND \
RUN cd /src && \
    git clone https://gitlab.mpifr-bonn.mpg.de/mhein/mksend.git && \
    cd mksend && \
    mkdir build &&\
    cd build && \
    cmake .. -DENABLE_CUDA=TRUE -DPSRDADA_CPP_INCLUDE_DIR=/src/psrdada_cpp/ -DPSRDADA_CPP_LIBRARIES=/src/psrdada_cpp/build/psrdada_cpp/libpsrdada_cpp.a && \
    make -j8 &&\
    make install

 ### MPIKAT dependencies\
RUN   cd /src && \
    apt-get --no-install-recommends -y install \
      libhdf5-dev \
      python-h5py \
	    python-numpy \
	    python-setuptools \
	    python-setuptools-git \
	    python-setuptools-scm \
	    python-pip \
	    python-pil \
      python-jinja2 \
      python-cmd2 \
      python-concurrent.futures \
      libpng-dev \
      pkg-config \
      libfreetype6-dev \
      python-scipy \
      python-pytest \
      python-redis \
      python-astropy &&\
      \
    pip install tornado==4.5.3 ujson==2.0.3 nvector==0.7.4 katpoint==0.9 kiwisolver==1.1.0 && \
    git clone https://github.com/ska-sa/katportalclient.git &&\
    cd katportalclient && \
    python setup.py install && \
    cd /src && \
    git clone https://gitlab.mpifr-bonn.mpg.de/wchen/Beamforming.git && \
    cd Beamforming && \
    git checkout f6e10a2bd7fd2c224aa04e1ddc9308b48eeddb4d && \
    python setup.py install && \ 
#    echo "Cleanup source codes ..." &&\
#    rm -rf /src &&\
    echo 'DONE!'

WORKDIR /root

