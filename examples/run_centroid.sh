#!/bin/bash

#source /cds/group/pcds/dist/pds/ami2-devel/setup_env_lcls1.sh
#ami-local -l centroid_demo.fc psana://exp=xpplx9220,run=133,interval=0.2,repeat=True
../bin/ami-s3df -e xpplx9220 -r 133 -l centroid_demo.fc
