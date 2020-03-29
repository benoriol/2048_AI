FROM nvidia/cuda:10.1-base-ubuntu18.04

RUN apt update -y; apt install -y \
	libsm6 \
	libxext6 \
	libxrender-dev \
	python3 \
	python3-pip \
	xsel

RUN python3 -m pip install --upgrade pip

ADD ./requirements.txt .
RUN pip3 install -r requirements.txt
