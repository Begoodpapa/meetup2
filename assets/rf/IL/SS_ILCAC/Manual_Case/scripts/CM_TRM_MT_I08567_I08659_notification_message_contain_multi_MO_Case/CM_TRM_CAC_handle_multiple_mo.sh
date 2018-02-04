#/bin/sh

OWNER_NAME=/QNUP-0
IFACE_NAME=ethtest20
NUM_TWO_OPERATE=185
NUM_THREE_OPERATE=157
monster_log_path=/srv/Log/

#-----------------two_operator-----------------------
create_add_set_transaction_script () {
comm_bw=$1
dcn_bw=$2
sig_bw=$3
route_bw=$4
phb=$5
ipbr_id=100
echo "#!/opt/nokiasiemens/bin/fsclish -f
set cli built-in echo-cmd on
start transaction"

for((i=10;i<=19;i++));
	do
  	for((j=100;j<=109;j++));
  	do

  		if [[ $ipbr_id -lt 185 ]];then 
				echo "
add ipbr ipbr-id $ipbr_id committed-bandwidth 1000 committed-dcn-bandwidth 100 committed-sig-bandwidth 100 route-bandwidth 1100 ipbr-name test-$ipbr_id ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type realQueue
add ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME 
set ipbr ipbr-id $ipbr_id committed-bandwidth $comm_bw committed-dcn-bandwidth $dcn_bw committed-sig-bandwidth $sig_bw route-bandwidth $route ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type none
set ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME  phb-set $phb"				
			ipbr_id=$(($ipbr_id+1));
			fi
			done;
		done;
#echo "delete ipro ipbr-id $ipbr_id ip-address $LOCAL_IP owner $OWNER_NAME iface $IFACE_NAME" 	
#echo "delete ipbr ipbr-id $ipbr_id"
echo "commit transaction
quit"
}

create_delete_add_transaction_script () {
comm_bw=$1
dcn_bw=$2
sig_bw=$3
route_bw=$4
phb=$5
ipbr_id=100
echo "#!/opt/nokiasiemens/bin/fsclish -f
set cli built-in echo-cmd on
start transaction"

for((i=10;i<=19;i++));
	do
  	for((j=100;j<=109;j++));
  	do

  		if [[ $ipbr_id -lt 185 ]];then 
				echo "
delete ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME
delete ipbr ipbr-id $ipbr_id 
add ipbr ipbr-id $ipbr_id committed-bandwidth $comm_bw committed-dcn-bandwidth $dcn_bw committed-sig-bandwidth $sig_bw route-bandwidth $route_bw ipbr-name test-$ipbr_id ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type realQueue
add ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME  phb-set $phb"				
			ipbr_id=$(($ipbr_id+1));
			fi
			done;
		done;
echo "commit transaction
quit"
}

create_set_set_transaction_script () {
comm_bw=$1
dcn_bw=$2
sig_bw=$3
route_bw=$4
phb=$5
ipbr_id=100
echo "#!/opt/nokiasiemens/bin/fsclish -f
set cli built-in echo-cmd on
start transaction"

for((i=10;i<=19;i++));
	do
  	for((j=100;j<=109;j++));
  	do

  		if [[ $ipbr_id -lt 185 ]];then 
				echo "
set ipbr ipbr-id $ipbr_id 
set ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME 
set ipbr ipbr-id $ipbr_id committed-bandwidth $comm_bw committed-dcn-bandwidth $dcn_bw committed-sig-bandwidth $sig_bw route-bandwidth $route ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type none
set ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME  phb-set $phb"				
			ipbr_id=$(($ipbr_id+1));
			fi
			done;
		done;
echo "commit transaction
quit"
}

create_set_delete_transaction_script () {
comm_bw=$1
dcn_bw=$2
sig_bw=$3
route_bw=$4
phb=$5
ipbr_id=100
echo "#!/opt/nokiasiemens/bin/fsclish -f
set cli built-in echo-cmd on
start transaction"

for((i=10;i<=19;i++));
	do
  	for((j=100;j<=109;j++));
  	do

  		if [[ $ipbr_id -lt 185 ]];then 
				echo " 
set ipbr ipbr-id $ipbr_id committed-bandwidth $comm_bw committed-dcn-bandwidth $dcn_bw committed-sig-bandwidth $sig_bw route-bandwidth $route ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type none
set ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME  phb-set $phb"
delete ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME
delete ipbr ipbr_id $ipbr_id				
			ipbr_id=$(($ipbr_id+1));
			fi
			done;
		done;
echo "commit transaction
quit"
}

create_add_delete_transaction_script () {
comm_bw=$1
dcn_bw=$2
sig_bw=$3
route_bw=$4
phb=$5
ipbr_id=100
echo "#!/opt/nokiasiemens/bin/fsclish -f
set cli built-in echo-cmd on
start transaction"

for((i=10;i<=19;i++));
	do
  	for((j=100;j<=109;j++));
  	do

  		if [[ $ipbr_id -lt 185 ]];then 
				echo " 
add ipbr ipbr-id $ipbr_id committed-bandwidth $comm_bw committed-dcn-bandwidth $dcn_bw committed-sig-bandwidth $sig_bw route-bandwidth $route_bw ipbr-name test-$ipbr_id ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type realQueue
add ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME  phb-set $phb"
delete ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME
delete ipbr ipbr_id $ipbr_id				
			ipbr_id=$(($ipbr_id+1));
			fi
			done;
		done;
echo "commit transaction
quit"
}

add_set_ipbr_ipro(){
				
				comm_bw=2000
				dcn_bw=200
				sig_bw=200
				route_bw=22000 
				phb=EF

				echo "now create scli script start"
				create_add_set_transaction_script $comm_bw $dcn_bw $sig_bw $route_bw $phb>add_set.scli
				echo "now create scli script done"
				chmod +x ./*
				
				monster -f 0x6DD -c "SR:NOT(NUM=1,2)" > /srv/Log/add_set.log&
				
				./add_set.scli|grep "Failed commands   :"|awk '{if($4!=0) print "test failed"}'
				
				
				pkill monster
				pkill monster

					check_ipbr_ipro_info 100 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
					check_ipbr_ipro_info 110 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
					check_ipbr_ipro_info 184 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
}

delete_add_ipbr_ipro () {
				comm_bw=1000
				dcn_bw=100
				sig_bw=100
				route_bw=11000
				phb=EF,AF4

				echo "now create scli script start"
				create_delete_add_transaction_script $comm_bw $dcn_bw $sig_bw $route_bw $phb>delete_add.scli
				echo "now create scli script done"
				chmod +x ./*				
				monster -f 0x6DD -c "SR:NOT(NUM=1,2)" > /srv/Log/delete_add.log&
				
				./delete_add.scli|grep "Failed commands   :"|awk '{if($4!=0) print "test failed"}'
				
				
				pkill monster
				pkill monster
				#ipbr_id_list=(100,150,184)
				#len=${#ipbr_id_list[*]}
				#for((index=0;index<$len;index++))
				#do
					#check_ipbr_ipro_info $ipbr_id_list[$index] $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
				#done
				
					check_ipbr_ipro_info 100 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
					check_ipbr_ipro_info 110 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
					check_ipbr_ipro_info 184 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
}

set_set_ipbr_ipro () {
				comm_bw=2000
				dcn_bw=200
				sig_bw=200
				route_bw=22000
				phb=EF,AF4,AF3

				echo "now create scli script start"
				create_set_set_transaction_script $comm_bw $dcn_bw $sig_bw $route_bw $phb>set_set.scli
				echo "now create scli script done"
				chmod +x ./*				
				monster -f 0x6DD -c "SR:NOT(NUM=1,2)" > /srv/Log/set_set.log&
				
				./set_set.scli|grep "Failed commands   :"|awk '{if($4!=0) print "test failed"}'
				
				
				pkill monster
				pkill monster
				#ipbr_id_list=(100,150,184)
				#len=${#ipbr_id_list[*]}
				#for((index=0;index<$len;index++))
				#do
				#	check_ipbr_ipro_info $ipbr_id_list[$index] $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
				#done
				check_ipbr_ipro_info 100 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
				check_ipbr_ipro_info 110 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
				check_ipbr_ipro_info 184 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
}

set_delete_ipbr_ipro () {
				comm_bw=2000
				dcn_bw=200
				sig_bw=200
				route_bw=22000
				phb=EF

				echo "now create scli script start"
				create_set_delete_transaction_script $comm_bw $dcn_bw $sig_bw $route_bw $phb>set_delete.scli
				echo "now create scli script done"
				chmod +x ./*				
				monster -f 0x6DD -c "SR:NOT(NUM=1,2)" > /srv/Log/set_delete.log&
				
				./set_delete.scli|grep "Failed commands   :"|awk '{if($4!=0) print "test failed"}'
				
				
				pkill monster
				pkill monster
				#ipbr_id_list=(100,150,184)
				#len=${#ipbr_id_list[*]}
				#for((index=0;index<$len;index++))
				#do
					#check_ipbr_ipro_info $ipbr_id_list[$index] $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
				#done
					check_ipbr_ipro_no_exist_info 100 
					check_ipbr_ipro_no_exist_info 110 
					check_ipbr_ipro_no_exist_info 184 
}

add_delete_ipbr_ipro () {
				comm_bw=1000
				dcn_bw=100
				sig_bw=100
				route_bw=11000
				phb=EF,AF4

				echo "now create scli script start"
				create_add_delete_transaction_script $comm_bw $dcn_bw $sig_bw $route_bw $phb>add_delete.scli
				echo "now create scli script done"
				chmod +x ./*				
				monster -f 0x6DD -c "SR:NOT(NUM=1,2)" > /srv/Log/add_delete.log&
				
				./add_delete.scli|grep "Failed commands   :"|awk '{if($4!=0) print "test failed"}'
				
				
				pkill monster
				pkill monster
				#ipbr_id_list=(100,150,184)
				#len=${#ipbr_id_list[*]}
				#for((index=0;index<$len;index++))
				#do
					#check_ipbr_ipro_info $ipbr_id_list[$index] $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
				#done
				
					check_ipbr_ipro_no_exist_info 100 
					check_ipbr_ipro_no_exist_info 110 
					check_ipbr_ipro_no_exist_info 184 
}

run_all_two_operation () {
						add_set_ipbr_ipro
            delete_add_ipbr_ipro
            set_set_ipbr_ipro
            set_delete_ipbr_ipro
            add_delete_ipbr_ipro
 }           

check_ipbr_ipro_info () {
				ipbr_index=$1
				comm_bw=$2
				dcn_bw=$3
				sig_bw=$4
				route_bw=$5
				phb=$6

				#phb_diff_value=`iltrmcli -C -m|grep 'Different:'|awk '{if($2==0) print 'success'}'` 
				#dsp_diff_value=`iltrmcli -C -m|grep 'Different:'|awk '{print $3}'`
				#ipbr_diff_value=`iltrmcli -C -m|grep 'Different:'|awk '{print $4}'`
				#ipro_diff_value=`iltrmcli -C -m|grep 'Different:'|awk '{print $5}'`
				iltrmcli -C -m|grep 'Different:'|awk '{if($2==0 && $3==0 && $4==0 && $5==0) print"test pass"}'
				iltrmcli -C -m|grep 'Different:'|awk '{if($2!=0 || $3!=0 || $4!=0 || $5!=0) print"test failed"}'
				fsclish -c "show ipbr ipbr-id $ipbr_index" |grep 'Committed BW:'|awk '{if($3!=$comm_bw) print"test failed"}'
				fsclish -c "show ipbr ipbr-id $ipbr_index" |grep 'Committed DCN BW:'|awk '{if($4!=$dcn_bw) print"test failed"}'
				fsclish -c "show ipbr ipbr-id $ipbr_index" |grep 'Committed signaling BW:'|awk '{if($4!=$sig_bw) print"test failed"}'
				fsclish -c "show ipbr ipbr-id $ipbr_index" |grep 'Route BW:'|awk '{if($3!=$route_bw) print"test failed"}'
				fsclish -c "show ipro ipbr-id $ipbr_index" |grep 'ethtest20 '|awk '{if($5!=$phb) print"test failed"}'
}

check_ipbr_ipro_no_exist_info () {


				#phb_diff_value=`iltrmcli -C -m|grep 'Different:'|awk '{if($2==0) print 'success'}'` 
				#dsp_diff_value=`iltrmcli -C -m|grep 'Different:'|awk '{print $3}'`
				#ipbr_diff_value=`iltrmcli -C -m|grep 'Different:'|awk '{print $4}'`
				#ipro_diff_value=`iltrmcli -C -m|grep 'Different:'|awk '{print $5}'`
				iltrmcli -C -m|grep 'Different:'|awk '{if($2==0 && $3==0 && $4==0 && $5==0) print"test pass"}'
				iltrmcli -C -m|grep 'Different:'|awk '{if($2!=0 || $3!=0 || $4!=0 || $5!=0) print"test failed"}'
				iltrmcli -S -i$ipbr_index |grep 'not exist'|awk '{if($5=="exist.") print"test pass"}'
				fsclish -c "show ipbr ipbr-id 4094" 2>&1 |grep "not exist"|awk '{if($7=="exist.") print"test pass"}'
}
#-----------------three_operator-----------------------
create_add_set_delete_transaction_script () {
comm_bw=$1
dcn_bw=$2
sig_bw=$3
route_bw=$4
phb=$5
ipbr_id=100
echo "#!/opt/nokiasiemens/bin/fsclish -f
set cli built-in echo-cmd on
start transaction"

for((i=10;i<=19;i++));
	do
  	for((j=100;j<=109;j++));
  	do

  		if [[ $ipbr_id -lt 157 ]];then 
				echo "
add ipbr ipbr-id $ipbr_id committed-bandwidth 1000 committed-dcn-bandwidth 100 committed-sig-bandwidth 100 route-bandwidth 1100 ipbr-name test-$ipbr_id ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type realQueue
add ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME 
set ipbr ipbr-id $ipbr_id committed-bandwidth $comm_bw committed-dcn-bandwidth $dcn_bw committed-sig-bandwidth $sig_bw route-bandwidth $route ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type none
set ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME  phb-set $phb"
delete ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME
delete ipbr ipbr_id $ipbr_id
				
			ipbr_id=$(($ipbr_id+1));
			fi
			done;
		done;
echo "commit transaction
quit"
}

create_delete_add_set_transaction_script () {
comm_bw=$1
dcn_bw=$2
sig_bw=$3
route_bw=$4
phb=$5
ipbr_id=100
echo "#!/opt/nokiasiemens/bin/fsclish -f
set cli built-in echo-cmd on
start transaction"

for((i=10;i<=19;i++));
	do
  	for((j=100;j<=109;j++));
  	do

  		if [[ $ipbr_id -lt 157 ]];then 
				echo "
delete ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME
delete ipbr ipbr-id $ipbr_id 
add ipbr ipbr-id $ipbr_id committed-bandwidth 1000 committed-dcn-bandwidth 50 committed-sig-bandwidth 50 route-bandwidth 5000 ipbr-name test-$ipbr_id
add ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME"
set ipbr ipbr-id $ipbr_id committed-bandwidth $comm_bw committed-dcn-bandwidth $dcn_bw committed-sig-bandwidth $sig_bw route-bandwidth $route ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type none
set ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME  phb-set $phb"				
			ipbr_id=$(($ipbr_id+1));
			fi
			done;
		done;
echo "commit transaction
quit"
}

create_set_set_delete_transaction_script () {
comm_bw=$1
dcn_bw=$2
sig_bw=$3
route_bw=$4
phb=$5
ipbr_id=100
echo "#!/opt/nokiasiemens/bin/fsclish -f
set cli built-in echo-cmd on
start transaction"

for((i=10;i<=19;i++));
	do
  	for((j=100;j<=109;j++));
  	do

  		if [[ $ipbr_id -lt 157 ]];then 
				echo "
set ipbr ipbr-id $ipbr_id 
set ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME 
set ipbr ipbr-id $ipbr_id committed-bandwidth $comm_bw committed-dcn-bandwidth $dcn_bw committed-sig-bandwidth $sig_bw route-bandwidth $route ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type none
set ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME  phb-set $phb"
delete ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME
delete ipbr ipbr-id $ipbr_id				
			ipbr_id=$(($ipbr_id+1));
			fi
			done;
		done;
echo "commit transaction
quit"
}

create_set_delete_add_transaction_script () {
comm_bw=$1
dcn_bw=$2
sig_bw=$3
route_bw=$4
phb=$5
ipbr_id=100
echo "#!/opt/nokiasiemens/bin/fsclish -f
set cli built-in echo-cmd on
start transaction"

for((i=10;i<=19;i++));
	do
  	for((j=100;j<=109;j++));
  	do

  		if [[ $ipbr_id -lt 157 ]];then 
				echo " 
set ipbr ipbr-id $ipbr_id committed-bandwidth 500 committed-dcn-bandwidth 50 committed-sig-bandwidth 50 route-bandwidth 5000 ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type none
set ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME"
delete ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME
delete ipbr ipbr_id $ipbr_id	
add ipbr ipbr-id $ipbr_id committed-bandwidth $comm_bw committed-dcn-bandwidth $dcn_bw committed-sig-bandwidth $sig_bw route-bandwidth $route_bw ipbr-name test-$ipbr_id ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type realQueue
add ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME  phb-set $phb"
			
			ipbr_id=$(($ipbr_id+1));
			fi
			done;
		done;
echo "commit transaction
quit"
}

create_add_delete_add_transaction_script () {
comm_bw=$1
dcn_bw=$2
sig_bw=$3
route_bw=$4
phb=$5
ipbr_id=100
echo "#!/opt/nokiasiemens/bin/fsclish -f
set cli built-in echo-cmd on
start transaction"

for((i=10;i<=19;i++));
	do
  	for((j=100;j<=109;j++));
  	do

  		if [[ $ipbr_id -lt 157 ]];then 
				echo " 
add ipbr ipbr-id $ipbr_id committed-bandwidth 100 committed-dcn-bandwidth 5 committed-sig-bandwidth 5 route-bandwidth 200 ipbr-name test-$ipbr_id ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type realQueue
add ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME"
delete ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME
delete ipbr ipbr_id $ipbr_id
add ipbr ipbr-id $ipbr_id committed-bandwidth $comm_bw committed-dcn-bandwidth $dcn_bw committed-sig-bandwidth $sig_bw route-bandwidth $route_bw ipbr-name test-$ipbr_id ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type realQueue
add ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME  phb-set $phb"
				
			ipbr_id=$(($ipbr_id+1));
			fi
			done;
		done;
echo "commit transaction
quit"
}

create_add_set_set_transaction_script () {
comm_bw=$1
dcn_bw=$2
sig_bw=$3
route_bw=$4
phb=$5
ipbr_id=100
echo "#!/opt/nokiasiemens/bin/fsclish -f
set cli built-in echo-cmd on
start transaction"

for((i=10;i<=19;i++));
	do
  	for((j=100;j<=109;j++));
  	do

  		if [[ $ipbr_id -lt 157 ]];then 
				echo " 
add ipbr ipbr-id $ipbr_id committed-bandwidth 100 committed-dcn-bandwidth 5 committed-sig-bandwidth 5 route-bandwidth 200 ipbr-name test-$ipbr_id ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type realQueue
add ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME"
set ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME
set ipbr ipbr_id $ipbr_id
set ipbr ipbr-id $ipbr_id committed-bandwidth $comm_bw committed-dcn-bandwidth $dcn_bw committed-sig-bandwidth $sig_bw route-bandwidth $route_bw ipbr-name test-$ipbr_id ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type realQueue
set ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME  phb-set $phb"
 
				
			ipbr_id=$(($ipbr_id+1));
			fi
			done;
		done;
echo "commit transaction
quit"
}

create_delete_add_delete_transaction_script () {
comm_bw=$1
dcn_bw=$2
sig_bw=$3
route_bw=$4
phb=$5
ipbr_id=100
echo "#!/opt/nokiasiemens/bin/fsclish -f
set cli built-in echo-cmd on
start transaction"

for((i=10;i<=19;i++));
	do
  	for((j=100;j<=109;j++));
  	do

  		if [[ $ipbr_id -lt 157 ]];then 
				echo " 
delete ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME
delete ipbr ipbr_id $ipbr_id
add ipbr ipbr-id $ipbr_id committed-bandwidth 100 committed-dcn-bandwidth 5 committed-sig-bandwidth 5 route-bandwidth 200 ipbr-name test-$ipbr_id ifc-nrtdch E-RED ifc-nrthsdpa E-RED scheduler-type realQueue
add ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME"
delete ipro ipbr-id $ipbr_id ip-address 191.251.10.$i owner $OWNER_NAME iface $IFACE_NAME
delete ipbr ipbr_id $ipbr_id
			ipbr_id=$(($ipbr_id+1));
			fi
			done;
		done;
echo "commit transaction
quit"
}
#------------------
add_set_delete_ipbr_ipro(){
				
				comm_bw=2000
				dcn_bw=200
				sig_bw=200
				route_bw=22000
				phb=EF

				echo "now create scli script start"
				create_add_set_delete_transaction_script $comm_bw $dcn_bw $sig_bw $route_bw $phb>add_set_delete.scli
				echo "now create scli script done"
				chmod +x ./*
				
				monster -f 0x6DD -c "SR:NOT(NUM=1,2)" > /srv/Log/add_set_delete.log&
				
				./add_set_delete.scli|grep "Failed commands   :"|awk '{if($4!=0) print "test failed"}'
				
				
				pkill monster
				pkill monster

					check_ipbr_ipro_info 100 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
					check_ipbr_ipro_info 110 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
					check_ipbr_ipro_info 156 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
}
delete_add_set_ipbr_ipro () {
				comm_bw=1000
				dcn_bw=100
				sig_bw=100
				route_bw=11000
				phb=EF,AF4

				echo "now create scli script start"
				create_delete_add_set_transaction_script $comm_bw $dcn_bw $sig_bw $route_bw $phb>delete_add_set.scli
				echo "now create scli script done"
				chmod +x ./*				
				monster -f 0x6DD -c "SR:NOT(NUM=1,2)" > /srv/Log/delete_add_set.log&
				
				./delete_add_set.scli|grep "Failed commands   :"|awk '{if($4!=0) print "test failed"}'
				
				
				pkill monster
				pkill monster
				#ipbr_id_list=(100,150,184)
				#len=${#ipbr_id_list[*]}
				#for((index=0;index<$len;index++))
				#do
					#check_ipbr_ipro_info $ipbr_id_list[$index] $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
				#done
				
					check_ipbr_ipro_info 100 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
					check_ipbr_ipro_info 110 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
					check_ipbr_ipro_info 156 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
}

set_set_delete_ipbr_ipro () {
				comm_bw=2000
				dcn_bw=200
				sig_bw=200
				route_bw=22000
				phb=EF,AF4,AF3

				echo "now create scli script start"
				create_set_set_delete_transaction_script $comm_bw $dcn_bw $sig_bw $route_bw $phb>set_set_delete.scli
				echo "now create scli script done"
				chmod +x ./*				
				monster -f 0x6DD -c "SR:NOT(NUM=1,2)" > /srv/Log/set_set_delete.log&
				
				./set_set_delete.scli|grep "Failed commands   :"|awk '{if($4!=0) print "test failed"}'
				
				
				pkill monster
				pkill monster

				check_ipbr_ipro_no_exist_info 100
				check_ipbr_ipro_no_exist_info 110
				check_ipbr_ipro_no_exist_info 156
}

set_delete_add_ipbr_ipro () {
				comm_bw=2000
				dcn_bw=200
				sig_bw=200
				route_bw=22000
				phb=EF

				echo "now create scli script start"
				create_set_delete_add_transaction_script $comm_bw $dcn_bw $sig_bw $route_bw $phb>set_delete_add.scli
				echo "now create scli script done"
				chmod +x ./*				
				monster -f 0x6DD -c "SR:NOT(NUM=1,2)" > /srv/Log/set_delete_add.log&
				
				./set_delete_add.scli|grep "Failed commands   :"|awk '{if($4!=0) print "test failed"}'
				
				
				pkill monster
				pkill monster

					check_ipbr_ipro_info 100 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
					check_ipbr_ipro_info 110 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
					check_ipbr_ipro_info 156 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
}

add_delete_add_ipbr_ipro () {
				comm_bw=1000
				dcn_bw=100
				sig_bw=100
				route_bw=11000
				phb=EF,AF4

				echo "now create scli script start"
				create_add_delete_add_transaction_script $comm_bw $dcn_bw $sig_bw $route_bw $phb>add_delete_add.scli
				echo "now create scli script done"
				chmod +x ./*				
				monster -f 0x6DD -c "SR:NOT(NUM=1,2)" > /srv/Log/add_delete_add.log&
				
				./add_delete_add.scli|grep "Failed commands   :"|awk '{if($4!=0) print "test failed"}'
				
				
				pkill monster
				pkill monster
				check_ipbr_ipro_info 100 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
				check_ipbr_ipro_info 110 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
				check_ipbr_ipro_info 156 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
}

add_set_set_ipbr_ipro () {
				comm_bw=1000
				dcn_bw=100
				sig_bw=100
				route_bw=11000
				phb=EF,AF4

				echo "now create scli script start"
				create_add_set_set_transaction_script $comm_bw $dcn_bw $sig_bw $route_bw $phb>add_set_set.scli
				echo "now create scli script done"
				chmod +x ./*				
				monster -f 0x6DD -c "SR:NOT(NUM=1,2)" > /srv/Log/add_set_set.log&
				
				./add_set_set.scli|grep "Failed commands   :"|awk '{if($4!=0) print "test failed"}'
				
				
				pkill monster
				pkill monster
				check_ipbr_ipro_info 100 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
				check_ipbr_ipro_info 110 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
				check_ipbr_ipro_info 156 $comm_bw $dcn_bw $sig_bw $route_bw $phb_set
}

delete_add_delete_ipbr_ipro () {
				comm_bw=1000
				dcn_bw=100
				sig_bw=100
				route_bw=11000
				phb=EF,AF4

				echo "now create scli script start"
				create_delete_add_delete_transaction_script $comm_bw $dcn_bw $sig_bw $route_bw $phb>delete_add_delete.scli
				echo "now create scli script done"
				chmod +x ./*				
				monster -f 0x6DD -c "SR:NOT(NUM=1,2)" > /srv/Log/delete_add_delete.log&
				
				./delete_add_delete.scli|grep "Failed commands   :"|awk '{if($4!=0) print "test failed"}'
				
				
				pkill monster
				pkill monster
				check_ipbr_ipro_no_exist_info 100
				check_ipbr_ipro_no_exist_info 110
				check_ipbr_ipro_no_exist_info 156
}
 
run_all_three_operation () {
						add_set_delete_ipbr_ipro
            add_delete_add_ipbr_ipro
            set_delete_add_ipbr_ipro
            delet_add_set_ipbr_ipro
            set_set_delete_ipbr_ipro
            add_set_set_ipbr_ipro
            delete_add_delete_ipbr_ipro

}
				
# ---------------------- the parameters for test result ---------------------------
test_file_path=/opt/nokiasiemens/testutils/sko_test_xml/
monster_log_path=/srv/Log/

#-----------------Main---------------
# make CFPU-0 is WORK
is_work=`fshascli -s /CFPU-0/QNOMUServer-0|grep "role(ACTIVE)"|wc -l`
if [[ "$is_work" == "0" ]];then
	echo "Make Sure /CFPU-0/QNOMUServer-0 Is WORK"
	fshascli -wnF /CFPU-0/QNOMUServer-0
	sleep 3
fi
 	
three_operates_in_one_message () {
				echo "Please select test scenario and select test from 1 to 7 or runall"
							
				echo "1) add_set_delete_ipbr_ipro"
				echo "2) add delete add ipbr ipro"
				echo "3) set delete add ipbr ipro"
				echo "4) delet add set ipbr ipro"
				echo "5) set set delete ipbr ipro"
				echo "6) add set set ipbr ipro"
				echo "7) delete add delete ipbr ipro"
				echo "9) run all three operates test auto scenerios"
				echo "0) quite"
				read sel
				case $sel in
						1)
            add_set_delete_ipbr_ipro
            ;;
            2)
            add_delete_add_ipbr_ipro
            ;;
            3)
            set_delete_add_ipbr_ipro
            ;;
            4)
            delet_add_set_ipbr_ipro
            ;;
            5)
            set_set_delete_ipbr_ipro
            ;;
            6)
            add_set_set_ipbr_ipro
            ;; 
						7)
            delete_add_delete_ipbr_ipro
            ;; 
            9)
            run_all_three_operation_script
            ;;
            0)
            exit 0
            ;;
            *)
            echo -e "\e[31;5m----------error choice----------\e[m"
            exit 1
            ;;
        esac
}	

two_operates_in_one_message () {
				echo "Please select test scenario and select test from 1 to 5 or runall"
				
				echo "1) add set ipbr ipro"
				echo "2) delete add ipbr ipro"
				echo "3) set set ipbr ipro"
				echo "4) set delete ipbr ipro"
				echo "5) add delete ipbr ipro"
				echo "6) run all two operates test auto scenerios"
				echo "0) quite"
				read sel
				case $sel in
						1)
            add_set_ipbr_ipro
            ;;
            2)
            delete_add_ipbr_ipro
            ;;
            3)
            set_set_ipbr_ipro
            ;;
            4)
            set_delete_ipbr_ipro
            ;;
            5)
            add_delete_ipbr_ipro
            ;;
            6)
            run_all_two_operation
            ;;
            0)
            exit 0
            ;;
            *)
            echo -e "\e[31;5m----------error choice----------\e[m"
            exit 1
            ;;
        esac
}

echo "Please select test scenario"

echo "1) run all two operates test auto scenerios"
echo "2) run all three operates test auto scenerios"
echo "3) prepare test ENV"
echo "0) quite"
read sel
case $sel in
     1)
     run_all_two_operation
     ;;
     2)
     run_all_three_operation 
     ;;
     3)
     prepare_test_ENV
     ;;
     0)
     exit 0
     ;;
     *)
     echo -e "\e[31;5m----------error choice----------\e[m"
     exit 1
     ;;
 esac	
 