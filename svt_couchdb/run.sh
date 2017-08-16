#!/bin/bash -e

pushd $(dirname ${BASH_SOURCE[0]})
export SERVICE=$(basename $PWD)
export SERVICE_NAME=$(egrep -o "[^_]+$" <<<"$SERVICE")
export SERVICE_VERSION=1.1

sudo docker run -d -v /home/zen/db/couch1/:/opt/couchdb/data --name $SERVICE_NAME --network=svt_net --network-alias=$SERVICE_NAME $SERVICE 


