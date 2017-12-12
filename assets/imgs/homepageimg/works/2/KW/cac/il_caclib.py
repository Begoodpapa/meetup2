from comm.communication import connections
from comm.communication import exceptions
from comm.communication.helper import CommonItem
from ilcallmgmt_subsystem_lib.library import upm_lib
from ilstarter_subsystem_lib import starter_fileparse
import re
import os

def _parse_release_result(output):
    #lines = output.strip().splitlines()
    return_value = CommonItem()
    if (-1 != output.lower().find("success")):
    	return_value.result = "success"
    else:
    	return_value.result = "failed"
    return return_value
    #for index in range(0, len(lines)):
     #   if lines[index].lower().find('release') == -1:
      #      continue
       # elif lines[index].lower().find('success') == -1:
        #    return_value.result = "failed"
         #   return_value. error_code=lines[index + 1].split(':')[1].strip()
          #  break
       # else:
       #     return_value.result = "success"
        #   return_value.ip = lines[index + 1].split(':')[1].strip()
         #   return_value.port = lines[index + 2].split(':')[1].strip()
         #   break
    #return return_value

def _cac_release_specified_object(command):
    exec_output = connections.execute_mml_without_check(command)
    return _parse_release_result(exec_output)
    
def release_udp_conn_resource(ip_addr, port_num):
    """
     This keyword is used to release specified UDP connection resource in CACPRB

    #COMMAND: iltrmcli -D -u 192.168.1.1:1024

    | Parameters | Man.| Description       |
    | ip_addr    | Yes | IP address        |
    | port_num   | Yes | UDP Port ID       |

    | Return value | an instance of String, success or failed |

    Example
    | result | release udp conn resource | ${IP_address} | ${UDP_PORT} |
    """
    command = "iltrmcli -D -u %s:%s" % (ip_addr, port_num)
    print "Command:", command
    return _cac_release_specified_object(command)

def release_gtp_conn_resource(ip_addr='', teid=''):
    """
     This keyword is used to release specified GTP connection resource in CACPRB

    #COMMAND: iltrmcli -D -g TEID

    | Parameters | Man.| Description       |
    | ip_addr    | Yes | IP address        |
    | teid       | Yes | GTP tunnel ID     |

    | Return value | an instance of String, success or failed |

    Example
    | result | release gtp conn resource | ${IP_address} | ${GTP_TEID} |
    """
    command = "iltrmcli -D -g 0x%s" % (teid)
    print "Command:", command
    
    return _cac_release_specified_object(command)

def release_all_udp_conn_resource():
    """
     This keyword is used to release all UDP connection resource in CACPRB

    #COMMAND: iltrmcli -D -u all

    | Parameters | Man.| Description       |
    |            |     |                   |


    | Return value | an instance of String, success or failed |

    Example
    | result | release all udp conn resource | 
    """
    command = "iltrmcli -D -u all"
    print "Command:", command
    exec_output = connections.execute_mml_without_check(command)
    return_value = CommonItem()
    if (-1 != exec_output.lower().find("success")):
        return_value.result = "success"
    else:
        return_value.result = "failed"
    return return_value


def _cac_release_all_leg_objects(command):
    exec_output = connections.execute_mml_without_check(command)
    return_value = CommonItem()
    if (-1 != exec_output.lower().find("success")):
        return_value.result = "success"
    else:
        return_value.result = "failed"
    return return_value

def release_all_gtp_conn_resource():
    """
     This keyword is used to release all GTP connection resource in CACPRB

    #COMMAND: iltrmcli -D -g all 

    | Parameters | Man.| Description       |
    |            |     |                   |

    | Return value | an instance of String, success or failed |

    Example
    | result | release all gtp conn resource |
    """
    command = "iltrmcli -D -g all"
    print "Command:", command
    return_value = _cac_release_all_leg_objects(command)
    return return_value

def release_all_conn_resource_with_owner_id(owner_id):
    """
     This keyword is used to release all connection resource with specified owner ID in CACPRB

    #COMMAND: iltrmcli -D -o <owner_id> 

    | Parameters | Man.| Description       |
    |  owner_id  | Yes | Owner ID          |

    | Return value | an instance of String, success or failed |

    Example
    | result | release all conn resource with owner id | ${Owner_ID} |
    """    
    command = "iltrmcli -D -o %s" % (owner_id)
    print "Command:", command
    return_value = _cac_release_all_leg_objects(command)
    return return_value

def release_all_conn_resource():
    """
     This keyword is used to release all connection resource in CACPRB

    #COMMAND: iltrmcli -D -a

    | Parameters | Man.| Description       |
    |            |     |                   |

    | Return value | an instance of String, success or failed |

    Example
    | result | release all conn resource | 
    """    
    command = "iltrmcli -D -a"
    print "Command:", command
    return_value = _cac_release_all_leg_objects(command)
    return return_value

def _parse_conn_info(input_str, fliter_enable=True):
    if input_str.find('NO WORKING') != -1:
       return input_str
    elif input_str.find('CAN\'T FIND RU') != -1:
       return input_str
    else:
        if input_str.find('VRF_ID') != -1:
            pattern_str = '(\S+)\s+(\w+)\s+(\d+)\s+(\w+)\s+(\d+)\s+(\S+)' 
        else:
            pattern_str = '(\S+)\s+(\w+)\s+(\d+)\s+(\w+)\s+(\d+)\s+' 
        pattern = re.compile(pattern_str)
        items =  pattern.findall(input_str)
        filter_list = ['FREE','INVALID']
        info_list = {}
        for item in items:
            if fliter_enable and (item[1] in filter_list):
                continue
            leg_info = {'type': item[1], 'ipbr_id': item[2], 'owner_id': item[3], 'reserve_bw': item[4]}
            if input_str.find('VRF_ID') != -1:
                leg_info['vrf_id'] = item[5]
            if re.findall(r'0x(\S+)', item[0]) != -1:
                leg_key = item[0].replace('0x', '')
            else:
                leg_key = item[0]
            info_list[leg_key] = leg_info
        return info_list

def inquiry_udp_conn_resource_info(ip_address, port_num, vrf_id='', filter_str = 'true'):    
    """
     This keyword is used to inquiry specified UDP connection resource in CACPRB

    #COMMAND: iltrmcli -S -u 192.168.1.1:1024

    | Parameters | Man.| Description       |
    | ip_addr    | Yes | IP address        |
    | port_num   | Yes | UDP Port ID       |
    | vrf_id     | No  | Instance ID of virtual routing forward |
    | filter     | No  | Filter whether add the reserved, free, buffer port info into the list |

    | Return value | an instance of CommonItem |

    Example
    | result | inquiry udp conn resource info | ${IP_address} | ${UDP_PORT} |
    """
    
    command = "iltrmcli -S -u %s:%s " % (ip_address, port_num)
    if vrf_id != '' and connections.execute_mml('echo $HW_PLATFORM').count('FTLB') == 0:
        command = command + ' -v %s' % (vrf_id)
    print "Command:", command
    exec_output = connections.execute_mml_without_check(command)
    if filter_str.upper() == 'TRUE':
        filter_enable=True
    return _parse_conn_info(exec_output, filter_enable)

def inquiry_gtp_conn_resource_info(ip_address='', teid='', vrf_id='', filter = 'true'):
    """
     This keyword is used to inquiry specified GTP connection resource in CACPRB

    #COMMAND: iltrmcli -S -g TEID

    | Parameters | Man.| Description       |
    | ip_addr    | Yes | IP address        |
    | teid       | Yes | GTP tunnel ID     |
    | vrf_id     | No  | Instance ID of virtual routing forward |
    | filter     | No  | Filter whether add the reserved, free, buffer info into the list |

    | Return value | an instance of CommonItem |

    Example
    | result | inquiry gtp conn resource info | ${IP_address} | ${GTP_TEID} |
    """
    teid_hex = "0x%s" %(teid)
    command = "iltrmcli -S -g %s" %(teid_hex)
    #if vrf_id !='' and connections.execute_mml('echo $HW_PLATFORM').count('FTLB') == 0:
       # command = command + " -v %s" %(vrf_id)
    print "Command:", command
    exec_output = connections.execute_mml_without_check(command)
    return _parse_conn_info(exec_output, filter)

def inquiry_udp_conn_port_info(ip_address, port_num, vrf_id='', filter_str = 'true'):    
    """
     This keyword is used to inquiry specified UDP connection resource in CACPRB

    #COMMAND: iltrmcli -S -u 192.168.1.1:1024

    | Parameters | Man.| Description       |
    | ip_addr    | Yes | IP address        |
    | port_num   | Yes | UDP Port ID       |
    | vrf_id     | No  | Instance ID of virtual routing forward |
    | filter     | No  | Filter whether add the reserved, free, buffer port info into the list |

    | Return value | an instance of CommonItem |

    Example
    | result | inquiry udp conn resource info | ${IP_address} | ${UDP_PORT} |
    """
    
    command = "iltrmcli -S -u %s:%s " % (ip_address, port_num)
    if vrf_id != '' and connections.execute_mml('echo $HW_PLATFORM').count('FTLB') == 0:
        command = command + ' -v %s' % (vrf_id)
    print "Command:", command
    exec_output = connections.execute_mml_without_check(command)
    if filter_str.upper() == 'TRUE':
        filter_enable=True
    else:
    	filter_enable=False
    return _parse_conn_info_udp(exec_output, filter_enable)

def _parse_conn_info_udp(input_str, fliter_enable=True):
    if input_str.find('VRF_ID') != -1:
        pattern_str = '(\d+\.\d+\.\d+\.\d+\:\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)' #if input_str.find('VRF_ID') != -1 else ''
    else:
        pattern_str = '(\d+\.\d+\.\d+\.\d+\:\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+' 
    pattern = re.compile(pattern_str)
    items =  pattern.findall(input_str)
    filter_list = ['FREE','INVALID']
    info_list = {}
    for item in items:
        if fliter_enable and (item[1] in filter_list):
            continue
        leg_info = {'type': item[1], 'ipbr_id': item[2], 'owner_id': item[3], 'reserve_bw': item[4]}
        if input_str.find('VRF_ID') != -1:
            leg_info['vrf_id'] = item[5]
        info_list[item[0]] = leg_info
    return info_list

def list_all_udp_conn_resource_info(filter = 'true'):
    """
     This keyword is used to list all UDP connection resource in CACPRB

    #COMMAND: iltrmcli -S -u all

    | Parameters | Man.| Description       |
    | filter     | No  | Filter whether add the reserved, free, buffer port info into the list |

    | Return value | an instance of CommonItem |

    Example
    | result | list all udp conn resource info |
    """
    command = "iltrmcli -S -u all"
    print "Command:", command
    exec_output = connections.execute_mml_without_check(command)
    return _parse_conn_info(exec_output, filter)

def list_all_gtp_conn_resource_info(filter = 'true'):
    """
     This keyword is used to list all GTP connection resources in CACPRB

    #COMMAND: iltrmcli -S -g all

    | Parameters  | Man.| Description       |
    | filter     | No  | Filter whether add the reserved, free, buffer info into the list |

    | Return value | an instance of CommonItem |

    Example
    | result | list all gtp conn resource info |
    """
    command = "iltrmcli -S -g all"
    print "Command:", command
    exec_output = connections.execute_mml_without_check(command)
    return _parse_conn_info(exec_output, filter)

def list_all_ipro_resource_info(filter = 'true'):
    """
     This keyword is used to all connection resource in CACPRB with specified owner ID

    #COMMAND: iltrmcli -S -o

    | Parameters | Man.| Description       |
    | owner_id   | Yes | Owenr ID          |
    | filter     | No  | Filter whether add the reserved, free, buffer port info into the list |

    | Return value | an instance of CommonItem |

    Example
    | result | list all conn resource info with owner id | ${Owner_ID} |
    """
    command = "iltrmcli -S -o"
    print "Command:", command
    exec_output = connections.execute_mml_without_check(command)
    return _parse_conn_info(exec_output, filter)

def list_all_conn_resource_info(filter = 'true'):
    """
     This keyword is used to list all connection resource in CACPRB

    #COMMAND: iltrmcli -S -a

    | Parameters | Man.| Description       |
    | filter     | No  | Filter whether add the reserved, free, buffer port info into the list |

    | Return value | an instance of CommonItem |

    Example
    | result | list all conn resource info | true | 
    """
    command = "iltrmcli -S -a"
    print "Command:", command
    exec_output = connections.execute_mml_without_check(command)
    print "exec_out_put", exec_output 
    return _parse_conn_info(exec_output, filter)

def check_all_MO_between_LDAP_and_CAC():
    """
     This keyword is used to check all MO difference between CAC and LDAP.

    #COMMAND: iltrmcli -C -m

    | Parameters | Man.| Description       |
    |            | No  |      |

    | Return value | an instance of CommonItem |

    Example
    | result | list all conn resource info | true | 
    """
    command = "iltrmcli -C -m"
    print "Command:", command
    exec_output = connections.execute_mml(command)
    #if (-1 != exec_output.find("No Difference")):
	#pattern = re.compile("""(\S+)\s+No Difference\s+""", re.DOTALL)
	#items = pattern.findall(exec_output)
	#if len(items) == 4:
      #      return "No Difference"
       # else:
       #     return _parse_sync_compare(exec_output)
    #else:
    return _parse_sync_compare(exec_output)
     
def _parse_in_leg_creation_output(exec_output):

    result = CommonItem()
    if (-1 != exec_output.find("SUCCESSFUL")):
        pattern = re.compile("""^.*IP-RESOURCE\s+(IN-\d+)\s+RESERVED\s+(\S+).*IPv4\s+Addr:\s+(\d+\.\d+\.\d+\.\d+)\s+:\s*(\d+).*$""", re.DOTALL)
        match = re.match(pattern, exec_output) 
        if match:
            result.result = "success"
            result.leg_id = match.group(1)
            result.ip = match.group(3)
            result.port = match.group(4)
    elif (-1 != exec_output.find("FAILED")):
        pattern = re.compile("""^.*IP-RESOURCE\s+RESERVATION\s+(\S+),\s*EC=(\S+).*$""", re.DOTALL | re.VERBOSE)
        match = re.match(pattern, exec_output) 
        if match:
            result.result = "failed"
            result.error_code = match.group(2)
    else:
        result.result = "failed"
    return result

def create_iub_leg_with_cac_params(call_id, ipbr_id_1, params="", ipbr_id_2="", computer="USCP-0"):
    """
     This keyword is used to create Iub leg with CACPRB parameters
     
    #COMMAND: lgutilgx RRI:USCP-0:7D1:IN,:,,,12,13:1::NCAC=0

    | Parameters | Man.| Description       |
    | call_id    | Yes | Call ID           |
    | ipbr_id_1  | Yes | IPBR ID           |
    | params     | No  | traffic parameters used for leg creation |
    | ipbr_id_2  | No  | Second IPBR ID in IPBR list |
    | computer   | No  | Recovery Unit specified to create leg, default is USCP-0 |

    | Return value | an instance of CommonItem |

    Example
    | result | create_iub_leg_with_cac_params | ${Call_ID} | ${IPBR_ID_1} | NCAC=0 | ${IPBR_ID_2} | ${USCP-0}|
    """
    if ipbr_id_2 != "":
        command = """lgutilgx RRI:%s:%s:IN,:,,,%s,%s:1::%s""" % (computer, call_id, ipbr_id_1, ipbr_id_2, params)
    else:
        command = """lgutilgx RRI:%s:%s:IN,:,,,%s:1::%s""" % (computer, call_id, ipbr_id_1, params)        
    print "execute command:", command
    
    exec_output = connections.execute_mml_without_check(command)
    return _parse_in_leg_creation_output(exec_output)

def _parse_out_leg_creation_output(exec_output):
    result = CommonItem()
    if (-1 != exec_output.find("SUCCESSFUL")):
        pattern = re.compile("""^.*CALL_ID\s+(\S+).*RM2\s+HAND\s+=\s+(\S+)\s+(\S+).*IPv4\s+Addr:\s+(\d+\.\d+\.\d+\.\d+)\s+:\s*(\d+).*$""", re.DOTALL)
        match = re.match(pattern, exec_output)
        if match:
            result.result = "success"
            result.call_id = match.group(1)
            result.hand_id = match.group(2)
            result.focus_id = match.group(3)
            result.ip = match.group(4)
            result.port = match.group(5)
        else:
            print "not match"
    elif (-1 != exec_output.find("FAILED")):
        pattern = re.compile("""^.*CALL_ID\s+(\S+).*EC=(\S+).*$""", re.DOTALL)
        match = re.match(pattern, exec_output)
        if match:
            result.result  = "failed"
            result.call_id = match.group(1)
            result.error_code = match.group(2)
    return result

def create_iucs_leg_with_cac_params(ipbr_id_1, params=" ", computer="USCP-0"):
    """
     This keyword is used to create Iub leg with CACPRB parameters
     
    #COMMAND: lgutilgx RRI:USCP-0::OUT,:,,,2:34::NCAC=0

    | Parameters | Man.| Description       |
    | ipbr_id_1  | Yes | IPBR ID           |
    | params     | No  | traffic parameters used for leg creation |
    | computer   | No  | Recovery Unit specified to create leg, default is USCP-0 |

    | Return value | an instance of CommonItem |

    Example
    | result | create_iucs_leg_with_cac_params | ${IPBR_ID_1} | NCAC=0 | ${USCP-0} |
    """

    command = """lgutilgx RRI:%s::OUT,:,,,%s:34::%s""" %(computer, ipbr_id_1, params)
    print "execute command:", command
    exec_output = connections.execute_mml_without_check(command)
    result = _parse_out_leg_creation_output(exec_output)
    result.computer = computer
    return result

def release_iucs_leg(call_id, computer="USCP-0"):
    """
     This keyword is used to release iucs leg
     
    # COMMAND: lgutilgx RV:USCP-0:123:OUT

    | Parameters | Man.| Description       |
    | call_id    | Yes | IPBR ID           |
    | computer   | No  | recovery unit where the leg reserved, default is USCP-0 |

    | Return value | string "success" when the operation success |

    Example
    | result | release_iucs_leg | ${CALL_ID} | ${USCP-0} |
    """
    command = """lgutilgx RV:%s:%s:OUT""" %(computer, call_id)
    print "execute command:", command
    exec_output = connections.execute_mml_without_check(command)
    if -1 == exec_output.find("RELEASING SUCCESSFUL"):
        raise exceptions.raise_ILError("ILCommandExecuteError", exec_output)
    return "success"

def release_iub_leg(call_id, leg_id="IN", computer="USCP-0"):
    """
     This keyword is used to release iub leg
     
    #COMMAND: lgutilgx RV:<computer>:<call_id>:<leg_id>

    | Parameters | Man.| Description       |
    | call_id    | Yes | call ID           |
    | leg_id     | No  | Leg ID            |
    | computer   | No  | recovery unit where the leg reserved, default is USCP-0 |

    | Return value | an instance of CommonItem |

    Example
    | result | release_iub_leg | ${CALL_ID} | ${LEG_ID}| ${USCP-0} |
    """
    command = """lgutilgx RV:%s:%s:%s"""  % (computer, call_id, leg_id)
    exec_output = connections.execute_mml_without_check(command)
    if -1 == exec_output.find("RELEASING SUCCESSFUL"):
        raise exceptions.raise_ILError("ILCommandExecuteError", exec_output)
    return "success"

def CLI_about_iltrmcli_help_info(filter = 'true'):
    """
     This keyword is used to list all connection resource in CACPRB

    #COMMAND: iltrmcli -h

    | Parameters | Man.| Description       |
    | filter     | No  | Filter whether add the reserved, free, buffer port info into the list |

    | Return value | an instance of CommonItem |

    Example
    | result | list all conn resource info | true | 
    """
    command = "iltrmcli -h"
    print "Command:", command
    exec_output = connections.execute_mml_without_check(command)
    return _parse_conn_info(exec_output, filter)


def create_iur_leg_with_cac_params(call_id, ipbr_id, params="", computer="USCP-0"):
    """
     This keyword is used to create Iur leg with CACPRB parameters
     
    #COMMAND: lgutilgx RRI:USCP-0:7D1:IN,:,,,12,13:1::NCAC=0

    | Parameters | Man.| Description       |
    | call_id    | Yes | Call ID           |
    | ipbr_id_1  | Yes | IPBR ID           |
    | params     | No  | traffic parameters used for leg creation |
    | computer   | No  | Recovery Unit specified to create leg, default is USCP-0 |

    | Return value | an instance of CommonItem |

    Example
    | result | create_iur_leg_with_cac_params | ${Call_ID} | ${IPBR_ID_1} | NCAC=0 | ${USCP-0}|
    """
    command = """lgutilgx RRI:%s:%s:IN,:,,,%s:1::%s""" %(computer, call_id, ipbr_id, params)
    print "execute command:", command
    exec_output = connections.execute_mml_without_check(command)
    result = _parse_in_leg_creation_output(exec_output)
    result.computer = computer
    return result

def _search_vcp_connection_list_with_conn_id(conn_id):
    command = """vcp_conn_list -c 0x%s""" %(conn_id)
    exec_output = connections.execute_mml_without_check(command)
    items = exec_output.strip().splitlines()
    vcp_res = {}
    for item in items:
        infos = item.split("|")
        if len(infos) == 10:
            vcp_res = CommonItem()
            vcp_res.index = infos[0].strip()
            vcp_res.conn_id =infos[1].strip()
            vcp_res.owner_id =infos[2].strip()
            vcp_res.type =infos[3].strip()
            local_ip = infos[4].strip().split(":")
            vcp_res.local_ip=local_ip[1].strip()
            vcp_res.local_port = local_ip[2].strip()
            remote_ip =  infos[5].strip().split(":")
            vcp_res.remote_ip=remote_ip[1].strip()
            vcp_res.remote_port=remote_ip[2].strip()
    return vcp_res

def _parse_sync_compare(output):
    lines = output.splitlines()
    mo_type = ''
    diff_type = ''
    idsp_pattern = re.compile('.*\s+(?P<id>\d+)\s+(?P<name>\S+)')
    iphb_pattern = re.compile('.*\s+(?P<id>\d+)\s+(?P<name>\S+)')
    ipbr_pattern = re.compile('.*\s+(?P<id>\d+)\s+(?P<name>\S+)\s+(?P<route_bw>\d+)\s+(?P<comm_bw>\d+)\s+(?P<dcn_bw>\d+)\s+(?P<sig_bw>\d+)\s+(?P<scheculer_type>\w+)\s+(?P<mux>\w+)')
    ipbr_ada_pattern = re.compile('.*\s+(?P<id>\d+)\s+(?P<name>\S+)\s+(?P<route_bw>\d+)\s+(?P<comm_bw>\d+)\s+(?P<dcn_bw>\d+)\s+(?P<sig_bw>\d+)\s+(?P<scheculer_type>\w+)')
    ipro_vrf_pattern = re.compile('.*\s+(?P<id>\d+)\s+(?P<ip_addr>\d+\.\d+\.\d+\.\d+)\s+(?P<owner>\S+)\s+(?P<iface>\S+)\s+(?P<vrf>\S+)\s+(?P<phb_set>ALL|[ABEF1-4,]+)')
    ipro_pattern = re.compile('.*\s+(?P<id>\d+)\s+(?P<ip_addr>\d+\.\d+\.\d+\.\d+)\s+(?P<owner>\S+)\s+(?P<iface>\S+)\s+(?P<phb_set>ALL|[ABEF1-4,]+)')
    result_dict={'IDSP':{}, 'IPHB':{}, 'IPBR':{}, 'IPRO':{}, 'SUMMARY':{}}
    for line in lines:       
        if line.strip().startswith('Same:'):
            items = line.split()
            result_dict['SUMMARY']['same']={'IDSP': items[1], 'IPHB': items[2], 'IPBR':items[3], 'IPRO':items[4]}
            continue
        
        if line.strip().startswith('Different:'):
            items = line.split()
            result_dict['SUMMARY']['different']={'IDSP': items[1], 'IPHB': items[2], 'IPBR':items[3], 'IPRO':items[4]}
            continue
        
        if line.strip().startswith('IDSP'):
            mo_type = 'IDSP'
            pattern = idsp_pattern
            continue
        elif line.strip().startswith('IPHB'):
            mo_type = 'IPHB'
            pattern = iphb_pattern
            continue
        elif line.strip().startswith('IPBR') and line.strip().startswith('IPBR_ID') != 1:
            mo_type = 'IPBR'
            if (-1 != output.find("MUX_ENABLE")):
                pattern = ipbr_pattern
            else:
                pattern = ipbr_ada_pattern
            continue
        elif line.strip().startswith('IPRO'):
            mo_type = 'IPRO'
            if (-1 != output.find("VRF")):
                pattern = ipro_vrf_pattern
            else:
                pattern = ipro_pattern
            continue

        if line.strip().startswith('Difference'):
            diff_type = 'ALL'
        elif line.strip().startswith('Only in LDAP:'):
            diff_type = 'Only in LDAP'
        elif line.strip().startswith('Only in Memory:'):
            diff_type = 'Only in Memory'
        
        if mo_type == '' and diff_type == '':
            continue
            
        match = re.match(pattern, line)
        if match:  
            result = match.groupdict()
        else:
            continue
        if 'ALL' == diff_type:
            if line.find('LDAP') != -1:
                location = 'LDAP'
            elif line.find('Memory') != -1:
                location = 'Memory'
            else:
                location = 'Unkown'
        else:
            location = diff_type
        if mo_type == 'IPRO':
            key = result['id'] + ':' + result['ip_addr'] + ':' + result['owner'] + ':' + result['iface']
        else:
            key = result['id']
        if result_dict[mo_type].has_key(key):
            result_dict[mo_type][key][location] = result
        else:
            result_dict[mo_type][key]={location:result}
    pattern = re.compile("""(\S+)\s+No Difference\s+""", re.DOTALL)
    items = pattern.findall(output)
    if len(items) == 4:
           result_dict['IPRO'] = "No Difference"
           result_dict['IPBR'] = "No Difference"
           result_dict['IPHB'] = "No Difference"
           result_dict['IDSP'] = "No Difference"
    return result_dict

def search_iu_transport_info_in_tf_table(leg_info):
    """
     This keyword is used to search transport information in TF routine table
     
    #COMMAND: lgutilgx RID:USCP-0:1,2; vcp_conn_list -c 0x12345

    | Parameters     | Man.| Description       |
    | leg_info    | Yes | Iu Leg info parsed by keyword create_iucs_leg_with_cac_params      |
    
    | Return value | two instance of CommonItem, transport info in RM2 and TF table |

    Example
    | result | search_iu_transport_info_in_tf_table | ${iu_leg_info} |
    """
    command = """lgutilgx RID:%s:%s,%s""" % (leg_info.computer, leg_info.hand_id, leg_info.focus_id)
    exec_output = connections.execute_mml_without_check(command)
    pattern = re.compile("""CONNECTION\s+ID:(\S+)""")
    leg_pattern = re.compile("""RES_TYPE\s+PRID\s+ENC\s+CAC_ALLOC\s+OUT\s+IPv4\s+(\S+):(\S+)""")
    rg_pattern = re.compile("""PROVIDER\s+QNUP-(\S+)""")
    conn_id = pattern.findall(exec_output)[0]
    rg_index = rg_pattern.findall(exec_output)
    result = leg_pattern.findall(exec_output)
    rm2_info = CommonItem()
    rm2_info.ip   = result[0][0]
    rm2_info.port = result[0][1]
    eitpuptrm_list = upm_lib.class_all_units_info('QUNP')
    eitpuptrm_key = 'QNUP-000%d' % (int(rg_index[0]))
    print "QNUP key:",eitpuptrm_key
    starter_fileparse.change_ru(eitpuptrm_list[eitpuptrm_key].moname)
    vcp_info = _search_vcp_connection_list_with_conn_id(conn_id)
    
#    if (connections.execute_mml('echo $HW_PLATFORM').count('BCN') > 0):
#        ssh_eipu = 'ssh EIPU-%d' % (int(rg_index[0]))
#        connections.execute_mml(ssh_eipu)
#        for conn_id in result:
#            vcp_info = _search_vcp_connection_list_with_conn_id(conn_id)
#        connections.execute_mml('exit')
#    else:
#        vcp_info = _search_vcp_connection_list_with_conn_id(conn_id)
   
    return rm2_info, vcp_info

def release_specfied_call(call_id, computer, hand_id, focus_id):
    """
     This keyword is used to release specified call with rm2prb hand's hand id and focus id
     
    #COMMAND: lgutilgx RID:CSPU-0:123,OUT; lgutilgx RID:CSPU-0:123,IN-01

    | Parameters | Man.| Description                        |
    | call_id    | Yes | Call ID                            |
    | computer   | Yes | CP name                            |
    | hand_id    | Yes | rm2prb hand's Hand ID of the call  |
    | focus_id   | Yes | rm2prb hand's Focus ID of the call |
    
    | Return value | None |

    Example
    | release_specfied_call | call_id | computer | hand_id | focus_id |
    """
    release_flag = True
    command = """lgutilgx RID:%s:%s,%s""" % (computer, hand_id, focus_id)
    print "collect call info with command:", command
    call_info_str = connections.execute_mml_without_check(command)
    leg_pattern = re.compile("RES_TYPE\s+PRID\s+ENC\s+CAC_ALLOC\s+(\S+)")
    leg_list = leg_pattern.findall(call_info_str)
        
    for leg in leg_list:
        if leg != "OUT":
            command = "lgutilgx RV:%s:%s:%s" %(computer, call_id, leg)
            result = connections.execute_mml_without_check(command)
            if -1 == result.find("SUCCESSFUL"):
                release_flag = False
    if "OUT" in leg_list:
        command = "lgutilgx RV:%s:%s:OUT" %(computer, call_id)
        result = connections.execute_mml_without_check(command)
        if -1 == result.find("SUCCESSFUL"):
            release_flag = False
    if release_flag == False:
        raise exceptions.raise_ILError("ILCommandExecuteError", "release leg failed")
    
