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

def eitpsd_test_list_uspx(uspx_num='1'):
   """
   This keyword is to list the number of usproxy .
   
   | Parameters     | Man. | Description                      |
   | uspx_num       | No   | 1                                |
   
   Example
   | ${result} | eitpsd test list uspx  |  2  |

   """
   
   command = 'eitpsd -- -c "debug;test xsup random ' +  uspx_num + ' uspx"';
   
   output = connections.execute_mml_without_check(command)
   
   lines = output.strip().splitlines()      
   stat = [] 
   for i in lines:
      if i != '':
         stat.append(i.strip());
   if len(stat) < 1:
      exceptions.raise_ILError("ILCommandExecuteError", output)
   print stat
   return stat

def __get_dscp(ipbr_id):
   idsp = [46, 34, 26, 18, 10, 0]
   idsp_len = len(idsp)
   index = ipbr_id % idsp_len;
   return idsp[index];

def __get_ip(ipbr_id, fpc, bcn):
   ip_index = (ipbr_id % 253) + 1
   return '191.%d.%d.%d' % (fpc, bcn, ip_index);

def __delete_ipbr(ipbr_id):
   cmd  = 'fsclish -c "delete networking ipbr ipbr-id %s"' % ipbr_id
   print cmd
   output = connections.execute_mml_without_check(cmd)

def __add_ipbr(ipbr_id):
   cmd  = 'fsclish -c "add networking ipbr'
   cmd += ' committed-bandwidth 1000000'
   cmd += ' route-bandwidth 1000000'
   cmd += ' committed-dcn-bandwidth 1'
   cmd += ' committed-sig-bandwidth 1'
   cmd += ' ipbr-name %d ipbr-id %d"' %(ipbr_id, ipbr_id)
   print cmd
   output = connections.execute_mml_without_check(cmd)


def __delete_ip(ipbr_id, fpc, bcn):
   cmd  = 'fsclish -c "delete networking address'
   cmd += ' /QNUP-0 iface ethtest20 ip-address'
   cmd += ' %s"' % __get_ip(ipbr_id, fpc, bcn)
   print cmd
   output = connections.execute_mml_without_check(cmd)
   
def __add_ip(ipbr_id, fpc, bcn):
   cmd  = 'fsclish -c "add networking address'
   cmd += ' /QNUP-0 iface ethtest20 ip-address'
   cmd += ' %s/16"' % __get_ip(ipbr_id, fpc, bcn)
   print cmd
   output = connections.execute_mml_without_check(cmd)

def __delete_ipro(ipbr_id, fpc, bcn):
   cmd  = 'fsclish -c "delete networking ipro'
   cmd += ' ipbr-id %d' % ipbr_id
   cmd += ' ip-address %s' % __get_ip(ipbr_id, fpc, bcn)
   cmd += ' iface ethtest20 owner /QNUP-0"'
   print cmd
   output = connections.execute_mml_without_check(cmd)
   __delete_ip(ipbr_id, fpc, bcn)
   __delete_ipbr(ipbr_id)

def __add_ipro(ipbr_id, fpc, bcn):
   __add_ipbr(ipbr_id)
   __add_ip(ipbr_id, fpc, bcn)
   cmd  = 'fsclish -c "add networking ipro iface ethtest20'
   cmd += ' owner /QNUP-0'
   cmd += ' ipbr-id %d' % ipbr_id
   cmd += ' ip-address %s"' % __get_ip(ipbr_id, fpc, bcn)
   print cmd
   output = connections.execute_mml_without_check(cmd)
   return [str(ipbr_id), __get_ip(ipbr_id, fpc, bcn)]


def __disable_mux(ipbr_id):
   cmd = 'eitputil -f mux disable %s' % ipbr_id
   print cmd
   output = connections.execute_mml_without_check(cmd)

def __enable_mux(ipbr_id):
   cmd = 'eitputil -f mux enable %d %d 30 65535 65535' % (ipbr_id, __get_dscp(ipbr_id))
   print cmd
   output = connections.execute_mml_without_check(cmd)

def eitpsd_test_delete_ipro(ipbr_base='2100', ipbr_num='1', fpc='34', bcn='13'):
   """
   This keyword is to add ipro.
   
   | Parameters     | Man. | Description                      |
   | ipbr_base      | No   | 2100                                |
   | ipbr_num       | No   | 1   
   | fpc            | No   | 34  
   | bcn            | No   | 13  
   
   
   Example
   | ${result} | eitpsd test delete ipro  |  

   """
   for i in range(0, int(ipbr_num)):
      __delete_ipro(int(ipbr_base) + i, int(fpc), int(bcn));

def eitpsd_test_add_ipro(ipbr_base='2100', ipbr_num='1', fpc='34', bcn='13'):
   """
   This keyword is to add ipro.
   
   | Parameters     | Man. | Description                      |
   | ipbr_base      | No   | 2100                                |
   | ipbr_num       | No   | 1   
   | fpc            | No   | 34  
   | bcn            | No   | 13  
   
   
   Example
   | ${result} | eitpsd test add ipro  |  

   """
   
   ipro_list = []
   for i in range(0, int(ipbr_num)):
      ipro = __add_ipro(int(ipbr_base) + i, int(fpc), int(bcn));
      if ipro != []:
         ipro_list.append(ipro)
   
   return ipro_list


def eitpsd_test_disable_mux(ipbr_base='2100', ipbr_num='1'):
   """
   This keyword is to disable mux.
   
   | Parameters     | Man. | Description                |
   | ipbr_base      | No   | 2100                       |
   | ipbr_num       | No   | 1   
   
   
   Example
   | ${result} | eitpsd test disable mux  |  

   """
   for i in range(0, int(ipbr_num)):
      __disable_mux(int(ipbr_base) + i);
      
def eitpsd_test_enable_mux(ipbr_base='2100', ipbr_num='1'):
   """
   This keyword is to enable mux.
   
   | Parameters     | Man. | Description                |
   | ipbr_base      | No   | 2100                       |
   | ipbr_num       | No   | 1   
   
   
   Example
   | ${result} | eitpsd test enable mux  |  

   """
   for i in range(0, int(ipbr_num)):
      __enable_mux(int(ipbr_base) + i);

def eitpsd_test_cs_iucs(iucs_ipro_list=[], uspx_list=[], remote_ip_list=[], leg_num='1'):
   """
   This keyword is to test dedicated Iucs performace of IuCS.
   
   | Parameters     | Man. | Description                               |
   | iucs_ipro_list | No   |  IPRO list                                |
   | uspx_list      | No   |  used USPX list, default is empty         |
   | remote_ip_list | No   |  used remote IP list, default is empty    |
   | leg_num        | No   |  Iucs leg number,default is 1             |
   | Return value   | None |
   
   Example
   | eitpsd test cs iucs  |

   """
   
   iucs_param = ''
   iucs_use_ipro = '0'
   
   for iucs_ipro in iucs_ipro_list:
      iucs_param += 'test ipro 2 ' + iucs_ipro[0] + ' ' + iucs_ipro[1] + ' 0;'
      iucs_use_ipro = '2'
   iucs_param += 'test iucs use ipro '+ iucs_use_ipro +';'
   
   uspx_param = ''
   use_uspx = '0'
   for uspx in uspx_list:
      uspx_param += 'test xsup 1 ' + uspx + ' uspx;'
      use_uspx = '1'
   uspx_param += 'test cs use uspx ' + use_uspx + ';'
   
   remote_ip_param=''
   for remote_ip in remote_ip_list:
      remote_ip_param += 'test ip-conf add ' + remote_ip +';'
   
   cs_param = 'test cs create iucs ' + leg_num
   
   command = 'eitpsd -- -c "debug;test dscp pool 7;' 
   command += iucs_param + uspx_param + remote_ip_param
   command += cs_param + '"'
   
   output = connections.execute_mml_without_check(command)
   
   expect = 'Create ' + leg_num + ' iucs legs of cs with ' + leg_num + ' in success'

   if output.count(expect) < 1:
      exceptions.raise_ILError("ILCommandExecuteError", output)


def __eitpsd_test_cs_iub_with_dscp_pool(iub_ipro_list=[], uspx_list=[], remote_ip_list=[], leg_num='1', dscp_pool='7'):
   """
   This keyword is to test dedicated iub performace of CS.
   
   | Parameters     | Man. | Description                               |
   | iub_ipro_list  | No   |  IPRO list                                |
   | uspx_list      | No   |  used USPX list, default is empty         |
   | remote_ip_list | No   |  used remote IP list, default is empty    |
   | leg_num        | No   |  iub leg number,default is 1              |
   | Return value   | None |
   
   Example
   | eitpsd test cs iub  |
   
   """
   
   iub_param = ''
   iub_use_ipro = '0'
   for iub_ipro in iub_ipro_list:
      iub_param += 'test ipro 2 ' + iub_ipro[0] + ' ' + iub_ipro[1] + ' 0;'
      iub_use_ipro = '2'
   iub_param += 'test iub use ipro '+ iub_use_ipro +';'
   
   uspx_param = ''
   use_uspx = '0'
   for uspx in uspx_list:
      uspx_param += 'test xsup 1 ' + uspx + ' uspx;'
      use_uspx = '1'
   uspx_param += 'test cs use uspx ' + use_uspx + ';'
   
   remote_ip_param=''
   for remote_ip in remote_ip_list:
      remote_ip_param += 'test ip-conf add ' + remote_ip + ';'
   cs_param = 'test cs create iub ' + leg_num
   
   command = 'eitpsd -- -c "debug;test dscp pool ' + dscp_pool + ';' 
   command += iub_param + uspx_param + remote_ip_param
   command += cs_param + '"'
   
   output = connections.execute_mml_without_check(command)
   
   expect = 'Create ' + leg_num + ' iub legs of cs with ' + leg_num + ' in success'

   if output.count(expect) < 1:
      exceptions.raise_ILError("ILCommandExecuteError", output)
      

def eitpsd_test_cs_iub(iub_ipro_list=[], uspx_list=[], remote_ip_list=[], leg_num='1'):
   return __eitpsd_test_cs_iub_with_dscp_pool(iub_ipro_list, uspx_list, remote_ip_list, leg_num, '7')

def eitpsd_test_cs_mux(iub_ipro_list=[], uspx_list=[], remote_ip_list=[], leg_num='1'):
   return __eitpsd_test_cs_iub_with_dscp_pool(iub_ipro_list, uspx_list, remote_ip_list, leg_num, '6')

def eitpsd_test_cs_call_loadsharing(ipro_list=[], uspx_list=[], remote_ip_list=[],call_num='1'):
   """
   This keyword is to test dedicated Iu performace of CS call.
   
   | Parameters     | Man.| Description                               |
   | ipro_list      | No  |  IPRO list                                 |
   | uspx_list      | No  |  used USPX list, default is empty         |
   | remote_ip_list | No  |  used remote IP list, default is empty    |
   | call_num       | No  |  CS call number,default is 1              |
   | Return value   | None |
   
   Example
   | ${result} | eitpsd test cs call  |
   
   """

   ipro_param = ''
   use_ipro = '0'
   for ipro in ipro_list:
      ipro_param += 'test ipro 1 ' + ipro[0] + ' ' + ipro[1] + ' 0;'
      use_ipro = '1'

   iub_param = 'test iub use ipro ' + use_ipro +';'
   
   iu_param = 'test iucs use ipro '+ use_ipro +';'
   
   uspx_param = ''
   use_uspx = '0'
   for uspx in uspx_list:
      uspx_param += 'test xsup 1 ' + uspx + ' uspx;'
      use_uspx = '1'
   uspx_param += 'test cs use uspx ' + use_uspx + ';'
   
   remote_ip_param=''
   for remote_ip in remote_ip_list:
      remote_ip_param += 'test ip-conf add ' + remote_ip +';'
   
   cs_param = 'test cs create call ' + call_num
   
   command = 'eitpsd -- -c "debug;test dscp pool 7;' 
   command += ipro_param + iub_param + iu_param + uspx_param + remote_ip_param
   command += cs_param + '"'
   
   output = connections.execute_mml_without_check(command)
   
   expect = 'Create ' + call_num + ' cs calls with ' + call_num + ' in success'

   if output.count(expect) < 1:
      exceptions.raise_ILError("ILCommandExecuteError", output)

if __name__ == '__main__':
    Echo("telnet ");
