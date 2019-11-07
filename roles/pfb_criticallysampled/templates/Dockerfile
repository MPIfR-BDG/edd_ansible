FROM {{docker_registry}}:{{docker_registry_port}}/eddbase
MAINTAINER Tobias Winchen "twinchen@mpifr-bonn.mpg.de"

# Suppress debconf warnings
ENV DEBIAN_FRONTEND noninteractive

# Switch account to root and adding user accounts and password
USER root

RUN \
  # INSTALL MPIKAT: TODO, move to base
  mkdir -p /src && \
  cd /src && \
  git clone https://TobiasWinchen@github.com/TobiasWinchen/mpikat.git &&\
  cd mpikat && \
  git checkout dev && \
  python setup.py install && \
  ### \
  cd /src && \
  git clone https://TobiasWinchen@github.com/TobiasWinchen/EDD_PFB.git  && \
  cd EDD_PFB && \
  git submodule init && \
  git submodule update && \
  mkdir -p build && \
  cd build && \
  cmake ..&& \
  make -j4 && \
  make test && \
  make install

WORKDIR /root
CMD /usr/bin/python /src/EDD_PFB/CriticalPFBPipeline.py
