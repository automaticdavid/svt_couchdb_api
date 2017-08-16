pushd $(dirname ${BASH_SOURCE[0]})
sudo docker rm -f generator
sudo bash build.sh 
sudo bash run.sh 
sudo docker logs -f generator
popd
