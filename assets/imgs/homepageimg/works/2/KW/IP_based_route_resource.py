from comm.communication.helper import CommonItem, CommonDict
from comm.communication import connections
from iltransport_subsystem_lib import il_ipbrlib


def _run_keyword(keyword, *args):
    from robot.libraries.BuiltIn import BuiltIn
    return BuiltIn().run_keyword(keyword, *args)

def my_log(info):
    _run_keyword('log', info)

class ipbr_default_attr(CommonItem):

    def __init__(self):
        self.ifc_nrtdch = ''
        self.ifc_nrthsdpa = ''
        self.scheduler_type = ''
        self.phb_profile = ''
        self.dspm_profile = ''
        self.mux_flag = ''
        self.max_mux_pkt_num = ''
        self.mux_local_port = ''
        self.mux_remote_port = ''
        self.mux_udp_dscp = ''


def create_ipbr_attribute_instance_with_specified_parameters(attribute_string,operation):
    attribute_items = attribute_string.split()
    attribute_instance = CommonItem()
    attribute_instance.ipbr_id = ''
    if (operation == 'update'):
        attribute_instance.ipbr_name = ''
        attribute_instance.route_bw = ''
        attribute_instance.commit_bw = ''
        attribute_instance.commit_sig_bw = ''
        attribute_instance.commit_dcn_bw = ''
    else:
        attribute_instance.ipbr_name = 'test-ipbr'
        attribute_instance.route_bw = '1000'
        attribute_instance.commit_bw = '1000'
        attribute_instance.commit_sig_bw = '0'
        attribute_instance.commit_dcn_bw = '0'
    attribute_instance.ifc_nrtdch = ''
    attribute_instance.ifc_nrthsdpa = ''
    attribute_instance.scheduler_type = ''
    attribute_instance.phb_profile = ''
    attribute_instance.dspm_profile = ''
    attribute_instance.mux_flag = ''
    attribute_instance.max_mux_pkt_num = ''
    attribute_instance.mux_local_port = ''
    attribute_instance.mux_remote_port = ''
    attribute_instance.mux_udp_dscp = ''
    for attribute in attribute_items:
        items = attribute.split('=')
        if len(items) != 2:
            continue
        setattr(attribute_instance, items[0].lower().strip(), items[1].strip())
    return attribute_instance


def create_expect_error_string_of_ipbr_operation_result(opt_type, error_type, param_value=''):
    scli_err_string = {
        'IPHB_NOT_EXIST': 'IPHB associated with IPBR does not exist.',
        'IDSP_NOT_EXIST': 'IDSP associated with IPBR does not exist.',
        'INVALID_BANDWIDTH': 'Invalid bandwidth values. Please refer to help information of route-bandwidth.',
        'IPBR_NOT_EXIST': 'IPBR with ipbr-id (NEED-UPDATE) does not exist.',
        'IPBR_EXIST': 'IPBR with ipbr-id (NEED-UPDATE) already exists.',
        'SECHEDULER_LIMIT': 'scheduler-type must be "none" when route-bandwidth is 0.',
        'IFC_LIMIT': 'ifc-nrtdch and ifc-nrthsdpa must be "E-RED" when scheduler-type is "none" or "realQueue".',
        'OCTAL_UNSUPPORT': 'Input value "NEED-UPDATE" is invalid. Input has to be a valid integer. The given value is an octal number. Integer values must not start with a leading zero.',
        'HEX_WITHOUT_PREFIX': 'Input value "NEED-UPDATE" is invalid. Input has to be a valid integer.',
        'LONG_IPBR_NAME': 'ipbr-name (NEED-UPDATE) length exceeds the limit (15 characters).',
        'IPBR_ID_OUT_OF_RANGE': 'Input value "NEED-UPDATE" is invalid. Input has to be a valid integer from 1 to 4095.',
        'MUX_DEACTIVATE': 'mux-enable must be "disable" because license state of multiplexing feature is "off".',
        'IPBR_NAME_REG_NOT_MATCH': 'Input value "%s" is invalid. Input has to match the regular expression: "^[a-zA-Z0-9.-]+$".' %(param_value),
        'IPHB_OUT_OF_RANGE': 'Input value "%s" is invalid. Input has to be a valid integer from 0 to 10.' %(param_value),
        'IDSP_OUT_OF_RANGE': 'Input value "%s" is invalid. Input has to be a valid integer from 0 to 10.' %(param_value)
    }
    scli_err_header = {
        'ADD':  'Failed to add IPBR.',
        'SET':  'Failed to set IPBR.',
        'DEL':  'Failed to delete IPBR.',
        'SHOW': '',
    }
    error_string = ''
    if error_type not in ['IPBR_ID_OUT_OF_RANGE', 'HEX_WITHOUT_PREFIX', 'OCTAL_UNSUPPORT', 'IPBR_NAME_REG_NOT_MATCH', 'IPHB_OUT_OF_RANGE', 'IDSP_OUT_OF_RANGE' ]:
        error_string += scli_err_header[opt_type] + ' '

    if param_value != '':
        error_string += scli_err_string[error_type].replace('NEED-UPDATE', param_value)
    else:
        error_string += scli_err_string[error_type]

    return error_string


def add_IP_based_route_with_attributes(attribute_string):
    attribute = create_ipbr_attribute_instance_with_specified_parameters(
        attribute_string, 'add')
    return il_ipbrlib.add_ip_based_route(
        attribute.ipbr_id, attribute.ipbr_name, attribute.route_bw,
        attribute.commit_bw, attribute.commit_sig_bw, attribute.commit_dcn_bw,
        attribute.ifc_nrtdch, attribute.ifc_nrthsdpa, attribute.scheduler_type,
        attribute.phb_profile, attribute.dspm_profile, attribute.mux_flag,
        attribute.max_mux_pkt_num, attribute.mux_local_port, attribute.mux_remote_port,
        attribute.mux_udp_dscp)


def update_IP_based_route_with_attributes(attribute_string):
    attribute = create_ipbr_attribute_instance_with_specified_parameters(
        attribute_string, 'update')
    return il_ipbrlib.mod_ip_based_route(
        attribute.ipbr_id, attribute.ipbr_name, attribute.route_bw,
        attribute.commit_bw, attribute.commit_sig_bw, attribute.commit_dcn_bw,
        attribute.ifc_nrtdch, attribute.ifc_nrthsdpa, attribute.scheduler_type,
        attribute.phb_profile, attribute.dspm_profile, attribute.mux_flag,
        attribute.max_mux_pkt_num, attribute.mux_local_port, attribute.mux_remote_port,
        attribute.mux_udp_dscp)


def delete_IP_based_route_with_attributes(attribute_string):
    attribute = create_ipbr_attribute_instance_with_specified_parameters(
        attribute_string, 'delete')
    return il_ipbrlib.del_ip_based_route(attribute.ipbr_id, attribute.ipbr_name)


def check_IP_based_route_operation_result(result_info, expect_result, opt_type, error_type='', error_param='', error_value=''):
    _run_keyword('should be equal', result_info['result'].upper(), expect_result.upper())

    if error_type:
        error_info = create_expect_error_string_of_ipbr_operation_result(opt_type, error_type, error_value)
        _run_keyword('should be equal', result_info['error_info'], error_info)

    if error_type and error_type in ['LONG_IPBR_NAME', 'IPBR_EXIST', 'IPBR_NOT_EXIST']:
        return

    if error_param:
        _run_keyword('should be equal', result_info['error_param'], error_param)
    if error_value:
        _run_keyword('should be equal', result_info['error_value'], error_value)

def initialize_IP_based_route_attribute_with_default_value(attribute_string):
    attribute_items = attribute_string.split()
    attribute_instance = CommonItem()
    attribute_instance.ipbr_id = ''
    attribute_instance.ipbr_name = ''
    attribute_instance.route_bw = '1000'
    attribute_instance.commit_bw = '1000'
    attribute_instance.commit_sig_bw = '0'
    attribute_instance.commit_dcn_bw = '0'
    attribute_instance.ifc_nrtdch = 'E-RED'
    attribute_instance.ifc_nrthsdpa = 'E-RED'
    attribute_instance.scheduler_type = 'none'
    attribute_instance.phb_profile = '0'
    attribute_instance.dspm_profile = '0'
    attribute_instance.mux_flag = 'disable'
    attribute_instance.max_mux_pkt_num = '30'
    attribute_instance.mux_local_port = '65535'
    attribute_instance.mux_remote_port = '65535'
    attribute_instance.mux_udp_dscp = '46'
    for attribute in attribute_items:
        items = attribute.split('=')
        if len(items) != 2:
            continue
        setattr(attribute_instance, items[0].lower().strip(), items[1].strip())
    return attribute_instance
    
def compare_IP_based_route_attributes_in_detail(show_result, expect_result):
    _run_keyword('should be equal', show_result['IPBR ID'], expect_result.ipbr_id, "The ipbr id should be same as the expected")
    _run_keyword('should be equal', show_result['IPBR name'], expect_result.ipbr_name, "The ipbr name should be same as the expected")
    _run_keyword('should be equal', show_result['Route bandwidth'], expect_result.route_bw, "The route bandwidth should be same as the expected")
    _run_keyword('should be equal', show_result['Committed bandwidth'], expect_result.commit_bw, "The committed bandwidth should be same as the expected")
    _run_keyword('should be equal', show_result['Committed signaling bandwidth'], expect_result.commit_sig_bw, "The committed signaling bandwidth should be same as the expected")
    _run_keyword('should be equal', show_result['Committed DCN bandwidth'], expect_result.commit_dcn_bw, "The committed DCN bandwidth should be same as the expected")
    _run_keyword('should be equal', show_result['IFC NRTDCH'], expect_result.ifc_nrtdch, "The IFC NRTDCH should be same as the expected")
    _run_keyword('should be equal', show_result['IFC NRTHSDPA'], expect_result.ifc_nrthsdpa, "The IFC NRTHSDPA should be same as the expected")
    _run_keyword('should be equal', show_result['Scheduler type'], expect_result.scheduler_type, "The scheduler type should be same as the expected")
    _run_keyword('should be equal', show_result['PHB profile ID'], expect_result.phb_profile, "The PHB profile ID should be same as the expected")
    _run_keyword('should be equal', show_result['DSPM profile ID'], expect_result.dspm_profile, "The DSPM profile ID should be same as the expected")
    _run_keyword('should be equal', show_result['MUX enable'], expect_result.mux_flag, "The Mux enable flag should be same as the expected")
    _run_keyword('should be equal', show_result['Max MUX packets number'], expect_result.max_mux_pkt_num, "The Max mux packets number should be same as the expected")
    _run_keyword('should be equal', show_result['Local MUX UDP port'], expect_result.mux_local_port, "The Local mux UDP port should be same as the expected")
    _run_keyword('should be equal', show_result['Remote MUX UDP port'], expect_result.mux_remote_port, "The Remote mux UDP port should be same as the expected")
    _run_keyword('should be equal', show_result['MUX UDP DSCP value'], expect_result.mux_udp_dscp, "The Mux UDP DSCP value should be same as the expected")
    
def compare_IP_based_route_attributes_in_list(show_result, total, *expect_results):
    _run_keyword('should be equal', show_result['total'], total, 'the number of IPBR should be same as the expected')
    for expect_result in expect_results:
        _run_keyword('should be equal', show_result[expect_result.ipbr_id]['id'], 
                     expect_result.ipbr_id, "The ipbr id should be same as the expected")
        _run_keyword('should be equal', show_result[expect_result.ipbr_id]['name'], 
                     expect_result.ipbr_name, "The ipbr name should be same as the expected")
        _run_keyword('should be equal', show_result[expect_result.ipbr_id]['cmmt_bw'], 
                     expect_result.commit_bw, "The committed bandwidth should be same as the expected")
        _run_keyword('should be equal', show_result[expect_result.ipbr_id]['sig_bw'], 
                     expect_result.commit_sig_bw, "The committed signaling bandwidth should be same as the expected")
        _run_keyword('should be equal', show_result[expect_result.ipbr_id]['dcn_bw'], 
                     expect_result.commit_dcn_bw, "The committed DCN bandwidth should be same as the expected")
        _run_keyword('should be equal', show_result[expect_result.ipbr_id]['mux'], 
                     expect_result.mux_flag, "The Mux enable flag should be same as the expected")
        _run_keyword('should be equal', show_result[expect_result.ipbr_id]['schedule_type'], 
                     expect_result.scheduler_type, "The scheduler type should be same as the expected")
        _run_keyword('should be equal', show_result[expect_result.ipbr_id]['route_bw'], 
                     expect_result.route_bw, "The route bandwidth should be same as the expected")


def check_IP_based_route_attributes_with_expect_value(attribute_string):
    instance = initialize_IP_based_route_attribute_with_default_value(attribute_string)
    result = _run_keyword('show ip based route', instance.ipbr_id, instance.ipbr_name)
    _run_keyword('compare IP based route attributes in detail', result, instance)
    return

def add_network_address(owner, iface, ip_addr, dedicated='', instance=''):
    command = ' '.join(['add', 'networking',
                        'instance %s' % instance if instance else '',
                        'address dedicated' if dedicated else 'address',
                        owner, 'ip-address', ip_addr + '/32', 'iface', iface])

    scli_command = 'fsclish -c "%s"' % command
    result = connections.execute_cli(scli_command)
    print result


def delete_network_address(owner, iface, ip_addr, dedicated='', instance=''):
    command = ' '.join(['delete', 'networking',
                        'instance %s' % instance if instance else '',
                        'address dedicated' if dedicated else 'address',
                        owner, 'ip-address', ip_addr + '/32', 'iface', iface])

    scli_command = 'fsclish -c "%s"' % command
    result = connections.execute_cli(scli_command)
    print result


def create_ipro_attribute_instance_with_specified_parameters(attribute_string):
    attribute_items = attribute_string.split()
    attribute_instance = CommonItem()
    attribute_instance.ipbr_id = ''
    attribute_instance.iface = ''
    attribute_instance.ip_address = ''
    attribute_instance.owner = ''
    attribute_instance.mode = ''
    attribute_instance.phb_set = ''
    attribute_instance.vrf = ''
    for attribute in attribute_items:
        items = attribute.split('=')
        if len(items) != 2:
            continue
        setattr(attribute_instance, items[0].lower().strip(), items[1].strip())

    return attribute_instance


def add_ipro_with_attributes(attribute_string):
    attribute = create_ipro_attribute_instance_with_specified_parameters(attribute_string)
    return il_ipbrlib.add_ipro(ipbr_id=attribute.ipbr_id, ip_address=attribute.ip_address, 
                               owner=attribute.owner, iface=attribute.iface,
                               phb_set=attribute.phb_set, vrf=attribute.vrf)


def update_ipro_with_attributes(attribute_string):
    attribute = create_ipro_attribute_instance_with_specified_parameters(attribute_string)
    return il_ipbrlib.modify_ipro(attribute.ipbr_id, attribute.ip_address,
                                  attribute.owner, attribute.iface,
                                  attribute.phb_set)


def delete_ipro_with_attributes(attribute_string):
    attribute = create_ipro_attribute_instance_with_specified_parameters(attribute_string)
    return il_ipbrlib.delete_ipro(attribute.ipbr_id, attribute.ip_address,
                                  attribute.owner, attribute.iface, attribute.mode)

def show_ipro_with_attributes(attribute_string):
    attribute = create_ipro_attribute_instance_with_specified_parameters(attribute_string)
    return il_ipbrlib.show_ipro(attribute.ipbr_id, attribute.ip_address, attribute.owner,  attribute.iface)

def compare_ipro_attribute_with_expect_string(search_result, *expect_list):
    for expect_result in expect_list:
        if expect_result == '':
            continue
        attribute = create_ipro_attribute_instance_with_specified_parameters(expect_result)
        key = '%s@%s@%s@%s' % (attribute.ipbr_id, attribute.ip_address, attribute.iface, attribute.owner)
        _run_keyword('should contain', search_result, key, 'search result should contain the expect instance')
        _run_keyword('should be equal', search_result[key].iface, attribute.iface, 
                     'iface (%s) should be equal to the expected (%s)' % (search_result[key].iface, attribute.iface))
        _run_keyword('should be equal', search_result[key].owner, attribute.owner,
                     'owner (%s) should be equal to the expected (%s)' % (search_result[key].owner, attribute.owner))
        _run_keyword('should be equal', search_result[key].ip_address, attribute.ip_address,
                     'ip_address (%s) should be equal to the expected (%s)' % (search_result[key].ip_address, attribute.ip_address))
        _run_keyword('should be equal', search_result[key].ipbr_id, attribute.ipbr_id,
                     'IPBR ID (%s) should be equal to the expected (%s)' % (search_result[key].ipbr_id, attribute.ipbr_id))
        if attribute.phb_set == '' or attribute.phb_set.lower() == 'all':
           af1 = 'on'
           af2 = 'on'
           af3 = 'on'
           af4 = 'on'
           ef = 'on'
           be = 'on'
        else:
           af1 = 'on' if attribute.phb_set.lower().find('af1') != -1 else 'off'
           af2 = 'on' if attribute.phb_set.lower().find('af2') != -1 else 'off'
           af3 = 'on' if attribute.phb_set.lower().find('af3') != -1 else 'off'
           af4 = 'on' if attribute.phb_set.lower().find('af4') != -1 else 'off'
           ef = 'on' if attribute.phb_set.lower().find('ef') != -1 else 'off'
           be = 'on' if attribute.phb_set.lower().find('be') != -1 else 'off'
	
        _run_keyword('should be equal', search_result[key].phb_set.af1, af1,
                     'af1 of phb_set (%s) should be equal to the expected (%s)' % (search_result[key].phb_set.af1, af1))
        _run_keyword('should be equal', search_result[key].phb_set.af2, af2,
                     'af2 of phb_set (%s) should be equal to the expected (%s)' % (search_result[key].phb_set.af2, af2))
        _run_keyword('should be equal', search_result[key].phb_set.af3, af3,
                     'af3 of phb_set (%s) should be equal to the expected (%s)' % (search_result[key].phb_set.af3, af3))
        _run_keyword('should be equal', search_result[key].phb_set.af4, af4,
                     'af4 of phb_set (%s) should be equal to the expected (%s)' % (search_result[key].phb_set.af4, af4))
        _run_keyword('should be equal', search_result[key].phb_set.ef, ef,
                     'ef of phb_set (%s) should be equal to the expected (%s)' % (search_result[key].phb_set.ef, ef))
        _run_keyword('should be equal', search_result[key].phb_set.be, be,
                     'be of phb_set (%s) should be equal to the expected (%s)' % (search_result[key].phb_set.be, be))

def create_expect_error_string_of_ipro_operation_result(opt_type, error_type, param_value=''):
    scli_err_header = {
        'ADD':  'Failed to add IPRO. ',
        'SET':  'Failed to set IPRO. ',
        'DEL':  'Failed to delete IPRO. ',
        'SHOW': '',
    }
    scli_err_string = {
        'IPRO_NOT_EXIST': 'IPRO identifier (ipbr-id + ip-address + iface + owner) does not exist.',
        'BE_OR_EF_MISSING': 'phb-set (NEED-UPDATE) does not contain EF or BE, or PHBs defined in the phb-set are not consecutive.',
        'PHB_DUPLICATE': 'phb-set (NEED-UPDATE) contains duplicated PHB.',
        'PHB_NOT_CONSECUTIVE': 'phb-set (NEED-UPDATE) does not contain EF or BE, or PHBs defined in the phb-set are not consecutive.',
        'PHB_INVALID_STR': 'phb-set (NEED-UPDATE) does not follow defined syntax. Please check help information of phb-set.',
        'IPRO_EXIST': 'IPRO identifier (ipbr-id + ip-address + iface + owner) already exists.',
        'SECHEDULER_LIMIT': 'scheduler-type of IPBR must be "none" when multiple IPROs with the same IPBR are distributed to different owners.',
        'IPBR_NOT_EXIST': 'IPBR with ipbr-id (NEED-UPDATE) does not exist.',
        'INVALID_PARAM': 'Parameter value or dynamic symbol value does not match constraint(s) or list of values',
	'PHB_REG_NOT_MATCH': 'Input value "%s" is invalid. Input has to match the regular expression: "^ALL$|^[ABEF1-4,]+$".' %(param_value)
    }

    error_string = ''
    if (error_type != 'INVALID_PARAM') and (error_type != 'PHB_REG_NOT_MATCH'):
        error_string += scli_err_header[opt_type]
    error_string += scli_err_string[error_type].replace('NEED-UPDATE', param_value)

    return error_string


def check_ipro_operation_result(result_info, expect_result, opt_type, error_type='', error_param='', error_value=''):
    _run_keyword('should be equal', result_info['result'].upper(), expect_result.upper())
    if error_type != '':
        error_info = create_expect_error_string_of_ipro_operation_result(opt_type, error_type, error_value)
        _run_keyword('should be equal', result_info['error_info'], error_info)
    
    if error_type == 'INVALID_PARAM':
        _run_keyword('should be equal', error_param, result_info['error_param'])
        _run_keyword('should be equal', error_value, result_info['error_value'])
    return


def get_feature_license(feature_name=''):
    command = 'fsclish -c "show license all" '
    result = connections.execute_mml_without_check(command)
    lines = result.splitlines()
    license_list = CommonDict()
    key = '0'
    for line in lines:
        items = line.split(':')
        if len(items) != 2:
            continue
        if items[0].strip() == 'Unique ID':
            key = items[1].strip()
            license_list[key] = CommonItem()
        if key == '0':
            print 'no key'
            continue
        setattr(license_list[key], items[0].strip().replace(' ', '_').lower(), items[1].strip())
    if not feature_name:
        return license_list

    for unique_id in license_list:
        if license_list[unique_id].feature_name_list == feature_name:
            return license_list[unique_id]
    return


def set_feature_license_with_feature_code(feature_code, status):
    command = 'fsclish -c "set license feature-mgmt code %s feature-admin-state %s"' % (feature_code, status)
    result = connections.execute_mml_without_check(command)
    return result
