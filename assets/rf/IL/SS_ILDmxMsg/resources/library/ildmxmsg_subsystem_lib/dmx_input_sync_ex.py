from comm.communication import exceptions
from comm.communication import connections
from comm.communication.helper import *
import re

def dmx_generic_stub_recv(family, log):
    """ This keyword to start dmx_generic_stub to recv dmxmsg and save log.

    #COMMAND: dmx_generic_stub recv

    | Parameters  | Man. | Description  |
    | family      | Yes  | family |
    | log         | Yes  | log file name|

    | Return value | No return value |

    Example
    | ${result}  | dmx generic stub recv | family | log |

    """
    command = "dmx_generic_stub recv " + family +  " >" + log +" & "
    connections.execute_mml_without_check(command)

def dmx_generic_stub_recv_and_no_optimizei_for_internal_msg(family, log):
    """ This keyword to start dmx_generic_stub to recv dmxmsg and save log.
	internal message will not be received first.
    #COMMAND: dmx_generic_stub recv
    | Parameters  | Man. | Description  |
    | family      | Yes  | family |
    | log         | Yes  | log file name|
    | Return value | No return value |
    Example
    | ${result}  | dmx generic stub recv | family | log |
    """
    command = "dmx_generic_stub recv -s " +  family + " > " + log +" & "
    connections.execute_mml_without_check(command)

def dmx_generic_stub_wait_to_recv_and_no_optimize_for_internal_msg(family, log):
    """ This keyword to start dmx_generic_stub to wait recv dmxmsg and save log.
	internal message will not be received first.
    #COMMAND: dmx_generic_stub recv

    | Parameters  | Man. | Description  |
    | family      | Yes  | family |
    | log         | Yes  | log file name|

    | Return value | No return value |

    Example
    | ${result}  | dmx generic stub recv | family | log |

    """
    command = "dmx_generic_stub recv -s " + family + " -w > " + log +" & "
    connections.execute_mml_without_check(command)

def dmx_generic_stub_wait_to_recv(family, log):
    """ This keyword to start dmx_generic_stub to recv dmxmsg and save log.

    #COMMAND: dmx_generic_stub recv

    | Parameters  | Man. | Description  |
    | family      | Yes  | family |
    | log         | Yes  | log file name|

    | Return value | No return value |

    Example
    | ${result}  |  dmx generic stub wait to recv | family | log |

    """
    command = "dmx_generic_stub recv " + family + " -w >" + log +"&"
    connections.execute_mml_without_check(command)


def dmx_generic_stub_send(src_family, dst_addr, send_num, seq_num='', priority='', interval='', msg_num = ''):
    """ This keyword to start dmx_generic_stub to send dmxmsg

    #COMMAND: killall

    | Parameters  | Man. | Description  |
    | family      | Yes  | family |
    | log         | Yes  | log file name|

    | Return value | No return value |

    Example
    | ${result}  |  dmx generic stub send | family | log |

    """
    command = "dmx_generic_stub send " + src_family + " "+ dst_addr + " -n " + send_num
    if seq_num != '':
        command += " -s " + seq_num
    if priority != '':
        command += " -p " + priority
    if interval != '':
        command += " -i " + interval
    if msg_num  != '':
        command += " -N " + msg_num
    connections.execute_mml_without_check(command)


def dmx_generic_stub_drop_msg(dst, num):
    """ This keyword to config dmx_generic_stub to drop dmxmsg of specified dst computer and num.

    #COMMAND: dmx_generic_stub drop_msg

    | Parameters  | Man. | Description  |
    | dst         | Yes  | dst computer |
    | num         | Yes  | drop msg num |

    | Return value | No return value |

    Example
    | ${result}  |  dmx generic stub drop msg | 12 | 3 |

    """
    command = "dmx_generic_stub drop_msg  " + dst + " -n " + num
    connections.execute_mml_without_check(command)
def compare_seq(log_file, exp1, exp2, exp3):
    """ This keyword to compare seq in log.

    #COMMAND: dmx_generic_stub drop_msg

    | Parameters   | Man. | Description    |
    | log_file     | Yes  | log file       |
    | exp1         | Yes  | seq1           |
    | exp2         | Yes  | seq2           |
	| exp3         | Yes  | seq3           |
    | Return value | 'Equal' or 'Not Euqal'|

    Example

    """
    seq_list = [] 
    expect_list = [str(exp1),str(exp2), str(exp3)]
    log_file = log_file.split('\n')
    for line in log_file:
        words = line.split(' ')
        if words[0] == 'Got':
            seq_list.append((words[11].split('.'))[0])
    print(seq_list)
    if seq_list == expect_list:
        return 'Equal'
    else:
        return 'Not Euqal'
