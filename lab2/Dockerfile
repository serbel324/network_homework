FROM ubuntu

RUN apt-get update
RUN apt-get install --yes python3
RUN apt-get install --yes iputils-ping

ENV PYTHONPATH "${PYTHONPATH}:/mtu"

COPY mtu.py /mtu/
ENTRYPOINT ["python3", "/mtu/mtu.py"]