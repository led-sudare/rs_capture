#!/bin/sh
cname=`cat ./cname`

cd /work/
exec python main_realsense_module.py
