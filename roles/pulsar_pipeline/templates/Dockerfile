FROM {{docker_registry}}:{{docker_registry_port}}/pulsar_base
MAINTAINER Jason Wu "jwu@mpifr-bonn.mpg.de"

# Suppress debconf warnings
ENV DEBIAN_FRONTEND noninteractive

USER root

# Software sources go to /src

# Additional dependencies
RUN   cd /src && \
    apt-get --no-install-recommends -y install \
    libxml2 \
    libxml2-dev \
    pgplot5 \
    autoconf \
    autotools-dev  \
    automake  \
    autogen  \
    libtool  \
    pkg-config \
    cmake  \
    csh  \
    gcc  \
    gfortran  \
    wget  \
    git  \
    expect \
    cvs  \
    libcfitsio-dev  \
    hwloc  \
    python  \
    python-dev  \
    python-pip \
    libfftw3-3  \
    libfftw3-bin  \
    libfftw3-dev  \
    libfftw3-single3  \
    libx11-dev \
    libpnglite-dev \
    libhdf5-dev  \
    libhdf5-serial-dev  \
    libxml2  \
    libxml2-dev  \
    libltdl-dev  \
    gsl-bin  \
    libgsl-dev 

ENV    PSRHOME /src/

WORKDIR $PSRHOME

RUN git clone https://github.com/MPIfR-BDG/mpikat.git &&\
    cd mpikat && \
    git checkout edd_pulsar_pipeline && \
    python setup.py install



WORKDIR /src/
CMD /bin/cp -r /media/scratch/jason/epta/ /tmp/ ; python /src/mpikat/mpikat/effelsberg/edd/pipeline/pipeline_rnt.py --host=0.0.0.0 --port=10001 --log_level=debug


