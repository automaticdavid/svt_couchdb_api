#!/bin/bash -e
# build a docker image for this service

pushd $(dirname ${BASH_SOURCE[0]}) > /dev/null
export SERVICE=$(basename $PWD)
export SERVICE_NAME=$(egrep -o "[^_]+$" <<<"$SERVICE")
export SERVICE_REPO=$(egrep -o '^[^_]*'  <<<"$SERVICE")
export SERVICE_VERSION=1.1

# docker does not allow to import files from external directories, so we
# temporarily copy our wheels here
cp -R ../svt_lib .
cp -R ../svt_cfg .
# build the image
docker build --build-arg SERVICE_NAME=$SERVICE_NAME --build-arg SERVICE_VERSION=$SERVICE_VERSION -t $SERVICE_REPO/$SERVICE_$SERVICE_NAME .

# clean up
rm -rf svt_lib
rm -rf svt_cfg
popd > /dev/null

