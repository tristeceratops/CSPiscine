FROM debian:bullseye

RUN apt update && apt upgrade -y && \
    apt install -y tor nginx openssh-server curl man

RUN mkdir -p /var/run/sshd
RUN ssh-keygen -A

COPY index.html /var/www/html/index.html
COPY nginx.conf /etc/nginx/nginx.conf
COPY torrc /etc/tor/torrc
COPY sshd_config /etc/ssh/sshd_config

RUN chown -R www-data:www-data /var/www/html

#setup a password for root just to pass the ssh connection
RUN echo "root:rootpassword" | chpasswd

COPY start-services.sh /start-services.sh
RUN chmod +x /start-services.sh

EXPOSE 80 4242

ENTRYPOINT ["/start-services.sh"]