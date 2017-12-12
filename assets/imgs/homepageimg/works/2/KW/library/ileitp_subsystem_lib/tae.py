from struct import *
from string import *

import re
import string
import math
import os
import time

from comm.communication.helper import *
from comm.communication import exceptions
from comm.communication import connections

def __get_mux_entry(output,status):
   """
   This keyword is to get multiplexing statistics.
   
   | Parameters | Man.| Description    |
   | output     | Yes | entry body     |
   | status     | Yes | WORK or BACKUP |
   | Return value | entry    |
   
   Example
   | ${result} | __get_mux_entry | jhasjdhkjahsujashd | WORK |
   """
   entry = CommonItem()
   pattern = re.compile('(\w+)\s+(' + status + ')\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\d+)', output)
   results = pattern.findall(output)
   print results

   for i in range(0,len(results)):
      entry = CommonItem()
      entry.addr = results[i][0]
      entry.status = results[i][1]
      entry.local_ip = results[i][2]
      entry.remote_ip = results[i][3]
      entry.local_port = results[i][4]
      entry.remote_port = results[i][5]
      entry.dscp = results[i][6]
      entry.packets = results[i][7]
      entry.reference = results[i][8]
      entry.vrf_id = results[i][11]
      entrys['%s'%i] = entry
   return entrys
   
def __get_tae_entry(output):
   """
   This keyword is to get tae statistics.
   
   | Parameters | Man.| Description  |
   | output     | Yes | entry body   |
   
   | Return value | entry    |
   
   Example
   | ${result} | __get_tae_entry | jhasjdhkjahsujashd |
   """
   entrys = CommonDict()
   pattern = re.compile('(\w+)\s+(WORK)\s+(\w+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\w+)\s+(\w+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\w+)/(\w+)\s+(\w+)/(\w+)')
   results = pattern.findall(output)
   print results
   
   for i in range(0,len(results)):
      entry = CommonItem()
      entry.rg_id = results[i][0]
      entry.status = results[i][1]
      entry.conn_id = results[i][2]
      entry.local_ip = results[i][3]
      entry.local_port = results[i][4]
      entry.local_teid = results[i][5]
      entry.remote_ip = results[i][6]
      entry.remote_port = results[i][7]
      entry.is_mux = results[i][8]
      entry.vrf_id = results[i][9]
      for j in range(0,i):
         if (entrys['%s'%j] == entry):
            return 0   
      entrys['%s'%i] = entry
   return entrys


def __get_qos_entry(output):
   """
   This keyword is to get qos statistics.
   
   | Parameters | Man.| Description       |
   | output     | Yes | entry body   |
   
   | Return value | entry    |
   
   Example
   | ${result} | __get_qos_entry | jhasjdhkjahsujashd |
   """
   entry = CommonItem()
   result = re.search('(\w+)\s+(\w+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)', output)
   if result is not None:
      entry.status = result.group(1)
      entry.conn_id = result.group(2)
      entry.local_ip = result.group(3)
      entry.local_port = result.group(4)
      entry.local_teid = result.group(5)
      entry.dscp = result.group(6)
      entry.phb = result.group(7)
      entry.ipbr = result.group(8)
      entry.queue = result.group(9)
      entry.ifc = result.group(10)
   return entry


def __get_tae_entry_all(output):
   """
   This keyword is to get all tae statistics.
   
   | Parameters | Man.| Description       |
   | output     | Yes | entry body   |
   
   | Return value | entry    |
   
   Example
   | ${result} | __get_tae_entry_all | jhasjdhkjahsujashd |
   """
   entrys = CommonDict()
   lines = output.splitlines()
   print lines
   j = 0
   for i in lines:
      eipu_str = '(\w+)\s+(WORK)\s+(\w+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\w+)\s+(\w+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\w+\/\w+)\s+(\w+\/\w+)'      
      eipu_res = re.search(eipu_str, i);
      if eipu_res is not None:
         entry = CommonItem()
         entry.address = eipu_res.group(1)
         entry.status = eipu_res.group(2)
         entry.connection = eipu_res.group(3)
         entry.local_ip = eipu_res.group(4)
         entry.local_port = eipu_res.group(5)
         entry.dl_teid = eipu_res.group(6)
         entry.remote_ip = eipu_res.group(7)   
         entry.remote_port = eipu_res.group(8)
         entry.vrf_id = eipu_res.group(10)
         entry.ingress = eipu_res.group(11) 
         entry.engress = eipu_res.group(12)
         entrys['connection_ID%s/IP%s/Port%s' %(entry.connection,entry.local_ip,entry.local_port)] = entry
         j = j + 1
   return entrys


def __get_tae_entry_imsi(output):
   """
   This keyword is to get imsi related tae statistics.
   
   | Parameters | Man.| Description       |
   | output     | Yes | entry body   |
   
   | Return value | entry    |
   
   Example
   | ${result} | __get_tae_entry_imsi | jhasjdhkjahsujashd |
   """
   entrys = CommonDict()
   lines = output.splitlines()
   print lines
   j = 0
   for i in lines:
      eipu_str = '(\w+)\s+(W\w+)\s+(\w+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\d+)\s+(\w+)\s+(\w+)'     
      eipu_res = re.search(eipu_str, i);
      if eipu_res is not None:
         entry = CommonItem()
         entry.address = eipu_res.group(1)
         entry.status = eipu_res.group(2)
         entry.connection = eipu_res.group(3)
         entry.local_ip = eipu_res.group(4)
         entry.local_port = eipu_res.group(5)
         entry.dl_teid = eipu_res.group(6)
         entry.imsi = eipu_res.group(7)   
         entry.own = eipu_res.group(8)
         entry.xsup = eipu_res.group(9)
         entry.index = eipu_res.group(10) 
         entry.mux = eipu_res.group(11)
         entry.flow_id = eipu_res.group(12)
         entrys['connection_ID%s/IP%s/Port%s/imsi%s' %(entry.connection,entry.local_ip,entry.local_port,entry.imsi)] = entry
         j = j + 1
   return entrys

def get_tae_entry_all():
    """This keyword is get all of tae entries.

    #COMMAND: eitputil tae show

    | Input Parameters | Man. | Description |
    | No               | No   | return the summary of tae entry |

    Examples
    | ${result}= | get_tae_entry_all |

    """
    command = "eitputil -f tae show"
    output = connections.execute_mml_without_check(command)
    return __get_tae_entry_all(output);

def get_mux_by_ip_port(ip, port):
   """Get mux according to the IP address and UDP port
   
   #COMMAND: eitputil mux show -i 192.168.1.1 -p 5555
   
   | Input Parameters | Man. | Description |
   | ip               | Yes  | ip address |
   | port             | Yes  | UDP port |
   
   Example :
   | ${item}= | get_mux_by_conn_ip_port | 0X2222 | 192.168.1.1 | 5000 |
   """
   command = 'eitputil -f mux show entry ' + ip + ':' + port
   output = connections.execute_mml_without_check(command)
   return __get_mux_entry(output, 'WORK')


def get_mux_all():
   """Get all multiplexing entries
   #COMMAND: eitputil mux show
   | Input Parameters | Man. | Description |
   
   Example :
   | ${item}= | get_mux_all |
   """
   command = 'eitputil -f mux show'
   output = connections.execute_mml_without_check(command)
   return __get_mux_entry(output,'\w+')


def get_tae_entry_by_conn(conn_id):
   """This keyword is to get entry according to connection id.
   
   #COMMAND: eitputil tae show -c 3333
   
   | Input Parameters | Man. | Description |
   | conn_id          | Yes  | connection id of entry |
   
   Examples
   | ${result}= | get_tae_entry_by_conn | 1 |

   """
   command = 'eitputil -f tae show -c ' + conn_id
   output = connections.execute_mml_without_check(command)
   return __get_tae_entry(output)


def get_tae_entry_in_uptrm(uptrm_index):
   """This keyword is to get entry in specified UPTRM.
   
   #COMMAND: eitputil tae show -u 0
   
   | Input Parameters | Man. | Description |
   | uptrm_index          | Yes  | index id of UPTRM |
   
   Examples
   | ${result}= | get_tae_entry_in_uptrm | 1 |

   """
   command = 'eitputil -f tae show -u ' + uptrm_index
   output = connections.execute_mml_without_check(command)
   return __get_tae_entry_all(output);

def get_tae_entry_by_teid(teid):
   """This keyword is to get entry according to GTP tunnel id.
   
   #COMMAND: eitputil tae show -t 0XBED11234
   
   | Input Parameters | Man. | Description   |
   | teid             | Yes  | GTP tunnel id |
   | ip               | No   | ip address    |
   
   Examples
   | ${result} | get_tae_entry_by_teid | 0XBED000001 |
   
   """
   command = 'eitputil -f tae show -t ' + teid
   output = connections.execute_mml_without_check(command)
   return __get_tae_entry(output)


def get_tae_entry_by_udp(ip, port):
   """Get tae entry according to the IP address and UDP port
   
   #COMMAND: eitputil tae show -i 192.168.1.1 -p 3333
   
   | Input Parameters | Man. | Description |
   | ip               | Yes  | ip address |
   | port             | Yes  | UDP port |
   
   Example :
   | ${item}= | get_tae_entry_by_udp | 192.168.1.1 | 5000 |
   """
   command = 'eitputil -f tae show' + ' -i ' + ip + ' -p ' + port
   output = connections.execute_mml_without_check(command)
   x = 3;
   while(x): 
      entities = __get_tae_entry(output)
      if (entities == 0):
         time.sleep(1)
         command = 'eitputil -f tae show' + ' -i ' + ip + ' -p ' + port
         output = connections.execute_mml_without_check(command)
      else:
         return entities
      x -= 1
   return __get_tae_entry(output)


def get_tae_imsi_entry():
   """Get all tae imsi entry 
   
   #COMMAND: eitputil -f tae show imsi all
   
   | Input Parameters | Man. | Description |
   
   
   Example :
   | ${item}= | get_tae_imsi_entry |
   """
   command = 'eitputil -f tae show imsi all'
   output = connections.execute_mml_without_check(command)
   return __get_tae_entry_imsi(output)


def delete_tae_entry_all():
   """Delete all tae entries
   
   #COMMAND: eitputil tae delete -f
   
   | Input Parameters | Man. | Description |
   | No               | No   | No |
   
   Example :
   | delete_tae_entry_all |
   """
   command = 'eitputil tae delete -f'
   output = connections.execute_mml_without_check(command)
   print output


def delete_tae_entry_by_conn(conn_id):
   """Delete TAE Entry according to connection
   
   #COMMAND: eitputil tae delete -c conn_id
   
   | Input Parameters | Man. | Description |
   | conn_id          | Yes  | connection of entry |
   
   Example :
   | delete_tae_entry_by_conn | 0X7ffff82 |
   """
   command = 'eitputil tae delete -f -c ' + conn_id
   output = connections.execute_mml_without_check(command)
   print output


def delete_tae_entry_by_teid(teid):
   """Delete TAE Entry according to GTP tunnel
   
   #COMMAND: eitputil tae delete -t teid
   
   | Input Parameters | Man. | Description |
   | teid             | Yes  | GTP tunnel  |
   
   Example :
   | delete_tae_entry_by_teid | 0XBED000002 |
   """
   command = 'eitputil tae delete -f -t ' + teid
   output = connections.execute_mml_without_check(command)
   print output
   
def delete_tae_entry_by_udp(ip, port):
   """Delete TAE Entry according to IP and UDP port
   
   #COMMAND: eitputil tae delete -f -i ip -p port
   
   | Input Parameters | Man. | Description        |
   | ip               | Yes  | IP address of entry|
   | port             | Yes  | UDP port of entry  |
   
   Example :
   | delete_tae_entry_by_udp | 192.168.1.1 | 2026 |
   """
   command = 'eitputil tae delete' + ' -f -i ' + ip + ' -p ' + port
   output = connections.execute_mml_without_check(command)
   print output
   

def get_qos_by_udp(ip, port):
   """Get tae Qos according to the IP address and UDP port
   
   #COMMAND: eitputil qos connections show <conn:ip:port:teid>
   
   | Input Parameters | Man. | Description |
   | ip               | Yes  | ip address |
   | port             | Yes  | UDP port |
   
   Example :
   | ${item}= | get_qos_from_udp | 192.168.1.1 | 5000 |
   """
   command = 'eitputil -f qos connections show' + ' :' + ip + ':' + port + ':'
   output = connections.execute_mml_without_check(command)
   return __get_qos_entry(output)

def get_qos_by_conn(conn_id):
   """Get tae entry according to the connection
   
   #COMMAND: eitputil qos connections show <conn:ip:port:teid>
   
   | Input Parameters | Man. | Description |
   | conn_id          | Yes  | connection id |
   
   Example :
   | ${item}= | get_qos_by_conn | 2344 |
   """
   command = 'eitputil -f qos connections show ' + conn_id + ':::'
   output = connections.execute_mml_without_check(command)
   return __get_qos_entry(output)


def get_qos_by_teid(teid):
   """Get tae entry according to the teid
   
   #COMMAND: eitputil qos connections show <conn:ip:port:teid>
   
   | Input Parameters | Man. | Description |
   | teid          | Yes  | teid id |
   
   Example :
   | ${item}= | get_qos_by_gtp | 2344 |
   """
   command = 'eitputil -f qos connections show' + ' :::' + teid
   output = connections.execute_mml_without_check(command)
   return __get_qos_entry(output)


def _mux_counter(a,b,c,d,e):
   entry = CommonItem()
   entry.out_mux = a
   entry.out_muxed = b
   entry.in_mux = c
   entry.in_muxed = d
   entry.in_disc = e
   return entry;

def get_mux_counter_by_ipbr(ipbr):
   """This keyword is to get mux counter according to ipbr id.
   
   #COMMAND: eitputil mux show stat 3333
   
   | Input Parameters | Man. | Description |
   | ipbr             | Yes  |  id of IPBR |
   
   Examples
   | ${result}= | get_mux_counter_by_ipbr | 1 |

   """

   command = 'eitputil -f mux show stat ' + ipbr
   output = connections.execute_mml_without_check(command)
   if (output == ''):
      return _mux_counter('0','0','0','0','0')
   lines=output.splitlines(False)
   rule = '\d+\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+'
   for j in lines:
      res = re.search(rule, j);
      if (res is not None):
         return _mux_counter(res.group(1),res.group(2),res.group(3),res.group(4),res.group(5));
   return _mux_counter('0','0','0','0','0')


def clear_mux_counter_by_ipbr(ipbr):
   """This keyword is to clear mux counter according to ipbr id.
   
   #COMMAND: eitputil mux zero stat 3333
   | Input Parameters | Man. | Description |
   | ipbr          | Yes  | id of IPBR |
   
   Examples
   | ${result}= | clear_mux_counter_by_ipbr | 1 |

   """
   command = 'eitputil -f mux zero stat ' + ipbr
   output = connections.execute_mml_without_check(command)


def __tt_get_handid_of_call(unit_name, call_id):
   command = 'lgutilgx RI:%s' % (unit_name);
   output = connections.execute_mml_without_check(command)
   pattern = '\s*%s\s+[0-9a-fA-F]+\s+(\d+)\s+(\d+)\s*' % (call_id);
   result = re.search(pattern, output)
   if result is not None:
      return result.group(1)
   return '0'


def tt_get_first_conn_of_call(unit_name, call_id):
   """This keyword is to get call's connection.
   
   #COMMAND: lgutilgx RID:
   | Input Parameters | Man. | Description |
   | unit_name        | Yes  | unit name |
   | call_id          | Yes  | call id |
   
   Examples
   | ${result}= | tt get first conn of call | uscp-0 |0x1|

   """

   hand_id = __tt_get_handid_of_call(unit_name, call_id);
   command = 'lgutilgx RID:%s:%s' % (unit_name, hand_id);
   output = connections.execute_mml_without_check(command)
   pattern = re.compile(r"""TPI\s+\d+\S\s+CONNECTION\s+ID\S(\w+)""", re.M | re.X);
   items = pattern.findall(output)
   if (len(items) != 0):
      for item in items:
         return item
   return '0'

def tt_get_iuetor_state(rg_name):
   """This keyword is to get iuetor state.
   
   #COMMAND: eitpste gtp get glo
   | Input Parameters | Man. | Description |
   | rg_name          | Yes  | RG name |
     
   Examples
   | ${result}= | tt_get_iuetor_state | QNUPRG-0 |

   """
   rg_index = rg_name.lstrip("QNUPRG-")
   iue_cmd = "eitpste gtp get glo"
   eipu_list = tt_get_eipu_from_rg(rg_name)
   log_addr = tt_get_logaddr_from_rg(rg_name)
   print eipu_list
   result = {}
   for i in range(0,len(eipu_list)):
      ssh_eipu= 'ssh %s' % (eipu_list[i])
      connections.execute_mml(ssh_eipu)
      iue_result = connections.execute_mml(iue_cmd)
      connections.execute_mml('exit')
      items=iue_result.splitlines(False)
      for j in range (1,24):
         str= 'Logical\s+Address:\s+(\w+)'
         address = re.search(str,items[j])
         if (address is not None):
            logical_address_0 = address.group(1)
         str= 'GTP\s+Unit\s+State:\s+(\w+)'
         state = re.search(str,items[j])
         if (state is not None):
            state_0 = state.group(1)
      print logical_address_0.lstrip("0x")
      for j in range (24,len(items)):
         str= 'Logical\s+Address:\s+(\w+)'
         address = re.search(str,items[j])
         if (address is not None):
            logical_address_1 = address.group(1)
         str= 'GTP\s+Unit\s+State:\s+(\w+)'
         state = re.search(str,items[j])
         if (state is not None):
            state_1 = state.group(1)
      index = string.atoi(rg_index,base=10)*2 + i
      if logical_address_0.lstrip("0x") == log_addr:
         #result[eipu_list[i]]= state_0
         result["QNUP-" + '%s' % index] = state_0
      else:
         #result[eipu_list[i]]= state_1
         result["QNUP-" + '%s' % index] = state_1
   return result

def tt_get_tae_state(rg_name):
   """This keyword is to get tae state.
   
   #COMMAND: eitpste tae summ r
   | Input Parameters | Man. | Description |
   | rg_name          | Yes  | RG name |
     
   Examples
   | ${result}= | tt_get_tae_state | QNUPRG-0 |

   """
   rg_index = rg_name.lstrip("QNUPRG-")
   eipu_list = tt_get_eipu_from_rg(rg_name)
   log_addr = tt_get_logaddr_from_rg(rg_name)
   log_addr = log_addr.lstrip("0x4")
   tae_cmd = "eitpste tae summ r |grep" + " " + log_addr
   print eipu_list
   result = {}
   for i in range(0,len(eipu_list)):
      ssh_eipu = 'ssh %s' % (eipu_list[i])
      connections.execute_mml(ssh_eipu)
      tae_result = connections.execute_mml(tae_cmd)
      connections.execute_mml('exit')
      items = tae_result.split()
      index = string.atoi(rg_index,base=10)*2 + i
      result["QNUP-" + '%s' % index] = items[4]
   return result
      


def tt_get_eipu_from_rg(rg_name):
   """This keyword is to get related eipu combined to one RG.
      
   | Input Parameters | Man. | Description |
   | rg_name          | Yes  | RG name |
      
   Examples
   | ${result}= | tt_get_eipu_from_rg | QNUPRG-0 |

   """
   cmd = "hascli --children " + "/" + rg_name
   output = connections.execute_mml(cmd)
   lines = output.splitlines(False)
   eipu = []
   for i in lines:
       str= '\/(EIPU-\d+)'
       eipu_res = re.search(str,i)
       if (eipu_res is not None):
          eipu.append(eipu_res.group(1))
   eipu_list = list(set(eipu))
   return eipu_list

def tt_get_logaddr_from_rg(rg_name):
   """This keyword is to get RG's logical address.
      
   | Input Parameters | Man. | Description |
   | rg_name          | Yes  | RG name     |
   
   
   Examples
   | ${result}= | tt_get_logaddr_from_rg | QNUPRG-0 |

   """
   cmd = "hascli --children " + "/" + rg_name
   output = connections.execute_mml(cmd)
   lines = output.splitlines(False)
   cmd = "ilclifunit -u |grep" + " " + lines[1] 
   output = connections.execute_mml(cmd)
   item = output.split()
   return item[1].lstrip("0x4")

def tt_get_detail_connection_info(conn_id,eipu='eipu-0'):
   """This keyword is to get detailed info of one connection.
   
   #COMMAND: eitpste tae detail connection 0x28002
   | Input Parameters | Man. | Description |
   | conn_id          | Yes  | id of Connection |
   | eipu             | No   | target eipu |
   
   Examples
   | ${result}= | tt_get_detail_connection_info | 0x28002 |

   """
   tae_cmd = "eitpste tae detail connection " + conn_id
   if(connections.execute_mml('echo $HW_PLATFORM').count('BCN')>0):
        ssh_eipu= 'ssh %s' % (eipu)
        connections.execute_mml(ssh_eipu)
        tae_result = connections.execute_mml(tae_cmd)
        connections.execute_mml('exit')
   else:
        tae_result = connections.execute_mml(tae_cmd)
   return tae_result

      


if __name__ == '__main__':
    Echo("telnet ");


