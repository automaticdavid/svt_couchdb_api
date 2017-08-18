#!/bin/bash -e

pushd $(dirname ${BASH_SOURCE[0]}) > /dev/null

export SERVICE=$(basename $PWD)
export SERVICE_NAME=$(egrep -o "[^_]+$" <<<"$SERVICE")
export SERVICE_REPO=$(egrep -o '^[^_]*'  <<<"$SERVICE")
export SERVICE_VERSION=1.1

sudo docker run -d --name $SERVICE_NAME --network=svt_net --network-alias=$SERVICE_NAME $SERVICE_REPO/$SERVICE_NAME 

popd > /dev/null
