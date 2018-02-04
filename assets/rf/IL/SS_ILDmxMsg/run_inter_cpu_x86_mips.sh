echo "*************  Total Run $1 times  **************"
rm -rf ./logs
mkdir logs

for ((  i = 1 ;  i <= $1;  i++  ))
do
  echo "************** Dmxmsg functional Test No. $i ************* "
  date
  pybot -P ../../TALIB/src -L TRACE ./dmxmsg_transmisson_between_mips_and_mips_functional.tsv
  cp ./log.html ./logs/dmxmsg_transmisson_between_mips_and_mips_functional_log_$i.html

  pybot -P ../../TALIB/src -L TRACE ./dmxmsg_transmisson_between_mips_and_x86_functional.tsv
  cp ./log.html ./logs/dmxmsg_transmisson_between_mips_and_x86_functional_log_$i.html

  pybot -P ../../TALIB/src -L TRACE ./dmxmsg_transmisson_between_x86_and_mips_functional.tsv
  cp ./log.html ./logs/dmxmsg_transmisson_between_x86_and_mips_functional_log_$i.html

  pybot -P ../../TALIB/src -L TRACE ./dmxmsg_transmisson_between_x86_and_x86_functional.tsv
  cp ./log.html ./logs/dmxmsg_transmisson_between_x86_and_x86_functional_log_$i.html
done
