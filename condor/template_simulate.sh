#!/bin/bash

# source /home/hunt-stokes/rat4_env.sh
source /home/carpinteiroinacio/RAT/env_rat-7-0-14-recoord.sh
cd ${PATH}/condor/logs

rat -n 300823 -N ${NUMEVS} ${PATH}/condor/macros/${MACNAME}.mac
