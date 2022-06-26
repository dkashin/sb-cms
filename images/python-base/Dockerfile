FROM python:3.7-alpine

RUN set -x \
	&& pip install --upgrade pip \
	&& apk update \
	&& apk add --no-cache libstdc++ \
	&& apk add --no-cache --virtual=build g++ \
	&& pip install grpcio==1.14.2 \
	&& pip install google-api-core==1.3.0 \
	&& pip install protobuf==3.6.1 \
	&& apk del --purge build \
	&& pip install pipenv \
	&& pip install rq
