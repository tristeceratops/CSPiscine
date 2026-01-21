FROM debian:bullseye

RUN apt update
RUN apt upgrade -y

RUN apt install tor -y
RUN apt install nginx -y
RUN apt install systemctl -y
RUN apt install man -y
RUN apt install curl -y

RUN apt install openssh-server -y

RUN systemctl enable nginx
#RUN systemctl start nginx

RUN systemctl enable tor
#RUN systemctl start tor

#COPY index.html /var/www/html/index.html
#COPY nginx.conf /etc/nginx/nginx.conf
#COPY torrc /etc/tor/torrc
#COPY sshd_config /etc/ssh/sshd_config