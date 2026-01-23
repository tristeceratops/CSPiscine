#!/bin/bash

/usr/sbin/sshd
tor &
nginx -g "daemon off;"