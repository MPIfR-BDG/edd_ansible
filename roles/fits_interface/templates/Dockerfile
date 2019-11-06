FROM {{docker_registry}}/eddbase
MAINTAINER Tobias Winchen "twinchen@mpifr-bonn.mpg.de"

# Suppress debconf warnings
ENV DEBIAN_FRONTEND noninteractive

# Switch account to root and adding user accounts and password
USER root

RUN  apt remove -y python-pip &&\
  easy_install pip &&\
  /usr/local/bin/pip install spead2 &&\
  # INSTALL MPIKAT: TODO, move to base
  mkdir -p /src && \
  cd /src && \
  git clone https://github.com/ewanbarr/mpikat.git && \
  cd mpikat && \
  git checkout spead_fi_server && \
  python setup.py install

WORKDIR /root
CMD /usr/bin/python /src/mpikat/mpikat/effelsberg/edd/spead2_fi_server_new_items.py -p 1235
