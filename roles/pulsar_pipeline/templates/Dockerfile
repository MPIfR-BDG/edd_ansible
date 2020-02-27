FROM {{docker_registry}}:{{docker_registry_port}}/eddbase
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
    libgsl-dev \
    openssh-server  \
    docker.io  \
    xorg  \
    openbox

RUN pip install pip -U && \
    pip install setuptools -U && \
    pip install numpy -U && \
    pip install scipy -U && \
    pip install watchdog && \
    pip install matplotlib -U
# PGPLOT
ENV PGPLOT_DIR /usr/lib/pgplot5  
ENV    PGPLOT_FONT /usr/lib/pgplot5/grfont.dat 
ENV    PGPLOT_INCLUDES /usr/include 
ENV    PGPLOT_BACKGROUND white 
ENV    PGPLOT_FOREGROUND black 
ENV    PGPLOT_DEV /xs 
ENV    PSRHOME /src/ 
ENV    OSTYPE linux 
ENV    CUDA_HOME /usr/local/cuda 
ENV    CUDA_ROOT /usr/local/cuda

WORKDIR $PSRHOME

RUN git clone https://github.com/MPIfR-BDG/mpikat.git &&\
    cd mpikat && \
    git checkout edd_pulsar_pipeline && \
    python setup.py install

WORKDIR $PSRHOME

RUN wget http://www.atnf.csiro.au/people/pulsar/psrcat/downloads/psrcat_pkg.tar.gz && \
    tar -xvf psrcat_pkg.tar.gz -C $PSRHOME && \
    wget https://www.imcce.fr/content/medias/recherche/equipes/asd/calceph/calceph-3.3.1.tar.gz && \
    tar -xvf calceph-3.3.1.tar.gz -C $PSRHOME && \
    git clone https://bitbucket.org/psrsoft/tempo2.git && \
    git clone git://git.code.sf.net/p/dspsr/code dspsr && \
    git clone git://git.code.sf.net/p/psrchive/code psrchive && \
    git clone https://github.com/SixByNine/psrxml.git && \
    git clone https://github.com/nextgen-astrodata/DAL.git && \
    git clone https://git.code.sf.net/p/tempo/tempo && \
    git clone https://github.com/straten/epsic.git

ENV PATH=$PATH:$PSRHOME/epsic/src
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PSRHOME/epsic/src/.lib
WORKDIR $PSRHOME/epsic/src/
RUN ./bootstrap && \
        ./configure &&\
        make && \
        make install && \
        make clean

ENV CALCEPH=$PSRHOME/calceph-3.3.1
ENV PATH=$PATH:$CALCEPH/install/bin
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CALCEPH/install/lib
ENV C_INCLUDE_PATH=$C_INCLUDE_PATH:$CALCEPH/install/include
WORKDIR $CALCEPH
RUN ./configure --prefix=$CALCEPH/install --with-pic --enable-shared --enable-static --enable-fortran --enable-thread && \
    make && \
    make check && \
    make install

ENV DAL=$PSRHOME/DAL
ENV PATH=$PATH:$DAL/install/bin
ENV    C_INCLUDE_PATH=$C_INCLUDE_PATH:$DAL/install/include
ENV    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DAL/install/lib
WORKDIR $DAL
RUN mkdir build && cd $DAL/build &&\
    cmake .. -DCMAKE_INSTALL_PREFIX=$DAL/install && \
        make -j $(nproc) && \
        make && \
        make install

ENV PSRCAT_FILE $PSRHOME/psrcat_tar/psrcat.db
ENV PATH $PATH:$PSRHOME/psrcat_tar
WORKDIR $PSRHOME/psrcat_tar
RUN /bin/bash makeit && \
    rm -f ../psrcat_pkg.tar.gz

ENV PSRCAT_FILE $PSRHOME/psrcat_tar/psrcat.db
ENV PATH $PATH:$PSRHOME/psrcat_tar
WORKDIR $PSRHOME/psrcat_tar
RUN /bin/bash makeit && \
    rm -f ../psrcat_pkg.tar.gz

ENV PSRXML $PSRHOME/psrxml
ENV PATH $PATH:$PSRXML/install/bin
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:$PSRXML/install/lib
ENV C_INCLUDE_PATH $C_INCLUDE_PATH:$PSRXML/install/include
WORKDIR $PSRXML
RUN autoreconf --install --warnings=none
RUN ./configure --prefix=$PSRXML/install && \
    make -j && \
    make install && \
    rm -rf .git


ENV TEMPO2=$PSRHOME/tempo2/T2runtime
ENV    PATH=$PATH:$PSRHOME/tempo2/T2runtime/bin
ENV    C_INCLUDE_PATH=$C_INCLUDE_PATH:$PSRHOME/tempo2/T2runtime/include
ENV    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PSRHOME/tempo2/T2runtime/lib
WORKDIR $PSRHOME/tempo2
RUN sync && perl -pi -e 's/chmod \+x/#chmod +x/' bootstrap # Get rid of: returned a non-zero code: 126.
RUN ./bootstrap && \
    ./configure --x-libraries=/usr/lib/x86_64-linux-gnu  --with-calceph=$CALCEPH/install/lib --enable-shared --enable-static --with-pic F77=gfortran LDFLAGS="-L"$CALCEPH"/install/lib" CPPFLAGS="-I"$CALCEPH"/install/include" && \
    make -j $(nproc) && \
    make install && \
    make plugins-install && \
    rm -rf .git

ENV TEMPO=$PSRHOME"/tempo"
ENV PATH=$PATH:$PSRHOME"/tempo/bin"
WORKDIR $PSRHOME/tempo
RUN ./prepare && \
    ./configure --prefix=$PSRHOME/tempo && \
    make && \
    make install && \
    echo " 5109318.8410  2006836.3673    -3238921.7749   1  MEERKAT             m  MK" >> obsys.dat && \
    awk '{print $(NF-1), $0}' obsys.dat | sort -V | cut -d\  -f2-


ENV PSRCHIVE=$PSRHOME/psrchive
ENV PATH=$PATH:$PSRCHIVE/install/bin
ENV C_INCLUDE_PATH=$C_INCLUDE_PATH:$PSRCHIVE/install/include
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PSRCHIVE/install/lib
ENV PYTHONPATH=$PSRCHIVE/install/lib/python2.7/site-packages
WORKDIR $PSRCHIVE
RUN ./bootstrap && \
    ./configure --prefix=$PSRCHIVE/install --x-libraries=/usr/lib/x86_64-linux-gnu --with-psrxml-dir=$PSRXML/install --enable-shared --enable-static F77=gfortran LDFLAGS="-L"$PSRXML"/install/lib" LIBS="-lpsrxml -lxml2" && \
    make -j $(nproc) && \
    make && \
    make install && \
    rm -rf .git

WORKDIR $PSRHOME
RUN echo "Predictor::default = tempo2" >> .psrchive.cfg && \
    echo "Predictor::policy = default" >> .psrchive.cfg

ENV DSPSR=$PSRHOME"/dspsr"
ENV    PATH=$PATH:$PSRHOME"/dspsr/install/bin"
ENV    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PSRHOME"/dspsr/install/lib"
ENV    C_INCLUDE_PATH=$C_INCLUDE_PATH:$PSRHOME"/dspsr/install/include"
WORKDIR $DSPSR
RUN sed -i s/-lgsl/-lgsl\ -fopenmp/ /usr/local/bin/psrdada_ldflags && \
    ./bootstrap && \
    echo "dada" > backends.list && \
    ./configure --prefix=$DSPSR/install --with-cuda-lib-dir=/usr/local/cuda/lib64/ --with-cuda-include-dir=/usr/local/cuda/include/ --x-libraries=/usr/lib/x86_64-linux-gnu CPPFLAGS="-I"$DAL"/install/include -I/usr/include/hdf5/serial -I"$PSRXML"/install/include" LDFLAGS="-L"$DAL"/install/lib -L/usr/lib/x86_64-linux-gnu/hdf5/serial -L"$PSRXML"/install/lib" LIBS="-lpgplot -lcpgplot -lpsrxml -lxml2" CUDA_NVCC_FLAGS="-gencode arch=compute_30,code=sm_52" && \
    make -j $(nproc) && \
    make && \
    make install

WORKDIR /src/


