FROM {{docker_registry}}:{{docker_registry_port}}/eddbase
MAINTAINER Tobias Winchen "twinchen@mpifr-bonn.mpg.de"

# Suppress debconf warnings
ENV DEBIAN_FRONTEND noninteractive

# Switch account to root and adding user accounts and password
USER root

RUN
  cd /src && \
  pip install --user -e git://github.com/casper-astro/tftpy.git#egg=tftpy-0.6.3_fork-py2.7.eg && \
  cd /src && \
  git clone --single-branch --branch devel https://gitlab.mpifr-bonn.mpg.de/abansod/casperfpga.git && \
  cd casperfpga &&\
  python setup.py install  && \
  cd /src && \
  git clone https://github.com/TobiasWinchen/mpikat.git &&\
  cd mpikat && \
  git checkout dev && \
  python setup.py install

WORKDIR /root
CMD /usr/bin/python /usr/local/lib/python2.7/dist-packages/mpikat-0.1-py2.7.egg/mpikat/effelsberg/edd/pipeline/SkarabPipeline.py --host=0.0.0.0 --port=1235
