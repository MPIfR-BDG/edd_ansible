FROM ubuntu:18.04

MAINTAINER Tobias Winchen "twinchen@mpifr-bonn.mpg.de"

# Suppress debconf warnings
ENV DEBIAN_FRONTEND noninteractive

USER root

ADD id_rsa.pub /tmp/id_rsa.pub
RUN apt-get -y check && \
    apt-get -y update && \
    apt-get install -y apt-utils apt-transport-https software-properties-common locales && \
    apt-get -y update --fix-missing && \
    apt-get -y upgrade && \
    echo en_US.UTF-8 > /etc/locale.gen && \
    echo LANG=en_US.UTF-8 > /etc/default/locale && \
    # Install dependencies \
    apt-get --no-install-recommends -y install \
      python \
      acl \
      net-tools \
      openssh-server \
      python-docker \
      docker.io && \
    mkdir -p ~/.ssh &&\
    cat /tmp/id_rsa.pub > ~/.ssh/authorized_keys && \
    service ssh start

WORKDIR /root
CMD ["/usr/sbin/sshd", "-D", "-p", "2222"]
