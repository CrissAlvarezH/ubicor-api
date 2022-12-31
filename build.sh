#!/bin/bash

version=$1
[ -z $version ] && version=0.1 && echo "\nset defaul version 0.1\n"

docker build -t crissalvarezh/ubicor-api:$version .

docker tag crissalvarezh/ubicor-api:$version crissalvarezh/ubicor-api:latest

docker push crissalvarezh/ubicor-api:$version
docker push crissalvarezh/ubicor-api:latest
