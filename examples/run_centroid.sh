#!/bin/bash

source /sdf/group/lcls/ds/ana/sw/conda1/rel/ami_current/setup_env_lcls1.sh
#source ~/dev/ami/setup_env_lcls1.sh

EXP="xpplx9220"
RUN="133"

ami-local -b 5 -f interval=0.02 -l centroid_demo.fc psana://exp=$EXP,run=$RUN,repeat=True
