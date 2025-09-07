FROM ubuntu:22.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y iputils-ping iputils-tracepath iptables iproute2 && \
    rm -rf /var/lib/apt/lists/*

CMD ["bash"]
