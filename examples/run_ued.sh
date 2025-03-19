#!/bin/bash

source /sdf/group/lcls/ds/ana/sw/conda2/manage/bin/psconda.sh

EXP="ued1010667"
RUN="5"

ami-local -b 5 -f interval=0.02 -l ued_example.fc psana://exp=$EXP,run=$RUN,repeat=true

