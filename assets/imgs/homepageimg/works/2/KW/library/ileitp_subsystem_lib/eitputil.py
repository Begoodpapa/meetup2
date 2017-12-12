from struct import *
from string import *

import re
import string
import math
import os
import random

from comm.communication.helper import *
from comm.communication import exceptions
from comm.communication import connections


def eitputil_profiling_show(eipu_name):
    """
     This keyword is to show eitp profiling result.

    #COMMAND:  eitpste -f pprofiling enable

    | Parameters | Man.| Description    |
    | eipu_name  | Yes | EIPU name      |

    | Return value | command execution result   | 
    * status (DISABLED|ENABLED)
    * egress_ave
    * egress_max
    * egress_num
    * ingress_ave
    * ingress_max
    * ingress_num
      
    Example
    | ${result} | Eitputil Profiling Show | EIPU-0 |
        
    """
	
    command = 'ssh -oStrictHostKeyChecking=no %s eitpste -f pprofiling show' % (eipu_name.lower())
    output = connections.execute_mml_without_check(command)
    
    lines = output.splitlines()
    result = CommonItem()
    
    for n in range(0, len(lines)):
        if lines[n].strip().startswith('Status'):
            break
    
    status = lines[n].split('|')[1].strip()
    if status == 'DISABLED':
        result.status = 'DISABLED'
        return result
    
    result.status = 'ENABLED'

    items = re.findall(r'\d+|\w+', lines[n + 5])
    result.egress_ave = int(items[2])
    result.egress_max = int(items[3])
    result.egress_num = int(items[4])
    
    items = re.findall(r'\d+|\w+', lines[n + 7])
    result.ingress_ave = int(items[2])
    result.ingress_max = int(items[3])
    result.ingress_num = int(items[4])

    return result
    

def eitputil_profiling_enable(eipu_name):
    """
     This keyword is to enable eitp profiling.

    #COMMAND:  eitpste -f pprofiling enable

    | Parameters | Man.| Description    |
    | eipu_name  | Yes | EIPU name      |

    | Return value | command execution result |
  *  True|False

    Example
    | ${result} |  Eitputil Profiling Enable | EIPU-0 |
    
    """
	
    command = 'ssh -oStrictHostKeyChecking=no %s eitpste -f pprofiling enable' % (eipu_name.lower())
    output = connections.execute_mml_without_check(command)

    items = re.findall(r'\w+', output)
    
    return str(items[3].strip().lower() == 'enabled')

    
def eitputil_profiling_disable(eipu_name):
    """
     This keyword is to disable eitp profiling.

    #COMMAND:  eitpste -f pprofiling disable

    | Parameters | Man.| Description    |
    | eipu_name  | Yes | EIPU name      |

    | Return value | command execution result |
   *  True|False

    Example
    | ${result} | Eitputil Profiling Disable | EIPU-0 |
    
    """

    command = 'ssh -oStrictHostKeyChecking=no %s eitpste -f pprofiling disable' % (eipu_name.lower())
    output = connections.execute_mml_without_check(command)

    items = re.findall(r'\w+', output)
    
    return str(items[3].strip().lower() == 'disabled')


    
def eitputil_mux_show_stat(ipbr_id):
    """
     This keyword is to show mux statistic.

    #COMMAND:  eitputil mux show stat

    | Parameters | Man.| Description    |
    | ipbr_id    | Yes |  IPBR ID       |

    | Return value | command execution result | 

    Example
    | ${result} | Eitputil Mux Show Stat | ${ipbr_id} |
    
    """
	
    command = 'eitputil mux show stat ' + str(ipbr_id)
    output = connections.execute_mml_without_check(command)
    
    result = CommonItem()

    items = [int(v) for v in re.findall(r'\d+', output)]

    result.ipbr_id = items[0]
    result.out_mux = items[1]
    result.out_muxed = items[2]
    result.in_mux = items[3]
    result.in_muxed = items[4]
    result.in_disc = items[5]
    
    return result

    
def eitputil_mux_zero_stat(ipbr_id = ''):
    """
     This keyword is to show mux statistic.

    #COMMAND:  eitputil -f mux zero stat [ipbr_id]

    | Parameters | Man.| Description    |
    | ipbr_id    | No |  IPBR ID, null means all IPBR |

    | Return value | command execution result | 

    Example
    | Eitputil Mux Zero Stat | ${ipbr_id} |
    | Eitputil Mux Zero Stat |  |
    
    """
	
    command = 'eitputil -f mux zero stat ' + str(ipbr_id)
    
    connections.execute_mml_without_check(command)
    

def eitputil_gtp_get_iups_counters(eipu_name, ipaddr='all'):
    """
     This keyword is to get GTP IuPS counters.

    #COMMAND:  eitpste gtp get iups counters

    | Parameters | Man.| Description    |
    | eipu_name  | Yes |  EIPU name     |
    | ipaddr     | No  |  IP address    |

    | Return value | command execution result | 
    The following attributes may be accessed:
  * eipu
  * rnc_ip
  * sgsn_ip
  * in_ip_packets
  * in_udp_bytes
  * in_ip_err
  * in_udp_err
  * in_tc_conversational
  * in_tc_stream
  * in_tc_interactive
  * in_tc_background
  * out_ip_packets
  * out_udp_bytes
  * out_ip_err
  * out_udp_err
  * out_tc_conversational
  * out_tc_stream
  * out_tc_interactive
  * out_tc_background
  * echo_request_received
  * echo_response_received
  * echo_rresponse_sent
  * error_indication_received
  * error_indication_sent
  * ext_hdr_notif_received
    
    Example
    | ${result} | Eitputil Gtp Get Iups Counters | EIPU-0 | 1 |
    
    """
	
    eipu_name = eipu_name.lower()
    command = 'ssh -oStrictHostKeyChecking=no %s eitpste  gtp get iups counters ip-address %s' % (eipu_name, ipaddr)
    output = connections.execute_mml_without_check(command)
    
    items = [ item.split(':')[1].strip() for item in re.findall(r'[\w ]+:[ ]*[0-9.]+', output) ]
    if len(items) != 24 :
        return None

    result = CommonItem()
    
    result.eipu = eipu_name.upper()
    result.rnc_ip = items[0]
    result.sgsn_ip = items[1]

    result.in_ip_packets = items[2]
    result.in_udp_bytes = items[3]
    result.in_ip_err = items[4]
    result.in_udp_err = items[5]

    result.in_tc_conversational = items[6]
    result.in_tc_stream = items[7]
    result.in_tc_interactive = items[8]
    result.in_tc_background = items[9]

    result.out_ip_packets = items[10]
    result.out_udp_bytes = items[11]
    result.out_ip_err = items[12]
    result.out_udp_err = items[13]

    result.out_tc_conversational = items[14]
    result.out_tc_stream = items[15]
    result.out_tc_interactive = items[16]
    result.out_tc_background = items[17]

    result.echo_request_received = items[18]
    result.echo_response_received = items[19]
    result.echo_rresponse_sent = items[20]
    result.error_indication_received = items[21]
    result.error_indication_sent = items[22]

    result.ext_hdr_notif_received = items[23]
    
    return result

    
    