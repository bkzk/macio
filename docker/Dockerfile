FROM python:3.7-alpine as base

FROM base as builder




RUN apk update && apk add --no-cache git && \
    pip3 install requests && \
    rm -r /root/.cache

WORKDIR /app

RUN git clone https://github.com/bkzk/macio.git /app/


ENTRYPOINT ["/app/macio.py"]

