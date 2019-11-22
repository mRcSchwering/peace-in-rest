# alpine python
FROM alpine:latest

LABEL purpose="Baseimage for python with some basic libraries"
LABEL maintainer="schweringmarc01@gmail.com"

# add python3 pip
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

# deps for psycopg2-binary, lxml and scipy
RUN apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    build-base \
    libxslt-dev \
    openblas-dev
