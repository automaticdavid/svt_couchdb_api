#!/bin/bash -e
# build a base docker image 

pushd $(dirname ${BASH_SOURCE[0]}) > /dev/null

export IMAGE=$(basename $(dirname $PWD))
export IMAGE_VERSION=1.1
export IMAGE_NAME=$(egrep -o "[^_]+$" <<<"$IMAGE")

docker build -t svt/${IMAGE_NAME}_base .

# clean up
popd > /dev/null
