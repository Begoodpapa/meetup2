from struct import *
from string import *

import re
import string
import math
import os

from comm.communication.helper import *
from comm.communication import exceptions
from comm.communication import connections


def fpcmd_dump_cpu_usage(eipu_name):
    """
     This keyword is to dump eitp cpu usage.

    #COMMAND: ssh eipu-0 fpcmd dump-cpu-usage

    | Parameters | Man.| Description   |
    | eipu_name  | Yes | EIPU name     |

    | Return value | command execution result |
    * [cpu_id, busy, cycles]
      
    Example
    | ${result} | Fpcmd Dump Cpu Usage | ${eipu_name} |
    
    """
	
    command = 'ssh -oStrictHostKeyChecking=no %s %s' % (eipu_name.lower(), 'fpcmd dump-cpu-usage')
    output = connections.execute_mml_without_check(command)
    
    result = []

    for line in output.splitlines():
        items = re.findall(r'\d+', line)
        if len(items) == 3 and items[1] != '0':
            usage = CommonItem()
            usage.cpu_id = int(items[0])
            usage.busy = int(items[1])
            usage.cycles = int(items[2])
            result.append(usage)
            
    return result

def fpcmd_get_average_cpu_usage(eipu_name):
    """
     This keyword is to get average eitp cpu usage.

    | Parameters | Man.| Description   |
    | eipu_name  | Yes | EIPU name     |

    | Return value | command execution result |

    Example
    | ${result} | Fpcmd Get Average Cpu Usage | ${eipu_name} |
    
    """
	
    output = fpcmd_dump_cpu_usage(eipu_name)
    
    total = 0
    for usage in output:
        total += usage.busy
    
    return total / len(output)
    
def fpcmd_get_bcn_type():
    """
    This keyword is used to get bcn type, it returns BMPP2-B or BCNOC-A. 
    
    #COMMAND: echo $HW_FRU_TYPE

    | Parameters | Man.| Description   |
    | Return value | command execution result |
    BMPP2-B or BCNOC-A

    Example
    | ${result} | Fpcmd Get BCN Type |   |
    """
    
    command = 'echo $HW_FRU_TYPE'
    result = connections.execute_mml(command)
    return result.strip()
