import random
import re
from string import atoi
from string import atof

from comm.communication import connections
from comm.communication import exceptions
from comm.communication.helper import CommonItem
from il_caclib import inquiry_udp_conn_resource_info

def get_ipbr_resource_info(ipbr_id):
    """    
    This keyword is used to get ipbr resource information from CAC PRB
    
    #COMMAND: iltrmcli -S -i<IPBR ID>
    
    | Parameters         | Man. | Description                                 |
    | ipbr_id            | Yes  | IPBR ID                                     |

    | Return value | an Instance of commonitem |

    Example
    | result | get_ipbr_resource_info | 12 |
    """
    command = "iltrmcli -S -i%s" % (ipbr_id)
    print "Command: " + command
    output = connections.execute_mml_without_check(command)
    if output.find('does not exist') != -1:
        output = 'IPBR with ipbr-id does not exist.'
        return output
    else:
        pattern = re.compile('''^.*
IPBR\sID\s+:\s+(?P<ipbr_id>\d+)\s+
IPBR\sname\s+:\s+(?P<ipbr_name>\S+)\s+
Route\sbandwidth\s+:\s(?P<route_bw>\d+)\s+kbps\s+
Committed\sbandwidth\s+:\s(?P<cmmt_bw_orig>\d+)\s+kbps\s+
Committed\sDCN\sbandwidth\s+:\s(?P<cmmt_dcn_bw>\d+)\s+kbps\s+
Committed\ssignaling\sbandwidth\s+:\s(?P<cmmt_sig_bw>\d+)\s+kbps\s+
Committed\suser\splane\sbandwidth\s+:\s(?P<up_bw>\d+)\s+kbps\s+
Reserved\sbandwidth\s+:\s(?P<res_bw>\S+)\s+kbps\s+
IFC\sNRTDCH\s+:\s+(?P<ifc_nrtdch>\S+)\s+
IFC\sNRTHSDPA\s+:\s+(?P<ifc_nrthsdpa>\S+)\s+
Scheduler\stype\s+:\s+(?P<scheduler_type>\S+)\s+ 
PHB\sprofile\sID\s+:\s+(?P<phb_profile>\d+)\s+
DSPM\sprofile\sID\s+:\s+(?P<dspm_profile>\d+)\s+
MUX\senable\s+:\s+(?P<mux_enable>\S+)\s+
Max\sMUX\spackets\snumber\s+:\s+(?P<max_mux_packet>\d+)\s+
Local\sMUX\sUDP\sport\s+:\s+(?P<local_mux_port>\d+)\s+
Remote\sMUX\sUDP\sport\s+:\s+(?P<remote_mux_port>\d+)\s+
MUX\sUDP\sDSCP\svalue\s+:\s+(?P<mux_udp_value>\d+)\s+ 
GTP\sleg\snumber\s+:\s+(?P<gtp_num>\d+)\s+
RTP\sleg\snumber\s+:\s+(?P<rtp_num>\d+)\s+
UDP\sleg\snumber\s+:\s+(?P<udp_num>\d+)\s+
IPBR\sstatus\s+:\s((?P<ipbr_status>\S+)\s+)
''', re.VERBOSE|re.DOTALL)
        item = pattern.match(output)
        ipbr_info = CommonItem()
        if item:
           ipbr_attr = item.groupdict()
           ipbr_info.ipbr_id = ipbr_attr['ipbr_id']
           ipbr_info.ipbr_name = ipbr_attr['ipbr_name']
           ipbr_info.route_bw = ipbr_attr['route_bw'] 
           ipbr_info.cmmt_bw_orig = ipbr_attr['cmmt_bw_orig'] 
           ipbr_info.cmmt_dcn_bw = ipbr_attr['cmmt_dcn_bw']
           ipbr_info.cmmt_sig_bw = ipbr_attr['cmmt_sig_bw']  
           ipbr_info.ifc_nrtdch = ipbr_attr['ifc_nrtdch'] 
           ipbr_info.ifc_nrthsdpa = ipbr_attr['ifc_nrthsdpa'] 
           ipbr_info.scheduler_type = ipbr_attr['scheduler_type'] 
           ipbr_info.phb_profile = ipbr_attr['phb_profile'] 
           ipbr_info.dspm_profile = ipbr_attr['dspm_profile'] 
           ipbr_info.mux_enable = ipbr_attr['mux_enable'] 
           ipbr_info.max_mux_packet = ipbr_attr['max_mux_packet'] 
           ipbr_info.local_mux_port = ipbr_attr['local_mux_port'] 
           ipbr_info.mux_udp_value = ipbr_attr['mux_udp_value']
           ipbr_info.cmmt_bw = "%d" % (atof(ipbr_attr['up_bw'])*1000) 
           ipbr_info.res_bw = "%d" % (atof(ipbr_attr['res_bw'])*1000)
           ipbr_info.free_bw = "%d" % (atof(ipbr_info.cmmt_bw) - atof(ipbr_info.res_bw))
           ipbr_info.gtp_num = ipbr_attr['gtp_num'] 
           ipbr_info.rtp_num = ipbr_attr['rtp_num'] 
           ipbr_info.udp_num = ipbr_attr['udp_num'] 
           ipbr_info.status = ipbr_attr['ipbr_status'] 
           ipbr_info.ip_list = []
        else:
           return ipbr_info
           
        if output.find('No IP address bound with the IPBR.') != -1:
           ipbr_info.ip_list  = 'No IP address bound with the IPBR.'
        else:
           vrf_enable = False
           if output.find('VRF ID') != -1:
                ip_pattern = re.compile('(\d+\.\d+\.\d+\.\d+)\s+(\d+)\s+(\S+)\s+(\S+)')
                vrf_enable = True
           else:
                ip_pattern = re.compile('(\d+\.\d+\.\d+\.\d+)\s+(\S+)\s+(\S+)')
           items = ip_pattern.findall(output)
           for item in items:
               ip_info = CommonItem()
               ip_info.ip_addr = item[0]
               ip_info.monitor = item[-2]
               ip_info.status = item[-1]
               if vrf_enable:
                   ip_info.vrf_id = item[1]
               ipbr_info.ip_list.append(ip_info)
                   
    return ipbr_info



def get_leg_cac_info(ip_addr, port_id):
    """    
    This keyword is used to basic ipbr config information from CAC PRB
    #COMMAND: iltrmcli -S -u <IP Address> <Port ID>
    | Parameters         | Man. | Description   |
    | ip_addr            | Yes  | IP address    |
    | port_id            | Yes  | port ID       |

    | Return value | an Instance of commonitem |

    Example
    | result | Get Leg CAC Info | 10.1.2.4 | 4000 |
    """

    result = inquiry_udp_conn_resource_info(ip_addr, port_id)
    ip_port = '%s:%s' % (ip_addr, port_id)
    return_var = CommonItem()
    if result.has_key(ip_port):
        return_var.port = port_id
        return_var.ipbr_id = result[ip_port]["ipbr_id"]
        return_var.bw = result[ip_port]["reserve_bw"]
    return return_var

def get_counters_in_cac():
    """    
    This keyword is used to shows counters in CAC part.
    #COMMAND: fsclish -c "show troubleshooting cac leg"
    | Parameters          | Man. | Description                                 |
    | NA                  |      |                                             |

    | Return value | an Instance of list with legs number and capacity         |

    Example
    | result | get_couters_in_cac  |  |
    """
    command = """fsclish -c "show troubleshooting cac leg" """ 
    print "Command: " + command
    output = connections.execute_mml_without_check(command)
    pattern = re.compile('''^.*
UDP\sleg\s:\s+(?P<udp_num>\d+)\s+
RTP\sleg\s:\s+(?P<rtp_num>\d+)\s+
GTP\sleg\s:\s+(?P<gtp_num>\d+)\s+
Capacities:\s+
UDP\sand\s+RTP\s+leg\s+:\s+(?P<udp_rtp_leg_capacity>\d+)\s+
GTP\sleg\s+:\s+(?P<gtp_leg_capacity>\d+)\s+
''', re.VERBOSE|re.DOTALL)
    item = pattern.match(output)
    leg_info = CommonItem()
    if item:
        leg_list = item.groupdict()
        leg_info.udp_num = leg_list['udp_num']
        leg_info.rtp_num = leg_list['rtp_num']
        leg_info.gtp_num = leg_list['gtp_num']
        leg_info.udp_rtp_leg_capacity = leg_list['udp_rtp_leg_capacity']
        leg_info.gtp_leg_capacity = leg_list['gtp_leg_capacity']

    return leg_info

def get_ip_resource_in_cac():
    """    
    This keyword is used to shows ip resource in CAC part.
    #COMMAND: fsclish -c "show troubleshooting cac ip"
    | Parameters          | Man. | Description                                 |
    | NA                  |      |                                             |

    | Return value | an Instance of list with IP resource,reserve BW and reserve port information |

    Example
    | result | get_ip_resource_in_cac  |  |
    """
    command = """fsclish -c "show troubleshooting cac ip" """  
    print "Command: " + command
    output = connections.execute_mml_without_check(command)
    if output.find('No IP address exists') != -1:
        output = 'No IP address exists.'
        return output
    else:
        items = re.findall('(\d+\.\d+\.\d+\.\d+)\s+(\d+)\s+(\d+)\s+', output)
        ip_list = {}
        
        for item in items:
            ip_info = {}
            ip_info['ip_add'] = item[0]
            ip_info['vrf_id'] = item[1]
            ip_info['reserve_port_num'] = item[2]
            ip_key = ip_info['ip_add'] + "@" + ip_info['vrf_id']
            ip_list[ip_key] = ip_info
        
    item = re.findall('Total\sIP\snumber\:\s+(\d+)', output)
    if len(item) == 1:
        ip_list['Total IP number'] = item[0]
           
    return ip_list

def get_specific_ipbr_info_in_cac(ipbr_id):
    """    
    This keyword is used to get ipbr resource information from CAC PRB
    
    #COMMAND: fsclish -c "show troubleshooting cac ipbr ipbr-id  <IPBR ID>"
    
    | Parameters         | Man. | Description                                 |
    | ipbr_id            | Yes  | IPBR ID                                     |

    | Return value | an Instance of commonitem with specific IPBR all information in CAC |

    Example
    | result | get_specific_ipbr_info_in_cac | 12 |
    """
    command = """fsclish -c "show troubleshooting cac ipbr ipbr-id %s" """ % (ipbr_id)
    print "Command: " + command
    output = connections.execute_mml_without_check(command)
    if output.find('does not exist') != -1:
        output = 'IPBR with ipbr-id (%s) does not exist in connection admission control part.' % (ipbr_id)
        return output
    if output.find('NO WORKING') != -1:
        return output
    else:
        pattern = re.compile('''^.*
IPBR\sID\s+:\s+(?P<ipbr_id>\d+)\s+
IPBR\sname\s+:\s+(?P<ipbr_name>\S+)\s+
Route\sbandwidth\s+:\s(?P<route_bw>\d+)\s+kbps\s+
Committed\sbandwidth\s+:\s(?P<cmmt_bw>\d+)\s+kbps\s+
Committed\sDCN\sbandwidth\s+:\s(?P<cmmt_dcn_bw>\d+)\s+kbps\s+
Committed\ssignaling\sbandwidth\s+:\s(?P<cmmt_sig_bw>\d+)\s+kbps\s+
Committed\suser\splane\sbandwidth\s+:\s(?P<up_bw>\d+)\s+kbps\s+
Reserved\sbandwidth\s+:\s(?P<res_bw>\S+)\s+kbps\s+
IFC\sNRTDCH\s+:\s+(?P<ifc_nrtdch>\S+)\s+
IFC\sNRTHSDPA\s+:\s+(?P<ifc_nrthsdpa>\S+)\s+
Scheduler\stype\s+:\s+(?P<scheduler_type>\S+)\s+ 
PHB\sprofile\sID\s+:\s+(?P<phb_profile>\d+)\s+
DSPM\sprofile\sID\s+:\s+(?P<dspm_profile>\d+)\s+
MUX\senable\s+:\s+(?P<mux_enable>\S+)\s+
Max\sMUX\spackets\snumber\s+:\s+(?P<max_mux_packet>\d+)\s+
Local\sMUX\sUDP\sport\s+:\s+(?P<local_mux_port>\d+)\s+
Remote\sMUX\sUDP\sport\s+:\s+(?P<remote_mux_port>\d+)\s+
MUX\sUDP\sDSCP\svalue\s+:\s+(?P<mux_udp_value>\d+)\s+ 
GTP\sleg\snumber\s+:\s+(?P<gtp_num>\d+)\s+
RTP\sleg\snumber\s+:\s+(?P<rtp_num>\d+)\s+
UDP\sleg\snumber\s+:\s+(?P<udp_num>\d+)\s+
IPBR\sstatus\s+:\s((?P<ipbr_status>\S+)\s+)
''', re.VERBOSE|re.DOTALL)
        item = pattern.match(output)
        ipbr_info = CommonItem()
        if item:
           ipbr_attr = item.groupdict()
           ipbr_info.ipbr_id = ipbr_attr['ipbr_id']
           ipbr_info.ipbr_name = ipbr_attr['ipbr_name']
           ipbr_info.route_bw = ipbr_attr['route_bw'] 
           ipbr_info.cmmt_bw = ipbr_attr['cmmt_bw'] 
           ipbr_info.cmmt_dcn_bw = ipbr_attr['cmmt_dcn_bw']
           ipbr_info.cmmt_sig_bw = ipbr_attr['cmmt_sig_bw']  
           ipbr_info.ifc_nrtdch = ipbr_attr['ifc_nrtdch'] 
           ipbr_info.ifc_nrthsdpa = ipbr_attr['ifc_nrthsdpa'] 
           ipbr_info.scheduler_type = ipbr_attr['scheduler_type'] 
           ipbr_info.phb_profile = ipbr_attr['phb_profile'] 
           ipbr_info.dspm_profile = ipbr_attr['dspm_profile'] 
           ipbr_info.mux_enable = ipbr_attr['mux_enable'] 
           ipbr_info.max_mux_packet = ipbr_attr['max_mux_packet'] 
           ipbr_info.local_mux_port = ipbr_attr['local_mux_port'] 
           ipbr_info.mux_udp_value = ipbr_attr['mux_udp_value']
           ipbr_info.up_bw = ipbr_attr['up_bw']
           ipbr_info.res_bw = "%d" % (atof(ipbr_attr['res_bw'])*1000)
           ipbr_info.free_bw = "%d" % (atof(ipbr_info.up_bw) - atof(ipbr_info.res_bw))
           ipbr_info.gtp_num = ipbr_attr['gtp_num'] 
           ipbr_info.rtp_num = ipbr_attr['rtp_num'] 
           ipbr_info.udp_num = ipbr_attr['udp_num'] 
           ipbr_info.ipbr_status = ipbr_attr['ipbr_status'] 
           ipbr_info.ip_list = []
        else:
           return ipbr_info
           
    if output.find('No IP address bound with the IPBR.') != -1:
           ipbr_info.ip_list  = 'No IP address bound with the IPBR.'
    else:
           ip_pattern = re.compile('(\d+\.\d+\.\d+\.\d+)\s+(\d+)\s+(\S+)\s+(\S+)')
           items = ip_pattern.findall(output)
           for item in items:
              ip_info = CommonItem()
              ip_info.ip_addr = item[0]
              ip_info.vrf_id = item[1]
              ip_info.monitor = item[2]
              ip_info.status = item[3]
              ipbr_info.ip_list.append(ip_info)           
    return ipbr_info

def get_ipbr_list_info_in_cac():
    """    
    This keyword is used to get all ipbr resource information from CAC PRB
    
    #COMMAND: fsclish -c "show troubleshooting cac ipbr ipbr-id"
    
    | Parameters         | Man. | Description                                 |
    | ipbr_id            | Yes  | IPBR ID                                     |

    | Return value | an Instance of list with all IPBR and simple infomation in CAC |

    Example
    | result | get_ipbr_list_info_in_cac |   |
    """
    command = """fsclish -c "show troubleshooting cac ipbr" """ 
    print "Command: " + command
    output = connections.execute_mml_without_check(command)
    if output.find('No IP based route exists.') != -1:
       result = 'No IP based route exists.'
       return result
    else:
       pattern = re.compile(r'(\d+)\s+(\S+)\s+(\w+)\s+(\d+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\d+)')
       items = pattern.findall(output)
       ipbr_list = {}
       for item in items:
           ipbr_info = {}
           ipbr_info['ipbr_id'] = item[0]
           ipbr_info['ipbr_name'] = item[1]
           ipbr_info['status'] = item[2]
           ipbr_info['commit_up_bw']= item[3]
           ipbr_info['res_bw'] = "%d" % (atof(item[4])*1000)
           ipbr_info['gtp_leg'] = item[5]
           ipbr_info['rtp_leg'] = item[6]
           ipbr_info['udp_leg'] = item[7]
           ipbr_list[ipbr_info['ipbr_id']]=ipbr_info
       item = re.findall('Total\sIPBR\snumber\:\s+(\d+)', output)
       ipbr_list['Total IPBR number'] = item[0]
       item= re.findall(r'\s*CMMT-UP-BW\s+:\s+(\S+)\s+RESV-BW\s+:\s+(\S+)\s+GTP\s+leg\s+:\s+(\d+)\s+RTP\s+leg\s+:\s+(\d+)\s+UDP\s+leg\s+:\s+(\d+)', output)
       ipbr_total = {}
       ipbr_total['total committed UP BW'] = item[0][0]
       ipbr_total['total reserve BW'] = "%d" % (atof(item[0][1])*1000)
       ipbr_total['total GTP num'] = item[0][2]
       ipbr_total['total RTP num'] = item[0][3]
       ipbr_total['total UDP num'] = item[0][4]
       ipbr_list['Total value'] = ipbr_total
    return ipbr_list

def get_ipro_info_in_cac():   
    """    
    This keyword is used to shows IPRO information in CAC part.
    #COMMAND: fsclish -c "show troubleshooting cac ipro  "
    | Parameters          | Man. | Description                                 |
    | NA                  |      |                                             |

    | Return value | an Instance of list with IPRO information  |

    Example
    | result | get_ipro_info_in_cac  |  |
    """
    command = """fsclish -c "show troubleshooting cac ipro" """ 
    print "Command: " + command
    output = connections.execute_mml_without_check(command)
    if output.find('No IPRO exists') != -1:
      result = 'No IPRO exists.'
      return result
    elif output.find('NO WORKING') != -1:
      return output 
    else:
      pattern = re.compile(r'\s*(\d+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)')
      items = pattern.findall(output)
      ipro_list = {}
      for item in items:
           ipro_info = {}
           ipro_info['ipbr_id'] = item[0]
           ipro_info['ip_addr'] = item[1]
           ipro_info['vrf_id']= item[2]
           ipro_info['phb_set'] = item[3]
           ipro_info['owner'] = item[4]
           ipro_info['monitor'] = item[5]
           ipro_info['status'] = item[6]
           ipro_key = ipro_info['ipbr_id'] + "@" + ipro_info['ip_addr'] + "@" + ipro_info['owner'] + "@" + ipro_info['vrf_id']
           ipro_list[ipro_key]=ipro_info
      item = re.findall('Total\sIPRO\snumber\:\s+(\d+)', output)
      ipro_list['Total IPRO number'] = item[0]
    return ipro_list


def get_owner_id_in_cac():   
    """    
    This keyword is used to shows owner ID information in connection admission control (CAC) part.
    #COMMAND: fsclish -c "show troubleshooting cac owner-id "
    | Parameters          | Man. | Description                                 |
    | NA                  |      |                                             |

    | Return value | an Instance of list with reserve BW,GTP,RTP,UDP leg number on owner ID  |

    Example
    | result | get_couters_in_cac  |  |
    """
    command = """fsclish -c "show troubleshooting cac owner-id"  """ 
    print "Command: " + command
    output = connections.execute_mml_without_check(command)
    if output.find('No owner ID exists.') != -1:
      result = 'No owner ID exists.'
      return result
    
    else:
      pattern = re.compile(r'\s*(\S+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\d+)\s+')
      items = pattern.findall(output)
      owner_list = {}
      for item in items:
           owner_info = {}
           owner_info['owner_id'] = item[0]
           owner_info['reserve_bw'] = "%d" % (atof(item[1])*1000)
           owner_info['gtp_num']= item[2]
           owner_info['rtp_num'] = item[3]
           owner_info['udp_num'] = item[4]
           owner_list[owner_info['owner_id']]=owner_info
      item = re.findall('Total\sowner\sID\snumber\:\s+(\d+)', output)
      owner_list['Total owner ID number'] = item[0]
    return owner_list

def check_ip_bitmap_in_cac(ip_address):
    """
    This keyword is used to show bitmap of IP in connection admission control (CAC) part.
    #COMMAND: iltrmcli -S -u bitmap -d <ip-address>"
    | Parameters          | Man. | Description                                 |
    | IP address          |      |                                             |

    | Return value | NA |

    Example
    | check_ip_bitmap_in_cac  | 1.1.1.1 |
    """
    command = "iltrmcli -S -u bitmap -d %s" % (ip_address)
    output = connections.execute_mml_without_check(command)
    return output

def execute_command_on_target_hw(command):
    """
    This keyword is used to execute command .
    #COMMAND: "
    | Parameters          | Man. | Description                                 |
    | command             |      |                                             |

    | Return value | execute result |

    Example
    | execute_command_on_target_hw  | sh try.sh |
    """
    command = "%s" % (command)
    output = connections.execute_mml_without_check(command)
    return output

