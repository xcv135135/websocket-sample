FROM ubuntu:18.04

WORKDIR /root

RUN \
	apt update -y && \
	apt-get install sudo && \
	sudo apt-get install -y vim  && \
	sudo apt-get install -y wget && \
	sudo apt-get install -y curl && \
	sudo apt-get install -y python3-pip && \
	pip3 install websockets && \
	sudo apt-get install -y net-tools && \
	sudo apt-get install -y fish

# docker build -t="koimeetercenter:v1.0" ./ && docker run --rm -v /share:/share -v /mnt:/mnt -it koimeetercenter:v1.0 /bin/bash;

# docker run -d --rm --network=host -v /share:/share -v /mnt:/mnt -it koimeetercenter:v1.0 /bin/bash && docker exec -it <ID> /usr/bin/fish

# docker run -d --rm -p 5678:5678 -v /share:/share -v /mnt:/mnt -it koimeetercenter:v1.0 /bin/bash
