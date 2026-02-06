FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3 python3-pip iproute2 iputils-ping arping net-tools && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /root
CMD ["bash"]

