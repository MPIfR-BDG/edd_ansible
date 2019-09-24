FROM {{docker_registry}}/eddbase
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
  mkdir -p EDD_PFB/build && \
  cd EDD_PFB/build && \
  cmake ..&& \
  make -j4 && \
  make install

WORKDIR /root
CMD /usr/bin/python /src/EDD_PFB/CriticalPFBPipeline.py
