FROM python:3.6.1
ENV PYTHONUNBUFFERED 1

MAINTAINER Imad Hamoumi <imad.hamoumi@wlw.de>

RUN pip install --upgrade pip
RUN pip install --no-cache-dir numpy certifi click requests virtualenv pandas django django-tenant-schemas djangorestframework markdown Pillow django-filter django-widget-tweaks

RUN mkdir /root/app
ADD . /root/app
WORKDIR /root/app


COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

