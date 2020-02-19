FROM {{docker_registry}}:{{docker_registry_port}}/eddbase
MAINTAINER Tobias Winchen "twinchen@mpifr-bonn.mpg.de"

# Suppress debconf warnings
ENV DEBIAN_FRONTEND noninteractive

# Switch account to root and adding user accounts and password
USER root

RUN git clone https://github.com/MPIfR-BDG/mpikat.git &&\
  cd mpikat && \
  git checkout dev && \
  python setup.py install && \
  cd ~ &&\
  apt-get --no-install-recommends -y install \
    openssh-client \
    python-docker \
    && \
  pip install ansible==2.9.5 &&\ 
  git clone https://github.com/MPIfR-BDG/edd_ansible.git &&\
  cp -r edd_ansible/roles /etc/ansible/ &&\
  cp edd_ansible/site.yml /etc/ansible/hosts &&\
  mkdir ~/.ssh

COPY ansible.cfg /etc/ansible/ansible.cfg
COPY id_rsa /root/.ssh/id_rsa

WORKDIR /root
CMD /usr/bin/python /usr/local/lib/python2.7/dist-packages/mpikat-0.1-py2.7.egg/mpikat/effelsberg/edd/edd_master_controller.py
