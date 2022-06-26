#!/bin/bash

base_path=../../services
services=($(ls $base_path | grep -v restapi))
for service in "${services[@]}"
do
    echo $base_path/$service
    cp -r ../../common/*pb2*.py $base_path/$service
    cp -r ../../common/tools.py $base_path/$service
done;
docker-compose build --no-cache $1
for service in "${services[@]}"
do
    echo $base_path/$service
    rm $base_path/$service/*pb2*.py
    rm $base_path/$service/tools.py
done;
