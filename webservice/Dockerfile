# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine AS builder

WORKDIR /webservice

COPY . /webservice

RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

RUN apk update && apk add nginx

COPY dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
CMD ["python3", "app.py"]

EXPOSE 5000
EXPOSE 80