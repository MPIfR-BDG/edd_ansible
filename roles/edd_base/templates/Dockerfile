FROM nvidia/cuda:8.0-devel-ubuntu16.04
#FROM nvidia/cuda:9.2-devel-ubuntu16.04

MAINTAINER Tobias Winchen "twinchen@mpifr-bonn.mpg.de"

# Suppress debconf warnings
ENV DEBIAN_FRONTEND noninteractive

USER root

ENV SRC /src

RUN mkdir $SRC && \
    cd /src && \
    apt-get -y check && \
    apt-get -y update && \
    apt-get install -y apt-utils apt-transport-https software-properties-common python-software-properties locales && \
    apt-get -y update --fix-missing && \
    apt-get -y upgrade && \
    echo en_US.UTF-8 > /etc/locale.gen && \
    echo LANG=en_US.UTF-8 > /etc/default/locale && \
    # Install dependencies \
    apt-get --no-install-recommends -y install \
      build-essential \
      autoconf \
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
      libgsl2 \
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
    wget http://content.mellanox.com/ofed/MLNX_OFED-4.7-1.0.0.1/MLNX_OFED_LINUX-4.7-1.0.0.1-ubuntu16.04-x86_64.tgz &&\ 
    tar -xzvf MLNX_OFED_LINUX-4.7-1.0.0.1-ubuntu16.04-x86_64.tgz &&\ 
    MLNX_OFED_LINUX-4.7-1.0.0.1-ubuntu16.04-x86_64/mlnxofedinstall --user-space-only --without-fw-update --all -q && \
    # boost all dev conflicts with MEllanox stuff thus install only here\
    apt-get --no-install-recommends -y install libboost1.58-all-dev && \ 
    ### PSRDADA \
    cd /src && \
    git clone git://git.code.sf.net/p/psrdada/code psrdada && \
    cd psrdada && \
    ./bootstrap && \
    ./configure --with-cuda-dir=yes --with-cuda-include-dir=/usr/local/cuda/include/ --with-cuda-lib-dir=/usr/local/cuda/lib64/ && \
    make -j4 && \
    make install && \ 
    ### PSRDADACPP 2 \
    cd /src && \
    git clone https://github.com/TobiasWinchen/psrdada_cpp.git && \
    cd psrdada_cpp/ &&\
    ### Could be lib for lib layout in VLBI mode \
    git checkout devel &&\
    git submodule init &&\
    git submodule update &&\
    mkdir build/ &&\
    cd build/ &&\
    cmake -DENABLE_CUDA=True .. &&\ 
    make -j 8 &&\
    make test &&\
		make install && \ 
    ### SPEAD 2 \
    # v1.8.0 or later is required by mksend \
    # v1.9.2 does not work with the ibverbs version MLNX_OFED-4.1-1.0.2.0 used above \
    cd /src && \
    git clone https://github.com/ska-sa/spead2.git && \
    cd spead2 && \
    git checkout v1.8.0  && \
    ./bootstrap.sh --no-python && \
    ./configure && \
    make -j8 &&\
    make install &&\
    ### MKRECV \ 
    cd /src && \
    git clone https://gitlab.mpifr-bonn.mpg.de/mhein/mkrecv.git && \
    cd mkrecv &&\
    mkdir build &&\
    cd build && \
    # TODO: AVOID LOCAL PATHS
    cmake .. -DENABLE_CUDA=TRUE -DPSRDADA_CPP_INCLUDE_DIR=/src/psrdada_cpp/ -DPSRDADA_CPP_LIBRARIES=/src/psrdada_cpp/build/psrdada_cpp/libpsrdada_cpp.a && \
    make -j8 &&\
    make install &&\
    ### MKSEND \
    cd /src && \
    git clone https://gitlab.mpifr-bonn.mpg.de/mhein/mksend.git && \
    cd mksend && \
    mkdir build &&\
    cd build && \
    cmake .. -DENABLE_CUDA=TRUE -DPSRDADA_CPP_INCLUDE_DIR=/src/psrdada_cpp/ -DPSRDADA_CPP_LIBRARIES=/src/psrdada_cpp/build/psrdada_cpp/libpsrdada_cpp.a && \
    make -j8 &&\
    make install &&\
    ### MPIKAT \
    cd /src && \
    apt-get --no-install-recommends -y install \
      libhdf5-dev \
      python-h5py \
	    python-numpy \
	    python-setuptools \
	    python-setuptools-git \
	    python-setuptools-scm \
	    python-pip \
	    python-pil \
      python-cmd2 \
      python-concurrent.futures \
      libpng12-dev \
      pkg-config \
      libfreetype6-dev \
      python-scipy \
      python-pytest \
      python-astropy &&\
      \
    pip install tornado nvector katpoint && \
    git clone https://github.com/ska-sa/katportalclient.git &&\
    cd katportalclient && \
    python setup.py install && \
    cd /src && \
    git clone https://gitlab.mpifr-bonn.mpg.de/wchen/Beamforming.git && \
    cd Beamforming && \
    python setup.py install &&\
    echo 'DONE!'

WORKDIR /root
 
