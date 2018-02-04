import random
import re
from string import atoi
from string import atof

from comm.communication import connections
from comm.communication import exceptions
from comm.communication.helper import CommonItem


def send_ip_scli_command(*args):
    """This keyword is to execute a command with SCLI.

    | Parameters  | Man. | Description                                 |
    | action_type | Yes  | the action type  |

    | Return value | command execution result |

    Example
    | result | send ef scli command | p |
    """

    temp = ""
    for arg in args:
        temp += " " + arg
    command = '''fsclish -m -c "%s" ''' % (temp)
    result = connections.execute_mml_without_check(command)
    return result

def _set_ipbr_attributes_list_str(ipbr_id='', ipbr_name='', route_bw='', commit_bw='', \
                                  commit_sig_bw='', commit_dcn_bw='', ifc_nrtdch='', ifc_nrthsdpa='', \
                                  scheduler_type='', phb_profile='', dspm_profile='', mux_flag='', \
                                  max_mux_pkt_num='', mux_local_port='', mux_remote_port='', mux_udp_dscp=''):
    return ('ipbr-id ' + ipbr_id if ipbr_id else '') + \
         (' ipbr-name ' + ipbr_name if ipbr_name else '') + \
         (' route-bandwidth ' + route_bw if route_bw else '') + \
         (' committed-bandwidth ' + commit_bw if commit_bw else '') + \
         (' committed-sig-bandwidth ' + commit_sig_bw if commit_sig_bw else '') + \
         (' committed-dcn-bandwidth ' + commit_dcn_bw if commit_dcn_bw else '') + \
         (' ifc-nrtdch ' + ifc_nrtdch if ifc_nrtdch else '') + \
         (' ifc-nrthsdpa ' + ifc_nrthsdpa if ifc_nrthsdpa else '') + \
         (' scheduler-type ' + scheduler_type if scheduler_type else '') + \
         (' phb-profile-id ' + phb_profile if phb_profile else '') + \
         (' dspm-profile-id ' + dspm_profile if dspm_profile else '') + \
         (' mux-enable ' + mux_flag  if mux_flag else '') + \
         (' max-mux-packets ' + max_mux_pkt_num if max_mux_pkt_num else '') + \
         (' local-mux-port ' + mux_local_port if mux_local_port else '') + \
         (' remote-mux-port ' + mux_remote_port if mux_remote_port else '') + \
         (' mux-dscp ' + mux_udp_dscp if mux_udp_dscp else '') 

def _parse_SCLI_command_output(operation, output):
    result = {}
    if output.find('successfully') != -1:
        result['result'] = 'Success'
        result[operation] = 'Success'
        return result
        
    result[operation] = 'Fail'    
    result['result'] = 'Fail'
    
    lines=output.strip().splitlines()
    line_num = 0
    index = -1
    for line in lines:
        if line.endswith('^'):
            index = line.find('^')
            break
        line_num +=1
        
    if index == -1:
        result['error_info'] = output.strip()
        return result        
    
    command_line = lines[line_num - 1]
    position = command_line[:index].count(' ')
    items = command_line.split()
    result['error_info'] = lines[0].strip()
    result['error_param'] = items[position-1]
    result['error_value'] = items[position]

    return result
    
def add_ip_based_route(ipbr_id, ipbr_name, route_bw, commit_bw, commit_sig_bw, commit_dcn_bw, \
                       ifc_nrtdch='', ifc_nrthsdpa='', scheduler_type='', phb_profile='', \
                       dspm_profile='', mux_flag='', max_mux_pkt_num='', mux_local_port='', \
                       mux_remote_port='', mux_udp_dscp=''):
    """This keyword is to used to add an ip based route.
    #COMMAND: fsclish -c "add networking ipbr ipbr-id <ipbr_id> ipbr-name <ipbr_name> route-bandwidth <route_bw> "

    | Parameters     | Man. |               Description                       |
    | ipbr_id        | Yes  | IPBR ID                                         |
    | ipbr_name      | Yes  | IPBR_name                                       |
    | route_bw       | Yes  | route bandwidth                 |
    | commit_bw      | Yes  | committed bandwidth              |
    | commit_sig_bw  | Yes  | committed signaling bandwidth   |
    | commit_dcn_bw  | Yes  | committed DCN bandwidth         |
    | ifc_nrtdch     | No   | IFC flag(enabled,disabled), default: Enabled    |
    | ifc_nrthsdpa   | No   | Ratio for Iur/Iub+Iur, default: 100             |
    | scheduler_type | No   | scheduler type(None, VQ, RQ) default: None      |
    | phb_profile    | No   | phb profile id, default: 0                      |
    | dspm_profile   | No   | dspm profile id, default: 0                     |
    | mux_flag       | No   | specify whether enable mux function |
    | max_mux_pkt_num| No   | specify max mux packets number |
    | mux_local_port | No   | specify local mux port: range 49152~65535, default is 65535 |
    | mux_remote_port| No   | specify remote mux port: range 49152~65535, default is 65535 |
    | mux_udp_dscp   | No   | specify mux DSCP value: range 0~63, default is 46 |
    | Return value   | an instance of dictionary |

    Example
    | ${result} | add ip based route | ${ipbr_id} | ${ipbr_name} |${route_bw}|${commit_bw}| ${commit_sig_bw} | ${commit_dcn_bw} | 

${ifc_nrtdch} | ${ifc_nrthsdpa} | ${scheduler_type} | ${phb_profile} | ${dspm_profile} |
    """
    ipbr_attributes_list_str = _set_ipbr_attributes_list_str(ipbr_id, ipbr_name, route_bw, commit_bw, \
                                  commit_sig_bw, commit_dcn_bw, ifc_nrtdch, ifc_nrthsdpa, \
                                  scheduler_type, phb_profile, dspm_profile, mux_flag, \
                                  max_mux_pkt_num, mux_local_port, mux_remote_port, mux_udp_dscp)
    command = 'fsclish -c "add networking ipbr %s"' % (ipbr_attributes_list_str )

    print "Command:" , command

    output_str = connections.execute_mml_without_check(command)
 
    return _parse_SCLI_command_output('IPBR Add', output_str)
    

def del_ip_based_route(ipbr_id, ipbr_name=""):
    """
    This keyword is to used to delete an ip based route.
    
    #COMMAND: fsclish -c "delete networking ipbr ipbr-id <IPBR ID> ipbr-name <IPBR Name>"

    | Parameters  | Man. | Description      |
    | ipbr_id     | Yes  | IPBR ID          |
    | ipbr_name   | No   | IPBR Name        |

    | Return value | an instance of dictionay |

    Example
    | result | del_ip_based_route | 123 |
    """
    ipbr_attributes_list_str = _set_ipbr_attributes_list_str(ipbr_id, ipbr_name)
    command = """fsclish -c "delete networking ipbr %s" """ % (ipbr_attributes_list_str)

    output_str = connections.execute_mml_without_check(command)
    return _parse_SCLI_command_output('IPBR Delete', output_str)


def show_ip_based_route(ipbr_id="", ipbr_name=""):
    """
    This keyword is to used to show ip based route information.
    
    #COMMAND: fsclish -c "show  ipbr ipbr-id <IPBR ID> ipbr-name <IPBR Name>"

    | Parameters  | Man. | Description      |
    | ipbr_id     | No   | IPBR ID          |
    | ipbr_name   | No   | IPBR Name        |

    | Return value | an instance of dictionay |

    Example
    | result | show ip based route | 123 | ipbr-123 |
    | result | show ip based route |     |          |
    | result | show ip based route | 123 |          |
    | result | show ip based route |     | ipbr-123 |
    """
        
    ipbr_attributes_list_str  = _set_ipbr_attributes_list_str(ipbr_id=ipbr_id, ipbr_name=ipbr_name)
    command = 'fsclish -c "show networking ipbr %s"' % (ipbr_attributes_list_str)
    print "Command:", command
    output = connections.execute_mml_without_check(command)
    output = output.strip()
    if output.find('NO WORKING') != -1:
       return output
    if output.find('does not exist') != -1:
        return {'result': 'FAILED', 'error_info': output}
    if output.find('Invalid') != -1:
       return _parse_SCLI_command_output('IPBR Show', output)      
    
    if output.find('Total IPBR count:') == -1:
        lines = output.strip().splitlines()
        result = {}
        for line in lines:
            items = line.split(':')
            if len(items) != 2:
                continue
            result[items[0].strip()] = items[1].replace('kbps', '').strip()
        result['result'] = 'SUCCESS'
        return result
    else:
        items = re.findall('(\d+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\w+)\s+(\w+)', output)
        ipbr_list = {}
        for item in items:
            ipbr_info = {}
            ipbr_info['id']=item[0]
            ipbr_info['name']=item[1]
            ipbr_info['route_bw']=item[2]
            ipbr_info['cmmt_bw']=item[3]
            ipbr_info['dcn_bw']=item[4]
            ipbr_info['sig_bw']=item[5]
            ipbr_info['schedule_type']=item[6]
            ipbr_info['mux']=item[7]
            ipbr_list[ipbr_info['id']]=ipbr_info
        
        item = re.findall('Total\sIPBR\scount:\s+(\d+)', output)
        if len(item) == 1:
            ipbr_list['total'] = item[0]
            ipbr_list['Total IPBR count'] = item[0]
        ipbr_list['result'] = 'SUCCESS'
        return ipbr_list

    
def mod_ip_based_route(ipbr_id, ipbr_name='', route_bw='', commit_bw='', commit_sig_bw='', commit_dcn_bw='', \
                       ifc_nrtdch='', ifc_nrthsdpa='', scheduler_type='', phb_profile='', dspm_profile='', \
                       mux_flag='', max_mux_pkt_num='', mux_local_port='', mux_remote_port='', mux_udp_dscp=''):
    """ This keyword is used to set networking ipbr info by ipbr-id
    #COMMAND: fsclish -c "set networking ipbr ipbr-id <ipbr_id> ipbr-name <ipbr_name> route-bandwidth <route_bw> "

    | Parameters     | Man. |        Description               |
    | ipbr_id        | Yes  | IPBR ID                          |
    | ipbr_name      | No   | IPBR_name                        |
    | route_bw       | No   | route bandwidth                  |
    | commit_bw      | No   | committed bandwidth              |
    | commit_sig_bw  | No   | committed signaling bandwidth    |
    | commit_dcn_bw  | No   | committed DCN bandwidth          |
    | ifc_flag       | No   | IFC flag(enabled,disabled)       |
    | ratio          | No   | Ratio for Iur/Iub+Iur            |
    | scheduler_type | No   | scheduler type(None, VQ, RQ)     |
    | phb_profile    | No   | phb profile id                   |
    | dspm_profile   | No   | dspm profile id                  |
    | mux_flag       | No   | specify whether enable mux function |
    | max_mux_pkt_num| No   | specify max mux packets number |
    | mux_local_port | No   | specify local mux port: range 49152~65535, default is 65535 |
    | mux_remote_port| No   | specify remote mux port: range 49152~65535, default is 65535 |
    | mux_udp_dscp   | No   | specify mux DSCP value: range 0~63, default is 46 |
    | Return value   | instance of dictionary |

    Example
    | result | mod_ip_based_route | 123 | bts-1 | 123124 |

    """
    ipbr_attributes_list_str = _set_ipbr_attributes_list_str(ipbr_id, ipbr_name, route_bw, commit_bw, \
                                  commit_sig_bw, commit_dcn_bw, ifc_nrtdch, ifc_nrthsdpa, \
                                  scheduler_type, phb_profile, dspm_profile, mux_flag, \
                                  max_mux_pkt_num, mux_local_port, mux_remote_port, mux_udp_dscp)
 

    command = 'fsclish -c "set networking ipbr %s"' % (ipbr_attributes_list_str)
    print "Command:", command

    output_str = connections.execute_mml_without_check(command)
    return _parse_SCLI_command_output('IPBR Modify', output_str)

def add_ip_based_route_with_specified_parameters(ipbr_id, *args):
    """ This keyword is used to add ip based route with attribute string description
    #COMMAND: fsclish -c "add networking ipbr ipbr-id <ipbr_id> ipbr-name <ipbr_name> route-bandwidth <route_bw> "

    | Parameters     | Man. |        Description                                    |
    | ipbr_id        | Yes  | IPBR ID                                               |
    | args           | No   | list of the ipbr attribute string: e.g. ipbr-name=xxx |
    | Return value   | instance of dictionary |

    Example
    | result | add_ip_based_route_with_specified_parameters | ${ipbr_id} | ipbr-name=bts1 |

    """
    command = "add networking ipbr ipbr-id %s" % (ipbr_id)
    for arg in args:
        items = arg.split("=")
        command = command + " " + items[0].strip() + " " + items[1].strip()
    command = """fsclish -c "%s" """ % (command)
    print "Command:", command
    output = connections.execute_mml_without_check(command)
    return _parse_SCLI_command_output('IPBR Add', output)

def set_ip_based_route_with_specified_parameters(ipbr_id, *args):
    """ This keyword is used to set ip based route attributes with attribute string description
    #COMMAND: fsclish -c "add networking ipbr ipbr-id <ipbr_id> ipbr-name <ipbr_name> route-bandwidth <route_bw> "

    | Parameters     | Man. |        Description                                    |
    | ipbr_id        | Yes  | IPBR ID                                               |
    | args           | No   | list of the ipbr attribute string: e.g. ipbr-name=xxx |
    | Return value   | instance of dictionary |

    Example
    | result | set_ip_based_route_with_specified_parameters | ${ipbr_id} | ipbr-name=bts1 |

    """
    command = "set networking ipbr ipbr-id %s" % (ipbr_id)
    for arg in args:
        items = arg.split("=")
        command = command + " " + items[0].strip() + " " + items[1].strip()
    command = """fsclish -c "%s" """ % (command)
    print "Command:", command
    output = connections.execute_mml_without_check(command)
    return _parse_SCLI_command_output('IPBR Modify', output)


def _set_ipro_attributes_list_str(ipbr_id='', ip_address='', owner='', iface='', phb_set='', vrf='', mode=''):
    return  ('ipbr-id ' + ipbr_id if ipbr_id else '') + \
            (' owner ' + owner if owner else '') + \
            (' ip-address ' + ip_address if ip_address else '') + \
            (' iface ' + iface if iface else '') + \
            (' phb-set ' + phb_set if phb_set else '') + \
            (' vrf ' + vrf if vrf else '')+\
            (' mode ' + mode if mode else '' )


    
         
def add_ipro(ipbr_id, ip_address, owner, iface, phb_set='', vrf='', mode=''):
    """
    This keyword is to used to add networking ipro .
    #COMMAND: fsclish -c "add networking ipro ipbr-id <ipbr id> iface <interface> ip-address <ip address> owner <recovery group> mode <add mode>"

    | Parameters  | Man. | Description                                 |
    | ipbr_id     | Yes  | IPBR ID                                     |
    | ip_address  | Yes  | IP address                                  |
    | owner       | Yes  | the Owner Recovery Group for the IP Address |
    | iface       | Yes  | the Interface for the IP Address            |
    | phb_set     | No   | PHB class setting for the IPRO              |
    | vrf         | No   | virtual routing and fowarding instance name |

    | Return value | instance of dictionary |

    Example
    | result | add_ipro | 123 | 12.0.0.1 | /EITPUPTRMRG | ether1_1 | 
    """
    ipro_attributes_list_str = _set_ipro_attributes_list_str(ipbr_id=ipbr_id, ip_address=ip_address, owner=owner, iface=iface, vrf=vrf, phb_set=phb_set,mode=mode)
    command = 'fsclish -c "add networking ipro %s"' % (ipro_attributes_list_str)
    print "Command:", command
    result = connections.execute_mml_without_check(command)
    return _parse_SCLI_command_output('IPRO Add', result)

def modify_ipro(ipbr_id, ip_address, owner, iface, phb_set='', vrf=''):
    """
    This keyword is to used to modify ipro .
    #COMMAND: fsclish -c "set networking ipro ipbr-id <ipbr id> iface <interface> ip-address <ip address> owner <recovery group>"

    | Parameters  | Man. | Description |
    | ipbr_id     | Yes  | IPBR ID    |
    | ip_address  | Yes  | IP address |
    | owner       | Yes  | the Owner Recovery Group for the IP Address |
    | iface       | Yes  | the Interface for the IP Address |
    | phb         | No   | PHB Class Setting for the IPRO   |
     
    | Return value | instance of dictionary |

    Example
    | result | modify_ipro | 123 | 12.0.0.1 | /EITPUPTRMRG | ether1_1 | 
    """
    ipro_attributes_list_str = _set_ipro_attributes_list_str(ipbr_id=ipbr_id, ip_address=ip_address, owner=owner, iface=iface, phb_set=phb_set)
    command = 'fsclish -c "set networking ipro %s"' % (ipro_attributes_list_str)
    print "Command:", command
    result = connections.execute_mml_without_check(command)
    return _parse_SCLI_command_output('IPRO Modify', result)

def delete_ipro(ipbr_id, ip_address, owner, iface, del_mode=''):
    """
    This keyword is used to unbind IPBR and IP Address
    #COMMAND: fsclish -c "delete networking ipro ipbr-id <ipbr id> iface <interface> ip-address <ip address> owner <owner recovery group> mode <delete mode>"
    
    | Parameters  | Man. | Description |
    | ipbr_id     | Yes  | IPBR ID    |
    | ip_addr     | Yes  | IP address | 
    | owner       | Yes  | owner recovery group |    
    | iface       | Yes  | network interface |    
    | del_mode    | no  | IPRO delete mode, default is normal|    
      
    | Return value | instance of dictionary |
    
    | ${result} | delete networking ipro | 123 | 12.0.0.1 | /EITPUPTRMRG | ether1_1 | normal | 
    """
    ipro_attributes_list_str = _set_ipro_attributes_list_str(ipbr_id=ipbr_id, ip_address=ip_address, owner=owner, iface=iface, mode=del_mode)
    command = 'fsclish -c "delete networking ipro %s"' % (ipro_attributes_list_str)
    print "Command:", command
    result = connections.execute_mml_without_check(command)
    return _parse_SCLI_command_output('IPRO Delete', result)

def show_ipro(ipbr_id='', ip_address='', owner='',  iface='',  vrf=''):
    """
    This keyword is used to show networking ipros
    #COMMAND: fsclish -c "show networking ipro ipbr-id <ipbr id> iface <interface> ip-address <ip address> owner <owner recovery group>"
    
    | Parameters  | Man. | Description             |
    | owner       | No   | owner recovery group    |  
    | ipbr_id     | No   | IPBR ID                 |
    | iface       | No   | network interface |    
    | ip_addr     | No   | IP address        |
     
    | Return value | instance of dictionary |
    
    | ${result} | show networking ipro | 123 | 12.0.0.1 | /EITPUPTRMRG | ether1_1 | VRF | 
    """
   
    ipro_attributes_list_str = _set_ipro_attributes_list_str(ipbr_id=ipbr_id, vrf=vrf, ip_address=ip_address, owner=owner, iface=iface)
    command = 'fsclish -c "show networking ipro %s"' % (ipro_attributes_list_str)
    print "Execute Command:", command
    ipro_info_str = connections.execute_mml_without_check(command)
    if ipro_info_str.upper().find('VRF') != -1:
        pattern = re.compile('(\d+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)')
    else:
        pattern = re.compile('(\d+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+')
    items = pattern.findall(ipro_info_str)
    if len(items) == 0:
        return {'result': 'FAILED', 'error_info': ipro_info_str.strip()}
 
    ipro_list = {'result': 'SUCCESS'}
    for item in items:
        ipro_info = CommonItem()
        ipro_info.ipbr_id = item[0]
        ipro_info.ip_address = item[1]
        ipro_info.owner = item[2]
        ipro_info.iface = item[3]
        ipro_info.phb_set = CommonItem()
        if item[4].find('ALL') != -1:
            ipro_info.phb_set.ef = 'on' 
            ipro_info.phb_set.af4 = 'on'
            ipro_info.phb_set.af3 = 'on'
            ipro_info.phb_set.af2 = 'on' 
            ipro_info.phb_set.af1 = 'on' 
            ipro_info.phb_set.be = 'on' 
        else:
           ipro_info.phb_set.ef = 'on' if item[4].find('EF') != -1 else 'off'
           ipro_info.phb_set.af4 = 'on' if item[4].find('AF4') != -1 else 'off'
           ipro_info.phb_set.af3 = 'on' if item[4].find('AF3') != -1 else 'off'
           ipro_info.phb_set.af2 = 'on' if item[4].find('AF2') != -1 else 'off'
           ipro_info.phb_set.af1 = 'on' if item[4].find('AF1') != -1 else 'off'
           ipro_info.phb_set.be = 'on' if item[4].find('BE') != -1 else 'off'
        if ipro_info_str.upper().find('VRF') != -1:
            ipro_info.vrf = item[5]
        ipro_key = ipro_info.ipbr_id + "@" + ipro_info.ip_address + "@" + ipro_info.iface + "@" + ipro_info.owner
        ipro_list[ipro_key] = ipro_info
    
    return ipro_list

def release_ipro_with_specified_ipbr_id(ipbr_id):
    """
    This keyword is used to release all IPROs with specified IPBR ID
    #COMMAND: fsclish -c "show networking ipro ipbr-id <ipbr id>" ; fsclish -c "delete networking ipro ipbr-id <ipbr id> iface <interface> ip-address <ip address> owner <owner recovery group> mode <delete mode>"
              
    
    | Parameters  | Man. | Description             |
    | ipbr_id     | Yes  | IPBR ID                 |
     
    | Return value | instance of dictionary |
    
    | ${result} | release_ipro_with_specified_ipbr_id | 123 |
    """
        
    ipro_list = show_ipro(ipbr_id=ipbr_id)
    print ipro_list
    if len(ipro_list) == 0:
        return True
        
    final_result = True
    for ipro in ipro_list.keys():
        if ipro in ['result', 'error_info']:
            continue
        result = delete_ipro(ipro_list[ipro].ipbr_id, ipro_list[ipro].ip_address, ipro_list[ipro].owner, ipro_list[ipro].iface, "forced")
        final_result = final_result and (result['IPRO Delete'].lower() == 'success')
    return final_result 

def add_ip_address(recovery_group, iface, ipaddress, vrfname=''):
    """
    This keyword is to used to add an ip address.
    
    #COMMAND: fsipaddress dedicated add <ip address> iface <interface> owner <recovery group>

    | Parameters         | Man. | Description  |
    | recovery_group     | Yes  | IPBR ID    |
    | ipaddress          | Yes  | IP address |
    | iface              | Yes  | network interface |

    | Return value | command execution result |

    Example
    | result | Add IP Address | /IL_CSCP | ether1_1 | 12.0.0.1 |
    """
    if vrfname != '':
        vrfinfo = "instance" + ' ' + vrfname
    else:
        vrfinfo = vrfname
    command = """fsclish -m -c "add networking %s address dedicated %s iface %s ip-address %s" """ % (vrfinfo, recovery_group, iface, ipaddress)
    print "Command: " + command

    result = connections.execute_mml_without_check(command)
    if (-1 != result.lower().find("failed")):
        return_value = "failed"
    else:
        return_value = "successfully"
    return return_value
    
def add_ip_address_modify(owner, rg_name, iface, ipaddress, vrfname = ''):
    """
    This keyword is to used to add an ip address.
    
    #COMMAND: fsipaddress dedicated add <ip address> iface <interface> owner <recovery group>

    | Parameters         | Man. | Description       |
    | owner              | Yes  | owner name        |
    | rg_name            | Yes  | rg name           |
    | ipaddress          | Yes  | IP address        |
    | iface              | Yes  | network interface |
    | vrf                | No   | vrf name          |

    | Return value | command execution result |

    Example
    | result | Add IP Address modify | /EIPU-0 | /QNCL-0 | 12.0.0.1 | 10 |
    """
    if vrfname != '':
        vrfinfo = "instance" + ' ' + vrfname
    else:
        vrfinfo = vrfname
    command = """fsclish -m -c "add networking %s address %s user %s iface %s ip-address %s" """ % (vrfinfo, owner, rg_name, iface, ipaddress)
    print "Command: " + command

    result = connections.execute_mml_without_check(command)
    if (-1 != result.lower().find("failed")):
        return_value = "failed"
    else:
        return_value = "successfully"
    return return_value

def show_ip_address(ipaddress):
    """
    This keyword is used to show the ip address in SCLI
    
    #COMMAND: fsclish -c "show show networking address ip-address <ip_addr>"

    | Parameters   | Man. | Description       |
    | ipaddress    | Yes  | IP address        |


    | Return value | command execution result |

    Example
    | result | show_ip_address  | 12.0.0.1 |
    """
    command = """fsclish -c "show networking address ip-address %s" """ % (ipaddress)
    print "Command: " + command
    output = connections.execute_mml_without_check(command)

    if output == "" or output == " ":
        exceptions.raise_ILError("ILCommandExecuteError", "ip address infomation doesn't exist")
    if output.find("type") != -1:
        pattern = re.compile("""\s+IP addresses in\s+\S+\s+instance:\s+(?P<inface>\S+)\s+type\s+:\s+(?P<type>\S+)\s+address\s+:\s+(?P<address>\S+)\s+owner\s+:\s+(?P<owner>\S+)\s+$""")
    else:
        pattern = re.compile("""\s+IP addresses in\s+\S+\s+instance:\s+(?P<inface>\S+)\s+address\s+:\s+(?P<address>\S+)\s+owner\s+:\s+(?P<owner>\S+)\s+$""")
    match = re.match(pattern, output)

    if match:
        return match.groupdict()
    else:
        print "not match"
        exceptions.raise_ILError("ILCommandExecuteError", "ip address infomation doesn't exist")

    return {}

def delete_ip_address(recovery_group, iface, ipaddress, vrfname = ''):
    """
    This keyword is to used to remove an ip address.
    
    #COMMAND: fsipaddress dedicated delete <ip address> iface <interface> owner <recovery group>
    
    | Parameters         | Man. | Description                                 |
    | recovery_group     | Yes  | recovery group name |
    | ipaddress          | Yes  | IP address |
    | iface              | Yes  | network interface |
    | vrf                | No   | vrf name          |

    | Return value | command execution result |

    Example
    | result | delete_ip_address | /IL_CSCP | ether1_1 | 12.0.0.1 |
    """
    if vrfname != '':
        vrfinfo = "instance" + ' ' + vrfname
    else:
        vrfinfo = vrfname
    command = """fsclish -m -c "delete networking %s address dedicated %s iface %s ip-address %s" """ % (vrfinfo, recovery_group, iface, ipaddress)
    print "Command: " + command

    result = connections.execute_mml_without_check(command)
    if (-1 != result.lower().find("failed")):
        return_value = result
    else:
        return_value = "successfully"
    return return_value

def get_GCU_info():
    """    
    This keyword is used to basic ipbr config information from CAC PRB
    #COMMAND: ilfunitcli -lx
    
    | Parameters         | Man. | Description   |
    | None               |      |               |
    
    | Return value | String |
    
    Example
    | result | get_GCU_info |  | 
    """
    command = 'ilfunitcli -lx'
    print "Command:", command
    output = connections.execute_mml_without_check(command)
    pattern = re.compile(r'\s*GCU-1\s+\S+\s+\S+\s+\S+\s+\S+\s+(\S+)', re.S)
    result = re.findall(pattern, output)
    result1 = result[0]
    print result
    print result1
    return result1

def get_ipbr_measurement_result(report_file):
    
    command = 'cat %s' % (report_file)
    print "Command:", command
    output = connections.execute_mml_without_check(command)
    pattern = re.compile(r'\s*<PMMOResult>\s+<MO>\s+<DN>\S+\-(\d+)</DN>\s+</MO>\s+<PMTarget\s+\S+>\s+<M568C0>(\d+)</M568C0>\s+<M568C1>(\d+)</M568C1>\s+<M568C2>(\d+)</M568C2>\s+<M568C3>(\d+)</M568C3>\s+<M568C4>(\d+)</M568C4>\s+<M568C5>(\d+)</M568C5>\s+<M568C6>(\d+)</M568C6>\s+<M568C7>(\d+)</M568C7>\s+<M568C8>(\d+)</M568C8>\s+<M568C9>(\d+)</M568C9>\s+<M568C10>(\d+)</M568C10>\s+<M568C11>(\d+)</M568C11>\s+<M568C12>(\d+)</M568C12>\s+<M568C13>(\d+)</M568C13>\s+<M568C14>(\d+)</M568C14>\s+<M568C15>(\d+)</M568C15>\s+<M568C16>(\d+)</M568C16>\s+<M568C17>(\d+)</M568C17>\s+<M568C18>(\d+)</M568C18>\s+<M568C19>(\d+)</M568C19>\s+<M568C20>(\d+)</M568C20>\s+<M568C21>(\d+)</M568C21>\s+<M568C22>(\d+)</M568C22>\s+</PMTarget>\s+</PMMOResult>', re.S)
    #pattern = re.compile(r'\s*<PMMOResult>\s+<MO>\s+<DN>\S+</DN>\s+</MO>\s+<PMTarget\s\S+\s+<M568C0>\d+</M568C0>\s+<M568C1>\d+</M568C1>\s+<M568C2>\d+</M568C2>\s+<M568C3>\d+</M568C3>\s+<M568C4>\d+</M568C4>\s+<M568C5>\d+</M568C5>\s+<M568C6>\d+</M568C6>\s+<M568C7>\d+</M568C7>\s+<M568C8>\d+</M568C8>\s+<M568C9>\d+</M568C9>\s+', re.S)
    result = re.findall(pattern, output)
    result_dict = {}
    for item in result:
        result_dict[item[0]] = {'M568C0':item[1], 'M568C1':item[2], 'M568C2':item[3], 'M568C3':item[4], 'M568C4':item[5], 'M568C5':item[6], 'M568C6':item[7], 'M568C7':item[8], 'M568C8':item[9], 'M568C9':item[10]}
    return result_dict

def delete_ip_based_route_resource_with_ipbr_id(ipbr_id):
    """    
    This keyword is used to release IPBR and IPRO based on it
    #COMMAND: 
    
    fsclish -c "show networking ipbr ipbr-id <ipbr id>"; 
    fsclish -c "show networking ipro ipbr-id";  
    fsclish -c "delete networking ipro ipbr-id <ipbr id> iface <interface> ip-address <ip address> owner <owner recovery group> mode <delete mode>"
    fsclish -c "delete networking ipbr ipbr-id"; 
    
    | Parameters  | Man. | Description                                              |
    | ipbr_id     | Yes  | IPBR ID    |
    | ip_addr     | Yes  | IP address | 
    | owner       | Yes  | owner recovery group |    
    | iface       | Yes  | network interface |    
    | filters     | Yes  | IPRO attributes list with IPRO which is not mandatory: vrf, phb-set, mode    |

    | Return value | Boolean |

    Example
    | result | delete_ip_based_route_resource_with_ipbr_id | 1 | 
    """   
    result = True
    ipbr_info = show_ip_based_route(ipbr_id=ipbr_id)
    if ipbr_info == None:
        return result
    result = release_ipro_with_specified_ipbr_id(ipbr_id)
    if result != True:
        return result
            
    result = del_ip_based_route(ipbr_id)
    return result
    
def add_ipro_with_specified_parameters(ipbr_id, ip_address, owner, iface, *args):
    """    
    This keyword is used to add networking ipro info with specified attributes which is not mandatory
    #COMMAND: fsclish -c "show networking ipro ipbr-id <ipbr id> iface <interface> ip-address <ip address> owner <owner recovery group> vrf <vrf name>"
    | Parameters  | Man. | Description                                              |
    | ipbr_id     | Yes  | IPBR ID    |
    | ip_addr     | Yes  | IP address | 
    | owner       | Yes  | owner recovery group |    
    | iface       | Yes  | network interface |    
    | filters     | Yes  | IPRO attributes list with IPRO which is not mandatory: vrf, phb-set, mode    |

    | Return value | an Instance of list with common item element instance |

    Example
    | result | list_ipro_with_filter | ipbr-id=1 | owner=/EITPUPTRMRG |
    """
    command = "add networking ipro ipbr-id %s iface %s ip-address %s owner %s" % (ipbr_id, iface, ip_address, owner)
    for arg in args:
        items = arg.split("=")
        command = command + " " + items[0].strip() + " " + items[1].strip()
    command = """fsclish -c "%s" """ % (command)
    print "Command:", command
    output = connections.execute_mml_without_check(command)
    return _parse_SCLI_command_output('IPRO Add', output)          

def list_ipro_with_filter(*filters):
    """    
    This keyword is used to list IPRO info with specified filters
    #COMMAND: fsclish -c "show networking ipro ipbr-id <ipbr id> iface <interface> ip-address <ip address> owner <owner recovery group> vrf <vrf name>"
    
    | Parameters          | Man. | Description                                              |
    | filters             | Yes  | arg filter list with IPRO attributes which sepcified: iface, ip-address, ipbr-id, owner, vrf     |

    | Return value | an Instance of list with common item element instance |

    Example
    | result | list_ipro_with_filter | ipbr-id=1 | owner=/EITPUPTRMRG |
    """
    param_dict = {'iface':'', 'ip-address':'', 'ipbr-id':'', 'owner':'', 'vrf':''}
    for item in filters:
        items = item.split("=")
        param_dict[items[0].strip()] = items[1].strip()
    return show_ipro(owner=param_dict['owner'], ipbr_id=param_dict['ipbr-id'], 
                     iface=param_dict['iface'], ip_address=param_dict['ip-address'], 
                     vrf=param_dict['vrf'])


def _get_available_ip_with_sepcified_recovery_group_type(rg_type):
    command = 'fsclish -c "show networking instance default address"'
    output = connections.execute_mml_without_check(command)
    if output.find('type') != -1:
        ip_addr_pattern_str = "(\w+)\s+type\s+:\s+(\w+)\s+address\s+:\s+(\d+.\d+.\d+.\d+)/(\d+)\s+owner\s+:\s+(\S+)"
        iface_index = 0
        addr_index = 2
        owner_index =4
    else:
        ip_addr_pattern_str = "(\w+)\s+address\s+:\s+(\d+.\d+.\d+.\d+)/(\d+)\s+owner\s+:\s+(\S+)"
        iface_index = 0
        addr_index = 1
        owner_index = 3
        
    ip_addr_list = re.findall(ip_addr_pattern_str, output)
    eitp_ip_list = []
    for ip_info in ip_addr_list:
        
        if ip_info[addr_index].startswith('169.254'):
            continue
        
        if -1 == ip_info[owner_index].find(rg_type):
            continue
        temp_items = ip_info[owner_index].split('-')
        
        if len(temp_items) == 1:
            index = 0
        else:
            index = atoi(temp_items[1])
            
        if index >= len(eitp_ip_list):
            for i in range(len(eitp_ip_list), index + 1):
                eitp_ip_list.append([])
        ip_content = CommonItem()
        ip_content.rg_name = ip_info[owner_index]
        ip_content.ip_addr = ip_info[addr_index] 
        ip_content.iface = ip_info[iface_index]
        eitp_ip_list[index].append(ip_content)

    return eitp_ip_list

def select_different_IP_address_in_different_recovery_group(ip_addr_num_str):
    """    
    This keyword is used to select ip addresses from different recovery groups randomly
    #COMMAND: fsclish -c "show networking instance default address"
    | Parameters          | Man. | Description                                 |
    | ip_addr_num_str     | Yes  | the number of IP addresses which needed     |

    | Return value | an Instance of list with common item element instance |

    Example
    | result | select_different_IP_address_in_different_recovery_group | 5 |
    """
    
    eitp_ip_list = _get_available_ip_with_sepcified_recovery_group_type('QNUP')
    ip_addr_num = atoi(ip_addr_num_str)
    
    if len(eitp_ip_list) < ip_addr_num:
        exceptions.raise_ILError("ILOutputParseError", "Not enough QNUP to provide IP Address with requirement")
    
    random.shuffle(eitp_ip_list)
    temp_eitp_ip_list = []
    for info in eitp_ip_list[0:ip_addr_num]:
        random.shuffle(info)
        temp_eitp_ip_list.append(info[0])
    return temp_eitp_ip_list

def select_different_IP_address_in_same_recovery_group(ip_addr_num_str):
    """    
    This keyword is used to select ip addresses from same recovery group randomly
    #COMMAND: fsclish -c "show networking instance default address"
    | Parameters          | Man. | Description                                 |
    | ip_addr_num_str     | Yes  | the number of IP addresses which needed     |

    | Return value | an Instance of list with common item element instance |

    Example
    | result | select_different_IP_address_in_same_recovery_group | 5 |
    """
    eitp_ip_list = _get_available_ip_with_sepcified_recovery_group_type('QNUP')
    ip_addr_num = atoi(ip_addr_num_str)
    random.shuffle(eitp_ip_list)
    for list_item in eitp_ip_list:
        if len(list_item) < ip_addr_num:
            continue
        random.shuffle(list_item)
        return list_item[0:ip_addr_num] 
    exceptions.raise_ILError("ILOutputParseError", "Not enough IP Address with requirement")

def select_random_IP_address_and_recovery_group(ip_addr_num_str):
    """    
    This keyword is used to select ip addresses randomly
    #COMMAND: fsclish -c "show networking instance default address"
    | Parameters          | Man. | Description                                 |
    | ip_addr_num_str     | Yes  | the number of IP addresses which needed     |

     | Return value | an Instance of list with common item element instance |

    Example
    | result | select_random_IP_address_and_recovery_group | 5 |
    """    
    eitp_ip_pool = []
    ip_addr_num = atoi(ip_addr_num_str)
    
    eitp_ip_list = _get_available_ip_with_sepcified_recovery_group_type('QNUP')
    for list_item in eitp_ip_list:
        eitp_ip_pool.extend(list_item)
    
    if len(eitp_ip_pool) < ip_addr_num:
        exceptions.raise_ILError("ILOutputParseError", "Not enough IP Address with requirement")
    
    random.shuffle(eitp_ip_pool)
    return eitp_ip_pool[0:ip_addr_num]

def select_random_IP_address_and_recovery_group_ADA(ip_addr_num_str):
    """    
    This keyword is used to select ip addresses randomly in ADA environment
    #COMMAND: fsclish -c "show networking instance default address"
    | Parameters          | Man. | Description                                 |
    | ip_addr_num_str     | Yes  | the number of IP addresses which needed     |

     | Return value | an Instance of list with common item element instance |

    Example
    | result | select_random_IP_address_and_recovery_group | 5 |
    """    
    eitp_ip_pool = []
    ip_addr_num = atoi(ip_addr_num_str)
    
    eitp_ip_list = _get_available_ip_with_sepcified_recovery_group_type('GFCP')
    for list_item in eitp_ip_list:
        eitp_ip_pool.extend(list_item)
    
    if len(eitp_ip_pool) < ip_addr_num:
        exceptions.raise_ILError("ILOutputParseError", "Not enough IP Address with requirement")
    
    random.shuffle(eitp_ip_pool)
    return eitp_ip_pool[0:ip_addr_num]
