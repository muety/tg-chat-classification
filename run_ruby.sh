#!/bin/bash

#DOCKER_IP=$(ip addr list docker0 |grep "inet " |cut -d' ' -f6|cut -d/ -f1|tr -d '\n')

docker run -it --rm --net=host -v "$PWD":/usr/src/myapp -w /usr/src/myapp ruby:alpine ruby $1
