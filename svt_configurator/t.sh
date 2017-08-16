pushd $(dirname ${BASH_SOURCE[0]})
sudo docker rm -f configurator
sudo bash build.sh 
sudo bash run.sh 
sudo docker logs -f configurator
popd
