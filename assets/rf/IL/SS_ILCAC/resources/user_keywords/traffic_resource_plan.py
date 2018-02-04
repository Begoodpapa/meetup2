from xml.dom import minidom
import os
from flexi_platform.fphaslib import get_all_node_names as _all_nodes
from flexi_platform.fphaslib import get_all_recovery_group_names as _all_recovery_groups
from flexi_platform.fphaslib import get_recovery_unit_names_with_recovery_group_name as _get_unit_of_group
from flexi_platform.fphaslib import recovery_group_control_switchover as _ctrl_sw
from flexi_platform.fphaslib import show_managed_object_state as _show_state
from flexi_platform.networking.switch import show_switch_port_infomation as _port_state
from flexi_platform.fphardwarelib import show_hardware_physical_information as _hardware_deployment
from flexi_platform.fpswmgmtlib import show_embedded_software_version_with_node_name as _node_software_version 
from comm.communication import execute_mml_without_check as _exec


class IPPlanFactory(object):
    def __init__(self, plan_version='', dn_prefix='RNC-02/IP-1', operation_type='created'):
        self.plan_version = os.getenv('IPPLAN_VER', 'mcRNC4.0')
        self.dn_prefix = dn_prefix
        self.operation_type = operation_type
        self.initXML()
        

    def initXML(self):
        document = minidom.getDOMImplementation() 
        doctype = document.createDocumentType('raml', '', 'raml21.dtd')
        self.doc = document.createDocument("raml21.xsd", "raml", doctype)
        raml_element = self.doc.documentElement
        raml_element.setAttribute("xmlns", "raml21.xsd")
        raml_element.setAttribute("version", '2.1')
        self.cmdata_element = self.doc.createElement('cmData')
        self.cmdata_element.setAttribute('type', 'actual')
        raml_element.appendChild(self.cmdata_element)
        self.addPlanAction()

    
    def addPlanAction(self):
        header_element = self.doc.createElement('header')
        log_element = self.doc.createElement('log')
        log_element.setAttribute('action', self.operation_type)
        log_element.setAttribute('dateTime', '2009-07-23T06:53:45Z')
        log_element.setAttribute('user', 'SKOIVU')        
        log_element.appendChild(self.doc.createTextNode('IP Plan file'))        
        header_element.appendChild(log_element)
        self.cmdata_element.appendChild(header_element)
        

    def _attr_node(self, name, value):
        node = self.doc.createElement('p')
        node.appendChild(self.doc.createTextNode(value))
        node.setAttribute('name', name)
        return node
    
        
    def _dn_node(self, name, operation, dist_name): 
        node = self.doc.createElement('managedObject')
        node.setAttribute('class', name)
        node.setAttribute('version', self.plan_version)
        node.setAttribute('operation', operation)
        node.setAttribute('distName', dist_name)
        return node
        
    
    def nodeIPBRAdd(self, ipbr_id, ipbr_name, commit_bw, route_bw, commit_sig_bw, commit_dcn_bw):
        dist_name = self.dn_prefix + '/IPBR-%s' % (ipbr_id)
        ipbr_element = self._dn_node('IPBR', 'create', dist_name) 
        ipbr_element.appendChild(self._attr_node('ipBasedRouteName', ipbr_name))
        ipbr_element.appendChild(self._attr_node('committedBW', commit_bw))
        ipbr_element.appendChild(self._attr_node('routeBW', route_bw))
        ipbr_element.appendChild(self._attr_node('committedSigBW', commit_sig_bw))
        ipbr_element.appendChild(self._attr_node('committedDcnBW', commit_dcn_bw))
        # TODO: check about the other attributes of IPBR        
        self.cmdata_element.appendChild(ipbr_element)  
    

    def nodeIPBRDel(self, ipbr_id):
        dist_name = self.dn_prefix + '/IPBR-%s' % (ipbr_id)
        self.cmdata_element.appendChild(self._dn_node('IPBR', 'delete', dist_name))
    
    
    def nodeIPROAdd(self, owner, ipbr_id, ip_addr, iface, vrf_name=''):
        dist_name = self.dn_prefix + '/OWNER-%s/IPRO-%s-%s-%s' % (owner, ipbr_id, ip_addr, iface)
        ipro_element = self._dn_node('IPRO', 'create', dist_name)
        # TODO: check about the phb_set parameters
        if vrf_name:
            ipro_element.appendChild(self._attr_node('vrf', vrf_name))
        self.cmdata_element.appendChild(ipro_element)
    
    
    def nodeIPRODel(self, owner, ipbr_id, ip_addr, iface):
        dist_name = self.dn_prefix + '/OWNER-%s/IPRO-%s-%s-%s' % (owner, ipbr_id, ip_addr, iface)
        self.cmdata_element.appendChild(self._dn_node('IPRO', 'delete', dist_name))
        
        
    def nodeVRFAdd(self, vrf_id, vrf_name):
        dist_name = self.dn_prefix + '/VRF-%s' % vrf_name
        vrf_element = self._dn_node('VRF', 'create', dist_name)
        vrf_element.appendChild(self._attr_node('id', vrf_id))
        self.cmdata_element.appendChild(vrf_element)
        
    
    def nodeVRFDel(self, vrf_name):
        dist_name = self.dn_prefix + '/VRF-%s' % vrf_name
        self.cmdata_element.appendChild(self._dn_node('VRF', 'delete', dist_name))
    
    
    def nodeIPAdd(self, owner, ip_addr, iface, mask='32', vrf_name=''):
        dist_name = self.dn_prefix + '/OWNER-%s/ADDR-%s-%s' % (owner, ip_addr, iface)
        ip_element = self._dn_node('ADDR', 'create', dist_name)
        ip_element.appendChild(self._attr_node('mask', mask))
        if vrf_name:
            ip_element.appendChild(self._attr_node('vrf', vrf_name))
        self.cmdata_element.appendChild(ip_element)
        
    
    def nodeIPDel(self, owner, ip_addr, iface):
        dist_name = self.dn_prefix + '/OWNER-%s/ADDR-%s-%s' % (owner, ip_addr, iface)
        self.cmdata_element.appendChild(self._dn_node('ADDR', 'delete', dist_name))
    
    
    def nodeInterfaceAdd(self, owner, iface_name, sfp_port, vrf_name=''):
        dist_name = self.dn_prefix + '/OWNER-%s/ETHER-%s' % (owner, iface_name)
        iface_element = self._dn_node('ETHER', 'create', dist_name)
        iface_element.appendChild(self._attr_node('port', sfp_port))
        iface_element.appendChild(self._attr_node('admin', '1'))
        iface_element.appendChild(self._attr_node('ipv4forwarding', '0'))
        iface_element.appendChild(self._attr_node('ipv4rpfilter', '0'))
        iface_element.appendChild(self._attr_node('proxyArp', '0'))
        iface_element.appendChild(self._attr_node('mtu', '1280'))
        iface_element.appendChild(self._attr_node('rateLimit', '2000'))
        if vrf_name:
            iface_element.appendChild(self._attr_node('vrf', vrf_name))        
        self.cmdata_element.appendChild(iface_element)
        
    
    def nodeInterfaceDel(self, owner, iface_name):
        dist_name = self.dn_prefix + '/OWNER-%s/ETHER-%s' % (owner, iface_name)
        self.cmdata_element.appendChild(self._dn_node('ETHER', 'delete', dist_name))
    
    
    def getXmlContent(self):
        return self.doc.toprettyxml(indent='  ', encoding='UTF-8')
    
    
    def save(self, filename):
        with open(filename, 'w') as planfile:        
            planfile.write(self.getXmlContent())


class ConfigBCN_A1_S5(object):
    bts_num = 1037
    ipbr_per_bts = 2
    mgw_num = 16
    ipbr_per_mgw = 40
    sgsn_num = 16
    ipbr_per_sgsn = 40
    ada_num = 100
    ipbr_per_ada = 2
    drnc_num = 32
    ipbr_per_drnc = 2    
    ip_num = 128


class ConfigBCN_B2_S7(object):
    bts_num = 1759
    ipbr_per_bts = 2
    mgw_num = 16
    ipbr_per_mgw = 16
    sgsn_num = 16
    ipbr_per_sgsn = 16
    ada_num = 1
    ipbr_per_ada = 1
    drnc_num = 32
    ipbr_per_drnc = 2    
    ip_num = 256
    

class ConfigBCN_A1_S1(object):
    bts_num = 200
    ipbr_per_bts = 2
    mgw_num = 16
    ipbr_per_mgw = 40
    sgsn_num = 16
    ipbr_per_sgsn = 40
    ada_num = 100
    ipbr_per_ada = 2
    drnc_num = 32
    ipbr_per_drnc = 2    
    ip_num = 64


class Generator(object):
    def __init__(self, 
                 fru_name,
                 dn_prefix='RNC-02/IP-1'):
        
        self.element_idx = {'bts': 1, 'mgw': 2, 'sgsn': 3, 'drnc': 4, 'ada': 5}     
        self._vrf_num = 3
        self.create_plan = IPPlanFactory(operation_type='created', 
                                         plan_version=os.getenv('IPPLAN_VER', 'mcRNC4.0'), 
                                         dn_prefix=dn_prefix)
        self.delete_plan = IPPlanFactory(operation_type='delete', 
                                         plan_version=os.getenv('IPPLAN_VER', 'mcRNC4.0'), 
                                         dn_prefix=dn_prefix)
        self._ipbr_id = 1
        self._ip_header = '%d' % (int(os.getenv('HOST_INDEX', '133')) % 256)
        
        self._deployment = None
        self._qnup_list = []
        self._eipu_list = []        
        self._switch_chassis_mapping = {}            
        self._port_list = {}
        self._fru_name = fru_name        
        self.ipbr_counter = 0
        self.ipro_counter = 0
        self.ip_counter = 0
        
        
    def setQNUPList(self, qnup_list):
        self._qnup_list = [qnup.replace('/', '') for qnup in qnup_list]
        
        
    def setEIPUList(self, eipu_list):
        self._eipu_list = [eipu.replace('/', '') for eipu in eipu_list]
        
        
    def setPortInfo(self, port_info):
        self._port_list = {}
        for lmp_name in port_info:
            self._port_list[lmp_name] = port_info[lmp_name].port_list.keys()
            
    
    def setHardwareDeployment(self, deployment):
        self._deployment = deployment
        self._switch_chassis_mapping = {}
        for name in deployment:
            if name.find('LMP') == -1:
                continue
            self._switch_chassis_mapping[self._deployment[name].chassis] = name 

    
    def initialize_capacity_requirement(self):
        if self._fru_name == 'BCNOC-A':
            if len(self._switch_chassis_mapping.keys()) == 6:
                self.config = ConfigBCN_A1_S5()
            elif len(self._switch_chassis_mapping.keys()) == 2:
                self.config = ConfigBCN_A1_S1() # for test
            
        elif self._fru_name == 'BMPP2-B':
            if len(self._switch_chassis_mapping.keys()) == 8:
                self.config = ConfigBCN_B2_S7()
        else:
            self.config = None
        
        self._vrf_num = self.config.ip_num / len(self._qnup_list) / len(self.element_idx.keys())
            
    
    def createAllVRF(self):
        # VRF name format: VRF_<vrf_idx>, vrf_idx starts from 1, 0 is reserved for default
        for idx in range(1, self._vrf_num):
            vrf_name = 'VRF_%d' % idx
            self.create_plan.nodeVRFAdd(str(idx), vrf_name)
            self.delete_plan.nodeVRFDel(vrf_name)
    
    
    def createAllIface(self):
        for eipu in self._eipu_list:
            sfp_port = self._port_list[self._switch_chassis_mapping[self._deployment[eipu].chassis]].pop()
            self.create_plan.nodeInterfaceAdd(eipu, 'eth_vrf0', sfp_port, 'default') 
            for idx in range(1, self._vrf_num):
                sfp_port = self._port_list[self._switch_chassis_mapping[self._deployment[eipu].chassis]].pop()
                self.create_plan.nodeInterfaceAdd(eipu, 'eth_vrf%d' % idx, sfp_port , 'VRF_%d' % idx)
                self.delete_plan.nodeInterfaceDel(eipu, 'eth_vrf%d' % idx)
                
                           
    def createAllIPAddress(self):
        # IP Address format: ip_header.qnup_index.iface_idx.interface_type
        for qnup in self._qnup_list:
            qnup_idx = qnup.split('-')[-1]
            for vrf_idx in range(0, self._vrf_num):
                iface = 'eth_vrf%d' % vrf_idx
                vrf_name = 'VRF_%d' % vrf_idx if vrf_idx != 0 else 'default'
                for element in self.element_idx:
                    address = '%s.%s.%d.%d' % (self._ip_header, qnup_idx, vrf_idx, self.element_idx[element])
                    self.create_plan.nodeIPAdd(qnup, address, iface, vrf_name=vrf_name)
                    self.delete_plan.nodeIPDel(qnup, address, iface)
                    self.ip_counter += 1

   
    def _setIPROInstance(self, ipbr_id, qnup, qnup_idx, element_idx):
        vrf_idx = ipbr_id % self._vrf_num
        vrf_name = 'VRF_%d' % vrf_idx if vrf_idx != 0 else 'default'
        ip_addr = '%s.%s.%d.%d' % (self._ip_header, qnup_idx, vrf_idx, element_idx)
        iface = 'eth_vrf%d' % vrf_idx
        self.create_plan.nodeIPROAdd(qnup, str(ipbr_id), ip_addr, iface, vrf_name)
        self.delete_plan.nodeIPRODel(qnup, str(ipbr_id), ip_addr, iface)
        self.ipro_counter += 1
        
        
    def _createIPROInstance(self, element, element_num, ipbr_num):
        element_idx = self.element_idx[element]
        for interface_idx in range(0, element_num):
            for ipbr_counter in range(0, ipbr_num):
                ipbr_id = self._ipbr_id
                self._ipbr_id += 1
                self.create_plan.nodeIPBRAdd(str(ipbr_id), '%s-%d-%d' % (element.upper(), interface_idx, ipbr_counter),
                                             commit_bw='10000', route_bw='10000', commit_sig_bw='0', commit_dcn_bw='0')
                self.delete_plan.nodeIPBRDel(str(ipbr_id))
                self.ipbr_counter += 1
                
                if element == 'mgw' or element == 'sgsn':
                    qnup = self._qnup_list[ipbr_counter % len(self._qnup_list)]
                    qnup_idx = qnup.split('-')[-1]
                    self._setIPROInstance(ipbr_id, qnup, qnup_idx, element_idx)
                    continue
                
                # This is for element = bts, drnc, ada
                for qnup in self._qnup_list:
                    qnup_idx = qnup.split('-')[-1]
                    if int(qnup_idx) % 2 != ipbr_counter % 2:
                        continue
                    self._setIPROInstance(ipbr_id, qnup, qnup_idx, element_idx)
                
        
    def createIPROBTS(self):
        self._createIPROInstance('bts', self.config.bts_num, self.config.ipbr_per_bts)
        
    def createIPROMGW(self):
        self._createIPROInstance('mgw', self.config.mgw_num, self.config.ipbr_per_mgw)
        
    def createIPROSGSN(self):
        self._createIPROInstance('sgsn', self.config.sgsn_num, self.config.ipbr_per_sgsn)
        
    def createIPROADA(self):
        self._createIPROInstance('ada', self.config.ada_num, self.config.ipbr_per_ada)
        
    def createIPRODRNC(self):
        self._createIPROInstance('drnc', self.config.drnc_num, self.config.ipbr_per_drnc)  
    
    def createCapacityPlanData(self):
        # Interface Type: 
        # IP Format: ip_header.qnup_index.iface_idx.interface_type
        # +-------+----------+--------+-------+---------------++-------+----------+--------+-------+---------------+
        # |  NE   | IPBR_ID  | OWNER  | IFACE | IP Address    ||  NE   | IPBR_ID  | OWNER  | IFACE | IP Address    |
        # +------------------+--------+-------+---------------||------------------+--------+-------+---------------+
        # |       |          | QNUP-0 |       |               ||       |          | QNUP-0 |       |               |
        # |       |          +--------+       +---------------||       |          +--------+       +---------------+
        # |       |          | QNUP-2 |       |               ||       |          | QNUP-1 |       |               |
        # |       | BTS-1-1  +--------+       +---------------||       |          +--------+       +---------------+
        # |       |          | QNUP-4 |       |               ||       |          | QNUP-2 |       |               |
        # |       |          +--------+       +---------------|| IUCS/ |          +--------+       +---------------+
        # |       |          | QNUP-6 |       |               || IUPS/ |          | QNUP-3 |       |               |
        # |  BTS  |----------+--------+       +---------------|| IUR/  |          +--------+       +---------------+
        # |       |          | QNUP-1 |       |               || ADA   |          | QNUP-4 |       |               |
        # |       |          +--------+       +---------------||       |          +--------+       +---------------+
        # |       |          | QNUP-3 |       |               ||       |          | QNUP-5 |       |               |
        # |       | BTS-1-2  +--------+       +---------------||       |          +--------+       +---------------+
        # |       |          | QNUP-5 |       |               ||       |          | QNUP-6 |       |               |
        # |       |          +--------+       +---------------||       |          +--------+       +---------------+
        # |       |          | QNUP-7 |       |               ||       |          | QNUP-7 |       |               |
        # |-------+----------+--------+-------+---------------++-------+----------+--------+-------+---------------+
        self.createAllVRF()
        self.createAllIface()
        self.createAllIPAddress()
        
        self.createIPROSGSN()
        self.createIPROMGW()
        self.createIPROADA()
        self.createIPRODRNC()
        self.createIPROBTS()
        
        
    def CapacityPlan(self, filename_prefix='flash_resource'):
        self.createCapacityPlanData()        
        create_file_name = filename_prefix + '_create.xml'
        delete_file_name = filename_prefix + '_delete.xml'
        self.create_plan.save(create_file_name)
        self.delete_plan.save(delete_file_name)
        return create_file_name, delete_file_name, self.ipbr_counter, self.ipro_counter, self.ip_counter
    
    def SimplePlan(self, ipbr_per_qnup, start_ipbr_id, filename_prefix='flash_resource'):
        iface = 'eth_cm'
        for eipu in self._eipu_list:
            sfp_port = self._port_list[self._switch_chassis_mapping[self._deployment[eipu].chassis]].pop()
            self.create_plan.nodeInterfaceAdd(eipu, iface, sfp_port, 'default')
            self.delete_plan.nodeInterfaceDel(eipu, iface)
        ipro_pool = {}
        self._ipbr_id = start_ipbr_id
        for qnup in self._qnup_list:
            ipro_pool[qnup] = {}            
            qnup_idx = qnup.split('-')[-1].strip()
            for idx in range(1, ipbr_per_qnup + 1):
                ip_addr = '%s.%s.0.%d' % (self._ip_header, qnup_idx, idx)
                
                self.create_plan.nodeIPAdd(qnup, ip_addr, iface)
                self.delete_plan.nodeIPDel(qnup, ip_addr, iface)
                self.create_plan.nodeIPBRAdd(self._ipbr_id, 
                                             'simpleplan-%d' % (self._ipbr_id), '10000000', '10000000', '0', '0')
                self.delete_plan.nodeIPBRDel(self._ipbr_id)
                self.create_plan.nodeIPROAdd(qnup, self._ipbr_id, ip_addr, iface)
                self.delete_plan.nodeIPRODel(qnup,self._ipbr_id, ip_addr, iface)
                
                ipro_pool[qnup]['%d'%self._ipbr_id]={'owner': qnup, 'ip_addr': ip_addr, 
                                                     'iface': iface, 'ipbr_id': '%d' % self._ipbr_id}
                
                self._ipbr_id += 1   
                  
        create_file_name = filename_prefix + '_create.xml'
        delete_file_name = filename_prefix + '_delete.xml'
        self.create_plan.save(create_file_name)
        self.delete_plan.save(delete_file_name)
        return create_file_name, delete_file_name, ipro_pool
        
        

def create_resource_plan_with_hardware_deployment():
    eipu_list = filter(lambda x: x.find('EIPU') != -1, _all_nodes())
    qnup_list = filter(lambda x: x.find('QNUP') != -1, _all_recovery_groups())
    fru_name = _node_software_version('CFPU-0')['CFPU-0'].info.fru_name
    hardware_deployment = _hardware_deployment()
    sfp_port_list = _port_state(admin='disabled')
    
    planner = Generator(fru_name)
    planner.setEIPUList(eipu_list)
    planner.setQNUPList(qnup_list)
    planner.setHardwareDeployment(hardware_deployment)
    planner.setPortInfo(sfp_port_list)
    planner.initialize_capacity_requirement()
    
    return planner.CapacityPlan()
        

def switch_OMU_on_logined_CFPU_to_WO():
    recovery_unit = _get_unit_of_group('/QNOMU')
    states = _show_state(' '.join(recovery_unit))
    active_unit = ''
    for unit in states:
        if states[unit].role == 'ACTIVE' and states[unit].usage == 'ACTIVE':
            active_unit = unit
            break
    node = active_unit.split('/')[1]
    hostname = _exec('echo $HOSTNAME')

    if node != hostname.strip():
        _ctrl_sw('/QNOMU')
    
    _exec('mount -o rw,remount /mnt/sysimg;')
    return 'SUCCESS'
 

def configure_ip_based_route_resource_with_simple_configure(ipbr_per_qnup, deployment=None, node_version=None, start_ipbr_id='3700'):
    eipu_list = filter(lambda x: x.find('EIPU') != -1, _all_nodes())
    qnup_list = filter(lambda x: x.find('QNUP') != -1, _all_recovery_groups())
    if not node_version:
        node_version = _node_software_version('CFPU-0')['CFPU-0'].info.fru_name
    if not deployment:
        deployment = _hardware_deployment()
    sfp_port_list = _port_state(admin='disabled')
    
    planner = Generator(node_version)
    planner.setEIPUList(eipu_list)
    planner.setQNUPList(qnup_list)
    planner.setHardwareDeployment(deployment)
    planner.setPortInfo(sfp_port_list)  

    return planner.SimplePlan(int(ipbr_per_qnup), start_ipbr_id=int(start_ipbr_id))
