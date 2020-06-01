FROM ubuntu:18.04
ARG requirements=requirements.txt

WORKDIR /bml

RUN apt-get update
RUN apt-get install -y python3-pip

RUN pip3 install celery==4.2.0 && \
    pip3 install redis==3.3.11 && \
    pip3 install web3==5.3.0 && \
    pip3 install bcrypt==3.1.7 && \
    pip3 install aiohttp==3.6.0 && \
    pip3 install itsdangerous==1.1.0 && \
    pip3 install elasticsearch==7.0.2 && \
    pip3 install Crypto==1.4.1

