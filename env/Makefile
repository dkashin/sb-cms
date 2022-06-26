protoc_path = /home/ozzmedia/grpc/bins/opt
build_path = common
restapi_path = services/restapi

protoc: export GOPATH := /home/ozzmedia/go:/home/ozzmedia/go/bin
protoc: export PATH := $(PATH):$(GOPATH)
protoc:
	rm -f $(build_path)/*pb*.py
	$(protoc_path)/protobuf/protoc \
		-I/usr/local/include \
		-I/home/ozzmedia/go/src/github.com/grpc-ecosystem/grpc-gateway/third_party/googleapis \
		--plugin=protoc-gen-grpc=$(protoc_path)/grpc_python_plugin \
		--python_out=$(build_path) \
		--grpc_out=$(build_path) \
		--go_out=plugins=grpc:$(restapi_path)/src/pb \
		--grpc-gateway_out=logtostderr=true:$(restapi_path)/src/pb \
		--proto_path=protos \
		protos/*.proto

build:
	$(MAKE) protoc
	cd $(restapi_path);	CGO_ENABLED=0 go build -x *.go
