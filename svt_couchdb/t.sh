#!/bin/bash -e
# run this service

pushd $(dirname ${BASH_SOURCE[0]}) > /dev/null
export SERVICE=$(basename $PWD)
export SERVICE_NAME=$(egrep -o "[^_]+$" <<<"$SERVICE")
export SERVICE_VERSION=1.1

sudo docker rm -f $SERVICE_NAME > /dev/null
rm -rf /home/zen/db/couch1
sudo bash build.sh > /dev/null
sudo bash run.sh 
popd > /dev/null
