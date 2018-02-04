#!/bin/bash
TIMES=${1:-1}

source func_run_case.sh

echo "*************  Total Run $TIMES times  **************"
rm -rf ./logs
mkdir logs

  cases="dmxmsg_transmisson_between_mips_and_mips_functional
         dmxmsg_transmisson_between_mips_and_ppc_functional
         dmxmsg_transmisson_between_mips_and_x86_functional
         dmxmsg_transmisson_between_ppc_and_mips_functional
         dmxmsg_transmisson_between_ppc_and_ppc_functional
         dmxmsg_transmisson_between_ppc_and_x86_functional
         dmxmsg_transmisson_between_x86_and_mips_functional
         dmxmsg_transmisson_between_x86_and_ppc_functional
         dmxmsg_transmisson_between_x86_and_x86_functional
         dmxmsg_input_sync_switchover.mips
         dmxmsg_input_sync_switchover.x86
         dmxmsg_input_sync_wosp_functional_ab2
         dmxmsg_input_sync_family_support"

for ((  i = 1 ;  i <= $TIMES;  i++  ))
do
  echo "************** Fastdist functional Test No. $i ************* "
  date
  for case in $cases; do 
    run_case $case
    if [ $? -ne 0 ]; then 
      echo -e "\n\tError occured while running fastdist case $case !\n" 1>&2
    else
      cp ./log.html ./logs/${case}_$i.html
    fi
  done
done
