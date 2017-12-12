from struct import *
from string import *

import re
import string
import math
import os

from comm.communication.helper import *
from comm.communication import exceptions
from comm.communication import connections


def __bootmem_compare(k, x, y):
    xsize = int(x[k], 0)
    ysize = int(y[k], 0)
    if xsize == ysize:
        return 0
    elif xsize > ysize:
        return -1
    else:
        return 1
    
def __bootmem_size_compare(x, y):
    return __bootmem_compare('size', x, y)


def __bootmem_index_compare(x, y):
    return __bootmem_compare('index', x, y)
   
    
def bootmem_show_free(node_name):
    """
     This keyword is to show free boot memory of specific node.

    #COMMAND: ssh node_name bootmem show free

    | Parameters | Man.| Description   |
    | node_name  | Yes | node name     |

    | Return value | command execution result |
    * [address, size, next]
      
    Example
    | ${result} | Bootmem Show Free | ${node_name} |
    
    """
    
    command = 'ssh -oStrictHostKeyChecking=no %s %s' % (node_name.lower(), 'bootmem show free')
    output = connections.execute_mml_without_check(command)
    result = []
    for line in output[2:].splitlines():
        items = re.findall(r'0x[0-9a-fA-F]+', line)
        if len(items) == 3:
            result.append({'address':items[0], 'size':items[1], 'next':items[2]})

    return result


def bootmem_get_max_free_size(node_name):
    """
     This keyword is to get max free memory size of specific node.

    | Parameters | Man.| Description   |
    | node_name  | Yes | node name     |

    | Return value | command execution result |
    [address, size, next]
      
    Example
    | ${result} | Bootmem Get Max Free Size | ${node_name} |
    
    """
    
    output = bootmem_show_free(node_name)
    output.sort(__bootmem_size_compare)
    return output[0]


def bootmem_show_named(node_name):
    """
     This keyword is to show named boot memory of specific node.

    #COMMAND: ssh node-name bootmem show named all

    | Parameters | Man.| Description   |
    | node_name  | Yes | node name     |

    | Return value | command execution result |
    * [name, address, size, index]
      
    Example
    | ${result} | Bootmem Show Named | ${node_name} |
    
    """
    
    command = 'ssh -oStrictHostKeyChecking=no %s %s' % (node_name.lower(), 'bootmem show named all')
    output = connections.execute_mml_without_check(command)
    result = []
    for line in output[1:].splitlines():
        items = line.split(',')
        if len(items) != 4:
            continue
        block = {}
        for item in items:
            pair = item.split(':')
            block[pair[0].strip().lower()] = pair[1].strip()
        result.append(block)
        
    return result


def bootmem_get_max_named_index(node_name):
    """
     This keyword is to get max named memory index of specific node.

    | Parameters | Man.| Description   |
    | node_name  | Yes | node name     |

    | Return value | command execution result |
    [name, address, size, index]
      
    Example
    | ${result} | Bootmem Get Max Named Index | ${node_name} |
    
    """
    
    output = bootmem_show_named(node_name)
    output.sort(__bootmem_index_compare)
    return output[0]

