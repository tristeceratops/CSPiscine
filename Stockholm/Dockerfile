FROM debian:bullseye

RUN apt update && apt upgrade -y && apt install -y man python3 pip
RUN pip install PyNaCl
RUN mkdir  /home/infection
RUN mkdir  /home/infection/test1 /home/infection/test2 /home/infection/test1/test3
RUN mkdir  /home/stockholm
RUN touch /home/infection/test1/test.txt
COPY infection /home/infection
COPY stockholm.py /home/stockholm/src/stockholm.py
COPY extensions.txt /home/stockholm/src/extensions.txt