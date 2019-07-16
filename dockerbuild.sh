#!/bin/sh
cname=`cat ./cname`
docker build ./ -t $cname
docker run -t --init --privileged --name $cname -v `pwd`:/work/ $cname