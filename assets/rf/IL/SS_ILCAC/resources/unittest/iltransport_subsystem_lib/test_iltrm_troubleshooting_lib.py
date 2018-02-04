from comm.communication import exceptions
from comm.communication.exceptions import ILException
from runall import BaseTestCase
from iltransport_subsystem_lib import iltrm_troubleshooting_lib as troubleshootingcli

class Test_get_ipbr_resource_info(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response('''
Operation started at 2012-5-25 13:20:47:005
IPBR ID                         : 4022
IPBR name                       : BFD-4022
Route bandwidth                 : 0            kbps
Committed bandwidth             : 0            kbps
Committed DCN bandwidth         : 0            kbps
Committed signaling bandwidth   : 0            kbps
Committed user plane bandwidth  : 1000         kbps
Reserved bandwidth              : 0.000        kbps
IFC NRTDCH                      : E-RED
IFC NRTHSDPA                    : E-RED
Scheduler type                  : none
PHB profile ID                  : 0
DSPM profile ID                 : 0
MUX enable                      : disable
Max MUX packets number          : 0
Local MUX UDP port              : 0
Remote MUX UDP port             : 0
MUX UDP DSCP value              : 0
GTP leg number                  : 0
RTP leg number                  : 0
UDP leg number                  : 0
IPBR status                     : Usable

IP address bound with IPBR:

IP Address       VRF ID  Monitor  Status
---------------  ------  -------  ---------
191.148.13.50         0  Yes      WORK     
191.148.13.51         0  Yes      CONN_DOWN

Operation completed at 2012-5-25 13:20:47:007
''', """iltrmcli -S -i4022""")
        self.add_mml_response('\n0\n', "echo $?")
        self.mml_responses_completed()
    def test_get_ipbr_resource_info(self):
        result = troubleshootingcli.get_ipbr_resource_info("4022")
        self.assertEqual(result.ipbr_id, '4022')
        self.assertEqual(result.cmmt_bw, '1000000')
        self.assertEqual(result.res_bw, '0')

class test_get_ip_resource_in_cac(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response('''
Operation started at 2013-11-12 14:19:39:586
                         
IP address       VRF ID  Reserved ports
---------------  ------  --------------
210.148.133.177       0           65535                    

Total IP number: 1
''', """fsclish -c "show troubleshooting cac ip" """)
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()
   
    def test_get_ip_resource_in_cac(self):
        result = troubleshootingcli.get_ip_resource_in_cac()
        self.assertEqual(result['210.148.133.177@0']['ip_add'], '210.148.133.177')
        self.assertEqual(result['210.148.133.177@0']['vrf_id'], '0')
        self.assertEqual(result['210.148.133.177@0']['reserve_port_num'], '65535')
        self.assertEqual(result['Total IP number'], '1')

ipro_show_in_CAC_by_troubleshooting = """
Operation started at 2013-11-12 14:54:12:089

IPBR ID IP Address      VRF ID PHB set            Owner    Monitor Status
------- --------------- ------ ------------------ -------- ------- ---------
   1    191.148.13.3         0 ALL                /QNUP-0  Yes      WORK        
   2    191.148.13.4         0 EF,AF4,AF3,AF2,AF1 /QNUP-1  No      RG_DOWN                

Total IPRO number: 2

Operation completed at 2013-11-12 14:54:12:092
"""
class test_get_ipro_info(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(ipro_show_in_CAC_by_troubleshooting, """fsclish -c "show troubleshooting cac ipro" """ )
        self.add_mml_response('\n0\n', "echo $?")
        self.mml_responses_completed()
   
    def test_get_ipro_info(self):
        result = troubleshootingcli.get_ipro_info_in_cac()
        self.assertEqual(result['2@191.148.13.4@/QNUP-1@0']['ip_addr'], '191.148.13.4')
        self.assertEqual(result['2@191.148.13.4@/QNUP-1@0']['status'], 'RG_DOWN')
        self.assertEqual(result['2@191.148.13.4@/QNUP-1@0']['monitor'], 'No')
        self.assertEqual(result['2@191.148.13.4@/QNUP-1@0']['ipbr_id'], '2')
        self.assertEqual(result['2@191.148.13.4@/QNUP-1@0']['owner'], '/QNUP-1')
        self.assertEqual(result['2@191.148.13.4@/QNUP-1@0']['vrf_id'], '0')
        self.assertEqual(result['2@191.148.13.4@/QNUP-1@0']['phb_set'], 'EF,AF4,AF3,AF2,AF1')
        self.assertEqual(result['Total IPRO number'], '2')
        self.assertEqual(result['1@191.148.13.3@/QNUP-0@0']['ip_addr'], '191.148.13.3')
        self.assertEqual(result['1@191.148.13.3@/QNUP-0@0']['status'], 'WORK')
        self.assertEqual(result['1@191.148.13.3@/QNUP-0@0']['monitor'], 'Yes')
        self.assertEqual(result['1@191.148.13.3@/QNUP-0@0']['ipbr_id'], '1')
        self.assertEqual(result['1@191.148.13.3@/QNUP-0@0']['owner'], '/QNUP-0')
        self.assertEqual(result['1@191.148.13.3@/QNUP-0@0']['vrf_id'], '0')
        self.assertEqual(result['1@191.148.13.3@/QNUP-0@0']['phb_set'], 'ALL')

counter_leg_show_in_CAC_by_troubleshooting = """
Operation started at 2013-12-9 16:27:18:055

Number:
  UDP leg : 65535
  RTP leg : 0
  GTP leg : 1

Capacities:
  UDP and RTP leg : 316298
  GTP leg         : 48000

Operation completed at 2013-12-9 16:27:18:073
"""
class test_get_leg_info(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(counter_leg_show_in_CAC_by_troubleshooting, """fsclish -c "show troubleshooting cac leg" """)
        self.add_mml_response('\n0\n', "echo $?")
        self.mml_responses_completed()
   
    def test_get_leg_info(self):
        result = troubleshootingcli.get_counters_in_cac()
        self.assertEqual(result.rtp_num, '0')
        self.assertEqual(result.udp_num, '65535')
        self.assertEqual(result.gtp_num, '1')
        self.assertEqual(result.udp_rtp_leg_capacity, '316298')
        self.assertEqual(result.gtp_leg_capacity, '48000')

ipbr_list_show_in_CAC_by_troubleshooting = """
Operation started at 2013-12-9 16:24:37:731

Abbreviations:
  CMMT-UP-BW : committed user plane bandwidth
  RES-BW     : reserved bandwidth of the IPBR

                              CMMT-UP-BW RES-BW
ID   Name            Status   (kbps)     (kbps)       GTP leg RTP leg UDP leg
---- --------------- -------- ---------- ------------ ------- ------- -------
4022 BFD-4022        Usable         1000        0.000       0       0       0
4095 ipbr4095        Usable         1000        0.000       0       0       0

Total IPBR number: 2

Sum:
  CMMT-UP-BW : 10048908
  RESV-BW     : 0.000
  GTP leg    : 0
  RTP leg    : 0
  UDP leg    : 0

Operation completed at 2013-12-9 16:24:39:741
"""
class test_get_ipbr_list_info(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(ipbr_list_show_in_CAC_by_troubleshooting, """fsclish -c "show troubleshooting cac ipbr" """)
        self.add_mml_response('\n0\n', "echo $?")
        self.mml_responses_completed()
   
    def test_get_ipbr_list_info(self):
        result = troubleshootingcli.get_ipbr_list_info_in_cac()
        self.assertEqual(result['4022']['ipbr_id'], '4022')
        self.assertEqual(result['4022']['ipbr_name'], 'BFD-4022')
        self.assertEqual(result['4022']['status'], 'Usable')
        self.assertEqual(result['4022']['commit_up_bw'], '1000')
        self.assertEqual(result['4022']['res_bw'], '0')
        self.assertEqual(result['4022']['gtp_leg'], '0')
        self.assertEqual(result['4022']['rtp_leg'], '0')
        self.assertEqual(result['4022']['udp_leg'], '0')
        self.assertEqual(result['Total IPBR number'], '2')
        self.assertEqual(result['4095']['ipbr_id'], '4095')
        self.assertEqual(result['4095']['ipbr_name'], 'ipbr4095')
        self.assertEqual(result['4095']['commit_up_bw'], '1000')
        self.assertEqual(result['4095']['res_bw'], '0')
        self.assertEqual(result['4095']['gtp_leg'], '0')
        self.assertEqual(result['4095']['rtp_leg'], '0')
        self.assertEqual(result['4095']['udp_leg'], '0')
        self.assertEqual(result['Total IPBR number'], '2')
        self.assertEqual(result['Total value']['total committed UP BW'], '10048908')
        self.assertEqual(result['Total value']['total reserve BW'], '0')
        self.assertEqual(result['Total value']['total GTP num'], '0')
        self.assertEqual(result['Total value']['total RTP num'], '0')
        self.assertEqual(result['Total value']['total UDP num'], '0')

owner_show_in_CAC_by_troubleshooting = """
Operation started at 2013-11-12 15:06:18:605

          Bandwidth    
Owner ID  (kbps)        GTP leg  RTP leg  UDP leg
--------  ------------  -------  -------  -------                             
    0x33  10000000.000        2        2        2
    0x32  10000000.000        2        2        2 

Total owner ID number: 2

Operation completed at 2013-11-12 15:06:18:606
"""
class test_get_owner_id_info(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(owner_show_in_CAC_by_troubleshooting, """fsclish -c "show troubleshooting cac owner-id"  """ )
        self.add_mml_response('\n0\n', "echo $?")
        self.mml_responses_completed()
   
    def test_get_owner_id_info(self):
        result = troubleshootingcli.get_owner_id_in_cac()
        self.assertEqual(result['0x33']['rtp_num'], '2')
        self.assertEqual(result['0x33']['udp_num'], '2')
        self.assertEqual(result['0x33']['gtp_num'], '2')
        self.assertEqual(result['0x33']['reserve_bw'], '10000000000')
        self.assertEqual(result['0x33']['owner_id'], '0x33')
        self.assertEqual(result['0x32']['rtp_num'], '2')
        self.assertEqual(result['0x32']['udp_num'], '2')
        self.assertEqual(result['0x32']['gtp_num'], '2')
        self.assertEqual(result['0x32']['reserve_bw'], '10000000000')
        self.assertEqual(result['0x32']['owner_id'], '0x32')

specific_ipbr_show_in_CAC_by_troubleshooting = """
Operation started at 2013-12-9 17:33:26:800

IPBR ID                         : 4022
IPBR name                       : BFD-4022
Route bandwidth                 : 0            kbps
Committed bandwidth             : 0            kbps
Committed DCN bandwidth         : 0            kbps
Committed signaling bandwidth   : 0            kbps
Committed user plane bandwidth  : 1000         kbps
Reserved bandwidth              : 0.000        kbps
IFC NRTDCH                      : E-RED
IFC NRTHSDPA                    : E-RED
Scheduler type                  : none
PHB profile ID                  : 0
DSPM profile ID                 : 0
MUX enable                      : disable
Max MUX packets number          : 0
Local MUX UDP port              : 0
Remote MUX UDP port             : 0
MUX UDP DSCP value              : 0
GTP leg number                  : 0
RTP leg number                  : 0
UDP leg number                  : 0
IPBR status                     : Usable

IP address bound with IPBR:

IP Address       VRF ID  Monitor  Status
---------------  ------  -------  ---------
191.148.13.50         0  Yes      WORK     
191.148.13.51         0  Yes      CONN_DOWN

Operation completed at 2013-12-9 17:33:26:802
#'''
"""
class test_get_specific_ipbr_info(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(specific_ipbr_show_in_CAC_by_troubleshooting, """fsclish -c "show troubleshooting cac ipbr ipbr-id 4022" """)
        self.add_mml_response('\n0\n', "echo $?")
        self.mml_responses_completed()
   
    def test_get_specific_ipbr_info(self):
        result = troubleshootingcli.get_specific_ipbr_info_in_cac('4022')
        self.assertEqual(result.ipbr_id, '4022')
        self.assertEqual(result.ipbr_name, 'BFD-4022')
        self.assertEqual(result.route_bw, '0')
        self.assertEqual(result.cmmt_bw, '0')
        self.assertEqual(result.cmmt_dcn_bw, '0')
        self.assertEqual(result.cmmt_sig_bw, '0')
        self.assertEqual(result.up_bw, '1000')
        self.assertEqual(result.res_bw, '0')
        self.assertEqual(result.ifc_nrtdch, 'E-RED')
        self.assertEqual(result.ifc_nrthsdpa, 'E-RED')
        self.assertEqual(result.scheduler_type, 'none')
        self.assertEqual(result.phb_profile, '0')
        self.assertEqual(result.dspm_profile, '0')
        self.assertEqual(result.mux_enable, 'disable')
        self.assertEqual(result.max_mux_packet, '0')
        self.assertEqual(result.local_mux_port, '0')
        self.assertEqual(result.mux_udp_value, '0')
        self.assertEqual(result.gtp_num, '0')
        self.assertEqual(result.rtp_num, '0')
        self.assertEqual(result.udp_num, '0')
        self.assertEqual(result.ipbr_status, 'Usable')
        self.assertEqual(result.ip_list[0].ip_addr, '191.148.13.50')
        self.assertEqual(result.ip_list[0].vrf_id, '0')
        self.assertEqual(result.ip_list[0].monitor, 'Yes')
        self.assertEqual(result.ip_list[0].status, 'WORK')
        self.assertEqual(result.ip_list[1].ip_addr, '191.148.13.51')
        self.assertEqual(result.ip_list[1].vrf_id, '0')
        self.assertEqual(result.ip_list[1].monitor, 'Yes')
        self.assertEqual(result.ip_list[1].status, 'CONN_DOWN')

