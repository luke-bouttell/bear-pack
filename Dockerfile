#FROM python:3.7-alpine
FROM ubuntu:20.04
WORKDIR /code
RUN apt-get update && apt-get install -y \
    software-properties-common
RUN add-apt-repository universe
RUN apt-get update && apt-get install -y \ 
    python3-pip \
    libusb-1.0-0-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY rosbag_rollover.py .
COPY rs_capture.py .
COPY process_handler.py .
COPY graceful_killer.py .

ENTRYPOINT ["python3", "-u", "process_handler.py"]