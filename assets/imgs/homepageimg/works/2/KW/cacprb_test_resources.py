from comm.communication import execute_mml_without_check, raise_ILError
from comm.communication import connections
from comm.communication import exceptions
from comm.communication.helper import CommonItem
from flexi_platform.fphaslib import get_all_recovery_group_names as __all_recovery_groups
from flexi_platform.fphaslib import show_managed_object_parent as __show_mo_parent
from flexi_platform.fphaslib import show_managed_objects_state_with_regex_name as __show_state_with_regex_name
from ilcallmgmt_subsystem_lib.library.upm_lib import get_service_id_info as get_owner_id
from iltransport_subsystem_lib.iltrm_troubleshooting_lib import get_owner_id_in_cac as get_owner_id_from_cac
from ILRobotAPI import BuiltIn
from robot.libraries import Collections
import random
import time
import os
from string import atof

def _kw(command, *args):
    return BuiltIn().run_keyword(command, *args)


def get_usable_recovery_groups():
    command = "ilclifunit -u -t USCP | grep USCP | awk '{if ($4==\"WO-EX\") {print $1}}'"
    uscp_list = execute_mml_without_check(command).strip().splitlines()
    command = "ilclifunit -u -t CSCP | grep CSCP | awk '{if ($4==\"WO-EX\") {print $1}}'"
    cscp_list = execute_mml_without_check(command).strip().splitlines()

    qnup_list = []
    for qnup in __all_recovery_groups():
        if qnup.find('QNUP') != -1:
            qnup_list.append(qnup)

    if len(qnup_list) == 0 or len(cscp_list) == 0 or len(uscp_list) == 0:
        raise_ILError('ILCommandExecuteError',
                      'no active recovery group or unit in the hardware')
    return uscp_list, cscp_list, qnup_list

def check_owner_id_info_in_cac(owner_id_from_call, leg_type, leg_num, old_owner_info_in_cac):
    new_owner_id_info_in_cac = _kw('_get_owner_id_from_cac')
    _kw('should be true', new_owner_id_info_in_cac.has_key(owner_id_from_call),'check owner_id from call whether in cac')

    if old_owner_info_in_cac == 'No owner ID exists.':
        _kw('should be equal', new_owner_id_info_in_cac['%s' % owner_id_from_call]['%s_num' % leg_type], leg_num, 'the owner ID and legs are compare')
        
    elif old_owner_info_in_cac.has_key(owner_id_from_call) == True:
        increase_leg_num = atof(new_owner_id_info_in_cac['%s' % owner_id_from_call]['%s_num' % leg_type]) - atof(old_owner_info_in_cac['%s' % owner_id_from_call]['%s_num' % leg_type])
	_kw('Should Be Equal As Numbers', increase_leg_num, atof(leg_num), 'the owner ID exist and the increase leg compare')
        
    else: 
        _kw('should be equal', new_owner_id_info_in_cac['%s' % owner_id_from_call]['%s_num' % leg_type], leg_num, 'the new owner ID and the new legs compare')
				
def reserve_ip_based_route_resource(ipbr_id, qnup, iface, ip_address, route_bandwidth='1000000',
                                commit_bw='1000000', commit_sig_bw='0', commit_dcn_bw='0'):    
    result = _kw('add_ip_based_route', ipbr_id, 'ipbr-' + ipbr_id,
                            route_bandwidth, commit_bw, commit_sig_bw, commit_dcn_bw)
    result = _kw('add_ipro', ipbr_id, ip_address, qnup, iface)

    return {'qnup': qnup, 'ip_addr': ip_address, 'iface': iface, 'ipbr_id': ipbr_id}

def release_ip_based_route_resource(ipbr_id, qnup, iface, ip_address):
    result = _kw('delete_ipro', ipbr_id, ip_address, qnup, iface)
    result = _kw('del_ip_based_route', ipbr_id)
    return

def reserve_ip_address_on_each_qnup(qnup_list):
    index = 0
    iface = 'lo'
    ip_pool = []
    for qnup in qnup_list:
        index += 1
        ip_address = '192.10.1.%d' % index
        result = _kw('add_ip_address', qnup, iface, ip_address + '/32')
        ip_pool.append({'owner': qnup, 'iface': iface, 'ip_addr': ip_address})
    return ip_pool

    
def reserve_ip_based_route_with_all_ip_address_based_on_same_id(ipbr_id, ip_pool, route_bandwidth='1000000',
                                                                commit_bw='1000000', commit_sig_bw='0', commit_dcn_bw='0'):
    ipro_pool = []
    result = _kw('add_ip_based_route', ipbr_id, 'ipbr-' + ipbr_id, route_bandwidth, commit_bw, commit_sig_bw, commit_dcn_bw)
    for ip_res in ip_pool:
        ipbr_res = _kw('add_ipro', ipbr_id, ip_res['ip_addr'], ip_res['owner'], ip_res['iface'])
        ipro_pool.append({'ipbr_id': ipbr_id, 'ip_addr': ip_res['ip_addr'], 'owner': ip_res['owner'], 'iface': ip_res['iface']})
    return ipro_pool


def reserve_test_ip_based_route_resource(ipbr_id, qnup_list):
    ip_pool = _kw('reserve_ip_address_on_each_qnup', qnup_list)
    ipro_pool = _kw('reserve_ip_based_route_with_all_ip_address_based_on_same_id', ipbr_id, ip_pool)
    return ip_pool, ipro_pool


def release_ipro_with_list(ipro_list):
    for ipro_info in ipro_list:
        result = _kw('delete_ipro', ipro_info['ipbr_id'], ipro_info['ip_addr'], ipro_info['owner'], ipro_info['iface'], 'forced')
    return
        

def release_ip_address_with_list(ipaddr_list):
    for ip_res in ipaddr_list:
        result = _kw('delete_ip_address', ip_res['owner'], ip_res['iface'], ip_res['ip_addr'])
    return


def reserve_psnrt_call_successfully(owner, ipbr_id, user_id=''):
    old_owner_id_in_cac = _kw('_get_owner_id_from_cac')
    print 'reserve_psnrt_call_successfully'
    gtp_leg = _kw(' Allocate Resource',
                  owner,
                  '',
                  'OUT',
                  '1.1.1.1',
                  '3000,,,%s' % ipbr_id,
                  '5',
                  '',
                  'DSP=4,F,0,IMSI=0123456789876540,DEST=FFFFFFFF,SDEST=22,CELL=6100' + ',USERID=%s' % user_id if user_id != '' else '')
    if gtp_leg.result == 'SUCCESSFUL':
        _kw('should be equal', gtp_leg.result, 'SUCCESSFUL')
        gtp_leg.owner = owner
        owner_info = _kw('get_owner_id','all', 'servid', gtp_leg.serv_id) 
        gtp_leg.owner_id =  '0x' + owner_info[gtp_leg.serv_id.upper()].owner_id
        _kw('check_owner_id_info_in_cac', gtp_leg.owner_id, 'gtp', '1', old_owner_id_in_cac)
    else:
        _kw('should be equal', gtp_leg.result, 'SUCCESSFUL')
        return None

    udp_leg = _kw(' Allocate Resource',
                  owner,
                  gtp_leg.call_id,
                  'IN',
                  '1.1.1.2',
                  '3000,,,%s' % ipbr_id,
                  '4',
                  '',
                  'DSP=4,7,0,IMSI=0123456789876540,BRA=T' + ',USERID=%s' % user_id if user_id != '' else '')
    if udp_leg.result == 'SUCCESSFUL':
        _kw('should be equal', udp_leg.result, 'SUCCESSFUL')
        udp_leg.owner = owner
        udp_leg.owner_id = gtp_leg.owner_id
        udp_leg.call_id = gtp_leg.call_id
    else:
        _kw('should be equal', udp_leg.result, 'SUCCESSFUL')
        return [gtp_leg]

    return[gtp_leg, udp_leg]

   
def reserve_srb_call_failed_with_expect_error(owner, ipbr_id, error_code, user_id=''):
    result = _kw('reserve_srb_call', owner, ipbr_id, 'NCAC=0', user_id)
    _kw('should be equal', result.result, 'FAILED')
    _kw('should be equal', result.error_code, error_code)
    return
    

def reserve_cell_and_cch_successfully(owner, ipbr_id, user_id='', cell_id=''):
    old_owner_id_in_cac = _kw('_get_owner_id_from_cac')
    # CELL Service Setup
    cell_info = _kw('Allocate Service', owner, '', 'CELL:2F:%s:2' % cell_id)
    if cell_info.result == 'SUCCESSFUL':
        _kw('should be equal', cell_info.result, 'SUCCESSFUL')
        cell_info.owner = owner
        #owner_info = _kw('get_owner_id', 'all', 'servid', cell_info.serv_id) 
        #cell_info.owner_id =  '0x' + owner_info[cell_info.serv_id.upper()].owner_id
    # RACH Setup
    cch_info = _kw(' Allocate Resource', owner, cell_info.call_id, 'TERM', '',
                   ',,,%s' % ipbr_id, '2,T', '', 'USERID=%s,ENC=52,BRA=F,DSP=00,00,00,CELL=%s,DEST=16' % (user_id, cell_id))
    if cch_info.result == 'SUCCESSFUL':
        _kw('should be equal', cell_info.result, 'SUCCESSFUL')
        cch_info.owner = owner
        owner_info = _kw('get_owner_id', 'all', 'servid', cch_info.serv_id) 
        cch_info.owner_id =  '0x' + owner_info[cch_info.serv_id.upper()].owner_id
        cch_info.call_id = cell_info.call_id
        _kw('check_owner_id_info_in_cac', cch_info.owner_id, 'udp', '1', old_owner_id_in_cac)
        return {'cell_info': cell_info, 'cch_info': cch_info}
    _kw('should be equal', cell_info.result, 'SUCCESSFUL')
    return
    
    
def reserve_srb_call_successfully(owner, ipbr_id, user_id='', trans_params=''):
    old_owner_id_in_cac = _kw('_get_owner_id_from_cac')
    trans_params = trans_params if trans_params else 'NCAC=0'
    result = _kw('reserve_srb_call', owner, ipbr_id, trans_params, user_id)
    if result.result == 'SUCCESSFUL':
        _kw('should be equal', result.result, 'SUCCESSFUL')
        owner_info = _kw('get_owner_id', 'all', 'servid', result.serv_id)
        result.owner_id =  '0x' + owner_info[result.serv_id.upper()].owner_id
        _kw('check_owner_id_info_in_cac', result.owner_id, 'udp', '1', old_owner_id_in_cac)
        result.owner = owner
        return result
    _kw('should be equal', result.result, 'SUCCESSFUL')
    return None

def reserve_srb_call(owner, ipbr_id, other_para='', user_id=''):
    tran_para = 'DSP=1,7,0,IMSI=0123456789876540,ENC=12,BRA=T'
    if user_id:
        tran_para += ',USERID=' + user_id
    if other_para:
        tran_para += ',' + other_para

    result = _kw(' Allocate Resource',
                  owner, '', 'IN', '10.10.10.10',
                  '3000,,,%s' % ipbr_id, '2,T', '',
                  tran_para)
    return result
   
def modify_srb_call(owner, ipbr_id, other_para, call_id):
    call_list = []
    result = _kw(' Allocate Resource',
                  owner, '%s' % call_id, 'IN', '10.10.10.10',
                  '3000,,,%s' % ipbr_id, '2,T', '',
                  'DSP=1,7,0,IMSI=0123456789876540,ENC=12,BRA=T,%s' % other_para)
    return result


def reserve_amr_call_successfully(owner, ipbr_id, user_id=''):
    old_owner_id_in_cac = _kw('_get_owner_id_from_cac')
    rtp_leg = _kw(' Allocate Resource',
                 owner,
                 '',
                 'OUT',
                 '10.10.10.10',
                 '3000,,,%s' % ipbr_id, '2,T', '',
                 'DSP=C,6,1,ENC=10' + ',USERID=%s' % user_id if user_id != '' else '')
    if rtp_leg.result == 'SUCCESSFUL':
        _kw('should be equal', rtp_leg.result, 'SUCCESSFUL')
        owner_info = _kw('get_owner_id', 'all', 'servid', rtp_leg.serv_id)
        rtp_leg.owner_id =  '0x' + owner_info[rtp_leg.serv_id.upper()].owner_id
        rtp_leg.owner = owner
        _kw('check_owner_id_info_in_cac', rtp_leg.owner_id, 'rtp', '1', old_owner_id_in_cac)
    else:
        _kw('should be equal', rtp_leg.result, 'SUCCESSFUL')
        return None

    fp_leg = _kw(' Allocate Resource',
                  owner,
                  rtp_leg.call_id,
                  'IN',
                  '10.10.10.10',
                  '3001,,,%s' % ipbr_id,
                  '1',
                  '',
                  'DSP=C,7,1,IMSI=0123456789876540,NCAC=0' + ',USERID=%s' % user_id if user_id != '' else '')
    if fp_leg.result == 'SUCCESSFUL':
        _kw('should be equal', fp_leg.result, 'SUCCESSFUL')
        fp_leg.owner = owner
        fp_leg.owner_id = rtp_leg.owner_id
        _kw('check_owner_id_info_in_cac', fp_leg.owner_id, 'udp', '1', old_owner_id_in_cac)
        fp_leg.call_id = rtp_leg.call_id
    else:
        _kw('should be equal', fp_leg.result, 'SUCCESSFUL')
        return None
    return [rtp_leg, fp_leg]


def release_leg_resource_successfully(owner, call_id, leg_type):
    result = _kw(' Release Resource', owner, call_id, leg_type)
    _kw('should be equal', result.result, 'SUCCESSFUL')
    return
    

def reserve_srb_amr_psnrt_calls_on_each_uscp(ipbr_id, uscp_list):
    call_list = []
    user_id = 30000
    print uscp_list
    for uscp in uscp_list:
        for keyword in ['reserve_amr_call_successfully', 'reserve_srb_call_successfully', 'reserve_psnrt_call_successfully']:
            result = _kw(keyword, uscp, ipbr_id, str(user_id))
            if not result: continue
            if type(result) != type([]):
                call_list.append(result)
            else:
                call_list.extend(result)
            user_id += 128
        
    return call_list


def reserve_rach_on_each_cscp(ipbr_id, cscp_list):
    call_list = []
    user_id = 40000
    cell_id = 3000
    for cscp in cscp_list:
        user_id += 1
        cell_id += 1
        result = _kw('reserve_cell_and_cch_successfully', cscp, ipbr_id, str(user_id), str(cell_id))
        if result: call_list.append(result)
    return call_list    


def release_calls_with_list(call_list):
    out_leg_list = []
    in_leg_list = []
    for call_info in call_list:
        if call_info.leg_id.find('IN') != -1:
            in_leg_list.append((call_info.owner, call_info.call_id, 'IN'))
        elif call_info.leg_id.find('OUT') != -1:
            out_leg_list.append((call_info.owner, call_info.call_id, 'OUT'))

    for leg_list in [in_leg_list, out_leg_list]:
        for leg_info in set(leg_list):
            result = _kw('release_leg_resource_successfully',
                         leg_info[0], leg_info[1], leg_info[2])
    return


def release_cell_service_with_list(call_list):
    for service in call_list:
        result = _kw(' Release Resource', service['cch_info'].owner, service['cch_info'].call_id, service['cch_info'].leg_id)
        result = _kw(' Release Service', service['cell_info'].owner, service['cell_info'].call_id, 'CELL')        
    return


def reserve_and_release_common_channel_for_each_cscp(ipbr_id, cscp_list):
    call_list = _kw('reserve_rach_on_each_cscp', ipbr_id, cscp_list)
    _kw('release cell service with list', call_list)
    return


def reserve_and_release_srb_amr_psnrt_calls_for_each_uscp(ipbr_id, uscp_list):
    call_list = _kw('reserve_srb_amr_psnrt_calls_on_each_uscp', ipbr_id, uscp_list)
    _kw('release_calls_with_list', call_list)
    return


def all_the_srb_call_should_assigned_with_expect_ip_address_averagely(call_list, ip_list):
    static_list = {}
    for call_info in call_list:
        if call_info.local_ip not in static_list:
            static_list[call_info.local_ip] = 1
        else:
            static_list[call_info.local_ip] += 1
    
    expect_list = [ip_info['ip_addr'] for ip_info in ip_list]
    assigned_list = static_list.keys()
    expect_ip_str = ','.join(sorted(expect_list))
    assigned_ip_str = ','.join(sorted(assigned_list))
    
    _kw('Should be True', sorted(expect_list) == sorted(assigned_list),
        'The assigned IP addresses and expect IP addresses should be same, expect IP address: [%s], assigned IP address: [%s]' % (expect_ip_str, assigned_ip_str))
    
    counter = 0
    average_flag = True
    static_str = ''
    for ip_address in static_list:
        static_str += '%s: %d, ' % (ip_address, static_list[ip_address])
        if counter == 0:
            counter = static_list[ip_address]
            continue
        if counter != static_list[ip_address]:
            average_flag = average_flag and False        
    _kw('Should be True', average_flag, 'The SRB call number allocated with different IP address should same: %s' % static_str)
    return
    
def allocate_leg_used_IP_number(leg_info, ip_list):
    static_list = {}
    if leg_info.local_ip not in static_list:
        static_list[leg_info.local_ip] = 1
    else:
        static_list[leg_info.local_ip] += 1
    expect_list = [ip_info['ip_addr'] for ip_info in ip_list]
    assigned_list = static_list.keys()
    expect_ip_str = ','.join(sorted(expect_list))
    assigned_ip_str = ','.join(sorted(assigned_list))
    print assigned_ip_str 
    return expect_ip_str
        
def reserve_srb_calls_with_same_ipbr_id(ipbr_id, reserve_time, uscp_list):
    call_list = []
    user_id_base = 30000
    
    for user_id in range(user_id_base, user_id_base + reserve_time):
        uscp = random.choice(uscp_list)
        result = _kw('reserve_srb_call_successfully', uscp, ipbr_id, str(user_id))
        if result: call_list.append(result)   
    return call_list
    
def select_random_qnup_and_set_disabled(qnup_list):
    qnup = random.choice(qnup_list)
    _kw('set_managed_object_lock', qnup)
    return qnup

def reserve_srb_call_and_the_disabled_qnup_should_not_assigned(ipbr_id, uscp_list, qnup_list, ip_list):
    uscp = random.choice(uscp_list)
    user_id = 30000
    ip_res = None
    
    qnup = random.choice(qnup_list)

    for ip_info in ip_list:
        if ip_info['owner'] == qnup:
            ip_res = ip_info
            break
    
    _kw('set_managed_object_lock', qnup)
    _kw('reserve_ip_based_route_resource', ipbr_id, qnup, ip_info['iface'], ip_info['ip_addr'])
    _kw('reserve_srb_call_failed_with_expect_error', uscp, ipbr_id, '0x267', str(user_id))
    _kw('set_managed_object_unlock', qnup)
    while True:
        state = _kw('show_managed_object_state', qnup)
        if state[qnup].admin == 'UNLOCKED' and state[qnup].opt == 'ENABLED' and state[qnup].usage == 'ACTIVE':
            break
    call_list = _kw('reserve_srb_call_successfully', uscp, ipbr_id, str(user_id))
    _kw('release_calls_with_list', [call_list])
    _kw('release_ip_based_route_resource', ipbr_id, qnup, ip_info['iface'], ip_info['ip_addr'])
    return

def check_CPC_value(leg_comm_bw, leg_used_bw, ipbr_comm_bw, ipbr_res_bw):
    if (ipbr_comm_bw == '0') or (atof(ipbr_comm_bw) > 1000000):
        _kw('Should Be Equal', leg_comm_bw, '4294967295', 'The committed BW is 0 or bigger than 1000000,the leg comm_bw of CPC value is 4294967295(FFFFFFFF)')
        _kw('Should Be Equal', leg_used_bw, '4294967295', 'The committed BW is 0 or bigger,the leg used_bw of CPC value is 4294967295(FFFFFFFF)') 
    else:
        _kw('Should Be Equal', leg_comm_bw, ipbr_comm_bw, 'The committed BW is not 0,the leg comm_bw of CPC value is equal to ipbr committed bw')
        _kw('Should Be Equal', leg_used_bw, ipbr_res_bw, 'The committed BW is not 0,the leg used_bw of CPC value is equal to ipbr reserve bw')
    return

def check_reserve_BW(ipbr_orig_res_bw, ipbr_new_res_bw, expect_bw):
    if ipbr_orig_res_bw > ipbr_new_res_bw:
        increase_bw = atof(ipbr_orig_res_bw) - atof(ipbr_new_res_bw)
        _kw('Should Be Equal As Numbers', increase_bw, expect_bw, 'the decrease BW value')
    else:
        increase_bw = atof(ipbr_new_res_bw) - atof(ipbr_orig_res_bw)
        _kw('Should Be Equal As Numbers', increase_bw, expect_bw, 'the increase BW value')
    return


def select_random_QNUP_from_hardware():
    qnup_list = __show_state_with_regex_name('^/QNUP*')
    active_qnups = []
    for qnup in qnup_list:
        state = qnup_list[qnup]
        if state.admin == 'UNLOCKED' and state.opt == 'ENABLED' and state.usage == 'ACTIVE':
            active_qnups.append(qnup)
    return random.choice(active_qnups)

     
    
if __name__ == "__main__":
    from comm.communication import connect_to_il, disconnect_all_ils
    connect_to_il('10.68.157.109', 22, '30sec', 'root', 'root', 'SSH')
    print select_random_QNUP_form_hardware()
    disconnect_all_ils()
