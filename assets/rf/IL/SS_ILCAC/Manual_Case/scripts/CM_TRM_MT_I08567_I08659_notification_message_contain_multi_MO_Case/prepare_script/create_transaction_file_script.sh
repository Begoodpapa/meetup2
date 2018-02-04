OWNER_NAME=/QNUP-0
ipbr_id=100
IFACE_NAME=ethtest20
echo "#!/opt/nokiasiemens/bin/fsclish -f
set cli built-in echo-cmd on
start transaction"

for((i=10;i<=19;i++));
	do
  	for((j=100;j<=109;j++));
  	do
  		num=185
  		if [[ $ipbr_id -lt $num ]];then 
				echo "
add ipbr ipbr-id $ipbr_id committed-bandwidth 1000 committed-dcn-bandwidth 100 committed-sig-bandwidth 100 route-bandwidth 1100 ipbr-name test-$ipbr_id ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type realQueue
add ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME 
set ipbr ipbr-id $ipbr_id committed-bandwidth 2000 committed-dcn-bandwidth 200 committed-sig-bandwidth 200 route-bandwidth 22000 ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type none
set ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME  phb-set EF"
			ipbr_id=$(($ipbr_id+1));
			fi
			done;
		done;
#echo "delete ipro ipbr-id $ipbr_id ip-address $LOCAL_IP owner $OWNER_NAME iface $IFACE_NAME" 	
#echo "delete ipbr ipbr-id $ipbr_id"
echo "commit transaction
quit"