#FROM python:3.7-alpine
FROM ubuntu:20.04
WORKDIR /code
RUN apt-get update && apt-get install -y \
    software-properties-common
RUN add-apt-repository universe
RUN apt-get update && apt-get install -y \ 
    python3-pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD python3 rs_capture.py