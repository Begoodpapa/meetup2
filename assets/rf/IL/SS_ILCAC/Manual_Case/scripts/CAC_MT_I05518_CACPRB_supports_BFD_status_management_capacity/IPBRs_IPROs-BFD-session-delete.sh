ipbr_id=3800
for((i=50;i<=59;i++));
do
  for((j=60;j<=69;j++));
  do 
	
       fsclish -c "delete networking ipro ipbr-id $ipbr_id iface ethtest20 owner /QNUP-0 ip-address 191.251.10.$i"
       fsclish -c "delete networking monitoring bfd session /QNUP-0 name Flash-$ipbr_id"
       fsclish -c "add networking monitoring bfd session /QNUP-2 name Flash-$ipbr_id"
       fsclish -c "delete networking ipbr ipbr-id $ipbr_id"  
       ipbr_id=$(($ipbr_id+1));
       done;
   done;
