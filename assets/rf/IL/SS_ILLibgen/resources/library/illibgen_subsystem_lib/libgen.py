from comm.communication import exceptions
from comm.communication import connections
from comm.communication import helper
from comm.communication.helper import CommonDict, CommonItem
from ipalight_platform import syslog_lib
import robot
import re
import os
import time
import datetime
from robot.libraries.BuiltIn import BuiltIn
from parsemon import *
from string import atoi

def send_a_msg_to_target_process(computer_id,family_id,process_id,msg_num,dmx_attr):
    """This keyword is to send a msg to target process with appointed msg number and dmx attribute.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -s

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
    | msg_num     | Yes  | the msg number                              |
    | dmx_attr    | Yes  | dilivery width                              |
   
    | Return value | command execution result |

    Example
    | result | send a msg to target process | 0x0000 0xA014 0x0000 0x0 0xffff11 |
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -s'%(computer_id,family_id,process_id,msg_num,dmx_attr)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_create_hand(computer_id,family_id,process_id,msg_num,dmx_attr,process_type,time_quota,task_dur):
    """This keyword is to send a msg to target process for create hand.if create hand timeout,return the process_id.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -c process_type time_quota task_dur

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
    | msg_num     | Yes  | the msg number                              |
    | dmx_attr    | Yes  | dilivery width                              |
    | process_type| Yes  | Type(hand group)of the process to be created|
    | time_quota  | Yes  | the time limited                            |
    | task_dur    | Yes  | task running time                           |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process create hand | 0x0000 0x**** 0x0000 0x**** 0xffff11 0x1 0x20 0x10|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -c %s %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,process_type,time_quota,task_dur)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('success') == 0:
          match = re.search(r"\bprocess_id:\s*([0-9a-x]*)", out, re.I)
          if match is not None:
            return match.group(1)
    else:
        return 'the return is wrong'

def send_msg_to_target_process_create_hand_unconcern_timeout(computer_id,family_id,process_id,msg_num,dmx_attr,process_type,time_quota,task_dur):
    """This keyword is to send a msg to target process for create hand.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -q -c process_type time_quota task_dur

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
    | msg_num     | Yes  | the msg number                              |
    | dmx_attr    | Yes  | dilivery width                              |
    | process_type| Yes  | type(hand group)of the process to be created|
    | time_quota  | Yes  | the time limited                            |
    | task_dur    | Yes  | task running time                           |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process create hand unconcern timeout | 0x0000 0x**** 0x0000 0x**** 0xffff11 0x1 0x20 0x10|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -q -c %s %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,process_type,time_quota,task_dur)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_refresh_hand(computer_id,family_id,process_id,msg_num,dmx_attr,rf_process,rf_focus,rf_time):
    """This keyword is to send a msg to target process for refresh appointed hand process.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -f rf_process rf_focus rf_time 

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
    | msg_num     | Yes  | the msg number                              |
    | dmx_attr    | Yes  | dilivery width                              |
    | rf_process  | Yes  | the hand process id which need to be refresh|
    | rf_focus    | Yes  | the hand focus                              |
    | rf_time     | Yes  | the refresh time limited                    |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process refresh hand | 0x0000 0x**** 0x0000 0x**** 0xffff11 0x1 0x1 0x20|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -f %s %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,rf_process,rf_focus,rf_time)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure in hand operation') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_stop_hand(computer_id,family_id,process_id,msg_num,dmx_attr,stop_proc_id):
    """This keyword is to send a msg to target process for stop appointed hand process.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -t stop_proc_id

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
    | msg_num     | Yes  | the msg number                              |
    | dmx_attr    | Yes  | dilivery width                              |
    | stop_proc_id| Yes  | the hand process id which need to be stop   |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process stop hand | 0x0000 0x**** 0x0000 0x**** 0xffff11 0x1|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -t %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,stop_proc_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'
        
def send_msg_to_target_process_stop_process(computer_id,family_id,process_id,msg_num,dmx_attr):
    """This keyword is to send a msg to target process for stop process.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -e

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
    | msg_num     | Yes  | the msg number                              |
    | dmx_attr    | Yes  | dilivery width                              |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process stop process | 0x0000 0x**** 0x0000 0x**** 0xffff11|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -e'%(computer_id,family_id,process_id,msg_num,dmx_attr)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def count_running_process_num_of_prb(prb_name):
    """This keyword is to count the num of appointed running prb .

    #COMMAND: ps -ef |grep *

    | Parameters  | Man. | Description                                 |
    | Return value | command execution result |

    Example
    | result | count running process num of prb |
    """
    command='ps -ef|grep '+ prb_name
    connections.execute_mml_without_check(command)
    command='ps -ef|grep '+ prb_name
    out = connections.execute_mml_without_check(command)
    return out.count('%s -f'%prb_name)

def send_msg_to_target_process_start_statistic_count(computer_id,family_id,process_id,msg_num,dmx_attr,start_mark):
    """This keyword is to send a msg to target process for start to do statistics for time quota and successful invoked hand_reservation_timeout counter.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -m start_mark

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
    | msg_num     | Yes  | the msg number                              |
    | dmx_attr    | Yes  | dilivery width                              |
    | start_mark  | Yes  | the mark as start to do statistics          |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process start statistic count | 0x0000 0x**** 0x0000 0x**** 0xffff11 0x0|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -m %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,start_mark)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_get_next_timeout_pid(computer_id,family_id,process_id,msg_num,dmx_attr,get_mark):
    """This keyword is to send a msg to target process for get time quota and successful invoked hand_reservation_timeout counter.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -m get_mark 

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
    | msg_num     | Yes  | the msg number                              |
    | dmx_attr    | Yes  | dilivery width                              |
    | get_mark    | Yes  | the mask as get statistics counter          |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process create hand | 0x0000 0x**** 0x0000 0x**** 0xffff11 0x1 0x20 0x10|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -m %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,get_mark)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
         match = re.search(r"\bsum:\s*([0-9a-fx]*)", out, re.I)
         if match is not None:
             if match.group(1) == '0x8':
                from string import atoi
                return atoi(str(match.group(1)), 16)
             else:
                  match = re.search(r"\bhand_reservation_time_out number:\s*([0-9a-fx]*)", out, re.I)
                  if match is not None:
                       from string import atoi
                       return atoi(str(match.group(1)), 16)
    else:
        return 'the return is wrong'

def create_multi_hands_and_return_time_out_number(computer_id,family_id,process_id,msg_num,dmx_attr,process_type,time_quota,task_dur,hand_num):
    """This keyword is to send a msg to target process for create a group of normal TNSDL hand process and get statistics report after time quota expired.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -gr hand_num -c process_type time_quota task_dur

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
    | msg_num     | Yes  | the msg number                              |
    | dmx_attr    | Yes  | dilivery width                              |
    | process_type| Yes  | type(hand group)of the process to be created|
    | time_quota  | Yes  | the time limited                            |
    | task_dur    | Yes  | task running time                           |
    | hand_num    | Yes  | the number of normal TNSDL hand process     |
   
    | Return value | command execution result |

    Example
    | result | create multi hands and return time out number| 0x0000 0x**** 0x0000 0x**** 0xffff11 0x64 0x1 0x20 0x10|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -gr %s -c %s %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,hand_num,process_type,time_quota,task_dur)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
         match = re.search(r"\bsum:\s*([0-9a-fx]*)", out, re.I)
         if match is not None:
                from string import atoi
                return atoi(str(match.group(1)), 16)
    else:
        return 'the return is wrong'


def send_msg_to_target_process_allocate_normal_memory_buffer(computer_id,family_id,process_id,msg_num,dmx_attr,buffer_size_type,buffer_size):
    """This keyword is to send a msg to target process for allocate normal memory buffer.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -mem a n buffer_size_type buffer_size

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | msg_num          | Yes  | the msg number                              |
    | dmx_attr         | Yes  | dilivery width                              |
    | buffer_size_type | Yes  | buffer size type(buffersize unit,1K or *1M) |
    | buffer_size      | Yes  | buffer size                                 |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process allocate normal memory buffer | 0x0000 0x**** 0x0000 0x**** 0xffff11 0x1 0x20|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -mem a n %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,buffer_size_type,buffer_size)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success in memory operation') == 1:
        return 'success'
    elif out.count('failure in memory operation') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_allocate_message_memory_buffer(computer_id,family_id,process_id,msg_num,dmx_attr,buffer_size):
    """This keyword is to send a msg to target process for allocate message memory buffer.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -mem a m buffer_size

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | msg_num          | Yes  | the msg number                              |
    | dmx_attr         | Yes  | dilivery width                              |
    | buffer_size      | Yes  | buffer size                                 |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process allocate normal memory buffer | 0x0000 0x**** 0x0000 0x**** 0xffff11 0x20|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -mem a m %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,buffer_size)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success in memory operation') == 1:
        return 'success'
    elif out.count('failure in memory operation') == 1:
        return 'failure'
    else:
        return 'the return is wrong'
    
    
def send_msg_to_target_process_free_memory_buffer(computer_id,family_id,process_id,msg_num,dmx_attr):
    """This keyword is to send a msg to target process for free memory buffer.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -mem f

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | msg_num          | Yes  | the msg number                              |
    | dmx_attr         | Yes  | dilivery width                              |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process free memory buffer | 0x0000 0x**** 0x0000 0x**** 0xffff11 |
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -mem f'%(computer_id,family_id,process_id,msg_num,dmx_attr)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success in memory operation') == 1:
        return 'success'
    elif out.count('failure in memory operation') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_read_memory_buffer(computer_id,family_id,process_id,msg_num,dmx_attr):
    """This keyword is to send a msg to target process for read memory buffer.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -mem f

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | msg_num          | Yes  | the msg number                              |
    | dmx_attr         | Yes  | dilivery width                              |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process read memory buffer | 0x0000 0x**** 0x0000 0x**** 0xffff11|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -mem r'%(computer_id,family_id,process_id,msg_num,dmx_attr)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success in memory operation') == 1:
         match = re.search(r"\bbuffer_size:(.+?)!", out, re.I)
         if match is not None:
                from string import atoi
                return atoi(str(match.group(1)), 16)
         else:
                return 'the return is wrong'  
    elif out.count('failure in memory operation') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_create_hand_with_sleep_unconcern_timeout(computer_id,family_id,process_id,msg_num,dmx_attr,process_type,time_quota,task_dur):
    """This keyword is to send a msg to target process for create hand.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -sl -c process_type time_quota task_dur

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
    | msg_num     | Yes  | the msg number                              |
    | dmx_attr    | Yes  | dilivery width                              |
    | process_type| Yes  | Type(hand group)of the process to be created|
    | time_quota  | Yes  | the time limited                            |
    | task_dur    | Yes  | task running time                           |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process create hand with sleep unconcern timeout | 0x0000 0x**** 0x0000 0x**** 0xffff11 0x1 0x20 0x10|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -sl -c %s %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,process_type,time_quota,task_dur)
    out = connections.execute_mml_without_check(command)
    
    match = re.search(r"\bprocess_id:\s*([0-9a-fx]*)", out, re.I)
    if match is not None:
       return match.group(1)
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_create_hand_with_while_unconcern_timeout(computer_id,family_id,process_id,msg_num,dmx_attr,process_type,time_quota,task_dur):
    """This keyword is to send a msg to target process for create hand.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -dl -c process_type time_quota task_dur

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
    | msg_num     | Yes  | the msg number                              |
    | dmx_attr    | Yes  | dilivery width                              |
    | process_type| Yes  | Type(hand group)of the process to be created|
    | time_quota  | Yes  | the time limited                            |
    | task_dur    | Yes  | task running time                           |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process create hand with while unconcern timeout | 0x0000 0x**** 0x0000 0x**** 0xffff11 0x1 0x20 0x10|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -dl -c %s %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,process_type,time_quota,task_dur)
    out = connections.execute_mml_without_check(command)
    
    match = re.search(r"\bprocess_id:\s*([0-9a-fx]*)", out, re.I)
    if match is not None:
       return match.group(1)
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def change_endless_loop_interval_threshold(computer_id,family_id,process_id,interval,threshold):
    """This keyword is to send a msg to target process to set the interval and threshold.

    #COMMAND: ILLGTestCli -- -i computer_id family_id process_id interval threshold

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | interval    | Yes  | endless loop monitoring interval            |
    | threshold   | Yes  | endless loop threshold for kill hand        |
   
    | Return value | command execution result |

    Example
    | result | change endless loop interval threshold | 0x0000 0xA014 0x0 0x0 0x0|
    """
    command='ILLGTestCli -- -i %s %s %s %s %s '%(computer_id,family_id,process_id,interval,threshold)
    out = connections.execute_mml_without_check(command)

    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'


def reset_endless_loop_interval_threshold_to_ldap(computer_id,family_id,process_id):
    """This keyword is to send a msg to target process to reset the endless loop value

    #COMMAND: ILLGTestCli -- -j computer_id family_id 

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | Return value | command execution result |

    Example
    | result |reset endless loop interval threshold to ldap| 0x0000 0xA014 |
    """
    command='ILLGTestCli -- -j %s %s %s'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)

    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_create_hand_with_stateful_procedure_unconcern_timeout(computer_id,family_id,process_id,msg_num,dmx_attr,process_type,time_quota,task_dur,sp_layer_number):
    """This keyword is to send a msg to target process for create hand.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -sp sp_layer_number -c process_type time_quota task_dur

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
    | msg_num     | Yes  | the msg number                              |
    | dmx_attr    | Yes  | dilivery width                              |
    | process_type| Yes  | Type(hand group)of the process to be created|
    | time_quota  | Yes  | the time limited                            |
    | task_dur    | Yes  | task running time                           |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process create hand with stateful procedure unconcern timeout | 0x0000 0x**** 0x0000 0x**** 0xffff11 0x1 0x20 0x10 0x1|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -sp %s -c %s %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,sp_layer_number,process_type,time_quota,task_dur)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        match = re.search(r"\bprocess_id:\s*([0-9a-fx]*)", out, re.I)
        if match is not None:
            return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def use_diagste_to_get_hand_count(computer_id,family_id):
    """This keyword is to get hand count of prb family using diagste tool.

    #COMMAND: ./diagste -m hum -u computer_id -f family_id -r han -t  

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
   
    | Return value | command execution result |

    Example
    | result | use diagste to get hand count | 0000 00a0 |
    """
    command='diagste -m hum -u %s -f %s -r han -t tcnt'%(computer_id,family_id)
    out = connections.execute_mml_without_check(command)
    
    
    match = re.search(r"\bactive hands \s*([0-9]*)", out, re.I)
    if match is not None:
                from string import atoi
                return atoi(str(match.group(1)), 10)
    else:
        return 'the return is wrong'

def start_libgen_message_performance_test(config_file,*args):
    """This keyword is to analyse the libgen msg test data

    #COMMAND: ./perftest.py sthread.ini  

    | Parameters  | Man. | Description                                 |
    | config_file | Yes  | appoint the config file                     |
    | args        | Yes  | msg test base data for compare              |
    | Return value | command execution result |

    Example
    | result | start libgen message performance test | sthread.ini * * * * * * * * |
    """  
    command='perftest.py %s'%(config_file)
    out = connections.execute_mml_without_check(command)

    keyr = re.compile("""case\[0\]: 1 hand Intra-family, average: ([0-9.]+) reqs/s.*?
^case\[1\]: 1 hand Inter-family, average: ([0-9.]+) reqs/s.*?
^case\[2\]: 1 hand Intra-family stateful, average: ([0-9.]+) reqs/s.*?
^case\[3\]: 1 hand Inter-family stateful, average: ([0-9.]+) reqs/s.*?
^case\[4\]: 20 hands Intra-family, average: ([0-9.]+) reqs/s.*?
^case\[5\]: 20 hands Inter-family, average: ([0-9.]+) reqs/s.*?
^case\[6\]: 20 hands Intra-family stateful, average: ([0-9.]+) reqs/s.*?
^case\[7\]: 20 hands Inter-family stateful, average: ([0-9.]+) reqs/s""", re.M)
    rerst = keyr.findall(out)
    isfail = False
    base =[]
    for arg in args:
         base.append(float(arg))
    if rerst is not None and rerst:
        result = [float(n) for n in rerst[0]]
        for i in range(len(result)):
            if result[i] < 0.1:
               result[i] = base[i]
        score = 0
        for i in range(8):
            if result[i] < base[i]:
                isfail = True
            score += result[i]/base[i]
        score = score * 100
        print result
        print base
        print 'score:', score
        if isfail:
            return 'failure'
        else:
            return 'success'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_set_c_timer(computer_id,family_id,process_id,msg_num,dmx_attr,timer,interval):
    """This keyword is to send a msg to target process for c set timer.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -ct s timer interval

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | msg_num          | Yes  | the msg number                              |
    | dmx_attr         | Yes  | dilivery width                              |
    | timer            | Yes  | Timer ID                                    |
    | interval         | Yes  | Timer interval                              |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process set c timer | 0x0000 0x**** 0x0000 0x**** 0xffff11 2 3|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -ct s %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,timer,interval)
    out = connections.execute_mml_without_check(command)

    print 'out:', out
    
    if out.index('success') > -1:
        return 'success'
    elif out.index('failure') > -1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_reset_c_timer(computer_id,family_id,process_id,msg_num,dmx_attr,timer,interval):
    """This keyword is to send a msg to target process for c reset timer.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -ct r timer interval

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | msg_num          | Yes  | the msg number                              |
    | dmx_attr         | Yes  | dilivery width                              |
    | timer            | Yes  | Timer ID                                    |
    | interval         | Yes  | Timer interval                              |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process reset c timer | 0x0000 0x**** 0x0000 0x**** 0xffff11 2 3|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -ct r %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,timer,interval)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_set_tnsdl_timer(computer_id,family_id,process_id,msg_num,dmx_attr,timer,interval):
    """This keyword is to send a msg to target process for TNSDL set timer.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -tt s timer interval

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | msg_num          | Yes  | the msg number                              |
    | dmx_attr         | Yes  | dilivery width                              |
    | timer            | Yes  | Timer ID                                    |
    | interval         | Yes  | Timer interval                              |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process set TNSDL timer | 0x0000 0x**** 0x0000 0x**** 0xffff11 2 3|
    """

    command='ILLGTestCli -- -r %s %s %s %s %s -tt s %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,timer,interval)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_reset_tnsdl_timer(computer_id,family_id,process_id,msg_num,dmx_attr,timer,interval):
    """This keyword is to send a msg to target process for TNSDL reset timer.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -tt r timer interval

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | msg_num          | Yes  | the msg number                              |
    | dmx_attr         | Yes  | dilivery width                              |
    | timer            | Yes  | Timer ID                                    |
    | interval         | Yes  | Timer interval                              |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process reset TNSDL timer | 0x0000 0x**** 0x0000 0x**** 0xffff11 2 3|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -tt r %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,timer,interval)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_read_c_timer(computer_id,family_id,process_id,msg_num,dmx_attr,timer):
    """This keyword is to send a msg to target process for c read timer.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -rt timer

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | msg_num          | Yes  | the msg number                              |
    | dmx_attr         | Yes  | dilivery width                              |
    | timer            | Yes  | Timer ID                                    |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process read c timer | 0x0000 0x**** 0x0000 0x**** 0xffff11 2|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -rt %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,timer)
    out = connections.execute_mml_without_check(command)

    if out.count('success') == 1:
        match = re.search(r"\bTimer interval is:\s*([0-9a-fx]*)", out, re.I)
        if match is not None:
            return match.group(1)
        else:
            return 'the return is wrong'  
    elif out.count('failure') == 1:
        if out.count('TIMER expired or unsetted') == 1:
            return 'TIMER expired or unsetted'
        else:
            return 'failure'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_inquery_timer_out(computer_id,family_id,process_id,msg_num,dmx_attr,timer):
    """This keyword is to send a msg to target process for inquery if timer out.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -to timer

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | msg_num          | Yes  | the msg number                              |
    | dmx_attr         | Yes  | dilivery width                              |
    | timer            | Yes  | Timer ID                                    |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process read c timer | 0x0000 0x**** 0x0000 0x**** 0xffff11 2|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -to %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,timer)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        if out.count('Given timer is expired') == 1:
               return 'expired'
        else:
               return 'the return is wrong'  
    elif out.count('failure in timer operation') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_creat_mass_hand(computer_id,family_id,process_id,msg_num,dmx_attr,hand_number,process_type,time_quota,time_duration):
    """This keyword is to send a msg to target process for creat mass tnsdl hand.
    
    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -mc hand_number -c process_type time_quota time_duration

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | msg_num          | Yes  | the msg number                              |
    | dmx_attr         | Yes  | dilivery width                              |
    | hand_number      | Yes  | hand number need to creat in this group     |
    | process_type     | Yes  | hand group                                  |
    | time_quota       | Yes  | time quota                                  |
    | time_duration    | Yes  | time duration                               |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process creat mass hand | 0x0000 0x**** 0x0000 0x**** 0xffff11 10 1 2 2|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -mc %s -c %s %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,hand_number,process_type,time_quota,time_duration)
    out = connections.execute_mml_without_check(command)
  
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_creat_failure_reason(computer_id,family_id,process_id,msg_num,dmx_attr,frfamily_id):
    """This keyword is to send a msg to target process for creat failure reason.
    
    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -fr frfamily_id

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    | msg_num          | Yes  | the msg number                              |
    | dmx_attr         | Yes  | dilivery width                              |
    | frfamily_id      | Yes  | get fail reason from this family            |
    
   
    | Return value | command execution result |

    Example
    | result | send msg to target process creat fail reason | 0x0000 0x**** 0x0000 0x**** 0xffff11 0x0ff3|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -fr %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,frfamily_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        match = re.search(r"\bFamily failed reason is \s*([a-zA-Z_]*)", out, re.I)
        if match is not None:
            return match.group(1)
        else:
            return 'the return is wrong'  
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'
    
def send_msg_to_target_process_clear_all_hands(computer_id,family_id,process_id,msg_num,dmx_attr):
    """This keyword is to send a msg to target process for clear all hand.
    
    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -ta

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | msg_num          | Yes  | the msg number                              |
    | dmx_attr         | Yes  | dilivery width                              |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process clear all hand | 0x0000 0x**** 0x0000 0x**** 0xffff11 |
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -ta'%(computer_id,family_id,process_id,msg_num,dmx_attr)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'
    
def send_msg_to_target_process_creat_specific_hand(computer_id,family_id,process_id,msg_num,dmx_attr,appointed_process_id,appointed_hand_group,time_quota,time_duration):
    """This keyword is to send a msg to target process for clear all hand.
    
    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -sc appointed_process_id -c apponited_hand_group time_quota time_duration

    | Parameters           | Man. | Description                                 |
    | computer_id          | Yes  | target computer address                     |
    | family_id            | Yes  | target family addres                        |
    | process_id           | Yes  | target process id                           |
    | msg_num              | Yes  | the msg number                              |
    | dmx_attr             | Yes  | dilivery width                              |
    | appointed_process_id | Yes  | appointed process id                        |
    | apponited_hand_group | Yes  | apponited_hand_group                        |
    | time_quota           | Yes  | time quota                                  |
    | time_duration        | Yes  | time duration                               |
    
    | Return value | command execution result |

    Example
    | result | send msg to target process creat specific hand | 0x0000 0x**** 0x0000 0x**** 0xffff11 1 0 1 3 2 |
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -sc %s -c %s %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,appointed_process_id,appointed_hand_group,time_quota,time_duration)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_msg_to_target_process_restart_hand(computer_id,family_id,process_id,msg_num,dmx_attr,restarter,restarted):
    """This keyword is to send a msg to target process for restart hand.
    
    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -rh restarter restarted

    | Parameters       | Man. | Description                                              |
    | computer_id      | Yes  | target computer address                                  |
    | family_id        | Yes  | target family addres                                     |
    | process_id       | Yes  | target process id                                        |
    | msg_num          | Yes  | the msg number                                           |
    | dmx_attr         | Yes  | dilivery width                                           |
    | restarter        | Yes  | Restart owner process id. For example 0x0( family master)|
    | restarted        | Yes  | target process id which request to be restarted          |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process restart hand | 0x0000 0x**** 0x0000 0x**** 0xffff11 0 2 |
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -rh %s %s '%(computer_id,family_id,process_id,msg_num,dmx_attr,restarter,restarted)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'
    
def send_msg_to_target_process_get_next_reserved(computer_id,family_id,process_id,msg_num,dmx_attr,hand_group,input_process_id):
    """This keyword is to send a msg to target process for get next reserved process id.
    
    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -gn hand_group input_process_id

    | Parameters         | Man. | Description                                              |
    | computer_id        | Yes  | target computer address                                  |
    | family_id          | Yes  | target family addres                                     |
    | process_id         | Yes  | target process id                                        |
    | msg_num            | Yes  | the msg number                                           |
    | dmx_attr           | Yes  | dilivery width                                           |
    | hand_group         | Yes  | hand group id                                            |
    | input_process_id   | Yes  | input hand process id                                    |
   
    | Return value | command execution result |

    Example
    | result | send msg to target process get next reserved | 0x0000 0x**** 0x0000 0x**** 0xffff11 0 2 |
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -gn %s %s '%(computer_id,family_id,process_id,msg_num,dmx_attr,hand_group,input_process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('failure') == 1:
        match = re.search(r"\bnext_reserved process_id is \s*([0-9xa-zA-Z/]*)", out, re.I)
        if match is not None:
            return match.group(1)
        else:
            match = re.search(r"\brecord not found", out, re.I) 
            if match is not None:
                return match.group(1)
            else:
                return 'the return is wrong'
    elif out.count('success') == 1:
        match = re.search(r"\bnext_reserved process_id is \s*([0-9xa-zA-Z/]*)", out, re.I)
        if match is not None:
            return match.group(1)
    else:
        return 'the return is wrong'

def send_msg_to_target_process_find_focus(computer_id,family_id,process_id,msg_num,dmx_attr,target_family,appointed_process_id):
    """This keyword is to send a msg to target process for find focus of appointed process.
    
    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -ff target_family appointed_process_id

    | Parameters           | Man. | Description                                             |
    | computer_id          | Yes  | target computer address                                 |
    | family_id            | Yes  | target family address                                   |
    | process_id           | Yes  | target process id                                       |
    | msg_num              | Yes  | the msg number                                          |
    | dmx_attr             | Yes  | dilivery width                                          |
    | target_family        | Yes  | appointed family                                        |
    | appointed_process_id | Yes  | appointed process id, to find the focus of this process |
    
    | Return value | command execution result |

    Example
    | result | send msg to target process find focus | 0x0000 0x**** 0x0000 0x**** 0xffff11 1|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -ff %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,target_family,appointed_process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        match = re.search(r"\bfocus is \s*([0-9xa-zA-Z/]*)", out, re.I)
        if match is not None:
            return match.group(1)
        else:
            return 'the return is wrong'  
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'


def send_msg_to_target_process_count_hand(computer_id,family_id,process_id,msg_num,dmx_attr,target_family,hand_group):
    """This keyword is to send a msg to target process for count hand in appointed hand group.
    
    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -hc target_family hand_group

    | Parameters           | Man. | Description                                             |
    | computer_id          | Yes  | target computer address                                 |
    | family_id            | Yes  | target family address                                   |
    | process_id           | Yes  | target process id                                       |
    | msg_num              | Yes  | the msg number                                          |
    | dmx_attr             | Yes  | dilivery width                                          |
    | target_family        | Yes  | appointed family                                        |
    | hand_group           | Yes  | hand group                                              |
    
    | Return value | command execution result |

    Example
    | result | send msg to target process count hand | 0x0000 0x**** 0x0000 0x**** 0xffff11 1|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -hc %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,target_family,hand_group)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        match = re.search(r"\bhand process count is \s*([0-9xa-zA-Z/]*)", out, re.I)
        if match is not None:
            return match.group(1)
        else:
            return 'the return is wrong'  
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'   

def send_msg_to_target_process_alive_check(computer_id,family_id,process_id,msg_num,dmx_attr,hand_process):
    """This keyword is to send a msg to target process for check if hand is alive.
    
    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -ha hand_process

    | Parameters           | Man. | Description                                             |
    | computer_id          | Yes  | target computer address                                 |
    | family_id            | Yes  | target family address                                   |
    | process_id           | Yes  | target process id                                       |
    | msg_num              | Yes  | the msg number                                          |
    | dmx_attr             | Yes  | dilivery width                                          |
    | hand_process         | Yes  | hand process to be checked                              |
    
    | Return value | command execution result |

    Example
    | result | send msg to target process alive check | 0x0000 0x**** 0x0000 0x**** 0xffff11 1|
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -ha %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,family_id,hand_process)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        match = re.search(r"\bhand is \s*([a-z ]*)", out, re.I)
        if match is not None:
            return match.group(1)
        else:
            return 'the return is wrong'  
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'
    
def create_hand_and_save_one_message(computer_id,family_id,process_id):
    """This keyword is to create normal hand process and save one message into it's SAVE queue.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -sq

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | create hand and save one message| 0x0000 0x**** 0x0000|
    """
    command='ILWMTestCli -- -r %s %s %s -sq'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def create_hand_and_goes_into_stateful_state(computer_id,family_id,process_id):
    """This keyword is to create normal hand process and goes into stateful receiving message state.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -sp

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | create hand and goes into stateful state| 0x0000 0x**** 0x0000|
    """
    command='ILWMTestCli -- -r %s %s %s -sp'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def create_dead_loop_hand_process(computer_id,family_id,process_id,process_type,time_quota,task_dur):
    """This keyword is to create dead loop hand process.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -dl process_type time_quota task_dur

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | process_type     | Yes  | Type(hand group)of the process to be created|
    | time_quota       | Yes  | the time limited                            |
    | task_dur         | Yes  | task running time                           |
    
    | Return value | command execution result |

    Example
    | result | create dead loop hand process| 0x0000 0x**** 0x0000 0x1 0x20 0x10|
    """
    command='ILWMTestCli -- -r %s %s %s -dl %s %s %s'%(computer_id,family_id,process_id,process_type,time_quota,task_dur)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_warming_test_message_and_can_handle(computer_id,family_id,process_id,msg_num,delivery_range,msg_count):
    """This keyword is to send test message with given delivery range to test process.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -msg msg_num delivery_range msg_count -s

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | msg_num          | Yes  | the msg num                                 |
    | delivery_range   | Yes  | dilivery width                              |
    | msg_count        | Yes  | the msg sending count                       |
      
    | Return value | command execution result |

    Example
    | result | send warming test message and can handle| 0x0000 0x**** 0x0000 0x**** 0x0 0x2|
    """
    command='ILWMTestCli -- -r %s %s %s -msg %s %s %s -s'%(computer_id,family_id,process_id,msg_num,delivery_range,msg_count)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') >0:
        return 'success'
    elif out.count('failure') >= 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_warming_test_message_and_can_handle_with_time_quota(computer_id,family_id,process_id,msg_num,delivery_range,msg_count,time_value):
    """This keyword is to send test message with given delivery range to test process.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -msg msg_num delivery_range msg_count -s time_value

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | msg_num          | Yes  | the msg num                                 |
    | delivery_range   | Yes  | dilivery width                              |
    | msg_count        | Yes  | the msg sending count                       |
    | time_value       | Yes  | send a msg and wait ack in appoint time     |
      
    | Return value | command execution result |

    Example
    | result | send warming test message and can handle| 0x0000 0x**** 0x0000 0x**** 0x0 0x2 300|
    """
    command='ILWMTestCli -- -r %s %s %s -msg %s %s %s -s %s'%(computer_id,family_id,process_id,msg_num,delivery_range,msg_count,time_value)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') >0:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_warming_request_message(computer_id,family_id,process_id):
    """This keyword is to send warming request message through socket.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -wrw

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |      

    | Return value | command execution result |

    Example
    | result | send warming request message| 0x0000 0x**** 0x0|
    """
    command='ILWMTestCli -- -r %s %s %s -wrw'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('warming possible success') == 1:
        return 'success'
    elif out.count('warming possible failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_warming_connection_request_in_sp(computer_id,family_id,process_id,sp_ipaddr,sp_ipport):
    """This keyword is to send warming connection request message through socket in sp.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -wcr sp_ipaddr sp_ipport

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | sp_ipaddr        | Yes  | sp unit ip address                          |
    | process_id       | Yes  | sp unit ip port num                         |

    | Return value | command execution result |

    Example
    | result | send warming connection request in sp| 0x0000 0x**** 0x0 192.168.23.1 3333|
    """
    command='ILWMTestCli -- -r %s %s %s -wcr %s %s'%(computer_id,family_id,process_id,sp_ipaddr,sp_ipport)
    out = connections.execute_mml_without_check(command)
    
    if out.count('port alloc success') == 1:
        return 'success'
    elif out.count('port alloc failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_warming_data_transfer_message_in_wo(computer_id,family_id,process_id,sp_ipaddr,sp_ipport):
    """This keyword is to send warming data transfer message through socket in wo.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -wdt sp_ipaddr sp_ipport

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | sp_ipaddr        | Yes  | sp unit ip address                          |
    | process_id       | Yes  | sp unit ip port num                         |

    | Return value | command execution result |

    Example
    | result | send warming data transfer message in wo| 0x0000 0x**** 0x0 192.168.23.1 3333|
    """
    command='ILWMTestCli -- -r %s %s %s -wdt %s %s'%(computer_id,family_id,process_id,sp_ipaddr,sp_ipport)
    out = connections.execute_mml_without_check(command)
    
    if out.count('data transfer success') == 1:
        return 'success'
    elif out.count('data transfer failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_warming_wake_up_message(computer_id,family_id):
    """This keyword is to send warming wake up message through socket.

    #COMMAND: ILWMTestCli -- -r computer_id family_id -wrw

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
      
    | Return value | command execution result |

    Example
    | result | send warming wake up message| 0x0000 0x****|
    """
    command='ILWMTestCli -- -r %s %s -wu'%(computer_id,family_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_warming_request_message_in_sp(computer_id,family_id,process_id,last_msg_computer,sequence_num):
    """This keyword is to send warming request message through socket in sp.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -wrs last_msg_computer sequence_num

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           | 
    | last_msg_computer| Yes  | the computer id last msg handled            |
    | sequence_num     | Yes  | the sequence num last msg handled           |     
      
    | Return value | command execution result |

    Example
    | result | send warming request message in sp| 0x0000 0x**** 0x0 0x0000 0x12345678|
    """
    command='ILWMTestCli -- -r %s %s %s -wrs %s %s'%(computer_id,family_id,process_id,last_msg_computer,sequence_num)
    out = connections.execute_mml_without_check(command)
    
    if out.count('warming possible success') == 1:
        return 'success'
    elif out.count('warming possible failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'


def send_warming_cancel_message(computer_id,family_id,process_id):
    """This keyword is to send warming cancel message through socket.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -wcn

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
      
    | Return value | command execution result |

    Example
    | result | send warming cancel message| 0x0000 0x**** 0x0|
    """
    command='ILWMTestCli -- -r %s %s %s -wcn'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('cancel success') == 1:
        return 'success'
    elif out.count('cancel failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'


def send_warming_complete_message(computer_id,family_id,process_id):
    """This keyword is to send warming complete msg to prb in wo.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -wcp

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
      
    | Return value | command execution result |

    Example
    | result | send warming complete message| 0x0000 0x**** 0x0|
    """
    command='ILWMTestCli -- -r %s %s %s -wcp'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('warming success') == 1:
        return 'success'
    elif out.count('warming failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_change_with_warm_variable_message(computer_id,family_id,process_id):
    """This keyword is to send change with-warm variable message to test process.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -cv

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
      
    | Return value | command execution result |

    Example
    | result | send change with warm variable message| 0x0000 0x**** 0x0|
    """
    command='ILWMTestCli -- -r %s %s %s -cv 1'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('change variable success') == 1:
        return 'success'
    elif out.count('change variable failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_change_variable_with_needless_warm_message(computer_id,family_id,process_id):
    """This keyword is to send change variable with needless warm message to test process.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -cv

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
      
    | Return value | command execution result |

    Example
    | result | send change variable with needless warm message| 0x0000 0x**** 0x0|
    """
    command='ILWMTestCli -- -r %s %s %s -cv 2'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('change variable success') == 1:
        return 'success'
    elif out.count('change variable failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def set_timer_needing_warming(computer_id,family_id,process_id,time_interval):
    """This keyword is to send msg to testproc set a timer needing warming used by warming.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -t time_interval sub_id

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | time_interval    | Yes  | timer value                                 |
    | sub_id           | Yes  | indicate what kind of timer you want to set |
      
    | Return value | command execution result |

    Example
    | result | set timer needing warming| 0x0000 0x**** 0x0 10 2|
    """
    command='ILWMTestCli -- -r %s %s %s -t %s 2'%(computer_id,family_id,process_id,time_interval)
    out = connections.execute_mml_without_check(command)
    
    if out.count('set timer success') == 1:
        return 'success'
    elif out.count('set timer failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'
        
def set_timer_needing_warming_used_by_control_swo(computer_id,family_id,process_id,time_interval):
    """This keyword is to send msg to testproc set a timer needing warming used by warming before control swo.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -t time_interval sub_id

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | time_interval    | Yes  | timer value                                 |
    | sub_id           | Yes  | indicate what kind of timer you want to set |
      
    | Return value | command execution result |

    Example
    | result | set timer needing warming used by control swo| 0x0000 0x**** 0x0 10 2|
    """
    command='ILWMTestCli -- -r %s %s %s -t %s 3 4'%(computer_id,family_id,process_id,time_interval)
    out = connections.execute_mml_without_check(command)
    
    if out.count('set timer success') == 1:
        return 'success'
    elif out.count('set timer failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'
        
def query_timer_receiving_situation(computer_id,family_id,process_id):
    """This keyword is to send msg to testproc query if received timer time out message.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -a

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
      
    | Return value | command execution result |

    Example
    | result | query timer receiving situation| 0x0000 0x**** 0x0|
    """
    command='ILWMTestCli -- -r %s %s %s -a'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def set_timer_needless_warming(computer_id,family_id,process_id,time_interval):
    """This keyword is to send msg to testproc set a timer needless warming used by warming.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -t time_interval sub_id

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | time_interval    | Yes  | timer value                                 |
    | sub_id           | Yes  | indicate what kind of timer you want to set |
      
    | Return value | command execution result |

    Example
    | result | set timer needless warming| 0x0000 0x**** 0x0 10 2|
    """
    command='ILWMTestCli -- -r %s %s %s -t %s 1'%(computer_id,family_id,process_id,time_interval)
    out = connections.execute_mml_without_check(command)
    
    if out.count('set timer success') == 1:
        return 'success'
    elif out.count('set timer failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def create_hand_used_by_warming(computer_id,family_id,process_id,time_quota):
    """This keyword is to send msg to testproc create hand used by warming.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -ch time_quota

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | time_quota       | Yes  | timer value                                 |
      
    | Return value | command execution result |

    Example
    | result | create hand used by warming| 0x0000 0x**** 0x0 10|
    """
    command='ILWMTestCli -- -r %s %s %s -ch %s'%(computer_id,family_id,process_id,time_quota)
    out = connections.execute_mml_without_check(command)
    
    if out.count('create hand success') == 1:
        match = re.search(r"\s*process id of created hand in testproc:\s*([0-9a-fx]*)", out, re.I)
        if match is not None:
            return 'success', match.group(1)
    elif out.count('create hand failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def refresh_hand_used_by_warming(computer_id,family_id,process_id,rf_process,rf_time):
    """This keyword is to send msg to testproc refresh hand used by warming.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -rf rf_process rf_time

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | rf_process       | Yes  | the hand process id which need to be refresh|
    | rf_time          | Yes  | the refresh time limited                    |
      
    | Return value | command execution result |

    Example
    | result | refresh hand used by warming| 0x0000 0x**** 0x0 1 100|
    """
    command='ILWMTestCli -- -r %s %s %s -rf %s %s'%(computer_id,family_id,process_id,rf_process,rf_time)
    out = connections.execute_mml_without_check(command)
    
    if out.count('refresh hand success') == 1:
        return 'success'
    elif out.count('refresh hand failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'


def warming_success_or_failure_inquire(computer_id,family_id,process_id,inquire_hand):
    """This keyword is to inquire warming success or failure for given process.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -iw inquire_hand

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | inquire_hand     | Yes  | given process id for inquire warming success|
      
    | Return value | command execution result |

    Example
    | result | warming success or failure inquire| 0x0000 0x**** 0x0000 0x0|
    """
    command='ILWMTestCli -- -r %s %s %s -iw %s'%(computer_id,family_id,process_id,inquire_hand)
    out = connections.execute_mml_without_check(command)
    
    if out.count('Family is warmed') == 1:
        return 'success'
    elif out.count('Family is un-warmed') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def check_if_time_quota_exist(computer_id,family_id,process_id):
    """This keyword is to use diagste to check if time quota exist of a hand process.

    #COMMAND: diagste -u computer_id -f family_id -p process_id -r han -t idata -m hum

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
      
    | Return value | command execution result |

    Example
    | result | check if time quota exist| 0x0000 0x**** 0x0|
    """
    command='diagste -u %s -f %s -p %s -r han -t idata -m hum'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('refresh hand timer  YES') == 1:
        return 'success'
    elif out.count('refresh hand timer   NO') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def check_if_timer_exist(computer_id,family_id):
    """This keyword is to use diagste to check if timer exist.

    #COMMAND: diagste -u computer_id -f family_id -r tim -t icnt -m hum

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
      
    | Return value | command execution result |

    Example
    | result | check if timer exist| 0x0000 0x****|
    """
    command='diagste -u %s -f %s -r tim -t icnt -m hum'%(computer_id,family_id)
    out = connections.execute_mml_without_check(command)
    
    
    if out.count('no active timers') == 1:
        return 'failure'
    elif out.count('active timers') == 1:
        return 'success'
    else:
        return 'the return is wrong'

def check_if_hand_related_data_equal(wo_computer_id,sp_computer_id,family_id,process_id):
    """This keyword is to use diagste to check if hand related data equal.

    #COMMAND: diagste -u computer_id -f family_id -p process_id -r han -t idata -m hum

    | Parameters       | Man. | Description                                 |
    | wo_computer_id   | Yes  | wo unit computer address                    |
    | sp_computer_id   | Yes  | sp unit computer address                    |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
      
    | Return value | command execution result |

    Example
    | result | check if hand related data equal| 0x0000 0x0100 0x****|
    """
    command='diagste -u %s -f %s -p %s -r han -t idata -m hum'%(wo_computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
  
    out_wo = out.split("rtimer expired time")[0]
    print out_wo
    
    
    out_rtimer = out.split("rtimer expired time")[1]
    print "out str: %s<end>" % out_rtimer
    
    rr = re.compile(r"time\s*(\d+?)\.(\d+)")
    
    out_rtimer_wo = rr.findall(out_rtimer)[0]
    print out_rtimer_wo
    ms_wo_time = int(out_rtimer_wo[0])*1000 + int(out_rtimer_wo[1])
    
    
    
    command='diagste -u %s -f %s -p %s -r han -t idata -m hum'%(sp_computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    out_sp = out.split("rtimer expired time")[0]
    print out_sp

    out_rtimer = out.split("rtimer expired time")[1]
    print "out str: %s<end>" % out_rtimer
    
    rr = re.compile(r"time\s*(\d+?)\.(\d+)")
    
    out_rtimer_sp = rr.findall(out_rtimer)[0]
    print out_rtimer_sp
    ms_sp_time = int(out_rtimer_sp[0])*1000 + int(out_rtimer_sp[1])
    
    
    diff_time = ms_sp_time - ms_wo_time
    if (diff_time <= 250 and diff_time >= 200)and(out_wo == out_sp):
        return 'success'
    else:
        return 'failure'



def check_if_with_warm_variable_equal(wo_computer_id,sp_computer_id,family_id,process_id):
    """This keyword is to use diagste to check if with warm variable equal.

    #COMMAND: diagste -u computer_id -f family_id -p process_id -r hmem -t get -m hum

    | Parameters       | Man. | Description                                 |
    | wo_computer_id   | Yes  | wo unit computer address                    |
    | sp_computer_id   | Yes  | sp unit computer address                    |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
      
    | Return value | command execution result |

    Example
    | result | check if with warm variable equal| 0x0000 0x0100 0x**** 0x1|
    """
    command='diagste -u %s -f %s -p %s -r hmem -t get -d -m hum'%(wo_computer_id,family_id,process_id)
    out_wo = connections.execute_mml_without_check(command)
    match = re.search(r"\bplain_variable_text\s*([0-9 ]*)", out_wo, re.I)
    print match.group(1)
    var_wo = match.group(1)
    
    command='diagste -u %s -f %s -p %s -r hmem -t get -d -m hum'%(sp_computer_id,family_id,process_id)
    out_sp = connections.execute_mml_without_check(command)
    match = re.search(r"\bplain_variable_text\s*([0-9 ]*)", out_sp, re.I)
    print match.group(1)
    var_sp = match.group(1)
    
    if (var_wo == var_sp):
        return 'success'
    else:
        return 'failure'


def check_if_timer_value_equal(wo_computer_id,sp_computer_id,family_id):
    """This keyword is to use diagste to check if timer value equal.

    #COMMAND: diagste -u computer_id -f family_id -r tim -t idata -m hum

    | Parameters       | Man. | Description                                 |
    | wo_computer_id   | Yes  | wo unit computer address                    |
    | sp_computer_id   | Yes  | sp unit computer address                    |
    | family_id        | Yes  | target family addres                        |
      
    | Return value | command execution result |

    Example
    | result | check if timer value equal| 0x0000 0x0100 0x****|
    """
    command='diagste -u %s -f %s -r tim -t idata -m hum'%(wo_computer_id,family_id)
    out_wo = connections.execute_mml_without_check(command)

    match = re.search(r"\btime \s*([0-9.]*)", out_wo, re.I)
    print match.group(1)
    s = match.group(1)
    l_time = s.split('.')
    ms_wo_time = int(l_time[0])*1000 + int(l_time[1])
    
    match = re.search(r"\bproc \s*([0-9]*)", out_wo, re.I)
    proc_wo = match.group(1)
    print proc_wo
   
    command='diagste -u %s -f %s -r tim -t idata -m hum'%(sp_computer_id,family_id)
    out_sp = connections.execute_mml_without_check(command)
    match = re.search(r"\btime \s*([0-9.]*)", out_sp, re.I)
    print match.group(1)
    s = match.group(1)
    l_time = s.split('.')
    ms_sp_time = int(l_time[0])*1000 + int(l_time[1])

    match = re.search(r"\bproc \s*([0-9]*)", out_sp, re.I)
    proc_sp = match.group(1)
    print proc_sp
    
    diff_time = ms_sp_time - ms_wo_time
    print diff_time
    if (diff_time <= 250 and diff_time >= 200 )and(proc_wo == proc_sp):
        return 'success'
    else:
        return 'failure'

def check_if_time_quota_of_hand_equal(wo_computer_id,sp_computer_id,family_id,process_id):
    """This keyword is to use diagste to check if time quota of hand equal.

    #COMMAND: diagste -u computer_id -f family_id -p process_id -r han -t idata -m hum

    | Parameters       | Man. | Description                                 |
    | wo_computer_id   | Yes  | wo computer address                         |
    | sp_computer_id   | Yes  | sp computer address                         |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
      
    | Return value | command execution result |

    Example
    | result | check if time quota of hand equal| 0x0000 0x0100 0x**** 0x0|
    """
    command='diagste -u %s -f %s -p %s -r han -t idata -m hum'%(wo_computer_id,family_id,process_id)
    out_wo = connections.execute_mml_without_check(command)
    match = re.search(r"\brtimer expired time  time \s*([0-9.]*)", out_wo, re.I)
    s = match.group(1)
    l_time = s.split('.')
    ms_wo_time = int(l_time[0])*1000 + int(l_time[1])

    command='diagste -u %s -f %s -p %s -r han -t idata -m hum'%(sp_computer_id,family_id,process_id)
    out_sp = connections.execute_mml_without_check(command)
    match = re.search(r"\brtimer expired time  time \s*([0-9.]*)", out_sp, re.I)
    s = match.group(1)
    l_time = s.split('.')
    ms_sp_time = int(l_time[0])*1000 + int(l_time[1])
    diff_time = ms_sp_time - ms_wo_time
    print diff_time
    if (diff_time <= 250 and diff_time >= 200 ):
        return 'success'
    else:
        return 'failure'
		
def absolute_send_a_msg_to_target_process(computer_id,family_id,process_id,msg_num,dmx_attr):
    """This keyword is to send a msg to target process by using libgen routine absolute_send.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -tras

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
    | msg_num     | Yes  | the msg number                              |
    | dmx_attr    | Yes  | dilivery width                              |
   
    | Return value | command execution result |

    Example
    | result | absolute send a msg to target process | 0x0000 0xA014 0x0000 0x0 0xffff11 |
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -tras'%(computer_id,family_id,process_id,msg_num,dmx_attr)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        match = re.search(r"\bsender pid is:\s*([/0-9a-fx]*)", out, re.I)
        if match is not None:
            return match.group(1)
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'	

def master_send_a_msg_to_hand_process(computer_id,family_id,process_id,msg_num,dmx_attr,han_msg_num,hand_process):
    """This keyword is to ask master to send a msg to its target hand process.

    #COMMAND: ILLGTestCli -- -r computer_id family_id process_id msg_num dmx_attr -sh 

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
    | msg_num     | Yes  | the msg number                              |
    | dmx_attr    | Yes  | dilivery width                              |
    | han_msg_num | Yes  | the msg number will be sent from mas to hand|
    | hand_process| Yes  | target hand process id to recv the msg      |
	   
    | Return value | command execution result |

    Example
    | result | master send a msg to hand process | 0x0000 0xA014 0x0000 0x0 0xffff11 |
    """
    command='ILLGTestCli -- -r %s %s %s %s %s -sh %s %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,han_msg_num,hand_process)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def send_a_msg_to_target_process_with_msg_ack_type(computer_id,family_id,process_id,msg_num,dmx_attr,msg_count,msg_ack_type):
    """This keyword is to send a msg to target process with msg ack type.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -msg msg_num dmx_attr msg_count -i msg_ack_type

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
    | msg_num     | Yes  | the msg number                              |
    | dmx_attr    | Yes  | dilivery width                              |
    | msg_count   | Yes  | the msg sending count                       |
    | msg_ack_type| Yes  | different address type used to ack          |
   
    | Return value | command execution result |

    Example
    | result | send a msg to target process with msg ack type| 0x0000 0x1773 0x0000 0x6034 0xffff11 0x1 0x1|
    """
    command='ILWMTestCli -- -r %s %s %s -msg %s %s %s -i %s'%(computer_id,family_id,process_id,msg_num,dmx_attr,msg_count,msg_ack_type)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def change_buffer_needing_warming(computer_id,family_id,process_id):
    """This keyword is to send a msg to tell process to modify an already existed buffer needing warming.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -bm

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
   
    | Return value | command execution result |

    Example
    | result | change buffer needing warming| 0x0000 0x1773 0x0000|
    """
    command='ILWMTestCli -- -r %s %s %s -bm'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def free_allocated_buffer(computer_id,family_id,process_id,sub_id):
    """This keyword is to send a msg to tell process to free a buffer.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -bm

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
    | sub_id      | Yes  | specify which buffer do you want to free    |
   
    | Return value | command execution result |

    Example
    | result | free allocated buffer| 0x0000 0x1773 0x0000 1|
    """
    command='ILWMTestCli -- -r %s %s %s -bf %s'%(computer_id,family_id,process_id,sub_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def set_a_buffer_needless_warming(computer_id,family_id,process_id):
    """This keyword is to send a msg to tell process to set a buffer needless warming.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -bwnl

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
   
    | Return value | command execution result |

    Example
    | result | set a buffer needless warming| 0x0000 0x1773 0x0000 |
    """
    command='ILWMTestCli -- -r %s %s %s -bwnl'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def set_a_buffer_needing_warming(computer_id,family_id,process_id):
    """This keyword is to send a msg to tell process to set a needing warming buffer.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -ba

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |
   
    | Return value | command execution result |

    Example
    | result | set a buffer needing warming| 0x0000 0x1773 0x0000 |
    """
    command='ILWMTestCli -- -r %s %s %s -ba'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def set_timer_needing_warming_and_receive_time_quota(computer_id,family_id,process_id,time_interval,wait_ack_time):
    """This keyword is to send msg to testproc set a timer needing warming used by warming and wait ack.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -t time_interval sub_id option wait_ack_time

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | time_interval    | Yes  | timer value                                 |
    | sub_id           | Yes  | indicate what kind of timer you want to set |
    | option           | Yes  | process ack msg immediately or not          |
    | wait_ack_time    | Yes  | time for wait msg ack                       |
      
    | Return value | command execution result |

    Example
    | result | set timer needing warming| 0x0000 0x**** 0x0 10 2 2 20|
    """
    command='ILWMTestCli -- -r %s %s %s -t %s 2 2 %s'%(computer_id,family_id,process_id,time_interval,wait_ack_time)
    out = connections.execute_mml_without_check(command)
    
    if out.count('set timer success') == 1:
        return 'success'
    elif out.count('set timer failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def set_timer_needless_warming_and_receive_time_quota(computer_id,family_id,process_id,time_interval,wait_ack_time):
    """This keyword is to send msg to testproc set a timer needless warming used by warming and wait ack.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -t time_interval sub_id option wait_ack_time

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | time_interval    | Yes  | timer value                                 |
    | sub_id           | Yes  | indicate what kind of timer you want to set |
    | option           | Yes  | process ack msg immediately or not          |
    | wait_ack_time    | Yes  | time for wait msg ack                       |
      
    | Return value | command execution result |

    Example
    | result | set timer needless warming| 0x0000 0x**** 0x0 10 2 2 20|
    """
    command='ILWMTestCli -- -r %s %s %s -t %s 1 2 %s'%(computer_id,family_id,process_id,time_interval,wait_ack_time)
    out = connections.execute_mml_without_check(command)
    
    if out.count('set timer success') == 1:
        return 'success'
    elif out.count('set timer failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def check_if_with_warm_buffer_equal(wo_computer_id,sp_computer_id,family_id,process_id):
    """This keyword is to use diagste to check if with warm buffer equal.

    #COMMAND: diagste -u computer_id -f family_id -p process_id -r hmem -t get -d -m hum

    | Parameters       | Man. | Description                                 |
    | wo_computer_id   | Yes  | wo unit computer address                    |
    | sp_computer_id   | Yes  | sp unit computer address                    |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
      
    | Return value | command execution result |

    Example
    | result | check if with warm buffer equal| 0x0000 0x0100 0x**** 0x1|
    """
    command='diagste -u %s -f %s -p %s -r hmem -t get -d -m hum'%(wo_computer_id,family_id,process_id)
    out_wo = connections.execute_mml_without_check(command)
    match = re.search(r"\bbuf_text\s*([0-9a-z ]*)", out_wo, re.I)
    print match.group(1)
    buf_wo = match.group(1)
    
    command='diagste -u %s -f %s -p %s -r hmem -t get -d -m hum'%(sp_computer_id,family_id,process_id)
    out_sp = connections.execute_mml_without_check(command)
    match = re.search(r"\bbuf_text\s*([0-9a-z ]*)", out_sp, re.I)
    print match.group(1)
    buf_sp = match.group(1)
    
    if (buf_wo == buf_sp):
        return 'success'
    else:
        return 'failure'

def check_if_with_warm_buffer_exist(computer_id,family_id,process_id):
    """This keyword is to use diagste to check if with warm buffer exist.

    #COMMAND: diagste -u computer_id -f family_id -p process_id -r hmem -t get -d -m hum

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | computer address                            |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
      
    | Return value | command execution result |

    Example
    | result | check if with warm buffer exist| 0x0000 0x**** 0x1|
    """
    command='diagste -u %s -f %s -p %s -r hmem -t get -d -m hum'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    match = re.search(r"\bbuf_text\s*([0-9 ]*)", out, re.I)
    if match is not None:
        return 'success'
    else:
        return 'failure'

def check_if_needless_warm_variable_changed(computer_id,family_id,process_id):
    """This keyword is to send msg to testproc check if needless warm variable changed or not.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -iw sub_id

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | sub_id           | Yes  | inqure variable or buffer select            |
      
    | Return value | command execution result |

    Example
    | result | check if needless warm variable changed| 0x0000 0x**** 0x0|
    """
    command='ILWMTestCli -- -r %s %s %s -iw 1'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('changed') == 1:
        return 'success'
    elif out.count('not change') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def check_if_needless_warm_buffer_changed(computer_id,family_id,process_id):
    """This keyword is to send msg to testproc check if needless warm buffer changed or not.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -iw sub_id

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | sub_id           | Yes  | inqure variable or buffer select            |
      
    | Return value | command execution result |

    Example
    | result | check if needless warm buffer changed| 0x0000 0x**** 0x0|
    """
    command='ILWMTestCli -- -r %s %s %s -iw 2'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('changed') == 1:
        return 'success'
    elif out.count('not change') == 1:
        return 'failure'
    else:
        return 'the return is wrong'
    
def send_msg_to_hand_to_create_sockets(computer_id,family_id,process_id):
    """This keyword is to send msg to one hand to create sockect on this hand.

    #COMMAND: ILPoxTestCli -- -r computer_id family_id process_id -sub

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | target process id                           |

    |Return value | command execution result |

    Example
    | result |send msg to hand to create sockets | 0x0 0x1B59 0x1 |
    """
    command = 'ILPoxTestCli -- -r %s %s %s -sub'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)

    if out.count('success') ==1:
        return 'success'
    elif out.count('failure') ==1:
        return 'failure'
    else:
        return 'the return is wrong'

def hand_could_response_msg_on_sockets(computer_id,family_id,in_process_id,socket_port1,socket_port2,socket_port3,socket_port4,socket_port5,socket_port6,socket_port7,socket_port8,socket_port9,socket_port10,socket_port11,socket_port12,socket_port13,socket_port14,out_process_id,rob_all_or_one):
    """This keyword is to send msg to the created socket to check whether the special process could response on the sockect correctly.

    #COMMAND: ILPoxTestCli -- -r computer_id family_id process_id -precv 20001 20002 20003 20004 20005 20006 20007 -psend 20008 20009 20010 20011 20012 20013 20014 -sock

    | Parameters        | Man. | Description                                   |
    | computer_id       | Yes  | target computer address                       |
    | family_id         | Yes  | target family addres                          |
    | in_process_id     | Yes  | input process id                              |
    | socket_port1      | Yes  | socket_port1                                  |
    | socket_port2      | Yes  | socket_port2                                  |
    | ...               | Yes  | ...                                           |
    | socket_port14     | Yes  | socket_port14                                 |
    | out_process_id    | Yes  | response process id                           |
    | rob_option        | Yes  | whether process has robbed socket from others |
    | rob_all_or_one    | Yes  | whether process has robbed socket from others |
    
    |Return value | command execution result |

    Example
    | result |send msg to hand to create sock | 0x0 0x1B59 0x1 20001 20002 20003 20004 20005 20006 20007 20008 20009 20010 20011 20012 20013 20014 |
    """
    
    command = 'ILPoxTestCli -- -r %s %s %s -precv %s %s %s %s %s %s %s -psend %s %s %s %s %s %s %s -sock'%(computer_id,family_id,in_process_id,socket_port1,socket_port2,socket_port3,socket_port4,socket_port5,socket_port6,socket_port7,socket_port8,socket_port9,socket_port10,socket_port11,socket_port12,socket_port13,socket_port14)
    out = connections.execute_mml_without_check(command)
    num = out.count('udp ack msg from process ' + str(out_process_id))

    if rob_all_or_one == '1' and num == 2:
        return 'success'
    elif rob_all_or_one == '2':
        command = 'ILPoxTestCli -- -r %s %s %s -precv %s %s %s %s %s %s %s -psend %s %s %s %s %s %s %s -sock'%(computer_id,family_id,0,socket_port1,socket_port2,socket_port3,socket_port4,socket_port5,socket_port6,socket_port7,socket_port8,socket_port9,socket_port10,socket_port11,socket_port12,socket_port13,socket_port14)
        out = connections.execute_mml_without_check(command)
        num = num + out.count('udp ack msg from process ' + str(out_process_id))
        if num == 4:
            return 'success'
        else:
            return 'failure'
        

def hand_b_rob_socket_from_hand_a(computer_id,family_id,robber_id,victim_id):
    """This keyword is to send msg to robber to rob socket from victim.

    #COMMAND: ILPoxTestCli -- -r computer_id family_id robber_id -rob victim_id

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | robber_id   | Yes  | process who will rob the socket             |
    | victim_id   | Yes  | process who will be robbed                  |

    |Return value | command execution result |

    Example
    | result |send msg to hand to create sockets | 0x0 0x1B59 0x11 0x1 |
    """
    command = 'ILPoxTestCli -- -r %s %s %s -rob %s'%(computer_id,family_id,robber_id,victim_id)
    out = connections.execute_mml_without_check(command)

    if out.count('success') ==1:
        return 'success'
    elif out.count('failure') ==1:
        return 'failure'
    else:
        return 'the return is wrong'

def hand_b_rob_socket_from_all_other_hands(computer_id,family_id,robber_id):
    """This keyword is to send msg to robber to rob sockets from all other hands.

    #COMMAND: ILPoxTestCli -- -r computer_id family_id robber_id -rob 

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | robber_id   | Yes  | process who will rob the socket             |


    |Return value | command execution result |

    Example
    | result |send msg to hand to create sockets | 0x0 0x1B59 0x11 |
    """
    command = 'ILPoxTestCli -- -r %s %s %s -rob'%(computer_id,family_id,robber_id)
    out = connections.execute_mml_without_check(command)

    if out.count('success') ==1:
        return 'success'
    elif out.count('failure') ==1:
        return 'failure'
    else:
        return 'the return is wrong'

def release_socket(computer_id,family_id,process_id):
    """This keyword is to release socket for special process.

    #COMMAND: ILPoxTestCli -- -r computer_id family_id robber_id -rob 

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | process_id  | Yes  | process who will release the socket         |


    |Return value | command execution result |

    Example
    | result |send msg to hand to create sockets | 0x0 0x1B59 0x11 |
    """
    command = 'ILPoxTestCli -- -r %s %s %s -free'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)

    if out.count('success') ==1:
        return 'success'
    elif out.count('failure') ==1:
        return 'failure'
    else:
        return 'the return is wrong'

def get_libgen_use_phys_addr(unit_type,unit_index):
    """This keyword is to get the libgen use phys addr.

    #COMMAND: ILLGTestCli -- -phys unit_type unit_index

    | Parameters       | Man. | Description                                 |
    | unit_type        | Yes  | appoint the recovery unit type              |
    | unit_index       | Yes  | appoint the recovery unit index             |
      
    | Return value | command execution result |

    Example
    | result | get libgen use phys addr| 0x2 0x0|
    """
    command='ILLGTestCli -- -phys %s %s'%(unit_type,unit_index)
    out = connections.execute_mml_without_check(command)

    print out
    match = re.search(r"\bunit physical address is: \s*(0x[0-9a-f]*)", out, re.I)
    if match is not None:
        return match.group(1).upper()
    else:
        return 'failure'

def get_libgen_use_grps_addr(unit_address):
    """This keyword is to get the libgen use phys addr.

    #COMMAND: ILLGTestCli -- -phys unit_type unit_index

    | Parameters       | Man. | Description                                 |
    | unit_type        | Yes  | appoint the recovery unit type              |
    | unit_index       | Yes  | appoint the recovery unit index             |
      
    | Return value | command execution result |

    Example
    | result | get libgen use phys addr| 0x2 0x0|
    """
    command='ILLGTestCli -- -agrps %s'%(unit_address)
    out = connections.execute_mml_without_check(command)

    match = re.search(r"group address is:\s*([0-9xA-Z]*)", out, re.I)
    if match is not None:
        return match.group(1).upper()
    else:
        return 'failure'
def set_configuration_of_pretending_thermo(computer_id,family_id,process_id,ack_computer_id,ack_family_id):
    """This keyword is to send unix socket message to prb set configuration of pretending thermo in libgen for warming test.

    #COMMAND: ILWMTestCli -f 0xffff -- -r computer_id family_id process_id -ts 1 ack_computer_id ack_family_id

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | ack_computer_id  | Yes  | the computer id for reporting sync error    |
    | ack_family_id    | Yes  | the family id for reporting sync error      |

    
    | Return value | command execution result |

    Example
    | result | set configuration of pretending thermo| 0x0000 0x**** 0x0 0x0000 0x****|
    """
    command='ILWMTestCli -f 0xffff -- -r %s %s %s -ts 1 %s %s'%(computer_id,family_id,process_id,ack_computer_id,ack_family_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def set_configuration_of_warming_state(computer_id,family_id,process_id,specific_process):
    """This keyword is to send unix socket message to prb set configuration of warming state in libgen for warming test.

    #COMMAND: ILWMTestCli -f 0xffff -- -r computer_id family_id process_id -ts 2 specific_process 1

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | specific_process| Yes  | specific process need to set warming state |

    
    | Return value | command execution result |

    Example
    | result | set configuration of warming state| 0x0000 0x**** 0x0 0x0000|
    """
    command='ILWMTestCli -f 0xffff -- -r %s %s %s -ts 2 %s 1'%(computer_id,family_id,process_id,specific_process)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def set_configuration_of_unit_state(computer_id,family_id,process_id,wo_or_sp):
    """This keyword is to send unix socket message to prb set configuration of wo or sp state in libgen for warming test.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -ts 3 wo_or_sp

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | wo_or_sp         | Yes  | the mark to set the unit state              |

    
    | Return value | command execution result |

    Example
    | result | set configuration of unit state| 0x0000 0x**** 0x0 0|
    """
    command='ILWMTestCli -- -r %s %s %s -ts 3 %s'%(computer_id,family_id,process_id,wo_or_sp)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def test_process_create_file(computer_id,family_id,process_id,file_warm_type,access_mode):
    """This keyword is to send msg to test process to create a file to be warmed.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -crf warm_type access_mode

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | master or hand process id                   |
    | warm_type        | Yes  | the warm type                               |
    | access_mode      | Yes  | access mode for the created file            |
      
    | Return value | command execution result |

    Example
    | result | send msg to create file to be warmed| 0x0 0x**** 0x0|
    """
    command='ILWMTestCli -- -r %s %s %s -crf %s %s'%(computer_id,family_id,process_id,file_warm_type,access_mode)
    out = connections.execute_mml_without_check(command)

    
    if (out.count('success') ==1):
        match = re.search(r"\bFile create handle: \s*([0-9]*)", out, re.I)
        if match is not None:
            create_handle = match.group(1)
        if (int(create_handle)>0):
            return 'success'
    elif out.count('failure') ==1:
        return 'failure'
    else:
        return 'the return is wrong' 

def test_process_open_created_file(computer_id,family_id,process_id,file_warm_type,access_mode):
    """This keyword is to send msg to test process to open the created file.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -clf warm_type access_mode

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | master or hand process id                   |
    | warm_type        | Yes  | the warm type                               |
    | access_mode      | Yes  | access mode for the created file            |
      
    | Return value | command execution result |

    Example
    | result | send msg to open created file| 0x0 0x**** 0x0|
    """
    command='ILWMTestCli -- -r %s %s %s -of %s %s'%(computer_id,family_id,process_id,file_warm_type,access_mode)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') ==1:
        command='ILWMTestCli -- -r %s %s %s -iwf %s'%(computer_id,family_id,process_id,file_warm_type)
        out = connections.execute_mml_without_check(command)
        match = re.search(r"\bFile open state: \s*([0-9]*)", out, re.I)
        if match is not None:
            open_state = match.group(1)
        if (open_state == '1'):
            return 'success'
    elif out.count('failure') ==1:
        return 'failure'
    else:
        return 'the return is wrong' 


def file_open_state_and_access_mode_should_be_correct(wo_computer_id,sp_computer_id,family_id,process_id,file_warm_type,open_state,access_mode):
    """This keyword is to send msg to test process to check if the file open state is consistent between WO and SP.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -iwf warm_type

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | master or hand process id                   |
    | warm_type        | Yes  | the warm type                               |
    | open_state       | Yes  | the oen state of the file                   | 
    | Return value | command execution result |

    Example
    | result | send msg to open created file| 0x0 0x**** 0x0|
    """
    command='ILWMTestCli -- -r %s %s %s -iwf %s'%(wo_computer_id,family_id,process_id,file_warm_type)
    out = connections.execute_mml_without_check(command)
    match = re.search(r"\bFile open state: \s*([0-9]*)", out, re.I)
    if match is not None:
        wo_open_state = match.group(1)
    if (wo_open_state != open_state):
        return 'failure'
    match = re.search(r"\bFile open handle: \s*([0-9]*)", out, re.I)
    if match is not None:
        wo_open_handle = match.group(1)
    match = re.search(r"\bFile access mode: \s*([0-9]*)", out, re.I)
    if match is not None:
        wo_access_mode = match.group(1)

    command='ILWMTestCli -- -r %s %s %s -iwf %s'%(sp_computer_id,family_id,process_id,file_warm_type)
    out = connections.execute_mml_without_check(command)

    match = re.search(r"\bFile open state: \s*([0-9]*)", out, re.I)
    if match is not None:
        sp_open_state = match.group(1)
    if (sp_open_state !=open_state):
        return 'failure'
    match = re.search(r"\bFile open handle: \s*([0-9]*)", out, re.I)
    if match is not None:
        sp_open_handle = match.group(1)
    match = re.search(r"\bFile access mode: \s*([0-9]*)", out, re.I)
    if match is not None:
        sp_access_mode = match.group(1)

    if (open_state == '0'):
        if (wo_open_handle == '0') and (sp_open_handle == '0'):
            return 'success'
        else:
            return 'failure'
    elif (open_state == '1'):
        if (int(wo_open_handle) > 0) and (int(sp_open_handle) > 0) and (int(wo_access_mode)==int(access_mode)) and (int(sp_access_mode)==int(access_mode)):
            return 'success'
        else:
            return 'failure'
    

def hand_sync_status_check(computer_id,family_id,process_id):
    """This keyword is to use diagste to check if hand sync status is ok.

    #COMMAND: diagste -u computer_id -f family_id -p process_id -r han -t idata -m hum

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
      
    | Return value | command execution result |

    Example
    | result | hand sync status check| 0x0000 0x**** 0x0|
    """
    command='diagste -u %s -f %s -p %s -r han -t idata -m hum'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    
    match = re.search(r"\warm sync      \s*([A-Za-z]*)", out, re.I)
    if match is not None:
       return match.group(1)
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def hand_stateful_status_check(computer_id,family_id,process_id):
    """This keyword is to use diagste to check if hand stateful status is ok.

    #COMMAND: diagste -u computer_id -f family_id -p process_id -r han -t idata -m hum

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
      
    | Return value | command execution result |

    Example
    | result | hand stateful status check| 0x0000 0x**** 0x0|
    """
    command='diagste -u %s -f %s -p %s -r han -t idata -m hum'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    
    if out.count("stateful proc   NO")==1:
        return 'success'
    else:
        return 'failure'

def test_process_create_file(computer_id,family_id,process_id,file_warm_type,access_mode):
    """This keyword is to send msg to test process to create a file to be warmed.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -crf warm_type access_mode

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | master or hand process id                   |
    | warm_type        | Yes  | the warm type                               |
    | access_mode      | Yes  | access mode for the created file            |
      
    | Return value | command execution result |

    Example
    | result | test process create file| 0x0 0x**** 0x0|
    """
    command='ILWMTestCli -- -r %s %s %s -crf %s %s'%(computer_id,family_id,process_id,file_warm_type,access_mode)
    out = connections.execute_mml_without_check(command)

    
    if (out.count('success') ==1):
        match = re.search(r"\bFile create handle: \s*([0-9]*)", out, re.I)
        if match is not None:
            create_handle = match.group(1)
        if (int(create_handle)>0):
            return 'success'
    elif out.count('failure') ==1:
        return 'failure'
    else:
        return 'the return is wrong' 

def test_process_open_created_file(computer_id,family_id,process_id,file_warm_type,access_mode):
    """This keyword is to send msg to test process to open the created file.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -clf warm_type access_mode

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | master or hand process id                   |
    | warm_type        | Yes  | the warm type                               |
    | access_mode      | Yes  | access mode for the created file            |
      
    | Return value | command execution result |

    Example
    | result | send msg to open created file| 0x0 0x**** 0x0|
    """
    command='ILWMTestCli -- -r %s %s %s -of %s %s'%(computer_id,family_id,process_id,file_warm_type,access_mode)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') ==1:
        command='ILWMTestCli -- -r %s %s %s -iwf %s'%(computer_id,family_id,process_id,file_warm_type)
        out = connections.execute_mml_without_check(command)
        match = re.search(r"\bFile open state: \s*([0-9]*)", out, re.I)
        if match is not None:
            open_state = match.group(1)
        if (open_state == '1'):
            return 'success'
    elif out.count('failure') ==1:
        return 'failure'
    else:
        return 'the return is wrong' 

def test_process_close_file(computer_id,family_id,op_process_id,file_warm_type):
    """This keyword is to send msg to test process close file.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -clf warm_type

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | master or hand process id                   |
    | warm_type        | Yes  | the warm type                               |
      
    | Return value | command execution result |

    Example
    | result | send msg to open created file| 0x0 0x**** 0x0|
    """

    command='ILWMTestCli -- -r %s %s %s -clf %s'%(computer_id,family_id,op_process_id,file_warm_type)
    out = connections.execute_mml_without_check(command)

    if out.count('success') ==1:
        return 'success'
    elif out.count('failure') ==1:
        return 'failure'
    else:
        return 'the return is wrong'
def test_process_delete_file(computer_id,family_id,delete_process_id,file_warm_type):
    """This keyword is to send msg to test process delete file.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -df warm_type

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | master or hand process id                   |
    | warm_type        | Yes  | the warm type                               |
      
    | Return value | command execution result |

    Example
    | result | send msg to open created file| 0x0 0x**** 0x0|
    """

    command='ILWMTestCli -- -r %s %s %s -df %s'%(computer_id,family_id,delete_process_id,file_warm_type)
    out = connections.execute_mml_without_check(command)
    if out.count('success') ==1:
        return 'success'
    elif out.count('failure') ==1:
        return 'failure'
    else:
        return 'the return is wrong'


def set_a_timer_and_receive_sync_error(computer_id,family_id,process_id,time_interval):
    """This keyword is to send msg to testproc set a timer needing warming and receive sync error message.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -t time_interval sub_id option

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | time_interval    | Yes  | timer value                                 |
    | sub_id           | Yes  | indicate what kind of timer you want to set |
      
    | Return value | command execution result |

    Example
    | result | set a timer and receive sync error| 0x0000 0x**** 0x0 10 2|
    """
    command='ILWMTestCli -- -r %s %s %s -t %s 2 1'%(computer_id,family_id,process_id,time_interval)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    else:
        return 'failure'

def create_hand_with_different_time_quota(computer_id,family_id,process_id,wo_time_quota,sp_time_quota):
    """This keyword is to send msg to testproc create hand with different time quota in both WO and SP.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -nch wo_time_quota sp_time_quota ack_opt

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | wo_time_quota    | Yes  | wo unit timer value                         |
    | sp_time_quota    | Yes  | sp unit timer value                         |
      
    | Return value | command execution result |

    Example
    | result | create hand with different time quota| 0x0000 0x**** 0x0 10 20|
    """
    command='ILWMTestCli -- -r %s %s %s -nch %s %s 2'%(computer_id,family_id,process_id,wo_time_quota,sp_time_quota)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        match = re.search(r"\bprocess_id:\s*(0x[0-9a-x]*)", out, re.I)
        if match is not None:
            return 'success', match.group(1)
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def create_hand_with_different_time_quota_and_receive_sync_error(computer_id,family_id,process_id,wo_time_quota,sp_time_quota):
    """This keyword is to send msg to testproc create hand with different time quota in both WO and SP and receive sync error.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -nch wo_time_quota sp_time_quota ack_opt

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | wo_time_quota    | Yes  | wo unit timer value                         |
    | sp_time_quota    | Yes  | sp unit timer value                         |
      
    | Return value | command execution result |

    Example
    | result | create hand with different time quota and receive sync error| 0x0000 0x**** 0x0 10 20|
    """
    command='ILWMTestCli -- -r %s %s %s -nch %s %s 1'%(computer_id,family_id,process_id,wo_time_quota,sp_time_quota)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    else:
        return 'failure'

def create_hand_with_same_time_quota(computer_id,family_id,process_id,time_quota):
    """This keyword is to send msg to testproc create hand with same time quota in both WO and SP.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -nch time_quota time_quota ack_opt

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | time_quota       | Yes  | timer value                                 |
      
    | Return value | command execution result |

    Example
    | result | create hand with same time quota| 0x0000 0x**** 0x0 10|
    """
    command='ILWMTestCli -- -r %s %s %s -nch %s %s 1'%(computer_id,family_id,process_id,time_quota,time_quota)
    out = connections.execute_mml_without_check(command)
    if out.count('success') == 1:
        match = re.search(r"\bprocess_id:\s*([0-9a-fx]*)", out, re.I)
        if match is not None:
            return 'success', match.group(1)
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def stop_hand_process_without_sync(computer_id,family_id,process_id):
    """This keyword is to send msg to testproc stop a hand process.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -stop

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
      
    | Return value | command execution result |

    Example
    | result | stop hand process without sync| 0x0000 0x**** 0x0|
    """
    command='ILWMTestCli -- -r %s %s %s -stop'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def stop_all_hand_processes_without_sync(computer_id,family_id,process_id,group_num):
    """This keyword is to send msg to testproc stop all hand processes.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -stop group_num

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | group_num        | Yes  | hand group number                           |
      
    | Return value | command execution result |

    Example
    | result | stop all hand processes without sync| 0x0000 0x**** 0x0 6|
    """
    command='ILWMTestCli -- -r %s %s %s -stop %s'%(computer_id,family_id,process_id,group_num)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def create_hand_with_incorrect_cookie(computer_id,family_id,process_id,sp_computer_id):
    """This keyword is to send msg to testproc create hand with incorrect cookie in wo and sp.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -nic sp_computer_id

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | sp_computer_id   | Yes  | sp unit computer address                    |
      
    | Return value | command execution result |

    Example
    | result | create hand with incorrect cookie| 0x0000 0x**** 0x0 0x0001|
    """
    command='ILWMTestCli -- -r %s %s %s -nic %s'%(computer_id,family_id,process_id,sp_computer_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def create_specific_hand_with_sync(computer_id,family_id,process_id,wo_time_quota,sp_time_quota,hand_id):
    """This keyword is to send msg to testproc create specific hand in both wo and sp.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -nch wo_time_quota sp_time_quota ack_opt hand_id

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | wo_time_quota    | Yes  | wo unit timer value                         |
    | sp_time_quota    | Yes  | sp unit timer value                         |
    | hand_id          | Yes  | hand process to be created                  |
      
    | Return value | command execution result |

    Example
    | result | create specific hand with sync| 0x0000 0x**** 0x0 10 20 0x33|
    """
    command='ILWMTestCli -- -r %s %s %s -nch %s %s 1 %s'%(computer_id,family_id,process_id,wo_time_quota,sp_time_quota,hand_id)
    out = connections.execute_mml_without_check(command)
    
    match = re.search(r"\bprocess_id:\s*([0-9a-fx]*)", out, re.I)
    if match is not None:
       return 'success', match.group(1)
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def create_specific_hand_and_receive_sync_error(computer_id,family_id,process_id,wo_time_quota,sp_time_quota,hand_id):
    """This keyword is to send msg to testproc create specific hand in both wo and sp and receive sync error.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -nch wo_time_quota sp_time_quota ack_opt hand_id

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | wo_time_quota    | Yes  | wo unit timer value                         |
    | sp_time_quota    | Yes  | sp unit timer value                         |
    | hand_id          | Yes  | hand process to be created                  |
      
    | Return value | command execution result |

    Example
    | result | create specific hand and receive sync error| 0x0000 0x**** 0x0 10 20 0x33|
    """
    command='ILWMTestCli -- -r %s %s %s -nch %s %s 1 %s'%(computer_id,family_id,process_id,wo_time_quota,sp_time_quota,hand_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    else:
        return 'failure'

def create_all_hand_in_a_hand_group(computer_id,family_id,process_id,group_num):
    """This keyword is to send msg to testproc create all hand in a hand group.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -nca group_num

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | group_num        | Yes  | hand group number                           |
      
    | Return value | command execution result |

    Example
    | result | create all hand in a hand group| 0x0000 0x**** 0x0 6|
    """
    command='ILWMTestCli -- -r %s %s %s -nca %s'%(computer_id,family_id,process_id,group_num)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def create_hand_in_needless_hand_group(computer_id,family_id,process_id,time_quota,option='0'):
    """This keyword is to send msg to testproc create hand in needless hand group.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -ncwnl time_quota

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | time_quota       | Yes  | refresh hand time quota                     |
    | option	       | Yes  | prb ack directly or wait for time out       |
      
    | Return value | command execution result |

    Example
    | result | create hand in needless hand group| 0x0000 0x**** 0x0 10|
    """
    
    command='ILWMTestCli -- -r %s %s %s -ncwnl %s %s'%(computer_id,family_id,process_id,time_quota,option)
    out = connections.execute_mml_without_check(command)
    
    match = re.search(r"\bprocess_id:\s*([0-9a-fx]*)", out, re.I)
    if match is not None:
       return 'success', match.group(1)
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def set_timer_needing_warming_with_time_quota_zero(computer_id,family_id,process_id,time_interval):
    """This keyword is to send msg to testproc set a timer needing warming with time quota zero.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -t time_interval sub_id option

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | time_interval    | Yes  | timer value                                 |
      
    | Return value | command execution result |

    Example
    | result | set timer needing warming with time quota zero| 0x0000 0x**** 0x0 10 2 3|
    """
    command='ILWMTestCli -- -r %s %s %s -t %s 2 2'%(computer_id,family_id,process_id,time_interval)
    out = connections.execute_mml_without_check(command)
    
    if out.count('set timer success') == 1:
        return 'success'
    elif out.count('set timer failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def warming_one_process(computer_id,family_id,process_id,sp_ipaddr,sp_ipport,target_process_id):
    """This keyword is to send warming data transfer message of one hand process through socket in wo.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -wdt sp_ipaddr sp_ipport 3 target_process_id

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | sp_ipaddr        | Yes  | sp unit ip address                          |
    | process_id       | Yes  | sp unit ip port num                         |
    | target_process_id| Yes  | process need to be warmed                   |
    

    | Return value | command execution result |

    Example
    | result | warming one process| 0x0000 0x**** 0x0 192.168.23.1 3333 0|
    """
    command='ILWMTestCli -- -r %s %s %s -wdt %s %s 3 %s'%(computer_id,family_id,process_id,sp_ipaddr,sp_ipport,target_process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('data transfer success') == 1:
        return 'success'
    elif out.count('data transfer failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def warming_one_hand_group(computer_id,family_id,process_id,sp_ipaddr,sp_ipport,target_hand_group):
    """This keyword is to send warming data transfer message of one hand group through socket in wo.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -wdt sp_ipaddr sp_ipport 2 target_process_id

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | sp_ipaddr        | Yes  | sp unit ip address                          |
    | process_id       | Yes  | sp unit ip port num                         |
    | target_hand_group| Yes  | hand group need to be warmed                |
    

    | Return value | command execution result |

    Example
    | result | warming one hand group| 0x0000 0x**** 0x0 192.168.23.1 3333 1|
    """
    command='ILWMTestCli -- -r %s %s %s -wdt %s %s 2 %s'%(computer_id,family_id,process_id,sp_ipaddr,sp_ipport,target_hand_group)
    out = connections.execute_mml_without_check(command)
    
    if out.count('data transfer success') == 1:
        return 'success'
    elif out.count('data transfer failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def set_configuration_of_warming_state_to_unwarming(computer_id,family_id,process_id,specific_process):
    """This keyword is to send unix socket message to prb set configuration of warming state to unwarming in libgen for warming test.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -ts 2 specific_process 0

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | specific_process| Yes  | specific process need to set unwarming     |

    
    | Return value | command execution result |

    Example
    | result | set configuration of warming state to unwarming| 0x0000 0x**** 0x0 0x0000|
    """
    command='ILWMTestCli -- -r %s %s %s -ts 2 %s 0'%(computer_id,family_id,process_id,specific_process)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def get_family_warming_related_info(computer_id,family_id,process_id):
    """This keyword is to get family warming info from libgen process.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -wgi

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
      
    | Return value | command execution result |

    Example
    | result | get family warming related info| 0x0000 0x**** 0x0|
    """
    command='ILWMTestCli -- -r %s %s %s -wgi'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'
    
"""THERMO PART"""
def query_sync_error_by_wutili(omu_unit_name,family_id,sync_err_num):
    """ This keyword is to query sync error by wutili for special family.

    #COMMAND:WUTILI -- -u[UNIT NAME] [UNIT INDEX] -f [family_id] -t
    
    | Parameters       | Man. | Description                                 |
    | omu_unit_name    | Yes  | omu unit name                               |
    | unit_index       | Yes  | unit index for omu                          |
    | family_id        | Yes  | target family address                       |
    | sync_err_num     | Yes  | sync error number                           |
      
    | Return value | command execution result |

    Example
    | result | query sync error number by wutili | 0x0000 0x**** 0x0 10 2 3|
    """
    
    command='wutili -- -u %s %s -f %s -t'%(omu_unit_name,0,family_id)
    out = connections.execute_mml_without_check(command)
    match = re.search(r"\btotal of\s*([0-9]*)", out, re.I)
    from string import atoi
    if (match is not None):
        wo_num = atoi(str(match.group(1)),10)
    elif out.count('family is not monitored by thermometer') == 1:
        wo_num = 0

    command='wutili -- -u %s %s -f %s -t'%(omu_unit_name,1,family_id)
    out = connections.execute_mml_without_check(command)
    match = re.search(r"\btotal of\s*([0-9]*)", out, re.I)
    if (match is not None):
        sp_num = atoi(str(match.group(1)),10)
    elif out.count('family is not monitored by thermometer') == 1:
        sp_num = 0

    num = wo_num + sp_num
    if (num == atoi(sync_err_num,10)):
        return 'success'
    else:
        return 'failure'

def query_and_return_sync_error_by_wutili(omu_unit_name,unit_index,family_id):
    """ This keyword is to query sync error by wutili for special family.

    #COMMAND:WUTILI -- -u[UNIT NAME] [UNIT INDEX] -f [family_id] -t
    
    | Parameters       | Man. | Description                                 |
    | omu_unit_name    | Yes  | omu unit name                               |
    | unit_index       | Yes  | unit index for omu                          |
    | family_id        | Yes  | target family address                       |
      
    | Return value | command execution result |

    Example
    | result | query and return sync error by wutili | omu 0 0x1773 |
    """

    command='wutili -- -u %s %s -f %s -t'%(omu_unit_name,unit_index,family_id)
    out = connections.execute_mml_without_check(command)
    match = re.search(r"\btotal of\s*([0-9]*)", out, re.I)
    from string import atoi
    if (match is not None):
        num = atoi(str(match.group(1)),10)
    elif out.count('family is not watched') == 1:
        num = -1
    if num == -1: 
        return 'family is not watched'
    else:
        return out
   
def start_monitoring_family_by_wutili(omu_unit_name,family_id,test_write='96'):
    """ This keyword is to start monitoring family by wutili.

    #COMMAND:WUTILI -- -u[UNIT NAME] [UNIT INDEX] -f [family_id] -a
    
    | Parameters       | Man. | Description                                 |
    | omu_unit_name    | Yes  | omu unit name                               |
    | family_id        | Yes  | target family address                       |
    | test_write       | No   | test_write |
      
    | Return value | command execution result |

    Example
    | result | start montioring family by wutili | 0x0000 0x**** 0x0 10 2 3|
    """
    
    command='wutili -- -u %s %s -f %s -a synerract %s '%(omu_unit_name,0,family_id, test_write)
    out = connections.execute_mml_without_check(command)

    command='wutili -- -u %s %s -f %s -a synerract %s'%(omu_unit_name,1,family_id, test_write)
    out1 = connections.execute_mml_without_check(command)
  
    if out.count('Monitoring started successfully.') and out1.count('Monitoring started successfully.') == 1:
        return 'success'
    elif out.count('family not found'):
        return 'not-exist'
    else:
        return 'failure'

def set_monitoring_family_test_write_by_wutili(omu_unit_name,family_id, test_write_value, test_id='10'):
    """ This keyword is to set test_write of monitoring family by wutili.

    #COMMAND:WUTILI -- -u[UNIT NAME] [UNIT INDEX] -f [family_id] -a
    
    | Parameters       | Man. | Description                                             |
    | omu_unit_name    | Yes  | omu unit name                                           |
    | family_id        | Yes  | target family address                                   |
    | test_write_value | Yes  | test_write value to be set to thespy for watched family |
    | test_id          | No  | test id in c_test_msg_s                                 |
      
    | Return value | command execution result |

    Example
    | result | set montioring family test write by wutili | omu | 0xA476 | 96 |
    """
    
    command='wutili -- -u %s %s -f %s -v %s -s %s'%(omu_unit_name,0,family_id, test_write_value, test_id)
    out = connections.execute_mml_without_check(command)

    command='wutili -- -u %s %s -f %s -v %s -s %s'%(omu_unit_name,1,family_id, test_write_value, test_id)
    out1 = connections.execute_mml_without_check(command)
    
    if out.count('start monitoring success') and out1.count('start monitoring success') == 1:
        return 'success'
    elif out.count('family not found'):
        return 'not-exist'
    else:
        return 'failure'

def start_monitoring_family_with_sync_error_change(omu_unit_name,family_id,index,value,test_write='96'):
    """ This keyword is to start monitoring family with sync error change by wutili.

    #COMMAND:WUTILI -- -u[UNIT NAME] [UNIT INDEX] -f [family_id] -a synerr <index>:<value>
    
    | Parameters       | Man. | Description                                 |
    | omu_unit_name    | Yes  | omu unit name                               |
    | unit_index       | Yes  | unit index for omu                          |
    | family_id        | Yes  | target family address                       |
    | index            | Yes  | index of sync error                         |
    | value            | Yes  | value of sync error weight                  |
    | Return value | command execution result |

    Example
    | result | start montioring family with sync error by wutili | 0x0000 0x**** 0x0 10 2 3|
    """
    
    command='wutili -- -u %s %s -f %s -a synerr %s:%s synerract %s'%(omu_unit_name,0,family_id,index,value,test_write)
    out = connections.execute_mml_without_check(command)
    command='wutili -- -u %s %s -f %s -a synerr %s:%s synerract %s'%(omu_unit_name,1,family_id,index,value,test_write)
    out1 = connections.execute_mml_without_check(command)
    
    if out.count('Monitoring started successfully.') and out1.count('Monitoring started successfully.') == 1:
        return 'success'
    else:
        return 'failure'


def stop_monitoring_family_by_wutili(omu_unit_name,family_id):
    """ This keyword is to stop monitoring family by wutili.

    #COMMAND:WUTILI -- -u[UNIT NAME] [UNIT INDEX] -f [family_id] -r
    
    | Parameters       | Man. | Description                                 |
    | omu_unit_name    | Yes  | omu unit name                               |
    | unit_index       | Yes  | unit index for omu                          |
    | family_id        | Yes  | target family address                       |
      
    | Return value | command execution result |

    Example
    | result | stop montioring family by wutili | 0x0000 0x**** 0x0 10 2 3|
    """
    
    command='wutili -- -u %s %s -f %s -r'%(omu_unit_name,0,family_id)
    out = connections.execute_mml_without_check(command)

    command='wutili -- -u %s %s -f %s -r'%(omu_unit_name,1,family_id)
    out1 = connections.execute_mml_without_check(command)
    
    if (out.count('Monitoring stopped successfully.') and out1.count('Monitoring stopped successfully.')) == 1:
        return 'success'
    else:
        return 'failure'

def create_hand_used_by_thermo(computer_id,family_id,process_id,time_quota):
    """This keyword is to send msg to testproc create hand used by thermo in WO.

    #COMMAND: ILWMTestCli -- -r computer_id family_id process_id -ch time_quota

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process id                           |
    | time_quota       | Yes  | timer value                                 |
      
    | Return value | command execution result |

    Example
    | result | create hand used by thermo| 0x0000 0x**** 0x0 10|
    """
    command='ILWMTestCli -- -r %s %s %s -ch %s'%(computer_id,family_id,process_id,time_quota)
    out = connections.execute_mml_without_check(command)
    if out.count('success') == 1:
        match = re.search(r"\btestproc:\s*([0-9a-fx]*)", out, re.I)
        if match is not None:
            return 'success', match.group(1)
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'the return is wrong'

def starting_monitoring_family_with_family_and_group_limit_change(omu_unit_name,family_id,family_weight,hand_index,hand_weight,test_write='96'):
    """ This keyword is to starting monitoring family with family and group limit change by wutili.

    #COMMAND:WUTILI -- -u[UNIT NAME] [UNIT INDEX] -f [family_id] -a [hw|hanl|faml|errd|time|synerr] [index:]<value>
    
    | Parameters       | Man. | Description                                 |
    | omu_unit_name    | Yes  | omu unit name                               |
    | unit_index       | Yes  | unit index for omu                          |
    | family_id        | Yes  | target family address                       |
    | family_limit     | Yes  | family value limit                          |
    | hand_index       | Yes  | hand group index to changed                 |
    | hand_weight      | Yes  | hand group weight to set                    |
    | Return value | command execution result |

    Example
    | result | start montioring family with family and group limit change by wutili | 0x0000 0x**** 0x0 10 2 3|
    """
    command='wutili -- -u %s %s -f %s -a hanl %s:%s faml %s synerract %s'%(omu_unit_name,0, family_id,hand_index,hand_weight,family_weight,test_write)
    out = connections.execute_mml_without_check(command)
    command='wutili -- -u %s %s -f %s -a hanl %s:%s faml %s synerract %s'%(omu_unit_name,1, family_id,hand_index,hand_weight,family_weight,test_write)
    out1 = connections.execute_mml_without_check(command)
        
    if out.count('Monitoring started successfully.') and out1.count('Monitoring started successfully.') == 1:
        return 'success'
    else:
        return 'failure'

def starting_monitoring_family_with_group_limit_change(omu_unit_name,family_id,hand_index,hand_weight,test_write='96'):
    """ This keyword is to starting monitoring family with family and group limit change by wutili.

    #COMMAND:WUTILI -- -u[UNIT NAME] [UNIT INDEX] -f [family_id] -a [hw|hanl|faml|errd|time|synerr] [index:]<value>
    
    | Parameters       | Man. | Description                                 |
    | omu_unit_name    | Yes  | omu unit name                               |
    | unit_index       | Yes  | unit index for omu                          |
    | family_id        | Yes  | target family address                       |
    | hand_index       | Yes  | hand group index to changed                 |
    | hand_weight      | Yes  | hand group weight to set                    |
    | Return value | command execution result |

    Example
    | result | start montioring family with family and group limit change by wutili | 0x0000 0x**** 0x0 10 2 3|
    """
    command='wutili -- -u %s %s -f %s -a hanl %s:%s synerract %s'%(omu_unit_name,0, family_id,hand_index,hand_weight,test_write)
    out = connections.execute_mml_without_check(command)
    command='wutili -- -u %s %s -f %s -a hanl %s:%s synerract %s'%(omu_unit_name,1, family_id,hand_index,hand_weight,test_write)
    out1 = connections.execute_mml_without_check(command)
        
    if out.count('Monitoring started successfully.') and out1.count('Monitoring started successfully.') == 1:
        return 'success'
    else:
        return 'failure'
    
def create_timer_process_used_by_thermo(computer_id, family_id,hand_group):
    """ This keyword is to create timer process used by thermo in hand group 3.

    #COMMAND: ILWMTestCli -- -r computer_id, family_id, process_id, -gch hand_group
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | master process id                           |
    | hand_group       | Yes  | hand group to creat the timer process       |
    | Return value | command execution result |

    Example
    | result | create timer process used by thermo | 0x7002 0x*** 0x0|
    """
    command='ILWMTestCli -- -r %s %s 0x0 -gch %s'%(computer_id,family_id,hand_group)
    out = connections.execute_mml_without_check(command)
        
    if out.count('create hand success') == 1:
        match = re.search(r"\bcreated process_id:\s*([0-9a-fx]*)", out, re.I)
        if match is not None:
            return 'success', match.group(1)
    elif out.count('create hand failure'):
        return 'failure'
    else:
        return 'return wrong'

""" socket & msg scheduler """
def initialize_socket_used_by_libgen(computer_id,family_id,process_id):
    """ This keyword is to initialize the socket.

    #COMMAND: ILPoxTestCli -- -r computer_id family_id process_id -init
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | initialize socket used by libgen | 0x300 0x*** 0x0|
    """
    command='ILPoxTestCli -- -r %s %s %s -init'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
        
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'return wrong'

def send_socket_events_to_process(computer_id,family_id,process_id,socket_port1,socket_port2,socket_port3,socket_port4,socket_port5,socket_port6,socket_port7,socket_port8,socket_port9,socket_port10,socket_port11,socket_port12,socket_port13,socket_port14):
    """ This keyword is to send several socket events to test process.

    #COMMAND: ILPoxTestCli -- -r computer_id family_id process_id -precv 20001 20002 20003 20004 20005 20006 20007 -psend 20008 20009 20010 20011 20012 20013 20014 -event
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    | socket_port1-14  | Yes  | socket_port1-14                             |
    | Return value | command execution result |

    Example
    | result | send socket events to process | 0x300 0x*** 0x0 20001 20002 20003 20004 20005 20006 20007 20008 20009 20010 20011 20012 20013 20014 |
    """
    command='ILPoxTestCli -- -r %s %s %s -precv %s %s %s %s %s %s %s -psend %s %s %s %s %s %s %s -event'%(computer_id,family_id,process_id,socket_port1,socket_port2,socket_port3,socket_port4,socket_port5,socket_port6,socket_port7,socket_port8,socket_port9,socket_port10,socket_port11,socket_port12,socket_port13,socket_port14)
    out = connections.execute_mml_without_check(command)
        
    if out.count('success') == 3:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'return wrong'

def register_given_linux_file_descriptor_to_libgen_with_type1(computer_id,family_id,process_id):
    """ This keyword is to register given linux file descriptor to libgen and receiving socket one by one.

    #COMMAND: ILPoxTestCli -- -r computer_id family_id process_id -sbs
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | register given linux file descriptor to libgen with type1 | 0x300 0x*** 0x0|
    """
    command='ILPoxTestCli -- -r %s %s %s -sbs'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
        
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'return wrong'
    
def register_given_linux_file_descriptor_to_libgen_with_type2(computer_id,family_id,process_id):
    """ This keyword is to register given linux file descriptor to libgen and receiving socket continuously.

    #COMMAND: ILPoxTestCli -- -r computer_id family_id process_id -sbc
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | register given linux file descriptor to libgen with type2 | 0x300 0x*** 0x0|
    """
    command='ILPoxTestCli -- -r %s %s %s -sbc'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
        
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'return wrong'
    
def check_correct_event_number_received(computer_id,family_id,process_id):
    """ This keyword is to check if event number received is right.

    #COMMAND: ILPoxTestCli -- -r computer_id family_id process_id -getcnt
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    | Return value c   | command execution result |

    Example
    | result | check correct event number received | 0x300 0x*** 0x0|
    """
    command='ILPoxTestCli -- -r %s %s %s -getcnt'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
        
    if out.count('socket event num: 12') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'return wrong'

def free_socket_used_by_libgen(computer_id,family_id,process_id):
    """ This keyword is to free the socket.

    #COMMAND: ILPoxTestCli -- -r computer_id family_id process_id -release
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | free socket used by libgen | 0x300 0x*** 0x0|
    """
    command='ILPoxTestCli -- -r %s %s %s -release'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
        
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'return wrong'

def check_if_with_warm_variable_equal_by_wutili(own_uindex,co_uindex,family_id,process_id):
    """ This keyword is to Check If With Warm Variable Equal By Wutili.

    #COMMAND: fsclish -c "show has process-family warming compare-variables unit-type omu unit-index 0 family-id 0x1773 process-id 0xb"
    
    | Parameters       | Man. | Description                                 |
    | own_uindex       | Yes  | own unit index                              |
    | co_uindex        | Yes  | co-unit index                               |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | master process id                           |
    | Return value | command execution result |

    Example
    | result | Check If With Warm Variable Equal By Wutili | 0x0 0x1 0x1773 0xb |
    """
    #l_has = BuiltIn().run_keyword("Libgen Get Scli Tree Has")
    command='''fsclish -c "show has process-family warming compare-variables unit-type omu unit-index %s family-id %s process-id %s"'''%(own_uindex, family_id,process_id)
    out = connections.execute_mml_without_check(command)
        
    if out.count('data is identical') == 1:
        return 'success'
    elif out.count('data is different') == 1:
        return 'failure'
    else:
        return 'return wrong'

def process_should_not_be_running(prb_name):
    """This keyword is to count the num of appointed running prb .

    #COMMAND: ps -ef |grep *

    | Parameters  | Man. | Description                                 |
    | Return value | command execution result |

    Example
    | result | count running process num of prb |
    """
    command='ps -ef|grep '+ prb_name
    out = connections.execute_mml_without_check(command)

    if out.count('%s'%prb_name) < 2:
        return 'success'
    else:
        return 'failure'

def save_current_buffer_and_reuse(computer_id,family_id,process_id):
    """ This keyword is to ask test process save the current buffer and restore it to use.

    #COMMAND: ILDMXTestCli -- -r computer_id family_id process_id -b
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | save current buffer and reuse | 0x300 0x*** 0x0|
    """
    command='ILDMXTestCli -- -r %s %s %s -b'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
        
    if out.count('c_test_msg_ack_s received') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'return wrong'

def send_msg_to_process_used_by_missingapi(computer_id,family_id,process_id,focus_id):
    """ This keyword is to send the c_test_msg_s to process.

    #COMMAND: ILDMXTestCli -- -r computer_id family_id process_id -e
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    | focus_id         | Yes  | target focus id                             |
    
    | Return value | command execution result |

    Example
    | result | send msg to process used by missingapi | 0x300 0x*** 0x0|
    """
    command='ILDMXTestCli -- -r %s %s %s -e 0x12 0x34 %s 0x1'%(computer_id,family_id,process_id,focus_id)
    out = connections.execute_mml_without_check(command)
        
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'return wrong'

def check_if_receive_err_msg(computer_id,family_id,process_id):
    """ This keyword is to check if process has receive the lib_error_msg_s msg.

    #COMMAND: ILDMXTestCli -- -r computer_id family_id process_id -a
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |

    
    | Return value | command execution result |

    Example
    | result | check if receive err msg | 0x300 0x*** 0x0|
    """
    command='ILDMXTestCli -- -r %s %s %s -a'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
        
    if out.count('lib_error_msg_s received successfully') == 1:
        match = re.search(r"\berror_reason:\s*([a-z| ]*)\.", out, re.I)
        if match is not None:
            return match.group(1)
    elif out.count('lib_error_msg_s did not received') == 1:
        return 'failure'
    else:
        return 'return wrong'

def create_one_hand_used_by_missingapi(computer_id,family_id,process_id,create_process):
    """ This keyword is to ask test process to create specific process.

    #COMMAND: ILDMXTestCli -- -r computer_id family_id process_id -c create_process
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    | create_process   | Yes  | the process need to created                 |
    
    | Return value | command execution result |

    Example
    | result | create one hand used by missingapi | 0x300 0x*** 0x0 0x1|
    """
    command='ILDMXTestCli -- -r %s %s %s -c %s'%(computer_id,family_id,process_id,create_process)
    out = connections.execute_mml_without_check(command)
        
    if out.count('hand created') == 1:
        match = re.search(r"\bfocus:\s*(0x[0-9a-z]*)", out, re.I)
        if match is not None:
            return match.group(1)
        else:
            return 'failure'      
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'return wrong'

def stop_one_hand_used_by_missingapi(computer_id,family_id,process_id,focus_id):
    """ This keyword is to stop one hand process.

    #COMMAND: ILDMXTestCli -- -r computer_id family_id process_id -s
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    | focus_id         | Yes  | target focus id                             |
    
    | Return value | command execution result |

    Example
    | result | stop one hand used by missingapi | 0x300 0x*** 0x0 0x0|
    """
    command='ILDMXTestCli -- -r %s %s %s -s 0x80 0x0 %s 0x1'%(computer_id,family_id,process_id,focus_id)
    out = connections.execute_mml_without_check(command)
        
    if out.count('hand stopped') == 1:
        return 'success'      
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'return wrong'

def send_msg1_to_own_and_stop_used_by_missingapi(computer_id,family_id,process_id,focus_id,msg_count):
    """ This keyword is to ask hand process to send msg to itself and stop the hand.

    #COMMAND: ILDMXTestCli -- -r computer_id family_id process_id -s
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    | focus_id         | Yes  | target focus id                             |
    | msg_count        | Yes  | the message count                           |
    
    | Return value | command execution result |

    Example
    | result | send msg1 to own and stop used by missingapi | 0x300 0x**** 0x**** 0x2 0xFF|
    """
    command='ILDMXTestCli -- -r %s %s %s -s 0x81 0 %s 0x2 %s'%(computer_id,family_id,process_id,focus_id,msg_count)
    out = connections.execute_mml_without_check(command)
        
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'return wrong'
    
def check_if_receive_err_msg_and_return_count(computer_id,family_id,process_id):
    """ This keyword is to check if process has receive the lib_error_msg_s msg.

    #COMMAND: ILDMXTestCli -- -r computer_id family_id process_id -a
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |

    
    | Return value | command execution result |

    Example
    | result | check if receive err msg | 0x300 0x*** 0x0|
    """
    command='ILDMXTestCli -- -r %s %s %s -a'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
        
    if out.count('lib_error_msg_s received successfully') == 1:
        match = re.search(r"\bmsg count:\s*([0-9]*)", out, re.I)
        if match is not None:
            return match.group(1)
    elif out.count('lib_error_msg_s did not received') == 1:
        return 'failure'
    else:
        return 'return wrong'

def check_if_receive_err_msg_and_count(computer_id,family_id,process_id,reason,count):
    """ This keyword is to check if process has receive the lib_error_msg_s msg.

    #COMMAND: ILDMXTestCli -- -r computer_id family_id process_id -a
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    | reason           | Yes  | error reason                                |
    | count            | Yes  | count                                       |

    
    | Return value | command execution result |

    Example
    | result | check if receive err msg | 0x300 0x*** 0x0|
    """
    command='ILDMXTestCli -- -r %s %s %s -a'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)

    if out.count('lib_error_msg_s received successfully') == 1:
        match1 = re.search(r"\bmsg count:\s*([0-9]*)", out, re.I)
        if match1 is not None and match1.group(1) == count:
             print match1.group(1)
        else:
             return 'failure'
        match2 = re.search(r"\berror_reason:\s(.*)", out, re.I)
        if match2.group(1).count(reason) == 1:
             print match2.group(1)
        else:
             return 'failure'
        return 'success'
    elif out.count('lib_error_msg_s did not received') == 1:
        return 'failure'
    else:
        return 'return wrong'

def send_msg2_to_own_and_stop_used_by_missingapi(computer_id,family_id,process_id,focus_id,msg_count):
    """ This keyword is to ask hand process to send msg to itself and save the message into save queue then stop the hand.

    #COMMAND: ILDMXTestCli -- -r computer_id family_id process_id -s
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    | focus_id         | Yes  | target focus id                             |
    | msg_count        | Yes  | the message count                           |
    
    | Return value | command execution result |

    Example
    | result | send msg2 to own and stop used by missingapi | 0x300 0x**** 0x**** 0x2 0xFF |
    """
    command='ILDMXTestCli -- -r %s %s %s -s 0x82 0 %s 0x2 %s'%(computer_id,family_id,process_id,focus_id,msg_count)
    out = connections.execute_mml_without_check(command)
        
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'return wrong'

def send_msg3_to_own_and_stop_used_by_missingapi(computer_id,family_id,process_id,focus_id,msg_count):
    """ This keyword is to ask hand process to send msg to itself and save the message into save chain then stop the hand.

    #COMMAND: ILDMXTestCli -- -r computer_id family_id process_id -s
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    | focus_id         | Yes  | target focus id                             |
    | msg_count        | Yes  | the message count                           |
    
    | Return value | command execution result |

    Example
    | result | send msg3 to own and stop used by missingapi | 0x300 0x**** 0x**** 0x2 0xFF |
    """
    command='ILDMXTestCli -- -r %s %s %s -s 0x83 0 %s 0x2 %s'%(computer_id,family_id,process_id,focus_id,msg_count)
    out = connections.execute_mml_without_check(command)
        
    if out.count('success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'return wrong'
def testing_receive_and_save_buffer_for_missingapi(test_case_id):
    """ This keyword is to test receive_buffer_r and save_buffer_r by ILDMXTestCli.

    #COMMAND: ILDMXTestCli -- -f [test_case_id]
    
    | Parameters       | Man. | Description                                         |
    | test_case_id     | Yes  | test case id for receive_buffer_r and save_buffer_r |
    |                  |      | test case id should be 0 <= id <= 2                 |
    
    | Return value | command execution result |
    Example
    | ${result} | Testing Receive And Save Buffer For Missingapi | 0 |
    """
    if (int(test_case_id) < 0 or int(test_case_id) > 2):
        raise AssertionError(" receive and save buffer test id should be in range 0 - 2, current value: %s." % test_case_id )
    command='ILDMXTestCli -- -f %s'%(test_case_id)
    out = connections.execute_mml_without_check(command)
    
    return out
def get_unit_pending_message_and_should_be_larger_than_value(computer_id,family_id,process_id):
    """ This keyword is to ask process to send messages to external queu and get unit pending messages count.

    #COMMAND: ILDMXTestCli -- -r computer_id family_id process_id -n 0x2
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | get unit pending message and should be larger than value | 0x300 0x*** 0x0|
    """
    
    command='ILDMXTestCli -- -r %s %s %s -n 0x2'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    match = re.search(r"\bget\s*([0-9]*)", out, re.I)
    if match is not None:
        print match.group(1)
        if int(match.group(1)) >= 10000:
            return 'success'
        else:
            return 'failure'    
    else:
        return 'failure'
    
def get_unit_pending_message_and_should_be_less_than_value(computer_id,family_id,process_id):
    """ This keyword is to get unit pending messages count.

    #COMMAND: ILDMXTestCli -- -r computer_id family_id process_id -n 0x0
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | get unit pending message and should be less than value | 0x300 0x*** 0x0|
    """
    command='ILDMXTestCli -- -r %s %s %s -n 0x0'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    match = re.search(r"\bget\s*([0-9]*)", out, re.I)
    if match is not None:
        print match.group(1)
        if int(match.group(1)) <= 10000:
            return 'success'
        else:
            return 'failure'    
    else:
        return 'failure'
def send_messages_to_external_queue_and_sleep(computer_id,family_id,process_id):
    """ This keyword is to let the process send messages to external queue and sleep.

    #COMMAND: ILDMXTestCli -- -r computer_id family_id process_id -n 0x1
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | send messages to external queue and sleep | 0x300 0x*** 0x0|
    """
    command='ILDMXTestCli -- -r %s %s %s -n 0x1'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)

    if out.count('Send external queue sleep success') == 1:
        return 'success'
    elif out.count('failure') == 1:
        return 'failure'
    else:
        return 'return wrong'

def libgen_test_receive_buffer_success():
    """ This keyword is to test receive buffer success by ILDMXTestCli.

    #COMMAND: ILDMXTestCli -- -f [test_case_id]
    
    | Return value | command execution result |

    Example
    | ${result}= | Libgen Test Receive Buffer Success |
    | Should Be Equal | ${result} | success |
    """
    out = BuiltIn().run_keyword("Testing Receive And Save Buffer For MissingAPI", "0")
    
    if out.count('receive_buffer_r successfully, msg received: number: 0x6034, length: 146, C_TEST_MSG_S test_id: 0x12, sub_id: 0x34.') != 1:
        return 'failure: receive_buffer_r not succeeded'
    if out.count('received No.1 c_test_msg_s successfully, test_id: 1, sub_id: 1.') != 1:
        return 'failure: No.1 c_test_msg_s (test_id=1, sub_id=1) not received'
    if out.count('received No.2 c_test_msg_s successfully, test_id: 2, sub_id: 2.') != 1:
        return 'failure: No.2 c_test_msg_s (test_id=2, sub_id=2) not received'
        
    return 'success'
    
def libgen_test_receive_buffer_timeout():
    """ This keyword is to test receive buffer timeout by ILDMXTestCli.

    #COMMAND: ILDMXTestCli -- -f [test_case_id]
    
    | Return value | command execution result |

    Example
    | ${result}= | Libgen Test Receive Buffer Timeout |
    | Should Be Equal | ${result} | success |
    """
    out = BuiltIn().run_keyword("Testing Receive And Save Buffer For MissingAPI", "1")
    
    if out.count('receive_buffer_r failed because of time out, error code: 0x65 101.') != 1:
        return 'failure: receive_buffer_r time out not found'
    if out.count('received No.1 c_test_msg_s successfully, test_id: 1, sub_id: 1.') != 1:
        return 'failure: No.1 c_test_msg_s (test_id=1, sub_id=1) not received'
    if out.count('received No.2 c_test_msg_s successfully, test_id: 2, sub_id: 2.') != 1:
        return 'failure: No.2 c_test_msg_s (test_id=2, sub_id=2) not received'
    if out.count('received No.3 c_test_msg_s successfully, test_id: 3, sub_id: 3.') != 1:
        return 'failure: No.3 c_test_msg_s (test_id=3, sub_id=3) not received'
    
    return 'success'
    

def libgen_test_save_buffer_success():
    """ This keyword is to test save buffer success by ILDMXTestCli.

    #COMMAND: ILDMXTestCli -- -f [test_case_id]
    
    | Return value | command execution result |

    Example
    | ${result}= | Libgen Test Save Buffer Success |
    | Should Be Equal | ${result} | success |
    """
    out = BuiltIn().run_keyword("Testing Receive And Save Buffer For MissingAPI", "2")
    
    if out.count('receive_buffer_r successfully, msg received: number: 0x6034, length: 146, C_TEST_MSG_S test_id: 0x12, sub_id: 0x34.') != 1:
        return 'failure: receive_buffer_r not succeeded'
    if out.count('save_buffer_r successfully.') != 1:
        return 'failure: save_buffer_r not succeeded'
    if out.count('received No.1 c_test_msg_s successfully, test_id: 18, sub_id: 52.') != 1:
        return 'failure: No.1 c_test_msg_s (test_id=18, sub_id=52) not received'
    if out.count('received No.2 c_test_msg_s successfully, test_id: 1, sub_id: 1.') != 1:
        return 'failure: No.2 c_test_msg_s (test_id=1, sub_id=1) not received'
    if out.count('received No.3 c_test_msg_s successfully, test_id: 2, sub_id: 2.') != 1:
        return 'failure: No.3 c_test_msg_s (test_id=2, sub_id=2) not received'
        
    return 'success'

def testing_allocate_buffers_for_256k_number_of_buffer_handles(test_case_id):
    """ This keyword is to test allocate_buffer_r by ILDMXTestCli for supporting 256k number of buffer handles.

    #COMMAND: ILDMXTestCli -- -g [test_case_id]
    
    | Parameters       | Man. | Description                          |
    | test_case_id     | Yes  | test case id for allocate_buffer_r   |
    |                  |      | test case id should be 0 <= id <= 1  |
    
    | Return value | command execution result |
    Example
    | $(result) =     | Testing Allocate Buffers For 256K Number Of Buffer Handles | 0 |
    """
    if (int(test_case_id) < 0 or int(test_case_id) > 1):
        raise AssertionError(" allocate buffer test id should be in range 0 - 1, current value: %s." % test_case_id )
    command='ILDMXTestCli -- -g %s'%(test_case_id)
    out = connections.execute_mml_without_check(command)
    
    return out


def libgen_test_allocate_maximum_buffers_success():
    """ This keyword is to test allocate maximum number (262143, 256k) of buffers successfully by ILDMXTestCli.

    #COMMAND: ILDMXTestCli -- -g [test_case_id]
    
    | Return value | command execution result |

    Example
    | ${result}= | Libgen Test Allocate Maximum Buffers Success |
    | Should Be Equal | ${result} | success |
    """
    out = BuiltIn().run_keyword("Testing Allocate Buffers For 256K Number Of Buffer Handles", "0")
    
    if out.count('ILDMXTestCli test allocate maximum number (262143) of buffers successfully.') != 1:
        return 'failure: allocate maximum number of buffers not succeeded'

    return 'success'

def libgen_test_allocate_one_more_after_maximum_buffers_failed():
    """ This keyword is to test allocate one more buffer failed after 
        maximum number (262143, 256k) of buffers allocated by ILDMXTestCli.

    #COMMAND: ILDMXTestCli -- -g [test_case_id]
    
    | Return value | command execution result |

    Example
    | ${result}= | Libgen Test Allocate One More After Maximum Buffers Failed |
    | Should Be Equal | ${result} | success |
    """
    out = BuiltIn().run_keyword("Testing Allocate Buffers For 256K Number Of Buffer Handles", "1")
    
    if out.count('ILDMXTestCli test allocate maximum number (262143) of buffers successfully.') != 1:
        return 'failure: allocate maximum number of buffers not succeeded'
    if out.count('ILDMXTestCli test allocate maximum+1 number (262144) buffers failed.') != 1:
        return 'failure: allocate maximum+1 number of buffers failed not found'
    
    return 'success'


def create_shm_buffer_by_test_process(computer_id,family_id,process_id):
    """ This keyword is to send msg to test process to creat shm buffer.

    #COMMAND: shmwarmproc -- -p "0x700 12345 0" -v create
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | create shm buffer by test process | 0x300 | 0x1f46 | 0x0 |
    """
    command='shmwarmproc -f 0xffff -- -p "%s %s %s" -v create'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
        

def change_shm_buffer_content_by_test_process(computer_id,family_id,process_id):
    """ This keyword is to send msg to test process to change shm buffer content.

    #COMMAND: shmwarmproc -- -p "0x700 12345 0" -v write
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | change shm buffer content by test process | 0x300 | 0x1f46 | 0x0 |
    """
    command='shmwarmproc -f 0xffff -- -p "%s %s %s" -v write'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
        
    
def delete_shm_buffer_by_test_process(computer_id,family_id,process_id):
    """ This keyword is to send msg to test process to delete shm buffer by test process.

    #COMMAND: shmwarmproc -- -p "0x700 12345 0" -v delete
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | delete shm buffer by test process | 0x300 | 0x1f46 | 0x0 |
    """
    command='shmwarmproc -f 0xffff -- -p "%s %s %s" -v delete'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)

def libgen_execute_command_and_check_result(in_success_result, in_success_res_count, in_failure_result, in_failure_res_count, in_command, *in_args):
    """This keyword is to execute a command and check result.
    If return contains in_success_res_count of in_success_result, return 'success'.
    Else if return contains in_failure_res_count of in_failure_result, return 'failure'.
    else return 'the return is wrong '+result.
    | Parameters           | Man. | Description                                                          |
    | in_success_result    | Yes  | string to be found in return result of the command, e.g., 'success'  |
    | in_success_res_count | Yes  | count of success_result, e.g., '1'                                   |
    | in_failure_result    | Yes  | string to be found in return result of the command, e.g., 'failure'  |
    | in_failure_res_count | Yes  | count of failure_result, e.g., '1'                                   |
    | in_command           | Yes  | command to be executed, e.g., 'ILLGTestCli -- -r %s %s %s'           |
    | in_args              | No   | arguments that may be needed in command                              |
   
    | Return value | command execution result |
    Example
    | ${result}= | Libgen Execute Command And Check Result | success | 1 | failure | 1 | 
    | ...        | ILLGTestCli -- -r %s %s %s %s %s -w %s %s %s %s %s % s | 0x700 | 0x1771 |
    | ...        | 0x0 | 0x6034 | 0xffff11 | 0x1 | 0x2 | 0x200 | 0x1 | 0x0 | 0x100 |
    """
    if len(in_args) > 0:
        command = in_command % (in_args)
    else:
        command = in_command
    out = connections.execute_mml_without_check(command)
    
    if out.count(in_success_result) == int(in_success_res_count):
        return 'success'
    elif out.count(in_failure_result) == int(in_failure_res_count):
        return 'failure'
    else:
        return 'the return is wrong: '+out

def read_system_ID(system_id = '000000'):
    """ This keyword is to read system ID.

    #COMMAND: ilsystemid.sh -r #1234
    
    | Parameters       | Man. | Description                                 |
    | system_id        | No   | the system ID to written                    |
    
    | Return value | command execution result |

    Example
    | result | read system ID | 12345 |
    """
    command='ilsystemid.sh -r'
    out = connections.execute_mml_without_check(command)
    if out.count('Open file fail') == 1:
        return 'not-exist'

    match = re.search(r"\SYSTEM ID:\s*([0-9]*)", out, re.I)
    #system_id_match = re.search(r"([0-9]*)(L|)", hex(int(system_id)))

    if match.group(1) == system_id:
        return 'success'
    else:
        return 'failure'

def read_system_ID_and_return():
    """ This keyword is to read system ID and return.

    #COMMAND: ilsystemid.sh -r
    
    | Parameters       | Man. | Description                 |
    
    | Return value | command execution result |

    Example
    | result | read system ID and return |
    """
    command='ilsystemid.sh -r'
    out = connections.execute_mml_without_check(command)
    if out.count('Open file fail') == 1:
        return 'not-exist'

    match = re.search(r"\SYSTEM ID:\s*([0-9]*)", out, re.I)
    #system_id = int(match.group(1), 16)
    return match.group(1)

def write_system_ID(system_id):
    """ This keyword is to write system ID.

    #COMMAND: ilsystemid.sh -w 1234
    
    | Parameters       | Man. | Description                                 |
    | system_id        | Yes  | the system ID to written                    |
    
    | Return value | command execution result |

    Example
    | result | write system ID | 12345 |
    """
    command='ilsystemid.sh -w %s'%(system_id)
    out = connections.execute_mml_without_check(command)
    if out.count('Invalid system id format') == 1:
        return 'failure'
    elif out.count('WRITE SUCCESS') == 1:
        return 'success'
    return 'failure'

def start_reallocate_buffer_test():
    """ This keyword is to start the reallocte buffer test.

    #COMMAND: reallocproc
    
    | Return value | command execution result |

    Example
    | result | reallocproc |
    """
    command='reallocproc'
    out = connections.execute_mml_without_check(command)
    if out.count('Test success.') == 1:
        return 'success'
    else:
        return 'failure'
		

def check_prb_used_by_family_exist(family_id):
    """ This keyword is used to check whether the PRB is alive

    #COMMAND: Family_Exist_Test -f 0xffff -- -t 0x1234

    | Parameters       | Man. | Description                                 |
    | family_id        | Yes  | family id of the PRB to be checked          |

    | Return value | command execution result |

    Example
    | result | check prb used by family exist | 0x1234 |
    """
    command='Family_Exist_Test -f 0xffff -- -t %s'%(family_id)
    out = connections.execute_mml_without_check(command)
    print out
    if out.count('is exist') == 1:
        return 'success'
    else:
        return 'failure'

def prb_should_not_running_used_by_family_exist():
    """ This keyword is used to check whether the PRB is alive

    #COMMAND: ps aux | grep Family_Exist_Test | grep -v grep
    
    | Return value | command execution result |

    Example
    | result | prb should not running used by family exist |
    """
    
    command = 'ps aux | grep Family_Exist_Test | grep -v grep'
    out = connections.execute_mml_without_check(command)
    if out.count('Family_Exist_Test')==0:
        return 'success'
    else:
        return 'failure'

def start_prb_used_by_family_exist(family_id):
    """ This keyword is used to start a PRB in the background

    #COMMAND: Family_Exist_Test -f 0x1234 -- -s &
    | Parameters       | Man. | Description                                 |
    | family_id        | Yes  | family id of the PRB to be started          |

    
    | Return value | command execution result |

    Example
    | result | start prb used by family exist | 0x1234 |
    """
    command1='Family_Exist_Test -f %s -- -s &'%(family_id)
    connections.execute_mml_without_check(command1)
    command2='ps aux | grep Family_Exist | grep -v grep'
    out=connections.execute_mml_without_check(command2)
    if out.count('Family_Exist_Test')==1:
        return 'success'
    else:
        return 'failure'

def remove_prb_files_used_by_family_exist(phy_address,str0, str2):
    """ This keyword is used to remove PRB directories

    #COMMAND: rm -rf /dev/shm/libgen/euid00000000/comp0700/fam1234
    | Parameters       | Man. | Description                                 |
    | phy_address      | Yes  | Phy_address of current RU                   |
    | str0             | Yes  | libgen directory path                       |
    | str1             | Yes  | PRB directory path                          |

    
    | Return value |command execution result |

    Example
    | remove prb files used by family exist | 0x700 /dev/shm/libgen/euid00000000/ /fam1234|
    """

    temp = phy_address[2:]
    while len(temp)<4:
        temp = '0'+temp
    command = "rm -rf  %scomp%s%s"%(str0, temp, str2)  
    print command
    connections.execute_mml_without_check(command)

def order_the_notification_stop_updating_s_by_test_process(computer_id,family_id,process_id):
    """ This keyword is to send msg to test process to order the stop_updating_s.

    #COMMAND: shmwarmproc -- -p "0x700 12345 0" -t "sub"
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | order the notification stop updating s by test process | 0x300 | 0x1f46 | 0x0 |
    """
    command='shmwarmproc -f 0xffff -- -p "%s %s %s"  -t "sub"'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    if out.count('Subscribe stop_updating_s success') == 1:
        return 'success'
    else:
        return 'failure'
        
def receive_the_notification_stop_updating_s_by_test_process(computer_id,family_id,process_id):
    """ This keyword is to send msg to test process to receive the stop_updating_s.

    #COMMAND: shmwarmproc -- -p "0x700 12345 0" -t "cnt"
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | receive the notification stop updating s by test process by test process | 0x300 0x1f46 0x0 |
    """
    command='shmwarmproc -f 0xffff -- -p "%s %s %s" -t "cnt"'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    if out.count('Recv stop_updating_s 1 times') == 1:
        return 'success'
    else:
        return 'failure'

def clear_information_of_the_notification_stop_updating_s_by_test_process(computer_id,family_id,process_id):
    """ This keyword is to send msg to test process to clear the information of the stop_updating_s received.

    #COMMAND: shmwarmproc -- -p "0x700 12345 0" -t "clean"
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | clear information of the notification stop updating s received by test process | 0x300 0x1f46 0x0 |
    """
    command='shmwarmproc -f 0xffff -- -p "%s %s %s" -t "clean"'%(computer_id,family_id,process_id)
    connections.execute_mml_without_check(command)

def get_own_pid_of_process(process):
    """ This keyword get the PID by process

    #COMMAND: ps -ef | grep 'laucherstub'

    | Parameters  | Man. | Description  |
    | process | No   | process name and running process options |

    | Return value | pid |

    Example
    | pid  |  get own pid of process  | laucherstub |

    """
    processlist = []
    line_index = 0
    real_index = 0
    pid_flag = 0
    grep_string = "grep "

    command = "ps -ef | grep '" + process +"'"
    out = connections.execute_mml(command)

    lines = out.splitlines()
    #find the PID whinch contain process and is not the grep pid
    for line_index in range(0, len(lines)):
        if lines[line_index].find(process) > 0 and lines[line_index].find(grep_string + process) == -1:
            real_index = line_index
            pid_flag = 1
            break

    if 0 == pid_flag:
        return None
    processlist = lines[real_index].split()
    return processlist[1].strip()
  
def send_msg_to_run_crashme_case(computer_id,family_id,process_id,test_case_id):
    """ This keyword is to send msg to test process to run crashme case.

    #COMMAND: launcherstub -- -u 0x700 -f  0xc367 -p 0 -t 1
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | send msg to run crashme case | 0x700 0xc367 0x0 1 |
    """
    command='launcherstub  -f 0xffff -- -u %s -f %s -p %s -t %s '%(computer_id,family_id,process_id,test_case_id)
    out = connections.execute_mml_without_check(command)
    if process_id == '1' and out.count('Receive process_frozen_by_dmxrte_s from hand 1') == 1:
        return 'success'
    elif process_id == '0' and out.count('SUCCESS') == 1:
        return 'success'
    else:
        return 'failure'

def send_test_msg_to_check_process_alive(computer_id,family_id,process_id):
    """ This keyword is to send msg to check process alive by test process.

    #COMMAND: launcherstub -- -u 0x700 -f 0xc367 -p 1 -m
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | send msg to check process alive | 0x700 0xc367 0x0 |
    """
    command='launcherstub  -f 0xffff -- -u %s -f %s -p %s -m '%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    print out
    if out.count('master Receive c_test_msg_s') == 1:
        return 'success'
    else:
        return 'failure'

def send_msg_to_generate_process_fail_with_crashme(computer_id,family_id,process_id):
    """ This keyword is to send msg to generate process fail with crashme by test process.

    #COMMAND: launcherstub -- -u 0x700 -f 0xc367 -p 0 -r
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | send msg to generate process fail with crashme | 0x700 0xc367 0x0 |
    """
    command='launcherstub  -f 0xffff -- -u %s -f %s -p %s -r '%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    print out
    if process_id == '1' and out.count('Receive process_frozen_by_dmxrte_s from hand 1') == 1:
        return 'success'
    elif process_id == '0' and out.count('master Receive c_test_msg_s') == 1:
        return 'success'
    else:
        return 'failure'

def send_msg_to_enter_stateful_procedure(computer_id,family_id,process_id):
    """ This keyword is to send msg to enter stateful procedure by test process.

    #COMMAND: launcherstub -- -u 0x700 -f 0xc367 -p 0 -l
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | process_id       | Yes  | target process id                           |
    
    | Return value | command execution result |

    Example
    | result | send msg to enter stateful procedure| 0x700 0xc367 0x0 |
    """
    command='launcherstub  -f 0xffff -- -u %s -f %s -p %s -l '%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    if out.count('Enter stateful') == 1:
        return 'success'
    else:
        return 'failure'

def get_prb_buffer_info_by_diagste(in_unit_addr, in_family_id, hand_id=0):
    """ This keyword is to get prb buffer info by diagste.

    #COMMAND: diagste -u in_unit_addr -f in_family_id -r hmem -t get -d -p hand_id -m hum
    
    | Parameters        | Man. | Description                                 |
    | in_unit_addr      | Yes  | target computer physical address            |
    | in_family_id      | Yes  | target family address                       |
    | hand_id           | Yes  | hand_id                                     |
    
    
    | Return value | list of buffer info dictionary |

    Example
    | result | Get PRB Buffer Info By Diagste | 0x501 | 0x1f47 | 0 |
    """
    command = 'diagste -u %s -f %s -r hmem -t get -d -p %s -m hum' % (in_unit_addr, in_family_id, hand_id)
    print command
    result = connections.execute_mml_without_check(command)
    return _parse_buf_info(result)

def _parse_buf_info(in_info):
    info = in_info.replace('\r\n', '\n')
    buffer_list = info.split('buf_handle buffer_size buf_ptr\n')
    buff = buffer_list[1:]
    res_list = []
    for i in range (0, len(buff)):
        res_list.append(_parse_one_buf(buff[i]))
    _print_buf_dict_list(res_list)
    return res_list

def _parse_one_buf(in_buf):
    b_l = in_buf.split('buf_text\n')
    b_h_list = b_l[0].split()
    #print b_h_list
    #print b_l[1]
    b_d = {}
    b_d['buffer_handle'] = int(b_h_list[0], 16)
    b_d['buffer_size'] = int(b_h_list[1].replace('H',''), 16)
    #b_d['buffer_ptr'] = b_h_list[2]
    b_d['buffer_text'] = b_l[1].replace('\n', ' ').replace('  ', ' ').strip()
    #print b_d
    return b_d

def __print_buf_dict(in_buf_dict):
    print '\n'
    print 'buffer_handle:', in_buf_dict['buffer_handle']
    print 'buffer_size:', in_buf_dict['buffer_size']
    #print 'buffer_ptr:', in_buf_dict['buffer_ptr']
    print 'buffer_text:', in_buf_dict['buffer_text']

def _print_buf_dict_list(in_buf_dict_list):
    for i in range (0, len(in_buf_dict_list)):
        _print_buf_dict(in_buf_dict_list[i])
    
def _print_buf_dict(in_buf_dict):
    print ' ... | %x | %x | %s |' % ( in_buf_dict['buffer_handle'], in_buf_dict['buffer_size'], in_buf_dict['buffer_text'] )
    

def _create_buf_dict(in_buf_handle, in_buf_size, in_buf_text):
    b_d = {}
    b_d['buffer_handle'] = int(in_buf_handle, 16)
    b_d['buffer_size'] = int(in_buf_size, 16)
    #b_d['buffer_ptr'] = b_h_list[2]
    b_d['buffer_text'] = in_buf_text.encode()
    return b_d

def create_buf_info_dict_list(*in_args):
    arg_len = len(in_args)
    if arg_len % 3 <> 0:
        raise AssertionError(" number of argments is not multiple of 3: %d." % arg_len )
    buf_list = []
    for i in range (0, arg_len, 3):
        buf_list.append(_create_buf_dict(in_args[i], in_args[i+1], in_args[i+2]))
    print buf_list
    return buf_list

def buf_info_dict_list_should_be_equal(in_buf_list1, in_buf_list2):
    buf_len1 = len(in_buf_list1)
    buf_len2 = len(in_buf_list2)
    #BuiltIn().run_keyword("Should Be Equal", buf_len1, buf_len2)
    if buf_len1 != buf_len2:
        print buf_len1, '!=', buf_len2
        return 'failure'
    for i in range(0, buf_len1):
        if in_buf_list1[i]['buffer_size'] != in_buf_list2[i]['buffer_size']:
            print in_buf_list1[i]['buffer_size'], '!=', in_buf_list2[i]['buffer_size']
            return 'failure'
        if in_buf_list1[i]['buffer_handle'] != in_buf_list2[i]['buffer_handle']:
            print in_buf_list1[i]['buffer_handle'], '!=', in_buf_list2[i]['buffer_handle']
            return 'failure'
        if in_buf_list1[i]['buffer_text'] != in_buf_list2[i]['buffer_text']:
            print in_buf_list1[i]['buffer_text'], '!=', in_buf_list2[i]['buffer_text']
            return 'failure'
    return 'success'
        #BuiltIn().run_keyword("Should Be Equal", in_buf_list1[i]['buffer_size'], in_buf_list2[i]['buffer_size'])
        #BuiltIn().run_keyword("Should Be Equal", in_buf_list1[i]['buffer_handle'], in_buf_list2[i]['buffer_handle'])
        #BuiltIn().run_keyword("Should Be Equal As Strings", in_buf_list1[i]['buffer_text'], in_buf_list2[i]['buffer_text'])

def libgen_string_should_contain_substrings(in_string, in_substr1, in_substr2):
    if in_substr1 in in_string or in_substr2 in in_string:
        return 'success'
    else:
        return 'Cannot find %s or %s in %s.' % (in_substr1, in_substr2, in_string)

def libgen_count_range_should_be(in_info, in_min, in_max, in_format='info: %d'):
    l_min = int(in_min)
    l_max = int(in_max)
    for i in range (l_min, l_max+1):
        l_str = in_format % i
        if l_str in in_info:
            return 'success'
    return 'Cannot find number between %s and %s in %s.' % (in_min, in_max, in_info)

def libgen_test_forward_msg_to_sync_created_hand(in_cmd):
    out = connections.execute_mml_without_check(in_cmd)
    if out.count('successfully') == 2:
        match = re.search(r"\btest PRB create hand05 process id:\s*([0-9]*)", out, re.I)
        if match is not None:
            return 'success', match.group(1)
    return "test failed: %s" % out, 0

def _parse_one_hand_info(h_info):
    hand_dict = {}
    match = re.search(r"\s*([0-9A-F]*)  id", h_info, re.I)
    if match is not None:
        hand_dict['hand_group'] = int(match.group(1), 16)
    
    match = re.search(r"\bid \s*([0-9A-F]*)", h_info, re.I)
    if match is not None:
        hand_dict['process_id'] = int(match.group(1), 16)

    match = re.search(r"\bfo s*([0-9A-F]*)", h_info, re.I)
    if match is not None:
        hand_dict['focus'] = int(match.group(1), 16)

    match = re.search(r"\barmed timers     \s*([0-9]*)", h_info, re.I)
    if match is not None:
        hand_dict['armed_timers'] = int(match.group(1))

    match = re.search(r"\bsaved msg       \s*([YESNO]*)", h_info, re.I)
    if match is not None:
        hand_dict['saved_msg'] = match.group(1)

    match = re.search(r"\bprocess msg     \s*([YESNO]*)", h_info, re.I)
    if match is not None:
        hand_dict['process_msg'] = match.group(1)

    match = re.search(r"\bstateful proc   \s*([YESNO]*)", h_info, re.I)
    if match is not None:
        hand_dict['stateful_proc'] = match.group(1)
    
    match = re.search(r"\block wait       \s*([YESNO]*)", h_info, re.I)
    if match is not None:
        hand_dict['lock_wait'] = match.group(1)
    
    match = re.search(r"\bpending msg     \s*([YESNO]*)", h_info, re.I)
    if match is not None:
        hand_dict['pending_msg'] = match.group(1)
    
    match = re.search(r"\bprocess state    \s*([0-9]*)", h_info, re.I)
    if match is not None:
        hand_dict['process_state'] = int(match.group(1))

    match = re.search(r"\bwarm sync      \s*([YESNO]*)", h_info, re.I)
    if match is not None:
        hand_dict['warm_sync'] = match.group(1)

    match = re.search(r"\brefresh hand timer   \s*([YESNO]*)", h_info, re.I)
    if match is not None:
        hand_dict['refresh_hand_timer'] = match.group(1)

    return hand_dict

def _print_hand_dict_list(hand_dict_list):
    for i in range (0, len(hand_dict_list)):
        _print_hand_dict(hand_dict_list[i])
    
def _print_hand_dict(in_dict):
    #print in_dict
    print '\n'
    print 'hand_group:        ', in_dict['hand_group']
    print 'process_id:        ', in_dict['process_id']
    print 'armed_timers:      ', in_dict['armed_timers']
    print 'saved_msg:         ', in_dict['saved_msg']
    print 'process_msg:       ', in_dict['process_msg']
    print 'stateful_proc:     ', in_dict['stateful_proc']
    print 'lock_wait:         ', in_dict['lock_wait']
    print 'pending_msg:       ', in_dict['pending_msg']
    print 'process_state:     ', in_dict['process_state']
    print 'warm_sync:         ', in_dict['warm_sync']
    print 'refresh_hand_timer:', in_dict['refresh_hand_timer']
        
        
def _parse_hands_info(in_out):
    hand_list=[]
    hand_count=0
    if in_out.count('no active hands') == 1:
        return hand_list, hand_count
    match = re.search(r"\bactive hands\s*([0-9]*)",in_out, re.I)
    if match is not None:
        hand_count = int(match.group(1))
    info = in_out.replace('\r\n', '\n') 
    hands = info.split('hg')
    hands = hands[1:]
    for i in range (0, len(hands)):
        hand_list.append(_parse_one_hand_info(hands[i]))
    return hand_list, hand_count   

def _get_process_id_by_hand_group(in_hand_info_list, in_hand_group, in_old_process_id_list):
    process_ids = []
    _print_hand_dict_list(in_hand_info_list)
    for i in range (0, len(in_hand_info_list)):
        if in_hand_info_list[i]['hand_group'] == int(in_hand_group) and in_hand_info_list[i]['process_id'] not in in_old_process_id_list:
            process_ids.append(in_hand_info_list[i]['process_id'])
    return process_ids

def libgen_get_process_id_by_diagste(in_cmd, in_hand_group_id, in_old_process_id_list=[]):
    """ This keyword is to get prb target hand group's process ids by diagste (excluding process ids in in_old_process_id_list).

    #COMMAND: diagste -u unit_addr -f family_id -r han -t idata -m hum
    
    | Parameters              | Man. | Description                                 |
    | in_cmd                  | Yes  | diagste command                             |
    | in_hand_group_id        | Yes  | target hand group id                        |
    | in_old_process_id_list  | No   | old process ids list                        |
    
    
    | Return value | list hand process ids |

    Example
    | result | Libgen Get Process Id By Diagste | diagste -u 0x0600 -f 0x1773 -r han -t idata -m hum | 6 |
    """
    out = connections.execute_mml_without_check(in_cmd)
    hand_list, hand_count = _parse_hands_info(out)
    return _get_process_id_by_hand_group(hand_list, in_hand_group_id, in_old_process_id_list)

def libgen_execute_command_and_return_result(in_success_result, in_success_res_count, in_failure_result, in_failure_res_count, in_command, *in_args):
    """This keyword is to execute a command and check result.
    If return contains in_success_res_count of in_success_result, return result.
    Else if return contains in_failure_res_count of in_failure_result, return 'failure'.
    else return 'the return is wrong '+result.
    | Parameters           | Man. | Description                                                          |
    | in_success_result    | Yes  | string to be found in return result of the command, e.g., 'success'  |
    | in_success_res_count | Yes  | count of success_result, e.g., '1'                                   |
    | in_failure_result    | Yes  | string to be found in return result of the command, e.g., 'failure'  |
    | in_failure_res_count | Yes  | count of failure_result, e.g., '1'                                   |
    | in_command           | Yes  | command to be executed, e.g., 'ILLGTestCli -- -r %s %s %s'           |
    | in_args              | No   | arguments that may be needed in command                              |
   
    | Return value | command execution result |
    Example
    | ${result}= | Libgen Execute Command And Check Result | success | 1 | failure | 1 | 
    | ...        | ILLGTestCli -- -r %s %s %s %s %s -w %s %s %s %s %s % s | 0x700 | 0x1771 |
    | ...        | 0x0 | 0x6034 | 0xffff11 | 0x1 | 0x2 | 0x200 | 0x1 | 0x0 | 0x100 |
    """
    if len(in_args) > 0:
        command = in_command % (in_args)
    else:
        command = in_command
    out = connections.execute_mml_without_check(command)

    if out.count(in_success_result) == int(in_success_res_count):
        return out
    elif out.count(in_failure_result) == int(in_failure_res_count):
        return 'failure'
    else:
        return 'failure, the return is wrong: '+out



def check_message_load_information(in_result, k_info, l_info, ker_used, lib_used, ker_limit, lib_limit, thread_num):
    """This keyword is to check message load information.
    | Parameters           | Man. | Description                                                      |
    | in_result    	   | Yes  | the return result need to check the message load infortion	     |
    | k_info       	   | Yes  | the msg number of kernel queue      	                     |
    | l_info               | Yes  | the msg number of libgen queue    	                             |
    | ker_used       	   | Yes  | the msg used size of kernel queue                                |
    | lib_used             | Yes  | the msg used size of libgen queue                                |
    | ker_limit       	   | Yes  | the msg size limit of kernel queue                               |
    | lib_limit            | Yes  | the msg size limit of libgen queue                               |
    | thread_num           | Yes  | thread num configured for the test process                       |
   
    | Return value | command execution result |
    Example
    | ${result}= | Check Message Load Information | in_result | 100 | 100 | 19498194 | 6624000 | 20971520 | 94370400 | 
    """
    match2 = re.search(r"\s*info:\s*([0-9]*),\s*([0-9]*),\s*([0-9]*)\s*([0-9]*),\s*([0-9]*),\s*([0-9]*)\s*", in_result, re.I)
    if match2 is not None:
        l_size = int(lib_used)
        k_size = int(ker_used)
        num = int(thread_num)-1
        if match2.group(1) == l_info and match2.group(3) == lib_limit and match2.group(4) == k_info and match2.group(6) == ker_limit:
            print 'lib and kernel queue msg count and limit match'
            if num > 0:
                if ( int(match2.group(2)) < ( l_size+65500 ) and int(match2.group(2)) > ( l_size-65500 ) ) or ( int(match2.group(2)) < ( l_size+65500-65500*2*num ) and int(match2.group(2)) > ( l_size-65500-65500*3*num ) ):
                    print 'lib used size match'
                else:
                    print 'failure, lib used size not match'
                    return 'failure'
            else:
                if int(match2.group(2)) < ( l_size+65500 ) and int(match2.group(2)) > ( l_size-65500 ):
                    print 'lib used size match'
                else:
                    print 'failure, lib used size not match'
                    return 'failure'
            if int(match2.group(5)) == k_size:
                print 'kernel used size match'
            else:
                print 'failure, kernel used size not match'
                return 'failure'
        else:
            print match2.group(1), match2.group(2), match2.group(3), match2.group(4), match2.group(5), match2.group(6)
            print l_info, lib_used, lib_limit, k_info, ker_used, ker_limit
            print l_size, k_size
            print 'lib and kernel queue not match'
            return 'failure'
    else:
        return 'no lib and kernel queue info, failure'
    return 'success'
    
def send_message_to_test_process_and_monitor(monitor_command, command, delay=3, retry=3):
    """This keyword is to trigger CLI to send message to test process and catch the received message by monster

    #COMMAND: testmon.py -p "-u 0x700 -f 0x1f48" -c "WMNotifstub -f 0xffff -- -u 0x700 -f 0x1f48 -t 1" -t delay
    | Parameters            | Man. | Description                                  |
    | monitor_command       | Yes  | the monster's commmand       |
    | command               | Yes  | the command to monitor      |
    | delay                 | No   | delay time python script will kill monster process after message sent out |
       
    | Return value | command execution result |

    Example
    | ${result} | send message to test process and monitor | -u 0x700 -f 0x1f48 | WMNotifstub -f 0xffff -- -u 0x700 -f 0x1f48 -t 1 | 3 | 
    """
    command='testmon.py -p "%s -V" -c "%s" -t %s -r %s'%(monitor_command,command,delay,retry)
    out = connections.execute_mml_without_check(command)
    if out.count('RECEIVE ACK MSG.') == 1 or out.count('Create hand success') == 1 or out.count('success') >= 1:
        return out
    else:
        return 'failure'

def get_msg_from_monitoring_result(msg_buf, filter_data=1):
    """This keyword is to get msg from monitoring result

    #COMMAND: get_msg_from_monitoring_result(msg_buf, 1, '^0[1-5] 00 00 00\s*$')
    | Parameters            | Man. | Description                                  |
    | msg_bug               | Yes  | the catched message string monitored by monster       |
    | filter_data           | Yes  | the option to whether filter specific data match regre      |
       
    | Return value | command execution result |

    Example
    | ${result} | get msg from monitoring result  | msg_buf | 1 | ^0[1-5] 00 00 00\s*$ | 
    """
    l = get_msg_from_buf(msg_buf)
    m_l = [parse_msg(i) for i in l]
    if filter_data == '0': 
        return m_l
    l = []
    for msg in m_l:
        if re.search(r"^0[1-5] 00 00 00\s*$", msg['data'], re.I) is None:
            l.append(msg)
    return l

def check_msg_comp_addr(msg_list, comp_addr):
    """This keyword is to check msg comp addr

    #COMMAND: check_msg_comp_addr(msg_list, comp_addr)
    | Parameters            | Man. | Description                                  |
    | msg_list              | Yes  | the catched message list monitored by monster       |
    | comp_addr             | Yes  | the computer address      |
       
    | Return value | command execution result |

    Example
    | ${result} | check msg comp addr | msg_list | comp_addr | 
    """
    if len(msg_list) < 1:
        return 'failure'
    from string import atoi
    phys_addr = atoi(comp_addr, 16)
    if len(msg_list) == 0:
        return 'failure'
    for msg in msg_list:
        if msg['bottom']['phys_computer'] == phys_addr:
            continue
        elif msg['bottom']['phys_computer'] == 28674:
            continue
        else:
           print 'fail: ', msg['bottom']['phys_computer']
           return 'failure'
    return 'success'

def check_equal_msg_sequence_number_in_both_side(msg_list, family_id=0):
    """This keyword is to check equal msg sequence number in both side

    #COMMAND: check_equal_msg_sequence_number_in_both_side(msg_list, family_id)
    | Parameters            | Man. | Description                                  |
    | msg_list              | Yes  | the catched message list monitored by monster       |
    | family_id             | Yes  | the family id                                |
       
    | Return value | command execution result |

    Example
    | ${result} | check equal msg sequence number in both side | msg_list | family_id |
    """
    from string import atoi
    if len(msg_list) <= 1:
        return 'failure'
    recv_list = get_msgs_by_type(msg_list, type='recv')
    send_list = get_msgs_by_type(msg_list, type='sent')
    if len(recv_list) != len(send_list):
        return 'failure'
    fam_id = int(atoi(family_id, 16))
    for smsg in send_list:
        found = 0
        if fam_id == 0:
            found = check_equal_msg_sequence_number(smsg, recv_list)
        else:
            print fam_id, smsg['msg']['family']
            if fam_id == smsg['msg']['family']:
                found = check_equal_msg_sequence_number(smsg, recv_list)
            else:
                continue
        if found == 0:
            return 'failure'
    return 'success'

def check_equal_msg_sequence_number(msg, recv_list):
    """This keyword is to check equal msg sequence number

    #COMMAND: check_equal_msg_sequence_number(msg, recv_list)
    | Parameters            | Man. | Description                                  |
    | msg                   | Yes  | the catched message                          |
    | recv_list             | Yes  | the catched message list  monitored by monster      |
       
    | Return value | command execution result |

    Example
    | ${result} | check equal msg sequence number | msg | recv_list |
    """
    found = 0
    if msg['bottom']['sequence_number'] == 0:
        return 0
        for rmsg in recv_list:
            if msg['bottom']['sequence_number'] == rmsg['bottom']['sequence_number'] and msg['data'] == rmsg['data']:
                found = 1; break
        if found == 0:
            print 'fail: ', msg['bottom']['sequence_number']
            return 0
    return 1

def sequence_number_increasing_by_order(msg_list, step):
    """This keyword is to get msg from monitoring result

    #COMMAND: sequence_number_increasing_by_order(msg_list, step)
    | Parameters            | Man. | Description                                  |
    | msg_list              | Yes  | the catched message list monitored by monster       |
    | step                  | Yes  | the increased number for sequence number in catched message |
       
    | Return value | command execution result |

    Example
    | ${result} | sequence number increasing by order | msg_list | step | 
    """
    if len(msg_list) >1:
      sequence = -2
      for msg in msg_list:
        if sequence == -2 and msg['bottom']['phys_computer'] == msg['msg']['phys_computer']:
            sequence =  msg['bottom']['sequence_number']
            if sequence == 0:
                return 'failure'
            else:
               sequence = sequence - 1
        print msg['bottom']['sequence_number']
        if step == '1':
            if msg['bottom']['phys_computer'] == msg['msg']['phys_computer']:
                if msg['bottom']['sequence_number'] == (sequence + 1):
                    print "==seqnum+1: ", sequence + 1
                    sequence = sequence + 1
                #elif (sequence - msg['bottom']['sequence_number']) > 65535:
                #    sequence = sequence - msg['bottom']['sequence_number' - 1
                else:
                    print msg['bottom']['sequence_number'], "!=", sequence
                    return 'failure'
        else:
            if msg['bottom']['phys_computer'] == msg['msg']['phys_computer']:
                if msg['bottom']['sequence_number'] > sequence:
                    print "> seqnum: ", sequence
                    sequence = msg['bottom']['sequence_number']
                #elif (sequence - msg['bottom']['sequence_number']) > 65535:
                #    sequence = sequence - msg['bottom']['sequence_number' - 1
                else:
                    print msg['bottom']['sequence_number'], '<=', sequence
                    return 'failure'

def check_the_sequence_number_increasing_by_order(msg_list, step=1):
    """This keyword is to check the sequence number increasing by order

    #COMMAND: check_the_sequence_number_increasing_by_order(msg_list, step)
    | Parameters            | Man. | Description                                  |
    | msg_list              | Yes  | the catched message list monitored by monster       |
    | step                  | Yes  | the increased number for sequence number in catched message |
       
    | Return value | command execution result |

    Example
    | ${result} | check the sequence number increasing by order | msg_list | step |
    """
    from string import atoi
    istep = int(atoi(step, 10)) 
    if len(msg_list) <= 1:
        return 'failure'
    send_list = get_msgs_by_type(msg_list, type='sent')
    recv_list = get_msgs_by_type(msg_list, type='recv')
    if len(send_list) <=1 and len(recv_list) <= 1:
       return 'failure'
    if sequence_number_increasing_by_order(send_list, istep) == 'failure':
        return 'failure'
    if sequence_number_increasing_by_order(recv_list, istep) == 'failure':
        return 'failure'
    return 'success'

def check_sequence_number_is_zero(msg_list, type='sent', flag='true'):
    """This keyword is to check whether the sequence number is zero

    #COMMAND: check_sequence_number_is_zero(msg_list, type, flag)
    | Parameters            | Man. | Description                                  |
    | msg_list              | Yes  | the catched message list monitored by monster       |
    | type                  | Yes  | the monitored message type: send or recv |
    | flag                  | Yes  | the flag check the sequence number is zero or not |
       
    | Return value | command execution result |

    Example
    | ${result} | check sequence number is zero | msg_list | sent | true |
    """
    if len(msg_list) <= 1:
        return 'failure'
    list = get_msgs_by_type(msg_list, type)
    print list
    for msg in list:
        if flag == 'true':
            if msg['bottom']['sequence_number'] == 0:
                continue
            else:
                return 'failure'
        else:
            if msg['bottom']['sequence_number'] > 0:  
                continue
            else:
                return 'failure'
    return 'success'

def check_two_date_time_is_match(date1, date2):
    """This keyword is to check whether two date time is match

    #COMMAND: check_two_date_time_is_match(date1, date2)
    | Parameters            | Man. | Description                                      |
    | date1                 | Yes  | the compared date printed by command ilglovar    |
    | date2                 | Yes  | the compared date printed by command date        |
       
    | Return value | command execution result |

    Example
    | ${result} | chech two date time is match | date1 | date2 |
    """
    times1 = [0,0,0,0,0,0]
    times2 = date2.strip().split('-')
    lines = date1.strip().splitlines()
    for line in lines:
        match = None
        match = re.search(r".*calendar_time\.([a-z]+):([0-9]+).*", line, re.I)
        if match is not None:
            if match.group(1) == 'year':
                times1[0] = match.group(2)
            if match.group(1) == 'month':
                times1[1] = match.group(2)
            if match.group(1) == 'day':
                times1[2] = match.group(2)
            if match.group(1) == 'hours':
                times1[3] = match.group(2)
            if match.group(1) == 'minutes':
                times1[4] = match.group(2)
            if match.group(1) == 'seconds':
                times1[5] = match.group(2)
    print times1, times2
    from string import atoi
    if atoi(times1[0]) == atoi(times2[0]) and atoi(times1[1]) == atoi(times2[1]) and atoi(times1[2]) == atoi(times2[2]) and atoi(times1[3]) == atoi(times2[3]) and atoi(times1[4]) <= atoi(times2[4]):
         return 'success'
    else:
         return 'failure'

def check_message_time(msg_buf):
    """This keyword is to check message time whether matched the datetime we expected

    #COMMAND: check_message_time(msg_buf)
    | Parameters            | Man. | Description                                      |
    | msg_buf                 | Yes  | the monitored messages                         |
       
    | Return value | command execution result |

    Example
    | ${result} | chech message time | msg_buf |
    """
    lines = msg_buf.strip().splitlines()
    for line in lines:
        match = re.search(r"MONITORING TIME: 2011-03-27\s*([01][0-9]):.*", line, re.I)
        if match is not None:
            if  match.group(1) == '02' or match.group(1) == '04':
                continue
            else:
                print line
                return 'failure'
    return 'success'

def check_all_rus_status(RUs):
    """This keyword is to check all RUs status

    #COMMAND: check_all_rus_status(RUs)
    | Parameters            | Man. | Description  		| 
    | RUs		    | Yes  | the RUs list 		|

    | Return value | command execution result |

    Example
    | ${result} | chech all rus status | RUs |
    """
    lines = RUs.splitlines()
    print lines
    for ru in lines:
        command='fshascli -s %s'%(ru)
        out = connections.execute_mml_without_check(command)
        match = re.search(r".*administrative.*", out, re.I)
        if match is not None:
            if out.count('operational(ENABLED)') == 1 and out.count('usage(ACTIVE)') == 1:
                continue
            else:
                return 'failure'
        return 'failure'
    return 'success'

def get_output(str=''):
    """This keyword is to get the output from screen

    #COMMAND: get_output()
    | Parameters            | Man. | Description  		| 

    | Return value | command execution result |

    Example
    | ${result} | get output |
    """
    if len(str) >0:
        out = connections.execute_cmd_with_check_expected('', str, 3)
    else:
        import time
        time.sleep(2)
        out = connections.execute_cmd_with_check_expected('echo test', "test", 2)
    return out

def get_node_from_unit(unit_name):
    """This keyword is to get node from unit name

    #COMMAND: get_node_from_unit(unit_name)
    | Parameters            | Man. | Description                | 
    | unit_name		    | Yes  | unit name			|

    | Return value | command execution result |

    Example
    | ${result} | Get Node From Unit | /CLA-0/OMUTestServer-0 |
    """
    match = re.search(r"/(.*)/(.*)", unit_name, re.I)
    if match is None:
        exceptions.raise_ILError("ILKeywordSyntaxError", "%s is not unit"%unit_name)
    else:
        return match.group(1)

def get_current_max_stack_count(in_unit_addr, in_family_id):
    """This keyword is to get current process max stack use

    #COMMAND: diagste -u in_unit_addr -f in_family_id -r stack -t idata
    
    | Parameters        | Man. | Description                                 |
    | in_unit_addr      | Yes  | target computer physical address            |
    | in_family_id      | Yes  | target family address                       |
    
    
    | Return value | the max stack count used in the process |

    Example
    | result | Get Current Max Stack Count | 0x501 | 0x1f47 |
    """
    command = 'diagste -u %s -f %s -r stack -t idata -m hum' % (in_unit_addr, in_family_id)
    out = connections.execute_mml_without_check(command)
    print out
    match = re.search(r"\Max stack count is\s*([0-9]*)", out, re.I)
    if match is not None:
        return match.group(1)
    else:
        return 'failure'
    #print result

def get_current_max_message_pool_used_size(in_unit_addr, in_family_id):
    """This keyword is to get current process message pool used size

    #COMMAND: diagste -u in_unit_addr -f in_family_id -r msgpool
    
    | Parameters        | Man. | Description                                 |
    | in_unit_addr      | Yes  | target computer physical address            |
    | in_family_id      | Yes  | target family address                       |
    
    
    | Return value | the max stack count used in the process |

    Example
    | result | Get Current Max Stack Count | 0x501 | 0x1f47 |
    """
    command = 'diagste -u %s -f %s -r msgpool -t idata -m hum' % (in_unit_addr, in_family_id)
    out = connections.execute_mml_without_check(command)

    lines = out.strip().splitlines()
    match = re.search(r"\max used size:\s*([0-9]*)", lines[4], re.I)

    if match is not None:
        return match.group(1)
    else:
        return 'failure'

def kill_process_by_pid_with_option_9(pid):
    """ This keyword to kill give process with -9 option by pid
    
    #COMMAND: kill

    | Parameters  | Man. | Description  |
    | pid         | Yes  | process id |
        
    | Return value | No return value |
        
    Example
    | ${result}  |  Kill Process By PID With Option 9| 4321  |

    """
    command = "kill -9 " + pid
    out = connections.execute_mml(command)

def start_cli_at_background_and_return_linux_pid(command):
    """This keyword is to start cli at background and return linux process id.
    
    | Parameters   | Man. | Description            |
    | command  | Yes  | the CLI command to be executed   |

    | Return value | the linux process id |

    Example
    | result | start cli at background and return linux pid |  monster & |
    """   
    out = connections.execute_cli(command)
    result_list = out.split()
    return result_list[1].strip()

def libgen_should_contain_x_times(in_item1, in_item2, in_count):
    """This keyword is to check if in_item1 contains in_item2 in_count times.
    It fails if in_item1 does not contain in_item2 in_count times
    
    Example
    | Libgen Should Contain X Times  |  Hello world | o | 2 |
    """   
    my_count = in_item1.count(in_item2)
    required_count = int(in_count)
    BuiltIn().run_keyword("Should Be Equal", my_count, required_count)

def libgen_timer_sequence_should_be(in_monitored_messages, in_timer_id, in_timer_seq):
    """This keyword is to check if in_monitored_messages contains timer in_timer_id message 
    and the timer sequence is in_timer_seq.
    It fails if in_monitored_messages does not contain timer message of in_timer_id or 
    the timer sequence is not in_timer_seq.
    
    Example
    ${mon_ifo} = 'MONITORING TIME: 2011-12-08    15:34:11.153011    000255B3 4EE0D8F3
RECEIVED BY: 1773 0000 00
BOTTOM: 7002 1773 0000 00 48 01 00 0206 0300 00 04 0000 00003C49
MONITORED MESSAGE: 0010 7002 1773 0000 00 21 0051 9915 0300'
    | Libgen Timer Sequence Should Be  |  ${mon_info} | 9915 | 02 |
    """   
    timer_msg = ' 0051 %s' % in_timer_id
    BuiltIn().run_keyword("Should Contain", in_monitored_messages, timer_msg)
    
    msg_list = in_monitored_messages.split("MONITORING TIME")
    wanted_msg = ''
    for msg in msg_list:
        if timer_msg in msg:
            wanted_msg = msg
            break
    BuiltIn().run_keyword("Should Not Be Equal", len(wanted_msg), 0)
    lines = wanted_msg.split('\n')
    wanted_line = ''
    for line in lines:
        if 'BOTTOM:' in line:
            wanted_line = line
            break
    strs = wanted_line.split(' ')
    cmd = 'echo $HW_PLATFORM'
    hw_type = connections.execute_mml_without_check(cmd)
    if hw_type.strip() == 'ATCA':
        timer_sequence = strs[8][2:4]
    else:
        timer_sequence = strs[8][0:2]
    BuiltIn().run_keyword("Should Be Equal As Strings", timer_sequence, in_timer_seq)

def libgen_get_pid_of_running_app(in_running_app):
    command = 'ps aux |grep %s |grep grep -v' % (in_running_app)
    out = connections.execute_mml_without_check(command)
    if len(out.split()) > 8:
        return out.split()[1]
    else:
        return "None"

def check_equal_msg_in_both_list(arrv_list, recv_list, msg_cnt):
    """This keyword is to check equal msg in both list

    #COMMAND: check_equal_msg_in_both_list(arrv_list, recv_list, msg_cntx)
    | Parameters            | Man. | Description                                  |
    | arrv_list              | Yes  | the catched message recv list monitored by monster       |
    | recv_list              | Yes  | the catched message arrv list monitored by monster       |
    | msg_cnt              | Yes  | the catched message msg count       |
       
    | Return value | command execution result |
    
    Example 
    | ${result} | check equal msg in both list | arrv_list | recv_list| msg_cnt |
    """
    for i in range(0, len(arrv_list)-1):
        msg = arrv_list[i]
        rmsg = recv_list[i]
        if msg['bottom']['sequence_number'] == rmsg['bottom']['sequence_number'] and msg['data'] == rmsg['data']:
            continue
        else:
            print 'fail: ', msg['bottom']['sequence_number']
            return 'failure'
    return 'success'

def check_each_msg_time_less_than(arrv_list, recv_list, diff_time):
    """This keyword is to check each msg time in arrv_list less than recv_list

    #COMMAND: check_each_msg_time_less_than(arrv_list, recv_list, msg_cnt, family_id)
    | Parameters            | Man. | Description                                  |
    | arrv_list              | Yes  | the catched message recv list monitored by monster       |
    | recv_list              | Yes  | the catched message arrv list monitored by monster       |
    | diff_time              | Yes  | diff time in unit 10ms       |
       
    | Return value | command execution result |
    
    Example 
    | ${result} | check each msg time less than | arrv_list | recv_list| diff_time |
    """
    import datetime
    if len(recv_list) != len(arrv_list):
        return 'failure'
    for i in range(len(arrv_list)):
        msg = arrv_list[i]
        rmsg = recv_list[i]
        if msg['bottom']['sequence_number'] == rmsg['bottom']['sequence_number'] and msg['data'] == rmsg['data']:
            dt_arrv= BuiltIn().run_keyword("convert_time", msg['time']['date'], msg['time']['time'])
            dt_recv = BuiltIn().run_keyword("convert_time", rmsg['time']['date'], rmsg['time']['time'])
            i_diff = int(diff_time)
            if i_diff != 0:
                 i_diff = i_diff - 1
            if dt_recv >= (dt_arrv+datetime.timedelta(microseconds=i_diff*10000)):
                continue
            else:
                print 'fail: ', msg['time']['time'], rmsg['time']['time']
                return 'failure'
    return 'success'

def get_process_heap_info_from_smaps(pid, item):
    """This keyword is to get process heap info:item from smaps

    #COMMAND: get_process_heap_info_from_smaps(pid, item)
    | Parameters            | Man. | Description                                  |
    | pid         	    | Yes  | the process PID
    | item             	    | Yes  | which info of process heap info 
       
    | Return value | command execution result |
    
    Example 
    | ${result} | get process heap info from smaps | 27575 | Rss |
    """
    command='grep heap /proc/%s/smaps  -A 6'%(pid)
    out = connections.execute_mml_without_check(command)
    output_pattern = re.compile(item+":\s+(\d+) kB", re.I)
    info=output_pattern.search(out)
    if info is None:
        exceptions.raise_ILError("ILCommandExecuteError", "failed to heap info from smaps")
    else:
        print info.group(1)
        return info.group(1)

def get_process_specific_segment_info_from_smaps(pid, seg, item):
    """This keyword is to get process specific segment info:item from smaps

    #COMMAND: get_process_specific_segment_info_from_smaps(pid, seg, item)
    | Parameters            | Man. | Description                                  |
    | pid                   | Yes  | the process PID
    | seg                   | Yes  | which seg of the process
    | item                  | Yes  | which info of one process segment
       
    | Return value | command execution result |
    
    Example 
    | ${result} | get process specific segment info from smaps | 27575 | 600000b000 | Rss |
    """
    command='grep %s /proc/%s/smaps  -A 6'%(seg, pid)
    out = connections.execute_mml_without_check(command)
    output_pattern = re.compile(item+":\s+(\d+) kB", re.I)
    info=output_pattern.search(out)
    if info is None:
        exceptions.raise_ILError("ILCommandExecuteError", "failed to get segment info from smaps")
    else:
        print info.group(1)
        return info.group(1)

def isset_robotvariable(name):
    if robot.__version__ < '2.1.3':
        iname = """${%s}""" % (name.lower().replace('_', ''))
        from robot.libraries.BuiltIn import Variables as var
        variables = var()._get_variables()
        names = variables.keys()
    else:
        iname = """${%s}"""% (name)
        variables = BuiltIn().get_variables()
        names = variables.keys()
    isset = iname in names
    print isset
    return isset

def restart_mo_and_register_alarm(name, alarm='70186',seconds='1.5'):
    """ This keyword is to restart the specific managed object.

    #COMMAND: fshascli -rnF <name>

    | Parameters | Man. | Description         |
    | name       | Yes  | managed object name |
    | alarm      | Yes  | 70186 	          |
    | seconds    | Yes  | 1.5                 |

    | Return Value | None  |

    Exceptions: If the command fails an exception is raised.
    | Exception | Text | Additional Output |
    | ILCommandExecuteError | ILCommandExecuteError | Output of command |

    Example
    | restart mo and register alarm |  name  |

    """
    ret = isset_robotvariable('TEST_NAME')
    print connections.execute_mml('date')
    if ret == True:
        print 'register alarm'
        syslog_lib.register_expect_alarm(alarm)
    command = "fshascli -rnF " + name
    out = connections.execute_mml(command)
    if out.count('successful') == 0:
        raise exceptions.raise_ILError("ILCommandExecuteError", out)
    connections.execute_mml("sleep " + seconds)

def update_ini_configuration(config_file, type, prb_idx, item, new_item, backup_flag=''):
    """ This keyword is to update the family's configuration in the ini configuration file

    | Parameters	| Man. | Description                                 |
    | config_file	| Yes  | libgen configuration file, it can be get via environment variable GET_CONFIG |
    | type 		| Yes  | remove, add, replace          |
    | prb_idx		| Yes  | target family master process name index in ini config file                      |
    | item		| Yes  | the old context, if add, it is ignored  |
    | new_item		| Yes  | the new context, if remove, it is ignored |
    | backup_file	| No   | whether backup the config file, 'SAVE' represent backup, others does not|

    Example
    | ${result} | update ini configuration  | remove | upgtstprocmas | handgroup_2_first_id=100 | null | SAVE |
    | ${result} | update ini configuration  | add | upgtstprocmas | null | handgroup_2_first_id=100 |
    | ${result} | update ini configuration  | replace | upgtstprocmas | handgroup_2_first_id=100 | handgroup_2_first_id=200 |
    """
    from string import atoi
    print 'update for prb %s: %s -> %s'%(prb_idx, item, new_item)

    command = """grep -n %s %s"""%(prb_idx, config_file)
    out = connections.execute_mml_without_check(command)
    if not out.count(prb_idx):
        print 'Can not found the prb %s in %s'%(prb_idx, config_file)
        return 'failure'

    if type.upper() == 'REMOVE':
        command="""sed -i '/%s/,/^ *$/ s/%s//' %s""" %(prb_idx, item, config_file)
    elif type.upper() == 'ADD':
        command="""sed -i '/%s/a \\%s' %s""" %(prb_idx, new_item, config_file)
    elif type.upper() == 'REPLACE':
        command="""sed -i '/%s/,/^ *$/ s/%s/%s/' %s""" %(prb_idx, item, new_item, config_file)
    else:
        print 'Operation must be remove, add, replase.'
        return 'failure'
    #only command and arguments correct, do backup original config file 
    if backup_flag.upper() == 'SAVE':
        bakup_file = config_file + ".bak"
        cmd = 'cp %s %s'%(config_file, bakup_file)
        connections.execute_mml_without_check(cmd,'yes')

    connections.execute_mml_without_check(command)

    if backup_flag.upper() == 'SAVE':
        return bakup_file
    else:
        return 'success'

def libgen_get_ru_startup_sequence(ru_type, ru_index, ru_mo_name, prb_filter="TestWarmStub|TestThermoStub"):
    """ This keyword is to get the ru startup sequnence for prb_filter

    | Parameters | Man. | Description                                 |
    | ru_type    | Yes  | the RU type, e.g., OMU |
    | ru_index   | Yes  | the RU index, e.g., 0 |
    | ru_mo_name | Yes  | the RU MO name, e.g., /CFPU-0/QNOMUServer-0 |
    | prb_filter | No   | filter used by grep -E prb_filter, default value: "TestWarmStub|TestThermoStub" |
    
    return the start up sequence of given prb filters.

    Example
    | ${result} | Libgen Get Ru Startup Sequence  | OMU | 0 | /CFPU-0/QNOMUServer-0 |
    
    """
    mo_name = ru_mo_name.replace("/", "\/")
    command =  '''fsclish -c "show has functional-unit startup-info parameter unit-type %s unit-index %s" |grep -E "%s" |sed ':a;N;s/\\n//g;ta'|sed 's/%s\///g'|sed 's/ //g' ''' %(ru_type, ru_index, prb_filter, mo_name)
    print command
    out = connections.execute_mml_without_check(command)
    print out
    return out.strip()

def libgen_get_hand_group_parameter_by_diagste(in_ru_phys_addr, in_family_id, in_hand_group_id, in_filter="hand group size"):
    """ This keyword is to get the family in_family_id 's hand group in_hand_group_id's parameter according to in_filter

    | Parameters    | Man. | Description                                 |
    | ru_phys_addr  | Yes  | 0x0100 |
    | family_id     | Yes  | 0x1773 |
    | hand_group_id | Yes  | 11 |
    | filter        | No   | filter used by grep -E filter, default value: "hand group size", return hand group size |
    
    return the parameter of hand group with given filter.

    Example
    | ${result} | Libgen Get Hand Group Parameter By Diagste  | 0x0100 | 0x1773 | 11 |
    
    """
    command = '''diagste -u %s -f %s -r hddt_stat |grep "hand group %s" -A 10|grep "%s" ''' %(in_ru_phys_addr, in_family_id, in_hand_group_id, in_filter)
    print command
    out = connections.execute_mml_without_check(command)
    print out
    if len(out) > 0 and out.find(":") > 0:
        return out.split(":")[1].strip()
    else:
        return out

def create_hand_for_specific_handgroup_in_warmtstproc(computer_id,family_id,handgroup_id,process_id='0'):
    """This keyword is to send a msg to target process for create hand.if create hand timeout,return the process_id.

    #COMMAND: mempoolproc -f 0xffff -- -p "0x7002 0x1773 0" -v warmtst_create_hand -t 9 

    | Parameters  | Man. | Description                                 |
    | computer_id | Yes  | target computer address                     |
    | family_id   | Yes  | target family addres                        |
    | handgroup_id   | Yes  | target family's handgroup id             |
    | process_id  | Yes  | target process id                           |
   
    | Return value | command execution result |

    Example
    | result | create_hand_for_specific_handgroup_in_warmtstproc | 0x7002 | 0x1773 | 9 | 0 |
    """
    if process_id == '0':
        command='mempoolproc -f 0xffff -- -p "%s %s 0" -v warmtst_create_hand -t %s'%(computer_id,family_id,handgroup_id)
    else:
        command='mempoolproc -f 0xffff -- -p "%s %s 0" -v warmtst_create_spec_hand -t %s -a %s'%(computer_id,family_id,handgroup_id,process_id)

    out = connections.execute_mml_without_check(command)

    if out.count('successfully') != 2:
        return 'failure'
    elif out.count('successfully') == 2:
        match = re.search(r"\s*Created hand process id:\s*([0-9a-fA-Z]*)", out, re.I)
        if match is not None:
            return 'success', match.group(1)
    else:
        return 'failure'
        
def get_configue_range_information(computer_id, family_id):
    """This keyword is to get the configue range information.

    #COMMAND: get the configue range information [computer_id] [family_id]

    | Parameters   | Man. | Description                                 |
    | computer_id  | Yes  | target computer address |
    | family_id    | Yes  | target_family_address   |

    | Return value | the list of config information |

    Example
    | ${result} | get configue range information | 0x100 | 0x1773 |
    | log    | ${result[0].handgroup_id}   |
    | log    | ${result[0].first_id}       |
    | log    | ${result[0].last_id}        |
    | log    | ${result[0].warming_enable} |
    """
    command = '''diagste -u %s -f %s -r all_hg_config'''%(computer_id,family_id)
    config_info_list = []

    result = connections.execute_mml_without_check(command)

    output_pattern = re.compile(r"\s*all\s+hand\s+group\s+config:", re.I)
    group_pattern = re.compile(r"\s*hand\s+group\s+(\d+):+", re.I)
    first_pattern = re.compile(r"\s*hand\s+group\s+first\s+id\s+:+\s+(\d+)", re.I)
    last_pattern = re.compile(r"\s*hand\s+group\s+last\s+id\s+:+\s+(\d+)", re.I)
    if output_pattern.search(result) is None:
        exceptions.raise_ILError("ILCommandExecuteError", "failed to get configue range information")
    else:
        line_list = result.split("hand warming enable")
        for line in line_list:
            group_result = group_pattern.search(line)
            first_result = first_pattern.search(line)
            last_result = last_pattern.search(line)
            if group_result is not None:
                config_item = CommonItem()
                config_item.handgroup_id = group_result.group(1)
                if first_result is not None:
                    config_item.first_id = first_result.group(1)
                    if last_result is not None:
                        config_item.last_id = last_result.group(1)
                        config_info_list.append(config_item)
    return config_info_list

def wait_until_succeeds_start_monster_monitor_family_on_specific_node(times, node_name, monster_cmd, expected_family):
    count = atoi(times, 10)
    current = connections.get_current_connection()._current
    print "old id '%s'" % current
    new_connection = connections.get_current_connection().clone_connection()
    print "new id '%s'" % new_connection
    connections.get_current_connection().switch_il_connection(new_connection)

    print 'start to run monster on %s' %(new_connection)
    cmd1 = "ssh -o StrictHostKeyChecking=no " + node_name
    connections.execute_mml_without_check(cmd1)

    for i in range(count):
        now = time.time()
        expected='Start monitoring for family %s in RU'%(expected_family)
        command = 'monster %s -V'%(monster_cmd)
        connections.get_current_connection().write(command)
        try:
            result = connections.get_current_connection().read_until(expected, '3s')
            if result:
                return {'result':'success', 'connection':new_connection}
        except:
            print "failed to monitor the family: %s, maybe connect timeout at %s"%(expected_family, now)
    connections.get_current_connection().switch_il_connection(current)
    return {'result':'failure', 'connection':new_connection}
    
def change_node_env_by_ru(ru_mo_name):
    """This keyword is used to change node evn by RU MO name.
       It will firstly get node name with RU name by keyword "get_node_from_unit",
       then call keyword "Change Node Env".

    | Parameters | Man. | Description                            |
    | ru_mo_name | Yes  | ru_mo_name which is in the target node |

    | No Return value | 

    Example 1:
    | Change Node Env by RU | /IPNIU-0/IPNIUTestServer-0 |

    Example 2:
        Variable table:
            ${IPNIU} | %{IPNIU_0_NAME} |
        Case:
            | Change Node ENv by RU | ${IPNIU} |
    """
    node_name = BuiltIn().run_keyword("Get Node From Unit", ru_mo_name)
    BuiltIn().run_keyword("Change Node Env", node_name)

def check_if_hand_id_range_of_each_hand_group_are_right(configue_list, first_id_list, last_id_list, count):
    """This keyword is to check hand id range of each hand group.

    #COMMAND: check if hand id range of each hand group are right [configue_list] [first_id_list] [last_id_list] [count]

    | Parameters    | Man. | Description      | 
    | configue_list | Yes  | configue_list    |
    | first_id_list | Yes  | first_id_list    |
    | last_id_list  | Yes  | last_id_list     |
    | count         | Yes  | hand_group_count |

    | Return value | check result |
    Example
    | ${result} | check if hand id range of each hand group are right | list | list | list | count |
    """

    for i in range(0, int(count)):
        item = parse_specific_config_range_result_by_hand_group_id(configue_list, str(i+1))
        if first_id_list[i] != item.first_id:
            print first_id_list[i], '!=', item.first_id
            return 'failure'
        if last_id_list[i] != item.last_id:
            print last_id_list[i], '!=', item.last_id
            return 'failure'
    return 'success'

def hand_id_range_of_special_hand_group_should_be_right(configue_list, first_id, last_id, hand_group_id):
    """This keyword is to check hand id range of special hand group.

    #COMMAND: hand id range of special hand group should be right [configue_list] [first_id] [last_id] [hand_group_id]

    | Parameters    | Man. | Description      | 
    | configue_list | Yes  | configue_list    |
    | first_id      | Yes  | first_id         |
    | last_id       | Yes  | last_id          |
    | hand_group_id | Yes  | hand_group_id    |

    Example
    | hand id range of special hand group should be right | list | first_id | last_id | hand_group_id |
    """
    
    item = parse_specific_config_range_result_by_hand_group_id(configue_list, hand_group_id)
    BuiltIn().run_keyword("Should Be Equal", first_id, item.first_id) 
    BuiltIn().run_keyword("Should Be Equal", last_id, item.last_id)


def get_hand_id_left_range_of_special_hand_group(configue_list, hand_group_id):
    """This keyword is to get hand id left range of special hand group.

    #COMMAND: get left range of special hand group [configue_list] [hand_group_id]

    | Parameters | Man. | Description                     | 
    | configue_list | Yes  | configue_list |
    | hand_group_id | Yes  | hand_group_id |

    | Return value | hand_id_left_range |

    Example
    | ${result} | get hand id left range of special hand group | list | hand_group_id |
    """
    item = parse_specific_config_range_result_by_hand_group_id(configue_list, hand_group_id)
    return item.first_id

def get_hand_id_right_range_of_special_hand_group(configue_list, hand_group_id):
    """This keyword is to get hand id right range of special hand group.

    #COMMAND: get right range of special hand group [configue_list] [hand_group_id]

    | Parameters | Man. | Description                     | 
    | configue_list | Yes  | configue_list |
    | hand_group_id | Yes  | hand_group_id |

    | Return value  | hand_id_right_range  |

    Example
    | ${result} | get hand id right range of special hand group | list | hand_group_id |
    """  
    item = parse_specific_config_range_result_by_hand_group_id(configue_list, hand_group_id)
    return item.last_id

def parse_specific_config_range_result_by_hand_group_id(configue_list, hand_group_id):
    """This keyword is to return the config range result, distinguish specific config range result by hand_group_id.

    #COMMAND:

    | Parameters    | Man. | Description    |
    | configue_list | Yes  | configue_list  |
    | hand_group_id | Yes  | hand_group_id  |

    | Return value  | config result |

    Example
    | configue_list | get the configue range information | 0x100 | 0x1773 |
    | ${result} | parse specific config range result by hand_group_id | configue_list | 10 |
    """
    for item in configue_list:
        if item.handgroup_id == hand_group_id:
            return item

def expect_buffer_and_actual_buffer_should_be_equal(buffers):
    """ This keyword is to check if expect buffer and actual buffer are equal.

    #COMMAND: expect buffer and actual buffer should be equal

    | Parameters | Man. | Description |
    | buffers    | Yes  | buffers     |

    Example
    | result     | expect buffer and actual buffer should be equal | buffers |

    """   

    buf = buffers.replace('\r\n', '\n')
    buf_list = buf.split('buf_ptr')
    buff = buf_list[1:]
    res_list = []
    for i in range (0, len(buff)):
        ret = check_and_parse_one_buf_text(buff[i])
        if ret == 'failure':
            return 'failure'
    return 'success'        

def check_and_parse_one_buf_text(in_buf):
    """ This keyword is to check and parse one buf text .

    #COMMAND: check and parse one buf text

    | Parameters | Man. | Description |
    | in_buf     | Yes  | in_buf      |

    Example
    | result     | check and parse one buf text | in_buf |

    """   

    buff = in_buf.split('The expected:\n')
    buffer_list = buff[1].split('The actual:\n')
    expect_buffer_list = buffer_list[0].strip().splitlines()
    actual_buffer_list = buffer_list[1].strip().splitlines()
    if expect_buffer_list != actual_buffer_list:
        print 'expect_buffer:', expect_buffer_list, '!=', 'actual_buffer:', actual_buffer_list
        return 'failure'
    return 'success'

def check_two_process_should_be_same(process1,process2):
    """This keyword is to check two process should be same.

    #COMMAND:   md5sum Libgen_translate.py

    | Parameters | Man. | Description                    |
    | process1   | Yes  | target process full path       |
    | process2   | Yes  | target process full path       |

    Example
    | result | check two process should be same | process1,process2 |
    """
    command='md5sum %s'%(process1)
    ret1 = connections.execute_mml_without_check(command)

    command='md5sum %s'%(process2)
    ret2 = connections.execute_mml_without_check(command)

    BuiltIn().run_keyword("Should Be Equal", ret1.split(process1)[0].strip(), ret2.split(process2)[0].strip())


def get_current_software_build():
    """This keyword is to get current software build.

    #COMMAND:  fsswcli -c

    | Parameters    | Man. | Description         |
    | Return value  | get current software build |

    Example
    | ${result}     | get current software build |

    """
    command='fsswcli -c'
    out = connections.execute_mml_without_check(command)

    if out.count('R_IL') == 1:
        return out.strip()

def get_runame_at_same_node_with_active_clusterstate(wo_omu_name,sp_omu_name):
    """This keyword is to get runame at same node with active clusterstate

    #COMMAND: fshascli -v |grep ClusterState|grep RecoveryUnit| awk '{print $2}'
    | Parameters    | Man. | Description       | 
    | Return value  | get runame at same node with active clusterstate |

    Example
    | ${result}     | get runame at same node with active clusterstate |
    """

    command="fshascli -v |grep ClusterState|grep RecoveryUnit| awk '{print $2}' "
    out = connections.execute_mml_without_check(command)

    ru1 = out.split('\n')[1].strip()
    ru2 = out.split('\n')[2].strip()

    command='fshascli -s %s'%(ru1)
    ret1 = connections.execute_mml_without_check(command)

    command='fshascli -s %s'%(ru2)
    ret2 = connections.execute_mml_without_check(command)

    if ret1.count('role(ACTIVE)') == 1:
        match = re.search(r"/(.*)/(.*)", ru1, re.I)
        if match is None:
            exceptions.raise_ILError("ILKeywordSyntaxError", "%s is not unit"%ru1)
        else:
            if match.group(1) in wo_omu_name:
                return wo_omu_name
            elif match.group(1) in sp_omu_name:
                return sp_omu_name

    if ret2.count('role(ACTIVE)') == 1:
        match = re.search(r"/(.*)/(.*)", ru2, re.I)
        if match is None:
            exceptions.raise_ILError("ILKeywordSyntaxError", "%s is not unit"%ru2)
        else:
            if match.group(1) in wo_omu_name:
                return wo_omu_name
            elif match.group(1) in sp_omu_name:
                return sp_omu_name

def get_mount_nfs_info():
    """This keyword is to get mount nfs info

    #COMMAND: mount | grep "/mnt/sysimg"
    | Parameters   | Man. | Description       | 
    | Return value | mount nfs info           |

    Example
    | ${result}    | get mount nfs info       |
    """
    command='mount | grep "/mnt/sysimg"'
    out = connections.execute_mml_without_check(command)

    if out.count('on /mnt/sysimg type nfs') == 1:
        return out.split("on /mnt/sysimg type nfs")[0].strip()

def expect_message_and_actual_message_should_be_equal(messages):
    """ This keyword is to check if expect message and actual message are equal.

    #COMMAND: expect message and actual message should be equal

    | Parameters | Man. | Description |
    | messages    | Yes  | messages   |

    Example
    | result     | expect message and actual message should be equal | messages |

    """   
    output_pattern = re.compile(r"\s*MemberNameOfMsgBody\s+Expected\s+Actual", re.I)

    if output_pattern.search(messages) is None:
        exceptions.raise_ILError("ILCommandExecuteError", "failed to get message information")
    else:
        line_list = messages.split("Actual")
        line_list = line_list[1].split("\r\n")
        for line in line_list:
            if line != '':
                match = re.search(r"0x(.*)0x(.*)", line, re.I)
                if match.group(1).strip() != match.group(2).strip():
                    print match.group(1).strip(), '!=', match.group(2).strip()
                    return 'failure'
        return 'success'   

def get_all_the_names_of_libgen_configuration_file():
    """This keyword is to get all the names of libgen configuration file

    #COMMAND: ls -l /etc/LibgenConfig*
    | Parameters   | Man. | Description       | 

    | Return value | all the names of libgen configuration file     |

    Example
    | ${result}    | get all the names of libgen configuration file |
    """
    command='ls -l /etc/LibgenConfig*'
    out = connections.execute_mml_without_check(command)

    configuration_file_name_list = []
    line_list = out.split("\r\n")
    for line in line_list:
        if line.count("etc") == 1:
            match = re.search(r"\s*/etc/LibgenConfig_(.*).ini", line, re.I)          
            if match is None:
                exceptions.raise_ILError("ILKeywordSyntaxError", "there is no configuration file in the node")
            else: 
                configuration_file_name_list.append(match.group(1))
    return configuration_file_name_list

def get_ru_type_on_a_node(node_name):
    """This keyword is to get ru type on a node

    #COMMAND: ilclifunit -u |grep -i CLA-0 | awk '{print $1}'
    | Parameters   | Man. | Description       | 
    | node_name    | node_name                |

    | Return value | all ru types on a node   |

    Example
    | ${result}    | get ru type on a node | CLA-0 |
    """
    command="ilclifunit -u |grep -i %s | awk '{print $1}'"%(node_name)
    out = connections.execute_mml_without_check(command)

    ru_type_list = []
    line_list = out.split("\r\n")
    for line in line_list:
        if line != '':
            match = re.search(r"(.*)-([0-9]+)", line, re.I)
            if match is None:
                exceptions.raise_ILError("ILKeywordSyntaxError", "Cannot find ru type in the node")
            else: 
                ru_type_list.append(match.group(1))
    ru_type_list = list(set(ru_type_list))
    ru_type_list.sort()
    return ru_type_list

def convert_to_hexadecimal_list(list):
    """ This keyword is to convert to hexadecimal list.

    #COMMAND: list[i] = hex(int(list[i]))

    | Parameters | Man. | Description |
    | list       | Yes  | list        |
    | Return value | hexadecimal list |

    Example
    | convert to hexadecimal list | list  |

    """   
    for i in range (0, len(list)):
        list[i] = hex(int(list[i]))
    return list

def two_list_should_be_same(list1, list2):
    """ This keyword is to check two list should be same.

    #COMMAND: two list should be same

    | Parameters | Man. | Description |
    | list1      | Yes  | list1       |
    | list2      | Yes  | list2       |
    | Return value | success if two list are same |

    Example
    | two list should be same | list1, list2      |

    """   
    for i in range (0, len(list1)):
        if (list1[i] != '' and list1[i] != []):
            if list1[i] != list2[i]:
                print 'list1[i]',list1[i],'!=','list2[i]',list2[i]
    return 'success'

def get_processor_type():
    """This keyword is to get processor type

    #COMMAND: sed -n '/processor_id/p' /proc/octeon_info
    | Parameters   | Man. | Description       | 

    | Return value | processor type           |

    Example
    | ${result}    | get processor type |
    """
    OCTEONPLUS_MASK_MAGIC = 0xd0400
    OCTEONII_MASK_MAGIC = 0xd9100
    OCTEONPLUS_NAME = "octeonplus"
    OCTEONII_NAME = "octeonii"

    processor_type=''
    octen_file = '/proc/octeon_info'

    command="sed -n '/processor_id/p' %s"%(octen_file)

    if check_if_file_exist(octen_file) == 'exist':
        out = connections.execute_mml_without_check(command)
        processor_id = out.split(":")[1].strip()
        pt_magic = int(processor_id, 16)
        if pt_magic & OCTEONPLUS_MASK_MAGIC == OCTEONPLUS_MASK_MAGIC:
            processor_type = OCTEONPLUS_NAME
        if pt_magic & OCTEONII_MASK_MAGIC == OCTEONII_MASK_MAGIC:
            processor_type = OCTEONII_NAME
    return processor_type

def get_specific_attribute_value_in_libgen_configuration_file(master_name_index,attribute_index,ru_type):
    """This keyword is to get specific attribute value in libgen configuration file

    #COMMAND: sed -n '/wutimas:40995/,/^[[:space:]]*$/p' /etc/LibgenConfig_OMU.ini | grep stack_size 
    | Parameters   | Man. | Description       | 
    | master_name_index   | master_name_index |
    | attribute_index     | attribute_index   |
    | ru_type             | ru_type           |

    | Return value | specific attribute value in libgen configuration file |

    Example
    | ${result}    | get specific attribute value in libgen configuration file | wutimas:40995 | stack_size | OMU |
    """  

    command="sed -n '/%s/,/^[[:space:]]*$/p' /etc/LibgenConfig_%s.ini | grep %s"%(master_name_index,ru_type,attribute_index)
    out = connections.execute_mml_without_check(command)

    if out.count('=') == 1:        
        return out.split("=")[1].strip()

def get_attributes_values_in_ldap_by_process_type(test_process_type):
    """This keyword is to get attributes values in ldap by process type

    #COMMAND: fsclish -c "show config fsClusterId=ClusterRoot fsFragmentId=HA fsFragmentId=ProcessTypes fshaProcessTypeName=IL_TestWarmStubType"
    | Parameters   | Man. | Description        | 
    | test_process_type   | test_process_type  |

    | Return value | attributes values in ldap |

    Example
    | ${result}    | get attributes values in ldap by process type | IL_WutiCLIType |
    """
    command='''fsclish -c "show config fsClusterId=ClusterRoot fsFragmentId=HA fsFragmentId=ProcessTypes fshaProcessTypeName=%s" |grep fshailava| awk '{print$2}' '''%(test_process_type)
    out = connections.execute_mml_without_check(command)

    values_in_ldap = []
    line_list = out.split("\r\n")
    for line in line_list:
        if line != '':
            line = line.lower()
            print line
            if line.count('family_number') == 1 \
                    or line.count('handgroup') == 1 \
                    or line.count('endless') == 1 \
                    or line.count('warming_enable') == 1 \
                    or line.count('tnsdl_timer') == 1 :
                values_in_ldap.append(line.strip())
    print values_in_ldap
    return values_in_ldap

def get_attributes_values_in_file_by_index(master_index,file_root_and_name):
    """This keyword is to get attributes values in file by index

    #COMMAND: sed -n '/wutimas:40995/,/^[[:space:]]*$/p' /etc/LibgenConfig_OMU.ini
    | Parameters   | Man. | Description        | 
    | master_index        | master_index       |
    | file_root_and_name  | file_root_and_name |


    | Return value | attributes values in file |

    Example
    | ${result}    | get attributes values in file by index | wutimas:40995 | /etc/LibgenConfig_OMU.ini |
    """
    print 'begin',datetime.datetime.now()
    command="sed -n '/%s/,/^[[:space:]]*$/p' %s "%(master_index,file_root_and_name)
    out = connections.execute_mml_without_check(command)
    print 'sed command success',datetime.datetime.now()
    values_in_file = []
    line_list = out.split("\r\n")
    print 'split with enter',datetime.datetime.now()
    for line in line_list:
        if line != '':
            if line.count('[') == 0:
                values_in_file.append(line.strip())
                print 'get every line',datetime.datetime.now()
    print 'end',datetime.datetime.now()
    print values_in_file
    return values_in_file

def get_default_value_in_Libgen_translate_script_by_hw_type():
    """This keyword is to get default value in libgen translate script by hw_type

    #COMMAND: sed -n "/ATCA/,/^'''/p" /opt/nokiasiemens/configure/py/Libgen_translate.py
    | Parameters   | Man. | Description       | 


    | Return value | default value in libgen translate script |

    Example
    | ${result}    | get default value in libgen translate script by hw_type |
    """
    file_root_and_name = '/opt/nokiasiemens/configure/py/Libgen_translate.py'
    command='echo $HW_PLATFORM'
    out = connections.execute_mml_without_check(command)
    hw_platform = out.strip()

    command1="""sed -n "/ATCA/,/^'''/p" %s"""%(file_root_and_name)

    command2="""sed -n "/FTLB/,/^'''/p" %s"""%(file_root_and_name)

    command3="""sed -n "/^else:/,/^'''/p" %s"""%(file_root_and_name)

    if hw_platform == 'ATCA':
        out = connections.execute_mml_without_check(command1)
    elif hw_platform == 'FTLB':
        out = connections.execute_mml_without_check(command2)
    else:
        out = connections.execute_mml_without_check(command3)
        other_hw_platform = re.search(r'else:.*\n.*header(.*)[default](.*)',out,re.I)
        if other_hw_platform is None:
            exceptions.raise_ILError("ILCommandExecuteError", "failed to get other hw_platform default values")

    values_in_script = []
    line_list = out.split("[default]")
    line_list = line_list[1].split("\r\n")
    for line in line_list:
        if line != '':
            if line.count('=') == 1:
                values_in_script.append(line.strip())
    return values_in_script

def get_libgen_translate_script_execution_time_of_target_node(target_node_name,wo_omu_node_name):
    """This keyword is to get libgen translate script execution time of target node

    #COMMAND: grep Libgen_translate.py::FULL_TRANSLATE: /var/log/master/* |grep CLA-0
    | Parameters    | Man. | Description       | 
    | target_node_name | target_node_name      |
    | wo_omu_node_name | wo_omu_node_name      |

    | Return value  | libgen translate script execution time of target node |

    Example
    | get libgen translate script execution time of target node | CLA-0 | CLA-0 |
    """
    time_index = 'Libgen_translate.py::FULL_TRANSLATE:'
    command1='grep %s /var/log/master/syslog |grep %s'%(time_index,target_node_name)
    command2='grep %s /tmp/copyconfig.out |grep %s'%(time_index,target_node_name)

    cmd = 'echo $HW_PLATFORM'
    hw_type = connections.execute_mml_without_check(cmd)
    hw_type = hw_type.strip()
    index = target_node_name.split('-')[0].strip()
   
    if (wo_omu_node_name.count(index) == 0 and hw_type == 'ATCA'):
        BuiltIn().run_keyword("Change Node Env", target_node_name)
        out = connections.execute_mml_without_check(command2)
    else:
        BuiltIn().run_keyword("Change Node Env", wo_omu_node_name)
        out = connections.execute_mml_without_check(command1)

def get_node_name_as_same_node_with_active_clusterstate(wo_omu_name,sp_omu_name):
    """This keyword is to get node name as same node with active clusterstate

    #COMMAND: fshascli -v |grep ClusterState|grep RecoveryUnit| awk '{print $2}'
    | Parameters    | Man. | Description       | 
    | wo_omu_name   | ru_name                  |
    | sp_omu_name   | ru_name                  |

    | Return value  | active_node_name         |

    Example
    | CLA-0 | get node name as same node with active clusterstate | /CLA-0/OMUTestServer-0 | /CLA-1/OMUTestServer-1 |
    """

    cmd = 'echo $HW_PLATFORM'
    hw_type = connections.execute_mml_without_check(cmd)
    hw_type = hw_type.strip()

    active_node_name = '' 
    ru_name = ''

    if hw_type != 'FTLB':
        ru_name = get_runame_at_same_node_with_active_clusterstate(wo_omu_name,sp_omu_name)
        match = re.search(r"/(.*)/(.*)", ru_name, re.I)
        if match is None:
            exceptions.raise_ILError("ILKeywordSyntaxError", "%s is not unit"%ru_name)
        else:
            active_node_name = match.group(1)
    return active_node_name

def check_if_file_exist(file_root_and_name):
    """This keyword is to check if file exist

    #COMMAND: ls -l /root/config_file
    | Parameters   | Man. | Description       | 
    | file_root_and_name | file_root_and_name |                      

    | Return value | return exist if file can be find  |

    Example
    | ${result}    | check if file exist | /root/config_file |
    """

    command='ls -l %s'%(file_root_and_name)
    out = connections.execute_mml_without_check(command)

    if out.count("No such file or directory") == 1:
        return 'not-exist'
    return 'exist'

def actual_message_should_be_zero(messages):
    """ This keyword is to check if actual message are zero.

    #COMMAND: actual message should be zero

    | Parameters | Man. | Description |
    | messages    | Yes  | messages   |

    Example
    | result     | actual message should be zero | messages |

    """   
    output_pattern = re.compile(r"\s*MemberNameOfMsgBody\s+Expected\s+Actual", re.I)

    if output_pattern.search(messages) is None:
        exceptions.raise_ILError("ILCommandExecuteError", "failed to get message information")
    else:
        line_list = messages.split("Actual")
        line_list = line_list[1].split("\r\n")
        for line in line_list:
            if line != '':
                match = re.search(r"0x(.*)0x(.*)", line, re.I)
                if match.group(2).strip() != '0':
                    print match.group(2).strip(), '!=0'
                    return 'failure'
        return 'success'

def check_if_hand_exist(computer_id,family_id,process_id):
    """This keyword is to use diagste to check if hand exist or not.

    #COMMAND: diagste -u [computer_id] -f [family_id] -p [process_id] -r han -t idata -m hum

    | Parameters       | Man. | Description                                 |
    | computer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family addres                        |
    | process_id       | Yes  | target process_id                           |
      
    | Return value | command str, exist or no-exist |

    Example
    | result | check if hand exist | 0x700 | 0x1F45 | 0 |
    """
    command='diagste -u %s -f %s -p %s -r han -t idata -m hum'%(computer_id,family_id,process_id)
    out = connections.execute_mml_without_check(command)
    if out.count('no active hands') == 1:
        return 'not-exist'
    if out.count('Diagterm request has failed') == 1:
        return 'not-exist'
    else:
        return 'exist'

def check_multi_msg_time_less_than(msg_list1, msg_list2, diff_time):
    """This keyword is to check multi msg time in msg_list1 less than msg_list2

    #COMMAND: check_each_msg_time_less_than(msg_list1, msg_list2, diff_time)
    | Parameters            | Man. | Description                                  |
    | msg_list1              | Yes  | the catched message list monitored by monster       |
    | msg_list2              | Yes  | the catched message list monitored by monster       |
    | diff_time              | Yes  | diff time in unit 10ms       |
       
    | Return value | command execution result if success, failure or two msg list length is different |
    
    Example 
    | ${result} | check multi msg time less than | msg_list1 | msg_list2 | diff_time |
    """
    if len(msg_list1) != len(msg_list2):
        return 'two msg list length is different'
    for i in range(len(msg_list1)):
        temp_list1 = []
        temp_list1 += [msg_list1[i]]
        temp_list2 = []
        temp_list2 += [msg_list2[i]]
        result = check_each_msg_time_less_than(temp_list1, temp_list2, diff_time)
        if result == 'success':
            continue
        else:
            return 'failure'
    return 'success'

def check_multi_msg_time_less_than_for_part_list_data(msg_list1, msg_list2, diff_time):
    """This keyword is to check multi msg time in msg_list1 less than msg_list2

    #COMMAND: check_each_msg_time_less_than(msg_list1, msg_list2, diff_time)
    | Parameters            | Man. | Description                                  |
    | msg_list1              | Yes  | the catched message list monitored by monster       |
    | msg_list2              | Yes  | the catched message list monitored by monster       |
    | diff_time              | Yes  | diff time in unit 10ms       |

    | Return value | command execution result if success, failure or two msg list length is different |

    Example
    | ${result} | check multi msg time less than | msg_list1 | msg_list2 | diff_time |
    """
    if len(msg_list1) != len(msg_list2):
        return 'two msg list length is different'
    for i in range(len(msg_list1)):
        if i != 0 :
            temp_list1 = []
            temp_list1 += [msg_list1[i]]
            temp_list2 = []
            temp_list2 += [msg_list2[i]]
            result = check_each_msg_time_less_than(temp_list1, temp_list2, diff_time)
            if result == 'success':
                continue
            else:
                return 'failure'
    return 'success'

def check_if_multi_msg_time_are_in_the_period_of_time_between_st1_and_st2(st1, st2, msg_list):
    """This keyword is to check if multi msg time are in the period of time between st1 and st2
   
    #COMMAND: check_if_multi_msg_time_are_in_the_period_of_time_between_st1_and_st2(st1, st2, msg_list)
    | Parameters            | Man. | Description                                   |
    | st1                   | Yes  | system time                                   |
    | st2                   | Yes  | system time                                   |
    | msg_list              | Yes  | the catched message list monitored by monster | 
  
    | Return value | command execution result if success, failure or msg list is zero |
   
    Example
    | ${result} | check if multi msg time are in the period of time between st1 and st2 | st1 | st2 | msg_list |
    """
    import datetime
    if len(msg_list) == 0:
        return 'msg list is zero'

    st1 = datetime.datetime.strptime(st1.strip(),'%Y-%m-%d %H:%M:%S.%f')
    st2 = datetime.datetime.strptime(st2.strip(),'%Y-%m-%d %H:%M:%S.%f')
    print 'st1=',st1
    print 'st2=',st2
   
    for i in range(len(msg_list)):
        msg = msg_list[i]
        result = check_if_each_msg_time_are_in_the_period_of_time_between_st1_and_st2(st1, st2, msg)
        if result == 'success':
            continue
        else:
            return 'failure'
    return 'success'

def check_if_each_msg_time_are_in_the_period_of_time_between_st1_and_st2(st1, st2, msg_list):
    """This keyword is to check if each msg time are in the period of time between st1 and st2
   
    #COMMAND: check_if_each_msg_time_are_in_the_period_of_time_between_st1_and_st2(st1, st2, msg_list)
    | Parameters            | Man. | Description                                   |
    | st1                   | Yes  | system time                                   |
    | st2                   | Yes  | system time                                   |
    | msg_list              | Yes  | the catched message list monitored by monster |
   
    | Return value | command execution result if success, failure or msg list is zero |
   
    Example
    | ${result} | check if each msg time are in the period of time between st1 and st2 | st1 | st2 | msg_list |
    """
    import datetime
    if len(msg_list) == 0:
        return 'msg list is zero'

    for i in range(len(msg_list)):
        msg = msg_list[i]
        for j in range(len(msg_list[i])):
            temp_list = msg[j]
            if temp_list['time']['date_time'] < st2 and temp_list['time']['date_time'] > st1:
                continue
            else:
                print 'temp_t=',temp_list['time']['date_time']
                return 'failure'
    return 'success'

def check_msg_count_of_specified_msg_type_should_be_equal_with_target_value(count, msg_num, msg_list):
    """This keyword is to check msg count of specified msg type should be equal with target value
   
    #COMMAND: check_msg_count_of_specified_msg_type_should_be_equal_with_target_value(count, msg_num, msg_list)
    | Parameters            | Man. | Description                                   |
    | count                 | Yes  | message count                                 |
    | msg num               | Yes  | message num                                   |
    | msg_list              | Yes  | the catched message list monitored by monster |
   
    | Return value | command execution result if success, failure or msg list is zero |
   
    Example
    | ${result} | check msg count of specified msg type should be equal with target value | count | msg_num | msg_list |
    """
    if len(msg_list) == 0:
        return 'msg list is zero'

    cnt = 0
    for i in range(len(msg_list)):
        msg = msg_list[i]
        if msg['msg']['number'] == int(msg_num):
            cnt = cnt + 1
            continue
    print 'cnt',cnt
    if cnt == int(count):
        return 'success'
    else: 
        return 'failure'

if __name__=="__main__":
    print "\n If you see this, it means this py file has no compiling error.\n"
