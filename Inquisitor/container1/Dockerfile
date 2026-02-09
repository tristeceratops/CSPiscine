FROM ubuntu:22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install tools
RUN apt-get update && \
    apt-get install -y python3 python3-pip iproute2 iputils-ping arping net-tools

RUN pip install scapy

# Copy Python ARP listener script (optional, you can mount)
COPY inquisitor.py /root/inquisitor.py

WORKDIR /root
CMD ["bash"]

