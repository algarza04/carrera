#!/bin/bash

cd P5-granjaweb/
docker-compose down
cd ..

cd P5-ab/
docker-compose down
cd ..

cd P5-locust/
docker-compose down
cd ..

docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -aq)
