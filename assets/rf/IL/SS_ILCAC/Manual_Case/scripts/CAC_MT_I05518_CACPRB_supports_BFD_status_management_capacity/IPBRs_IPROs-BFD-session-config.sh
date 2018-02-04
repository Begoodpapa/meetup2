ipbr_id=3800
for((i=50;i<=59;i++));
do
  for((j=60;j<=69;j++));
  do 
       fsclish -c "add networking ipbr ipbr-id $ipbr_id committed-bandwidth 100 committed-dcn-bandwidth 0 committed-sig-bandwidth 0 route-bandwidth 200 ipbr-name BFD"
       fsclish -c "add networking ipro ipbr-id $ipbr_id iface ethtest20 owner /QNUP-0 ip-address 191.251.10.$i"
       fsclish -c "add networking monitoring bfd session /QNUP-0 dstaddr 191.251.10.$j srcaddr 191.251.10.$i reference-id $ipbr_id name Flash-$ipbr_id"
       fsclish -c "add networking monitoring bfd session /QNUP-2 dstaddr 191.251.10.$i srcaddr 191.251.10.$j name Flash-$ipbr_id"
       ipbr_id=$(($ipbr_id+1));
       done;
   done;
