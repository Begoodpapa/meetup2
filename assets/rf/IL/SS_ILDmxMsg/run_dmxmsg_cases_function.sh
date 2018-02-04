#!/bin/bash
TIMES=${1:-1}

source func_run_case.sh

echo "*************  Total Run $TIMES times  **************"
rm -rf ./logs
mkdir logs

  cases="dmxmsg_xmission_linux_se.frag
         dmxmsg_xmission_linux_se.u8
         dmxmsg_xmission_linux_se.wqe
         dmxmsg_xmission_linux_se.log_addr
         dmxmsg_xmission_se_se.frag
         dmxmsg_xmission_se_se.u8
         dmxmsg_xmission_se_se.wqe
         dmxmsg_xmission_se_se.u8_frag
         dmxmsg_xmission_se_se.wqe_frag
         dmxmsg_xmission_se_se.wqe_u8
         dmxmsg_xmission_se_se_u8_alloc.frag
         dmxmsg_xmission_se_se_u8_alloc.u8
         dmxmsg_xmission_se_se_u8_alloc.wqe
         dmxmsg_transmisson_between_linux_and_se_functional_group_addr
         dmxmsg_query_addr_table
         dmxmsg_xmission_cover_prontos.tsv
         dmxmsg_transmisson_between_linux_and_se_functional_u8_alloc
         dmxmsg_se_monitor.tsv"

for ((  i = 1 ;  i <= $TIMES;  i++  ))
do
  echo "************** Dmxmsg functional Test No. $i ************* "
  date
  for case in $cases; do 
    run_case $case
    if [ $? -ne 0 ]; then 
      echo -e "\n\tError occured while running case $case !\n" 1>&2
    else
      cp ./log.html ./logs/${case}_$i.html
    fi
  done
done
