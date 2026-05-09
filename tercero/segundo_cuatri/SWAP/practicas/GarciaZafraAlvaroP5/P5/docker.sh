#!/bin/bash

cd P5-granjaweb/
docker-compose up -d
cd ..

cd P5-ab/
docker-compose up -d
cd ..

cd P5-locust/
docker-compose up -d
cd ..
