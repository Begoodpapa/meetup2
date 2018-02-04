if [ $1 = '-h' -o $1 = '--help' ]
then
   echo "Usage: $0 [NUM_TIMES]"
   exit 1
fi
TIMES=${1:-1}

source func_run_case.sh

echo "*************  Total Run $TIMES times  **************"
rm -rf ./logs
mkdir logs

  cases="dmxmsg_se_state_change_monitor
         dmxmsg_input_sync_reorder_test"

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
