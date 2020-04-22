FROM debian:buster

MAINTAINER Tobias Winchen "twinchen@mpifr-bonn.mpg.de"

# Suppress debconf warnings
ENV DEBIAN_FRONTEND noninteractive

USER root

RUN apt-get -y check && \
    apt-get -y update && \
    apt-get install -y apt-utils apt-transport-https software-properties-common locales && \
    apt-get -y update --fix-missing && \
    apt-get -y upgrade && \
    echo en_US.UTF-8 > /etc/locale.gen && \
    echo LANG=en_US.UTF-8 > /etc/default/locale && \
    apt-get --no-install-recommends -y install \
      vim \
      isc-dhcp-server \
    && touch /var/lib/dhcp/dhcpd.leases

COPY isc-dhcp-server /etc/default/isc-dhcp-server
COPY dhcpd.conf /etc/dhcp/dhcpd.conf

CMD dhcpd -d -4



    #  python \
    #  acl \
    #  net-tools \
    #  openssh-server \
    #  python-docker \
    #  iproute2 \
    #  docker.io && \
    #mkdir -p ~/.ssh &&\
    #cat /tmp/id_rsa.pub > ~/.ssh/authorized_keys && \
    #service ssh start

