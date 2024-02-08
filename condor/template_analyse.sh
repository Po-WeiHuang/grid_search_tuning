#!/bin/bash

source /home/hunt-stokes/rat4_env.sh
cd /data/snoplus3/hunt-stokes/tune_cleaning/scripts

python3 extract_time_residuals.py ${ITERATION} ${ISOTOPE} ${PARAMETERS} ${ZOFF} ${FV_CUT} ${E_LOW} ${E_HIGH} ${DOMAIN_LOW} ${DOMAIN_HIGH}
