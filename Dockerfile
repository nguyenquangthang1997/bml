FROM ubuntu:18.04
ARG requirements=requirements.txt


WORKDIR /bml
COPY . /bml
RUN apt-get update
RUN apt-get install -y python3-pip

RUN pip3 install -r $requirements

EXPOSE 7999
