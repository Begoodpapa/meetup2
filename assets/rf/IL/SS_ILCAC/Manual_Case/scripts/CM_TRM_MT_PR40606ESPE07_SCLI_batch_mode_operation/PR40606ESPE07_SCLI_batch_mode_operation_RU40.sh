 #!/bin/bash
script_prepare()
{
   if [ $HW_PLATFORM = "BCN" ]
   then
      iface=lo
      owner=/QNUP-0
   elif [ $HW_PLATFORM = "FTLB" ]
   then
      iface=eth0
      owner=/CLA-0
   fi

##########################replace iface owner IP######################
   ip_array=(`fsclish -c "show networking address owner $owner iface $iface" | grep address | awk -F"[:/]" '{print $2}'`)
   ip_num=${#ip_array[@]}
   if [ "$ip_num" = "0" ]
   then
      echo "No ip configured on interface $iface of $owner"
      exit
   fi

   ip_address=${ip_array[0]}
   sed -i "s/<ip_address>/${ip_address}/g" PR40606ESPE07_*.conf
   sed -i "s/<iface>/${iface}/g" PR40606ESPE07_*.conf
   sed -i "s#<owner>#${owner}#g" PR40606ESPE07_*.conf
}

##########################Prepare resource, IP Plan configuration of CI should be done########################
resource_prepare()
{
   prepare_ipro_info=`fsclish -c "show networking ipro ipbr-id 1 iface $iface owner $owner ip-address $ip_address" 2>&1 | grep "Error Info" | awk -F"[:]" '{print $2}'`
   if [ "$prepare_ipro_info" != "IPRO does not exist." ]
   then
      echo "Prepare fail: ipro exists with ipbr-id 1 iface $iface owner $owner ip-address $ip_address, remove it before test."
      exit
   fi

   prepare_ipbr_info=`fsclish -c "add networking ipbr ipbr-id 2002 committed-bandwidth 0 committed-dcn-bandwidth 0 committed-sig-bandwidth 0 route-bandwidth 0 ipbr-name ipbr2002" 2>&1`
   if [ "$prepare_ipbr_info" != "Add IPBR successfully." ] 
   then 
      echo "Prepare fail: $prepare_ipbr_info"
      exit
   fi
}

##########################
case_add()
{
   ipbr_add_err="add networking ipbr ipbr-id 2000 committed-dcn-bandwidth 0 committed-sig-bandwidth 1 committed-bandwidth 0 route-bandwidth 0 ipbr-name ipbr2000,255"
   err_result=`fsclish -f PR40606ESPE07_add_IPBR_failure.conf 2>&1 | grep -E "Failed commands|{cmd, result}"`
   err_num=`echo $err_result | awk -F"[:=]" '{print $2}'`
   err_info=`echo $err_result | awk -F"[{}]" '{print $4}'`
   
   if [ $err_num -ne 1 ]
   then
      echo "Casee failed: PR40606ESPE07_add_IPBR_failure, err_num is $err_num"
      exit
   fi

   if [ "$err_info" != "$ipbr_add_err" ]
   then
      echo "Case failed: PR40606ESPE07_add_IPBR_failure, $err_info"
      exit
   fi

   check_ipro=`fsclish -c "show networking ipro ipbr-id 1 iface $iface owner $owner ip-address $ip_address" 2>&1 | grep "Error Info" | awk -F"[:]" '{print $2}'`
   if [ "$check_ipro" != "IPRO does not exist." ]
   then
      echo "Case failed: PR40606ESPE07_add_IPBR_failure, $check_ipro"
      exit
   fi

   ipbr_info="IPBR does not exist."
   check_ipbr=`fsclish -c "show networking ipbr ipbr-id 2001" 2>&1 | grep "Error Info" | awk -F"[:]" '{print $2}'`
   if [ "$check_ipbr" != "$ipbr_info" ]
   then
      echo "Case failed: PR40606ESPE07_add_IPBR_failure, $check_ipbr"
      exit
   fi

   echo "Case pass: PR40606ESPE07_add_IPBR_failure" 
}
############################
case_delete()
{
   ipro_delete_err="delete networking ipro ipbr-id 2000 iface $iface owner $owner ip-address ${ip_address},255"
   err_result=`fsclish -f PR40606ESPE07_delete_IPRO_failure.conf 2>&1 | grep -E "Failed commands|{cmd, result}"`
   err_num=`echo $err_result | awk -F"[:=]" '{print $2}'`
   err_info=`echo $err_result | awk -F"[{}]" '{print $4}'`

   if [ $err_num -ne 1 ]
   then 
      echo "Case failed: PR40606ESPE07_add_IPRO_failure, err_num is $err_num"
      exit
   fi
   if [ "$err_info" != "$ipro_delete_err" ]
   then
      echo "Case failed: PR40606ESPE07_add_IPRO_failure, $err_info"
      exit
   fi

   ipbr_info="IPBR does not exist."
   check_ipbr=`fsclish -c "show networking ipbr ipbr-id 2000" 2>&1 | grep "Error Info" | awk -F"[:]" '{print $2}'`
   if [ "$check_ipbr" != "$ipbr_info" ]
   then
      echo "Case failed: PR40606ESPE07_delete_IPRO_failure, $check_ipbr"
      exit
   fi

   ipbr_info="IPBR does not exist."
   check_ipbr=`fsclish -c "show networking ipbr ipbr-id 2002" 2>&1 | grep "Error Info" | awk -F"[:]" '{print $2}'`
   if [ "$check_ipbr" = "$ipbr_info" ]
   then
      echo "Case failed: PR40606ESPE07_delete_IPRO_failure, $check_ipbr"
      exit
   fi


   echo "Case pass: PR40606ESPE07_delete_IPRO_failure"
}
###############################
case_show()
{
   fail_exe_num=`fsclish -f PR40606ESPE07_show.conf 2>&1 | grep "Failed commands" | awk -F"[:]" '{print $2}'`
   if [ $fail_exe_num -ne 0 ]
   then
      echo "Case failed: PR40606ESPE07_show, $fail_exe_num"
      exit
   fi

   ipbr_info="IPBR does not exist."
   check_ipbr=`fsclish -c "show networking ipbr ipbr-id 2002" 2>&1 | grep "Error Info" | awk -F"[:]" '{print $2}'`
   if [ "$check_ipbr" != "$ipbr_info" ]
   then
      echo "Case failed: PR40606ESPE07_show, $check_ipbr"
      exit
   fi

   echo "Case pass: PR40606ESPE07_show"
}


script_prepare
resource_prepare
case_add
case_delete
case_show
exit




