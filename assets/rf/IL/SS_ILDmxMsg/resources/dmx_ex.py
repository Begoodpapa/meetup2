from comm.communication import exceptions
from comm.communication import connections
from comm.communication.helper import *
from robot import utils
from robot import output 
from robot.libraries.BuiltIn import BuiltIn

import re

def get_dmxmsg_statistic():
    """This keyword is to get dmxmsg statistic info
    """

    cmd = 'cat /proc/dmxmsg/statistics'
    output = connections.execute_mml( cmd )

    statistic_list = CommonItem()

    re_item = '\s*[a-z\s.]+\s*(\d+)\s*'
    m = re.findall( re_item, output )

    if m is not None:
        statistic_list.discarded_msgs = m[9]
        statistic_list.discarded_sync_msgs_mismatch = m[10]
        statistic_list.discarded_sync_msgs_queue_full = m[11]
        statistic_list.discarded_reorder_msgs = m[13]
        statistic_list.discarded_timeout_sync_msgs = m[12]
        statistic_list.discarded_timeout_reorder_msgs = m[14]
        statistic_list.discarded_sync_msgs_unexpected = m[16]
    return statistic_list

def Get_Input_Sync_queue_size():
    cmd = 'cat /proc/dmxmsg/msg_queue_default_size '
    out = connections.execute_mml_without_check( cmd )
    return out.split( '\r\n' )[1]

def goto_node_and_run_keyword(node_addr, keyword, *args):
    BuiltIn().run_keyword("Switch Il Connection", node_addr)
    BuiltIn().run_keyword (keyword, *args)


def get_real_file_content(file):
    command = "cat '%s'" %(file)
          
    out = connections.execute_mml(command)
        
    return out.strip()


def Linux_Query_Logic_Address(log_addr):
    command = 'dmx_generic_stub query_logic_addr '+log_addr
    result = connections.execute_mml_without_check(command)
    addr_config_list = re.findall(':\s([0-9a-zx]+)', result)
    return addr_config_list
             

def reset_Logic_Address(addr_config_list):
    config_cmd = 'dmxcli2 -C '
    for i in addr_config_list:
        config_cmd = config_cmd + i + ','
    connections.execute_mml_without_check(config_cmd)

def Execute_Cli_Without_Check(cli_cmd):
    connections.execute_mml_without_check(cli_cmd)

def create_low_memory(disk_file):
    command = "free"
    output = connections.execute_mml_without_check(command)
    print output
    command = "free -g | grep Mem: |awk -F \" \" \'{print $4}\'"
    output = connections.execute_mml_without_check(command)
    memo_g = output.strip()
    print "create memory %s G" %memo_g
    mount_size = int(memo_g) + 1
    mount_size = str(mount_size)
    command = 'mkdir ' + disk_file    
    connections.execute_mml_without_check(command)
    command = 'mount -t tmpfs -o nosuid,mode=777,size=' + mount_size + 'G,rw tmpfs ' +  disk_file
    connections.execute_mml_without_check(command)
    command = 'cd ' + disk_file    
    connections.execute_mml_without_check(command)        

    command = 'dd if=/dev/zero of=emptyfile bs=1M count=' + memo_g + '000'
    output = connections.execute_mml_without_check(command)
    
    command = "free"
    output = connections.execute_mml_without_check(command)
    print output    
    command = "free -m | grep Mem: |awk -F \" \" \'{print $4}\'"
    output = connections.execute_mml_without_check(command)
    memo_m = output.strip()
    print "memo_m is: %s M" %memo_m
    cp_size = int(memo_m,10)
    cp_size = cp_size/2 - 10
    size = str(cp_size)
    print "write buffer %s M" %size

    command = 'dd if=/dev/zero of=occupyfile bs=1M count=' + size
    output = connections.execute_mml_without_check(command)    
    
    command = 'cd /root;'
    output = connections.execute_mml_without_check(command)
    command = 'free;ll ' + disk_file + "/*"
    output = connections.execute_mml_without_check(command)
    print output

def copy_occupied_buffer(disk_file):
    command = "cp " + disk_file + "/occupyfile /root/"
    output = connections.execute_mml_without_check(command)
    command = 'free'
    output = connections.execute_mml_without_check(command)
    print output
    
def clear_low_memory(disk_file):
    command = 'cd /root; umount ' + disk_file + '; rm -rf ' + disk_file +'/*; rm -rf /root/occupyfile'
    output = connections.execute_mml_without_check(command)
    command = 'free'
    output = connections.execute_mml_without_check(command)
    print output
    
def check_node_state_normal(node_name):
    command = 'fshascli -s /' + node_name
    output = connections.execute_mml_without_check(command)
    print output
    state_table = output.strip()
    match1 = re.findall( "(ENABLED)", state_table )
    match2 = re.findall( "(ACTIVE)", state_table )
    match3 = re.findall( "(INITIALIZING)", state_table )  
    if len(match1) > 0 and len(match2) > 0 and len(match3) == 0:
        return "sucessful"
    else:
        return "fail"   
    

def check_se_pid_tbl(se_pid_content, pid, flag):
   '''
   The valid se_pid_tbl should not contain duplicate items;  
   '''
   output=se_pid_content.splitlines()
   while output[0] == '':
      output.remove(output[0])
   
   pid_list=[]

   i = 3
   line_cnt = len(output)
   while i < line_cnt:
      item = output[i].split()[1]
      pid_list.append(item)
      i += 1

   print pid_list
   #get the pid count from the title line
   se_pid_cnt = int(output[0].split()[2], 10)
   line_cnt = len(pid_list)
   if (se_pid_cnt != line_cnt) :
      return "error: pid cnt mismatch"

   #check there are no duplicate pid items
   i = 0
   while i < line_cnt:
      cnt = pid_list.count(pid_list[i])
      if cnt > 1:
         return "error : duplicate pid found"
      i += 1
   
   if (flag == "dont care"):
      return "success"

   print pid
   
   if (flag == "exist") :
      cnt=pid_list.count(pid)
      if (cnt != 1):
         return "error : pid not found"

   if (flag == "not exist") :
      cnt=pid_list.count(pid)
      if (cnt != 0):
         return "error : pid was found, but is should not be found"

   return "success"
   
   
def check_node_up_by_mac():
    command = 'cat /proc/dmxmsg/mac_addr_tbl'
    output = connections.execute_mml_without_check(command)
    mac_table = output.strip()
    match1 = re.findall( "unavailable", mac_table)
    
    if len(match1) == 0:   
        return "sucessful"  #no unavailable node 
    else:
        return "fail"   