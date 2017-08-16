#!/bin/bash -e
# build a docker image for this service

pushd $(dirname ${BASH_SOURCE[0]})
export SERVICE=$(basename $PWD)
export SERVICE_NAME=$(egrep -o "[^_]+$" <<<"$SERVICE")
export SERVICE_VERSION=1.1

# build the image
docker build --build-arg SERVICE_NAME=$SERVICE_NAME --build-arg SERVICE_VERSION=$SERVICE_VERSION -t $SERVICE .

# clean up
popd
