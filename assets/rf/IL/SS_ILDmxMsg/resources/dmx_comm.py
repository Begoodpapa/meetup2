from comm.communication import exceptions
from comm.communication import connections
from comm.communication.helper import *
import re, time
from robot import utils
from robot import output

def Generic_Send_Msg(selffamily, target, number='', length='', sequence ='', interval ='',
                     back_groud = '', quite_flag = ''):
    command = "dmx_generic_stub send " + selffamily + " " + target
    if number != '':
        command += " -n " + number
    if length != '':
        command += " -l " + length
    if sequence != '':
        command += " -s " + sequence
    if interval != '':
        command += " -i " + interval
    if quite_flag != '':
        command += " -q "
    if back_groud != '':
        command += "&"
    out = connections.execute_mml_without_check(command)
    return out

def Get_Log_Content(log):
    command = 'cat ' + log
    out = connections.execute_mml_without_check(command)
    return out

def Generic_Send_Msg_With_Priority(selffamily, target, number='', priority = '', length='', sequence ='', interval ='',
                     back_groud = '', quite_flag = ''):
    command = "dmx_generic_stub send " + selffamily + " " + target
    if number != '':
        command += " -n " + number
    if length != '':
        command += " -l " + length
    if sequence != '':
        command += " -s " + sequence
    if interval != '':
        command += " -i " + interval
    if quite_flag != '':
        command += " -q "
    if priority != '':
    		command += " -p " + priority
    if back_groud != '':
        command += "&"
    out = connections.execute_mml_without_check(command)
    return out

def Get_Last_Line_Number(log_file, pid):

    cmd = "kill -USR1 %s" %pid
    connections.execute_mml( cmd )
    time.sleep(0.5)

    cmd = "cat %s" %log_file
    logcontent = connections.execute_mml( cmd )

    re_item = '(?<=Totally have received )\d*'
    numlist = re.findall( re_item, logcontent )

    if numlist is not None:
        output = numlist[len(numlist)-1]
    return output

def Get_Last_Stat_Size(log_file, pid):
    cmd = "kill -USR1 %s" %pid
    connections.execute_mml( cmd )
    time.sleep(0.5)

    cmd = "kill -INT %s" %pid
    connections.execute_mml( cmd )
    time.sleep(0.5)

    cmd = "cat %s" %log_file
    logcontent = connections.execute_mml( cmd )
    print "logcontent is: %s" %logcontent
    re_item = '(?<=Buffers in queue:)\d*'

    queue_buffer = re.findall( re_item, logcontent )

    if queue_buffer is not None:
        output = queue_buffer[len(queue_buffer)-1]
    return output

def Get_Last_Queue_Size(log_file, pid):
    cmd = "kill -USR1 %s" %pid
    connections.execute_mml( cmd )
    time.sleep(0.5)

    cmd = "kill -USR2 %s" %pid
    connections.execute_mml( cmd )
    time.sleep(0.5)

    cmd = "cat %s" %log_file
    logcontent = connections.execute_mml( cmd )
    print "logcontent is: %s" %logcontent
    re_item = '(?<=Buffers in queue:)\d*'

    queue_buffer = re.findall( re_item, logcontent )

    if queue_buffer is not None:
        output = queue_buffer[len(queue_buffer)-1]
    return output

def Get_Last_Queue_Limit(log_file, pid):

    cmd = "kill -USR2 %s" %pid
    connections.execute_mml( cmd )
    time.sleep(0.5)

    cmd = "cat %s" %log_file
    logcontent = connections.execute_mml( cmd )

    re_item = '(?<=Queue limit:)\d*'
    queue_limit = re.findall( re_item, logcontent )

    if queue_limit is not None:
        output = queue_limit[len(queue_limit)-1]
    return output

def Get_Last_Queue_Msgs(log_file, pid):

    cmd = "kill -USR2 %s" %pid
    connections.execute_mml( cmd )
    time.sleep(0.5)

    cmd = "cat %s" %log_file
    logcontent = connections.execute_mml( cmd )

    re_item = '(?<=msgs:)\s*\d*'
    queue_msgs = re.findall( re_item, logcontent )

    print "queue_msgs is: %d" %(len(queue_msgs))
    if queue_msgs is not None:
        output = queue_msgs[len(queue_msgs)-1]
    return output

def Get_Node_Process_Id():
    cmd = "cat /proc/dmxmsg/processor_index"
    output = connections.execute_mml( cmd )
    id = output.strip()
    return id

def Check_Node_Mac_State(phy_addr, expect_str):
    cmd = "cat /proc/dmxmsg/mac_addr_tbl"
    output = connections.execute_mml( cmd )
    mac_table = output.strip()
    re_item = '00%s(?=\s*%s)' %(phy_addr, expect_str)
    match = re.findall( re_item, mac_table )
    if len(match) > 0:
        output = "sucessful"
    else:
        output = "fail"
    return output

def Get_Delay_Sync_Timeout():
    cmd = "cat /proc/dmxmsg/delay_sync_timeout"
    output = connections.execute_mml( cmd )
    size = output.strip()
    return size

def Set_Delay_Sync_Timeout(size):
    if size != '':
        cmd = "echo %s > /proc/dmxmsg/delay_sync_timeout" %size
        output = connections.execute_mml( cmd )
    Get_Delay_Sync_Timeout()
    return


def Get_Reorder_Queue_Timeout():
    cmd = "cat /proc/dmxmsg/g_reorder_queue_empty_check_time"
    output = connections.execute_mml( cmd )
    size = output.strip()
    return size


def Set_Reorder_Queue_Timeout(size):
    if size != '':
        cmd = "echo %s > /proc/dmxmsg/g_reorder_queue_empty_check_time" %size
        output = connections.execute_mml( cmd )
    Get_Reorder_Queue_Timeout()
    return

def MakeDictionary(keys, values):
        return dict(zip(keys, values))


def Get_irpoff_state(address):
    cmd = "sed -n '/:0\{0,4\}%s:\w\{2,\}$/p' /proc/dmxmsg/irpoff_ustate_tbl |  awk -F':' '{ print $4}'" %address
    output = connections.execute_mml( cmd )
    return output


def Make_L2_Sending_With_Cos(sender, receiver, cos):
    command = "dmxcli -s "+sender+" -r "+receiver +" -P "+cos+" -t 30"
    out = connections.execute_mml_without_check(command)
    return out

def Direct_L2_Sending(sender, receiver, cos, len):
    command = "dmxcli -s "+sender+" -r "+receiver+" -P "+cos+" -l " +len+" -w "+"-t 30"
    out = connections.execute_mml_without_check(command)
    return out

def Replace_L2_handler(sender, receiver):
    command = "dmxcli -s "+sender+" -r "+receiver+" -V "+"-t 30"
    connections.execute_mml_without_check(command)

def Restore_L2_handler(sender, receiver):
    command = "dmxcli -s "+sender+" -r "+receiver+" -E "+"-t 30"
    connections.execute_mml_without_check(command)

def Lock_RU_On_Node(node):
    command = "fshascli -lnEF /"+node+"/*Server*"
    out = connections.execute_mml_without_check(command)
    return out

def Unlock_RU_On_Node(node):
    command = "fshascli -unEF /"+node+"/*Server*"
    out = connections.execute_mml_without_check(command)
    return out

def LnE_RU_On_Node(node):
    command = "fshascli -lnE /"+node+"/*Server*"
    out = connections.execute_mml_without_check(command)
    return out

def UnE_RU_On_Node(node):
    command = "fshascli -unE /"+node+"/*Server*"
    out = connections.execute_mml_without_check(command)
    return out

def Check_RU_State_On_Node(node):
    command = "fshascli -s /"+node+"/*Server*"
    out = connections.execute_mml_without_check(command)
    return out

def Check_All_RU_State():
    command = "ilclifunit -u"
    out = connections.execute_mml_without_check(command)
    return out

def gen_stub_recv_sync(family, wait, log):
    """ This keyword to start dmx_generic_stub to recv dmxmsg and save log.

    #COMMAND: dmx_generic_stub recv_sync

    | Parameters  | Man. | Description  |
    | family      | Yes  | family       |
    | wait        | Yes  | wait         |
    | log         | Yes  | log file name|

    | Return value | No return value |

    Example
    | ${result}  | dmx generic stub recv_sync | family | yes | log |

    """
    if wait == 'yes':
       command = "dmx_generic_stub recv_sync " + family +  " -w -b > " + log +" 2>&1 & "
    else:
       command = "dmx_generic_stub recv_sync " + family +  " -b > " + log +" 2>&1 & "
    connections.execute_mml_without_check(command)

def decode_sync_id(sync_id_log):
   tmp=sync_id_log.split(',')
   swo_cnt=int(tmp[2].split(':')[1], 10)
   local_cnt=int(tmp[3].split(':')[1], 10)
   return (swo_cnt, local_cnt)


def check_sync_id_continuous(sync_id_content, msg_num):
   output=sync_id_content.splitlines()
   total_lines_cnt=len(output)

   swo_cnt_pre=0
   local_cnt_pre=-1
   recv_msg_cnt=0
   context_line_cnt=0


   #find the first sync id log and get the first sync msg id
   i=0
   while i < total_lines_cnt:
      line=output[i]
      context_line_cnt += 1
      if line.lower().find('sync swo cnt') > 0:
         (swo_cnt, local_cnt)=decode_sync_id(line)
         swo_cnt_pre = swo_cnt
         local_cnt_pre = local_cnt - 1
         break

      i += 1

   while i < total_lines_cnt:
      line=output[i]
      context_line_cnt += 1
      if line.lower().find('sync swo cnt') > 0:
         (swo_cnt, local_cnt)=decode_sync_id(line)
         if (swo_cnt == swo_cnt_pre ):
            if local_cnt != local_cnt_pre + 1:
               return 'failed: local_cnt miss-continous at line:%d, log:%s' %(context_line_cnt, line)
            else:
               local_cnt_pre += 1
            recv_msg_cnt  += 1
         else:
            #swo happened
            if swo_cnt != swo_cnt_pre + 1:
               return 'failed: swo_cnt does not continous at swo_cnt_pre=%d, swo_cnt=%d' %(swo_cnt_pre, swo_cnt)
            swo_cnt_pre = swo_cnt
            if local_cnt != 0:
               return 'failure: local_cnt does not start with 0'

            local_cnt_pre = 0
            recv_msg_cnt  += 1
      i += 1

   #print "recv_msg_cnt=", recv_msg_cnt
   if recv_msg_cnt != msg_num:
      return 'failed: msg number mismatch, expect %d, but is %d' %(msg_num, recv_msg_cnt)

   return 'success'

def check_wosp_sync_id_matched(wo_sync_id_content, sp_sync_id_content, msg_num):
   wo_sync_id=wo_sync_id_content.splitlines()
   sp_sync_id=sp_sync_id_content.splitlines()

   wo_swo_cnt = 0
   wo_local_cnt = 0
   sp_swo_cnt = 0
   sp_local_cnt = 0
   i = 0
   total_lines=len(wo_sync_id)
   while i < total_lines:
      if wo_sync_id[i].lower().find('sync swo cnt') > 0:
         (wo_swo_cnt, wo_local_cnt)=decode_sync_id(wo_sync_id[i])
      if sp_sync_id[i].lower().find('sync swo cnt') > 0:
         (sp_swo_cnt, sp_local_cnt)=decode_sync_id(sp_sync_id[i])

      if (wo_swo_cnt != sp_swo_cnt) or (wo_local_cnt != sp_local_cnt):
         return 'failed: wo and sp mismatch at %d' %i

      i += 1

   return 'success'

def  check_sync_id(wo_sync_id_content, sp_sync_id_content, msg_num):
   result = check_sync_id_continuous(wo_sync_id_content, msg_num)
   if 'success' != result:
      return result

   result = check_sync_id_continuous(sp_sync_id_content, msg_num)
   if 'success' != result:
      return result

   result = check_wosp_sync_id_matched(wo_sync_id_content, sp_sync_id_content, msg_num)
   return result



