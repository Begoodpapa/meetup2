echo "*************  Total Run $1 times  **************"
rm -rf ./logs
mkdir logs
TIMES=${1:-1}

for ((  i = 1 ;  i <= $TIMES;  i++  ))
do
  echo "************** Dmxmsg input sync functional Test No. $i ************* "
  date
  pybot -P ../../TALIB/src -L TRACE ./dmxmsg_input_sync_reorder_test.tsv
  cp ./log.html ./logs/dmxmsg_input_sync_reorder_test_log_$i.html
done
