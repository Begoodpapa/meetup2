echo "*************  Total Run $1 times  **************"
rm -rf ./inter-cpu/logs
mkdir ./inter-cpu/logs

for ((  i = 1 ;  i <= $1;  i++  ))
do
  echo "************** Dmxmsg functional Test No. $i ************* "
  date
  
  pybot -P ../../TALIB/src -L TRACE ./inter-cpu/dmxmsg_transmisson_between_linux_and_se_functional_inter_cpu.tsv
  cp ./log.html ./inter-cpu/logs/dmxmsg_transmisson_between_linux_and_se_functional_inter_cpu_log_$i.html
  
  pybot -P ../../TALIB/src -L TRACE ./inter-cpu/dmxmsg_transmisson_between_linux_and_se_functional_u8_alloc_inter_cpu.tsv
  cp ./log.html ./inter-cpu/logs/dmxmsg_transmisson_between_linux_and_se_functional_u8_alloc_inter_cpu_log_$i.html

  pybot -P ../../TALIB/src -L TRACE ./inter-cpu/dmxmsg_transmisson_between_linux_and_se_functional_u8_inter_cpu.tsv
  cp ./log.html ./inter-cpu/logs/dmxmsg_transmisson_between_linux_and_se_functional_u8_inter_cpu_log_$i.html
  
  pybot -P ../../TALIB/src -L TRACE ./inter-cpu/dmxmsg_transmisson_between_linux_and_se_functional_wqe_inter_cpu.tsv
  cp ./log.html ./inter-cpu/logs/dmxmsg_transmisson_between_linux_and_se_functional_wqe_inter_cpu_log_$i.html
  
  pybot -P ../../TALIB/src -L TRACE ./inter-cpu/dmxmsg_transmisson_between_se_and_se_functional_frag_u8_alloc_inter_cpu.tsv
  cp ./log.html ./inter-cpu/logs/dmxmsg_transmisson_between_se_and_se_functional_frag_u8_alloc_inter_cpu_log_$i.html
  
  pybot -P ../../TALIB/src -L TRACE ./inter-cpu/dmxmsg_transmisson_between_se_and_se_functional_inter_cpu.tsv
  cp ./log.html ./inter-cpu/logs/dmxmsg_transmisson_between_se_and_se_functional_inter_cpu_log_$i.html
  
  pybot -P ../../TALIB/src -L TRACE ./inter-cpu/dmxmsg_transmisson_between_se_and_se_functional_u8_frag_inter_cpu.tsv
  cp ./log.html ./inter-cpu/logs/dmxmsg_transmisson_between_se_and_se_functional_u8_frag_inter_cpu_log_$i.html
  
  pybot -P ../../TALIB/src -L TRACE ./inter-cpu/dmxmsg_transmisson_between_se_and_se_functional_u8_inter_cpu.tsv
  cp ./log.html ./inter-cpu/logs/dmxmsg_transmisson_between_se_and_se_functional_u8_inter_cpu_log_$i.html
  
  pybot -P ../../TALIB/src -L TRACE ./inter-cpu/dmxmsg_transmisson_between_se_and_se_functional_u8_u8_alloc_inter_cpu.tsv
  cp ./log.html ./inter-cpu/logs/dmxmsg_transmisson_between_se_and_se_functional_u8_u8_alloc_inter_cpu_log_$i.html
  
  pybot -P ../../TALIB/src -L TRACE ./inter-cpu/dmxmsg_transmisson_between_se_and_se_functional_wqe_frag_inter_cpu.tsv
  cp ./log.html ./inter-cpu/logs/dmxmsg_transmisson_between_se_and_se_functional_wqe_frag_inter_cpu_log_$i.html
  
  pybot -P ../../TALIB/src -L TRACE ./inter-cpu/dmxmsg_transmisson_between_se_and_se_functional_wqe_inter_cpu.tsv
  cp ./log.html ./inter-cpu/logs/dmxmsg_transmisson_between_se_and_se_functional_wqe_inter_cpu_log_$i.html
  
  pybot -P ../../TALIB/src -L TRACE ./inter-cpu/dmxmsg_transmisson_between_se_and_se_functional_wqe_u8_alloc_inter_cpu.tsv
  cp ./log.html ./inter-cpu/logs/dmxmsg_transmisson_between_se_and_se_functional_wqe_u8_alloc_inter_cpu_log_$i.html
  
  pybot -P ../../TALIB/src -L TRACE ./inter-cpu/dmxmsg_transmisson_between_se_and_se_functional_wqe_u8_inter_cpu.tsv
  cp ./log.html ./inter-cpu/logs/dmxmsg_transmisson_between_se_and_se_functional_wqe_u8_inter_cpu_log_$i.html

  pybot -P ../../TALIB/src -L TRACE ./inter-cpu/dmxmsg_transmisson_between_linux_and_se_functional_group_addr_inter_cpu.tsv
  cp ./log.html ./inter-cpu/logs/dmxmsg_transmisson_between_linux_and_se_functional_group_addr_inter_cpu_log_$i.html

done
