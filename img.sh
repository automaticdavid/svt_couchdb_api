#!/bin/bash -e

pushd $(dirname ${BASH_SOURCE[0]}) > /dev/null

for service in ./svt_*
do
  if [ -e $service/base/ ]
  then
    echo ">>> Building $service"
    bash $service/base/build.sh
  fi
done

popd > /dev/null
