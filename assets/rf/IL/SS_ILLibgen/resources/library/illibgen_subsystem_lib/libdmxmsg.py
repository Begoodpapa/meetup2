from comm.communication import exceptions
from comm.communication import connections
from comm.communication.helper import *
from comm.communication import misc
from string import atoi
from parsemon import *
import re
import os
from robot.libraries.BuiltIn import BuiltIn

def send_message_to_test_process(monitor_computer_id,receiver_computer_id, family_id,process_id,send_msg_to_self,ncount=10,delay=3,data="'01 34 56 ff 01 21'",retry=3):
    """This keyword is to trigger CLI to send message to test process and catch the received message by monster

    #COMMAND: testmon.py -p "-u monitor_computer_id -f family_id" -c "montest -u receiver_computer_id -f family_id -p process_id -d data -n ncount" -t delay
    | Parameters            | Man. | Description                                  |
    | monitor_computer_id   | Yes  | the computer address monster to monitor      |
    | receiver_comptuer_id  | Yes  | the target computer address message sent to  |
    | family_id             | Yes  | the target family to monitor and send message|
    | process_id            | Yes  | the target process id send message to        |
    | send_msg_to_self      | Yes  | the tag to indicate the msg will be sent to self or other process |
    | ncount                | No   | the message count send out                   |
    | delay                 | No   | delay time python script will kill monster process after message sent out |
    | data                  | No   | the message data vlaue  |
       
    | Return value | command str, the catched message string monitored by monster |

    Example
    | ${result} | send message to test process | 0x700 | 0x700 | 0x193B | 0 | false | 
    """
    if send_msg_to_self == 'false':
        command='testmon.py -p "-u %s -f %s -V" -c "montest -f 0xffff -- -u %s -f %s -p %s -d %s -n %s" -t %s -r %s'%(monitor_computer_id,family_id,receiver_computer_id,family_id,process_id,data,ncount,delay,retry)
        out = connections.execute_mml_without_check(command)
    else:
        command='testmon.py -p "-u %s -f %s -V" -c "montest -f 0xffff -- -u %s -f %s -p %s -d %s -n %s -t 1" -t %s -r %s'%(monitor_computer_id,family_id,receiver_computer_id,family_id,process_id,data,ncount,delay,retry)
        out = connections.execute_mml_without_check(command)
    match = re.search(r"\bIn total [0-9]+ frames sent, 0 lost.", out, re.I)
    if match is None:
        return 'failure'
    print match.group()
    return out

def send_message_to_test_process_by_libdmxmsg(monitor_computer_id,receiver_computer_id, family_id,process_id,send_msg_to_self,ncount=10,delay=3,data="'01 34 56 ff 01 21'",retry=3):
    """This keyword is to trigger CLI to send message to test process by libdmxmsg and catch the received message by monster

    #COMMAND: testmon.py -p "-u monitor_computer_id -f family_id" -c "montest -u receiver_computer_id -f family_id -p process_id -d data -n ncount" -t delay
    | Parameters            | Man. | Description                                  |
    | monitor_computer_id   | Yes  | the computer address monster to monitor      |
    | receiver_comptuer_id  | Yes  | the target computer address message sent to  |
    | family_id             | Yes  | the target family to monitor and send message|
    | process_id            | Yes  | the target process id to send message to     |
    | send_msg_to_self      | Yes  | the tag to indicate the msg will be sent to self or other process |
    | ncount                | No   | the message count send out                   |
    | delay                 | No   | delay time python script will kill monster process after message sent out |
    | data                  | No   | the message data vlaue  |
       
    | Return value | command str, the catched message string monitored by monster |

    Example
    | ${result} | send message to test process by libdmxmsg | 0x700 | 0x700 | 0x1941 | 0 | false |
    """
    if send_msg_to_self == 'false':
        command='testmon.py -p "-u %s -f %s -V" -c "msgmonstub -u %s -f %s -p %s -d %s -n %s" -t %s -r %s'%(monitor_computer_id,family_id,receiver_computer_id,family_id,process_id,data,ncount,delay,retry)
        out = connections.execute_mml_without_check(command)
    else:
        command='testmon.py -p "-u %s -f %s -V" -c "msgmonstub -u %s -f %s -p %s -d %s -n %s -t 1" -t %s -r %s'%(monitor_computer_id,family_id,receiver_computer_id,family_id,process_id,data,ncount,delay,retry)
        out = connections.execute_mml_without_check(command)
    match = re.search(r"\bIn total [0-9]+ frames sent, 0 lost.", out, re.I)
    if match is None:
        return 'failure'
    print match.group()
    return out

def testcli_send_message_to_test_process(receiver_computer_id, family_id,process_id,ncount=10,data="'01 34 56 ff 01 21'"):
    """This keyword is to trigger CLI to send message to test process

    #COMMAND: montest -u receiver_computer_id -f family_id -p process_id -d data -n ncount
    | Parameters            | Man. | Description                                  |
    | receiver_comptuer_id  | Yes  | the target computer address message sent to  |
    | family_id             | Yes  | the target family to monitor and send message|
    | process_id            | Yes  | the target process id to send message to     |
    | ncount                | No   | the message count send out                   |
    | data                  | No   | the message data vlaue  |
       
    | Return value | command str, success for only 1 string of 'Next working' in the execute result |

    Example
    | ${result} | test cli send message to test process |  0x200 | 0x193B | 0 |
    """

    command='montest -f 0xffff -- -u %s -f %s -p %s -d %s -n %s'%(receiver_computer_id,family_id,process_id,data,ncount)
    out = connections.execute_mml_without_check(command)
    if out.count('Next working') == 1:
        return 'success'
    else:
        return 'failure'

def send_message_to_test_process_with_condition_by_libdmxmsg(monitor_computer_id,receiver_computer_id, family_id,process_id,condition,ncount=10,delay=3,data="'01 34 56 ff 01 21'",retry=3):
    """This keyword is to trigger CLI to send message to test process by libdmxmsg and catch the received message with condition by monster

    #COMMAND: testmon.py -p "-u monitor_computer_id -f family_id -c contion" -c "montest -u receiver_computer_id -f family_id -p process_id -d data -n ncount" -t delay
    | Parameters            | Man. | Description                                  |
    | monitor_computer_id   | Yes  | the computer address monster to monitor      |
    | receiver_comptuer_id  | Yes  | the target computer address message sent to  |
    | family_id             | Yes  | the target family to monitor and send message|
    | process_id            | Yes  | the target process id to send message to     |
    | condition             | Yes  | condition used by monster to filter the message out |
    | ncount                | No   | the message count send out                   |
    | delay                 | No   | delay time python script will kill monster process after message sent out |
    | data                  | No   | the message data vlaue  |
       
    | Return value | command str, the catched message string monitored by monster |

    Example
    | ${result} | send message to test process with condition by libdmxmsg | 0x700 | 0x700 | 0x1942 | 0 | ":NUM=FF01" |
    """
    command='testmon.py -p "-u %s -f %s -V -c %s" -c "msgmonstub -u %s -f %s -p %s -d %s -n %s" -t %s -r %s'%(monitor_computer_id,family_id,condition,receiver_computer_id,family_id,process_id,data,ncount,delay,retry)
    out = connections.execute_mml_without_check(command)
    return out
   
def message_count_should_be_correct(msg_buf, send_msg_to_self='false', ncount=10):
    """This keyword is to check whether message count is correct or not.
    
    | Parameters            | Man. | Description                                 |
    | msg_buf               | Yes  | This is the output of monster captured      |
    | send_msg_to_self      | No   | the tag to indicate the msg will be sent to self or other process |
    | ncount                | No   | the message count send out                  |
       
    | Return value | command str, success if the message count is correct |

    Example
    | ${result} | message count should be correct | ${msg_buf} | 
    """
    l = get_msg_from_buf(msg_buf)
    print l
    if send_msg_to_self == 'true':
        ncount = 2
        m_l = [parse_msg(i) for i in l]
        assert len(get_msgs_by_id(m_l, 65282, type='recv')) == ncount
        msg_list = get_msgs_by_id(m_l, 65282, type='recv')
        msg1=msg_list[0]
        msg2=msg_list[1]
        data1=msg1['data']
        data2=msg2['data']
        assert data1 == data2
        return 'success'
    m_l = [parse_msg(i) for i in l]
    print m_l
    print len(get_msgs_by_id(m_l, 65281, type='recv'))
    assert  len(get_msgs_by_id(m_l, 65281, type='recv')) == ncount
    return 'success'

def message_count_should_be_correct_with_condition(msg_buf, in_ncount='1', in_msg_num='ff01', send_recv='recv'):
    """This keyword is to check whether message count is correct or not.
    
    | Parameters            | Man. | Description                                 |
    | msg_buf               | Yes  | This is the output of monster captured      |
    | send_msg_to_self      | No   | the tag to indicate the msg will be sent to self or other process |
    | ncount                | No   | the message count send out                  |
       
    | Return value | command str, success if the message count is correct |

    Example
    | ${result} | message count should be correct | ${msg_buf} | 
    """
    ncount = int(in_ncount)
    msg_num = int(in_msg_num, 16)
    l = get_msg_from_buf(msg_buf)
    m_l = [parse_msg(i) for i in l]
    print len(get_msgs_by_id(m_l, msg_num, type=send_recv))
    if  len(get_msgs_by_id(m_l, msg_num, type=send_recv)) == ncount:
        return 'success'
    else:
        return 'failure'

def received_message_order_should_be_consistent_with_send(msg_buf):
    """This keyword is to check whether message order consistent with sender.
    
    | Parameters  | Man. | Description                                 |
    | msg_buf     | Yes  | This is the output of monster captured      |
       
    | Return value | command str, success if the received message order is consistent with send |

    Example
    | result | received_message_order_should_be_consistent_with_send  | ${msg_buf} |
    """
    l = get_msg_from_buf(msg_buf)

    m_l = [parse_msg(i) for i in l]

    msg_list = get_msgs_by_id(m_l, 65281, type='recv')
    i = 1
    for msg in msg_list:
        str1 = msg['data']
        assert atoi(str1[:2],16) == i
        assert str1[3:17] == '34 56 FF 01 21'
        i = i + 1
    return 'success'

def address_for_received_message_should_be_correct(send_computer_id,recv_computer_id, msg_buf):
    """This keyword is to check whether received computer address is consistent with sender.
    
    | Parameters       | Man. | Description                                 |
    | send_cmputer_id  | Yes  | This is the computer address of the sender  |
    | send_cmputer_id  | Yes  | This is the computer address of the receiver|
    | msg_buf          | Yes  | This is the output of monster captured      |
       
    | Return value | command str, sender address of the received message is correct  |

    Example
    | result | address_for_received_message_should_be_correct  |  0x700 | 0x200 | ${msg_buf} |
    """
    l = get_msg_from_buf(msg_buf)

    m_l = [parse_msg(i) for i in l]
    msg_list = get_msgs_by_id(m_l, 65281, type='recv')
    base_logical_address='0x4002'
    for msg in msg_list:
        print msg
        assert check_msg({'msg': {'computer': int(send_computer_id,0)}}, msg)  or check_msg({'msg': {'computer': int(base_logical_address,0)}}, msg) == True
        assert check_msg({'bottom':{'computer': int(recv_computer_id,0)}}, msg) == True
    return 'success'

def start_libdmxmsg_process(prb_name, inst_num):
    """This keyword is to start libdmxms process and return the process id.
    
    | Parameters  | Man. | Description                                  |
    | prb_name    | Yes  | the libdmxmsg prb name, such as msgmonstub   |
    | inst_num    | Yes  | the startup instance num for this prb        |

    | Return value | the process id |

    Example
    | result | start_libdmxmsg_process |  msgmonstub | 2 |
    """   
    command = "%s -s %s &" % (prb_name, inst_num)
    out = connections.execute_cli(command)
    result_list = out.split()
    return result_list[1].strip()
    
def start_monster_at_background(computer_id,family_id,out_file):
    """This keyword is to start monster monitoring at background.
    
    | Parameters   | Man. | Description            |
    | computer_id  | Yes  | the computer address   |
    | family_id    | Yes  | the target family to monitor and send message  |

    | Return value | the process id |

    Example
    | result | start monster at background |  0x700 | 0x1B58 | /root/bottom.bin |
    """   
    command = 'monster -u %s -f %s -c "SR:NUM=6034,9901" -b %s >/dev/null&' % (computer_id,family_id,out_file)
    out = connections.execute_cli(command)
    result_list = out.split()
    return result_list[1].strip()
    
def send_msg_to_not_exist_process(computer_id,family_id):
    """This keyword is to send msg to not exist process
    
    | Parameters   | Man. | Description            |
    | computer_id  | Yes  | the computer address   |
    | family_id    | Yes  | the target family to monitor and send message  |

    | Return value | failure, for the process does not exist so the result will be failure |

    Example
    | result | send msg to not exist |  0x700 | 0x1B58 |
    """   
    command = 'ILDMXTestCli -f 0xfffe -- -r %s %s 0 -a' % (computer_id,family_id)
    out = connections.execute_cli(command)

    if out.count('failure')==1:
        return 'failure'
    else:
        return 'the result is wrong'

def decode_monster_binary_message(out_file):
    """This keyword is to decode captured message by monster
    
    | Parameters   | Man. | Description            |
    | out_file     | Yes  | The monster msg out put file |

    | Return value | decoded msg bottoms and headers    |
 
    Example
    | result | decode monster binary message | /root/bottom.bin |
    """
    command='debot.py %s'%(out_file)
    out = connections.execute_mml_without_check(command)
    return out

def check_bottom_values(msg_buf,omu_phy_addr, omu_logical_address='7002'):
    """This keyword is to check decoded msg bottom vlaues
    
    | Parameters   | Man. | Description            |
    | msg_buf      | Yes  | The decoded msg values |

    | Return value | success, if the bottom values are correct    |
 
    Example
    | result | check bottom values | ${msg_buf} |
    """

    if (msg_buf.find("Bottom:") == -1):
       exceptions.raise_ILError("ILCommandExecuteError", "failed to get msg bottom")
       
    msg_list = []
    msg_buf = msg_buf[msg_buf.find("time of day (dword):"):]
    msg_text = msg_buf.split("Bottom:")
  
    for msg in msg_text:
        print msg
        match = re.search(r"control \(byte\):\s*([0-9]*)", msg, re.I)
        msg_info = CommonItem()
        msg_info.control = match.group(1)
        match = re.search(r"hop_count \(byte\):\s*([0-9]*)\s*", msg, re.I)
        msg_info.hop = match.group(1)
        match = re.search(r"\s*msg number \(word\):\s*([0-9]*)\s*", msg, re.I)
        msg_info.msgnum = match.group(1)
        match = re.search(r"\s*next phys computer \(word\):\s*([0-9]*)\s*", msg, re.I)
        msg_info.nextcomp = match.group(1)
        match = re.search(r"\s*computer_addr \(word\):\s*([0-9]*)\s*", msg, re.I)
        msg_info.comp = match.group(1)
        match = re.search(r"\s*phys_computer \(word\):\s*([0-9]*)\s*", msg, re.I)
        msg_info.phycomp = match.group(1)
        msg_list.append(msg_info)
    print msg_list
    omu_phy_addr = omu_phy_addr.split('X')[1]
    omu_phy_addr = atoi(omu_phy_addr,16)
    omu_logical_address = atoi(omu_logical_address,16)
    result = misc.select_entries_from_list(msg_list,'msgnum=9901')
    for msg in result:
        msg.nextcomp = atoi(msg.nextcomp,16)
        msg.phycomp = atoi(msg.phycomp,16)
        msg.comp = atoi(msg.comp,16)
        if ( msg.control <> '08' ) or (msg.hop <> '01') or (msg.comp <> omu_logical_address) or ((msg.nextcomp <> omu_phy_addr) and (msg.nextcomp <> omu_logical_address)) or ((msg.phycomp <> omu_phy_addr) and (msg.phycomp <> omu_logical_address)):
            return 'failure'
    result = misc.select_entries_from_list(msg_list,'msgnum=6034')
    for msg in result:
        msg.comp = atoi(msg.comp,16)
        msg.nextcomp = atoi(msg.nextcomp,16)
        msg.phycomp = atoi(msg.phycomp,16)
        if ( msg.control <> '80' and msg.control <> '00' and msg.control <> '08' ) or (msg.hop <> '04' and msg.hop <> '01') or (msg.comp <> omu_phy_addr) or (msg.nextcomp <> omu_phy_addr) or (msg.phycomp <> omu_phy_addr):
            return 'failure'
        if msg.control == '80' and msg.hop <> '04':
            return 'failure'
        if msg.control == '00' and msg.hop <> '01':
            return 'failure'
        if msg.control == '08' and msg.hop <> '01':
            return 'failure'
    return 'success'
    
def check_whether_process_is_exist_or_not(prb_name):
    """This keyword is to whether given PRB exist or not
    
    | Parameters   | Man. | Description             |
    | prb_name     | Yes  | The name of checked PRB |

    | Return value | success, if the checked prb exist |
 
    Example
    | result | check whether process is exist or not | ${prb_name} |
    """

    command = 'ps -ef|grep %s'%(prb_name)
    out = connections.execute_mml_without_check(command)

    lines = out.strip().splitlines()
    count = 0
    for line in lines:
        count = count +1
    if count ==2:
        return 'success'

def execute_dmxmsg_command(computer_id,family_id,command_str,timeout='2000'):
    """This keyword is to execute specified command
    
    | Parameters   | Man. | Description            |
    | computer_id  | Yes  | the computer address   |
    | family_id    | Yes  | the target family to monitor and send message  |
    | command      | Yes  | the command to be executed |

    | Return value | success, if the command executed successfully |

    Example
    | result | execute dmxmsg command |  0x700 | 0x1941 | refer |
    """
    if (command_str.strip() == 'time'):
        command = 'msgmonstub -u %s -f %s -r %s -T %s'%(computer_id,family_id,command_str,timeout)
    else: 
        command = 'msgmonstub -u %s -f %s -r %s'%(computer_id,family_id,command_str)
    out = connections.execute_mml_without_check(command)
    if (command_str.strip() == 'time'):
        time_out = int(timeout)
        print 'timeout is:', time_out
        match = re.search(r"\s*time elapsed:\s*([0-9]*)\s*", out, re.I)
        if match is not None:
            time1 = match.group(1)
            time2 = atoi(str(time1), 10)
            if (time2 >= time_out) and (time2 < (time_out+99)):
                return 'success'
            else:
                return 'failure'
        else:
            return 'failure'
    if (command_str.strip() == 'mthread'):
        if out.count('success') ==2:
            return 'success'
        else:
            return 'failure'

    if out.count('success') ==1:
        return 'success'
    else:
        return 'failure'

def process_receive_wanted_ACK(computer_id,family_id,command_str):
    """This keyword is to receive wanted ACK
    
    | Parameters   | Man. | Description            |
    | computer_id  | Yes  | the computer address   |
    | family_id    | Yes  | the target family to monitor and send message  |
    | command      | Yes  | the command to be executed |

    | Return value | success, if the command executed successfully |

    Example
    | result | process received wanted ACK |  0x700 | 0x1941 | save |
    """

    command = 'msgmonstub -u %s -f %s -r %s'%(computer_id,family_id,command_str)
    out = connections.execute_mml_without_check(command)
    out = out[out.find("recv message"):]
  
    lines = out.strip().splitlines()
    i = 1
    msg_num_list = []
    for line in lines:
        match = re.search(r"\s*message id:\s*([0x0-9a-f]*)", line, re.I)
        if match is not None:
            msg_num=match.group(1)
            msg_num_list.append(msg_num)
        i = i + 1
    if (msg_num_list[0]=='0xff01') and  (msg_num_list[1]=='0xff02') and (msg_num_list[2]=='0x1234') and (msg_num_list[3]=='0x1235'):
        return 'success'
    else:
        return 'failure'

def process_receive_ACK_including_bottom(computer_id,family_id,command_str):
    """This keyword is to receive ACK including bottom
    
    | Parameters   | Man. | Description            |
    | computer_id  | Yes  | the computer address   |
    | family_id    | Yes  | the target family to monitor and send message  |
    | command_str  | Yes  | the command to be executed |

    | Return value | success, if the command executed successfully |

    Example
    | result | execute dmxmsg command |  0x700 | 0x1941 | bottom |
    """

    command = 'msgmonstub -u %s -f %s -r %s'%(computer_id,family_id,command_str)
    out = connections.execute_mml_without_check(command)
    out = out[out.find("bottom:"):]
  
    match = re.search(r"\s*family:\s*([0x0-9a-f]*)", out, re.I)
    if match is not None:
        family = match.group(1)
    if family == '0x1940':
        return 'success'
    else:
        return 'failure'

def send_msg_from_specified_context(computer_id,family_id,command_str):
    """This keyword is to send msg from specified context
    
    | Parameters   | Man. | Description            |
    | computer_id  | Yes  | the computer address   |
    | family_id    | Yes  | the target family to monitor and send message  |
    | command_str  | Yes  | the command to be executed |

    | Return value | success, if the command executed successfully |

    Example
    | result | execute dmxmsg command |  0x700 | 0x1941 | from |
    """

    command = 'msgmonstub -u %s -f %s -r %s'%(computer_id,family_id,command_str)
    out = connections.execute_mml_without_check(command)
    bottom_1 = out.split("bottom")[1]
    bottom_2 = out.split("bottom")[2]

    
    match = re.search(r"\s*family:\s*([0x0-9a-f]*)", bottom_1, re.I)
    if match is not None:
        family_1 = match.group(1)
    match = re.search(r"\s*family:\s*([0x0-9a-f]*)", bottom_2, re.I)
    if match is not None:
        family_2 = match.group(1)
    if (family_1 == '0x1940') and (family_2 == '0x1949'):
        return 'success'
    else:
        return 'failure'
    
def test_libdmxmsg_family_register_limit(prb_name, inst_num):
    """This keyword is to start libdmxms process and return the process id.
    
    | Parameters  | Man. | Description                                  |
    | prb_name    | Yes  | the libdmxmsg prb name, such as msgmonstub   |
    | inst_num    | Yes  | the startup instance num for this prb        |

    | Return value | 'success' or 'failure' |

    Example
    | result | Test Libdmxmsg Family Register Limit |  msgmonstub | 555 |
    """   
    command = "%s -s %s" % (prb_name, inst_num)
    out = connections.execute_cli(command)
    if out.count('Registering pid fail. (ret 0x11e)') == 1:
        return 'success'
    else:
        return 'failure'

def execute_dmxmsg_command_and_check_result(computer_id,family_id,command_str,result,res_count):
    """This keyword is to execute specified command
    
    | Parameters   | Man. | Description            |
    | computer_id  | Yes  | the computer address   |
    | family_id    | Yes  | the target family to monitor and send message  |
    | command      | Yes  | the command to be executed |

    | Return value | success, if the command executed successfully |

    Example
    | result | execute dmxmsg command and check result |  0x700 | 0x1941 | register | success | 2 |
    """

    command = 'msgmonstub -u %s -f %s -r %s'%(computer_id,family_id,command_str)
    out = connections.execute_mml_without_check(command)

    if out.count(result) == int(res_count):
        return 'success'
    else:
        return 'failure'

def kill_process_by_pid_with_option(pid):
    """ This keyword to kill give process with -2 option by pid

    #COMMAND: kill

    | Parameters  | Man. | Description  |
    | pid         | Yes  | process id |

    | Return value | No return value |

    Example
    | ${result}  |  Kill Process By PID With Option| 4321  |

    """
    command = "kill -2 " + pid
    out = connections.execute_mml(command)

def process_receive_ACK_with_correct_context(computer_id,family_id,wanted_family_id):
    """This keyword is to receive ACK with correct context
    
    | Parameters         | Man. | Description            |
    | computer_id        | Yes  | the computer address   |
    | family_id          | Yes  | the target family to monitor and send message  |
    | wanted_family_id   | Yes  | the family in ack info |

    | Return value | success, if the command executed successfully |

    Example
    | result | process received ACK with correct context |  0x700 | 0x1941 | 0x1941 |
    """

    command = 'msgmonstub -u %s -f %s'%(computer_id,family_id)
    out = connections.execute_mml_without_check(command)
    if out.count('time out!')==1:
        return 'failure'
    out = out[out.find("recv message"):]

    match = re.search(r"\s*family id:\s*([0x0-9a-f]*)", out, re.I)
    if match is not None:
        return_family_id = match.group(1)
    if return_family_id ==wanted_family_id:
        return 'success'
    else:
        return 'failure'

def execute_dmxmsg_with_no_command(computer_id,family_id):
    """This keyword is to execute dmxmsg sending message to process
    
    | Parameters   | Man. | Description            |
    | computer_id  | Yes  | the computer address   |
    | family_id    | Yes  | the target family to send message  |

    | Return value | success, if the command executed successfully |

    Example
    | result | execute dmxmsg command with no command|  0x700 | 0x1941|
    """

    command = 'msgmonstub -u %s -f %s'%(computer_id,family_id)
    out = connections.execute_mml_without_check(command)
    if out.count('success') ==1:
        return 'success'
    else:
        return 'failure'

def libdmxmsg_send_message_to_test_process_and_monitor(monitor_command, command, delay=3, retry=3):
    """This keyword is to trigger CLI to send message to test process and catch the received message by monster

    #COMMAND: testmon.py -p "-u 0x700 -f 0x1f48" -c "WMNotifstub -f 0xffff -- -u 0x700 -f 0x1f48 -t 1" -t delay
    | Parameters            | Man. | Description                                  |
    | monitor_command       | Yes  | the monster's commmand       |
    | command               | Yes  | the command to monitor      |
    | delay                 | No   | delay time python script will kill monster process after message sent out |
       
    | Return value | command str, the catched message string monitored by monster |

    Example
    | ${result} | send message to test process and monitor | -u 0x700 -f 0x1f48 | WMNotifstub -f 0xffff -- -u 0x700 -f 0x1f48 -t 1 | 3 | 
    """
    command='testmon.py -p "%s -V" -c "%s" -t %s -r %s'%(monitor_command,command,delay,retry)
    out = connections.execute_mml_without_check(command)
    return out

def message_bufbottom_should_be_correct(msg_buf, bufbot_index=0):
    """This keyword is to check whether message count is correct or not.
    
    | Parameters            | Man. | Description                                 |
    | msg_buf               | Yes  | This is the output of monster captured      |
    | bufbot_index          | No   | the message buffer bottom index in bufbot   |
       
    | Return value | command str, success if the message count is correct |
    
    Example
    | ${result} | message count should be correct | ${msg_buf} | 
    """ 
    index = atoi(str(bufbot_index), 10)
    bufbot = [[0,1,0,128,4,0], [64,1,0,128,4,0]]
    print bufbot[index]
    l = get_msg_from_buf(msg_buf)
    m_l = [parse_msg(i) for i in l]
    for m in m_l:
        if m['type'] == 'recv':
            assert m['bottom']['control']&bufbot[index][3] != bufbot[index][3]
            assert m['bottom']['hop_count'] == bufbot[index][1]
            assert m['bottom']['bottom_flag'] == bufbot[index][2]
        else:
            assert m['bottom']['control'] == bufbot[index][3]
            assert m['bottom']['hop_count'] == bufbot[index][4]
            assert m['bottom']['bottom_flag'] == bufbot[index][5]
    return 'success'
