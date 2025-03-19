#!/bin/bash

source /sdf/group/lcls/ds/ana/sw/conda1/rel/ami_current/setup_env_lcls1.sh
#source ~/dev/ami/setup_env_lcls1.sh

#ami-local -f interval=0.1 -l random_source.fc random:///sdf/home/e/espov/dev/ami-user-library/examples/random_source.json
ami-local -f interval=2 -b 3 random:///sdf/home/e/espov/dev/ami-user-library/examples/random_source.json


