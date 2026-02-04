FROM debian:bullseye

RUN apt update && apt upgrade -y && apt install -y man python3 pip vim
RUN pip install PyNaCl
RUN mkdir  /home/infection
RUN mkdir  /home/stockholm
COPY infection /home/infection
COPY src /home/stockholm/src
ENV HOME="/home"