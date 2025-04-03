#!/bin/bash

source /sdf/group/lcls/ds/ana/sw/conda2/manage/bin/psconda.sh
#source ~/dev/lcls2/setup_env.sh

#ami-local -f interval=0.1 -l random_source.fc random:///sdf/home/e/espov/dev/ami-user-library/examples/random_source.json
ami-local -f interval=0.2 -b 5 random://./random_source.json


