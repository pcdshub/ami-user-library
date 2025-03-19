#!/bin/bash

source /sdf/group/lcls/ds/ana/sw/conda1/rel/ami_current/setup_env_lcls1.sh
#source ~/dev/ami/setup_env_lcls1.sh

EXP="xpptut15"
RUN="650"

ami-local -b 5 -f interval=0.02 psana://exp=$EXP,run=$RUN,repeat=True

