FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt

RUN apt-get update && \
    apt-get -y install gdal-bin python3-pip && \
    pip3 install -r /app/requirements.txt

ADD app /app
WORKDIR /app

ENTRYPOINT [ "python3", "manage.py" ]
