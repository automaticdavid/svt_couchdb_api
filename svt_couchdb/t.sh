pushd $(dirname ${BASH_SOURCE[0]})
sudo docker rm -f couchdb
rm -rf /home/zen/db/couch1
sudo bash build.sh 
sudo bash run.sh 
popd
