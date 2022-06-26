.PHONY: all

IMAGE = reg.tebox.eu/python-base:dev

all: build push

build:
	docker build -t $(IMAGE) .

push:
	docker push $(IMAGE)
