#!/bin/bash -e
sudo docker network create --driver bridge svt_net
bash ./svt_couchdb/t.sh
bash ./svt_configurator/t.sh
bash ./svt_generator/t.sh
