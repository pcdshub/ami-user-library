#!/bin/bash

source /sdf/group/lcls/ds/ana/sw/conda1/rel/ami_current/setup_env_lcls1.sh
#source ~/dev/ami/setup_env_lcls1.sh

EXP="xpply2121"
RUN="40"

ami-local -b 10 -f interval=0.01 -l rocking_curve.fc psana://exp=$EXP,run=$RUN,repeat=true
