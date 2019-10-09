# Use an official Python runtime as a parent image
FROM python:3.6

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONPATH "/isharp-core"
ENV isharp_hub_host "rabbit:5672"
CMD tail -f dev/null



