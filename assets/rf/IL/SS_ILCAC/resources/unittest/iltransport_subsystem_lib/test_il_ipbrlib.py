from comm.communication import exceptions
from comm.communication.exceptions import ILException
from runall import BaseTestCase
from iltransport_subsystem_lib import il_ipbrlib as ipbrcli

class Test_add_ip_based_route(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response('', \
                'fsclish -c "add networking ipbr ipbr-id 350 ipbr-name TEST-ID-350 route-bandwidth 10000 committed-bandwidth 10000 committed-sig-bandwidth 1 committed-dcn-bandwidth 1 ifc-nrtdch E-RED ifc-nrthsdpa E-RED"')
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()
    def test_add_ip_based_route(self):
        result = ipbrcli.add_ip_based_route("350","TEST-ID-350","10000","10000","1","1","E-RED","E-RED")
        print result
        self.assertEqual(result["IPBR Add"], "Fail")

class Test_del_ip_based_route(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response('', \
                """fsclish -c "delete networking ipbr ipbr-id 350 ipbr-name TEST-ID-350-1" """)
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()
    def test_del_ip_based_route(self):
        result = ipbrcli.del_ip_based_route("350", "TEST-ID-350-1")
        self.assertEqual(result["IPBR Delete"], "Fail")

class Test_mod_ip_based_route(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response('', \
                'fsclish -c "set networking ipbr ipbr-id 450 ipbr-name TEST_ID_450 route-bandwidth 1000000 committed-bandwidth 1000000 committed-sig-bandwidth 50000 committed-dcn-bandwidth 1000 ifc-nrtdch enabled ifc-nrthsdpa 100 scheduler-type none phb-profile-id 0 dspm-profile-id 0"')
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()
    def test_mod_ip_based_route(self):
        result = ipbrcli.mod_ip_based_route("450", "TEST_ID_450", "1000000", "1000000", "50000", "1000", "enabled", "100", "none", "0", "0")
        self.assertEqual(result["IPBR Modify"], "Fail")

class Test_show_ip_based_route(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response('''
IPBR ID:                1
IPBR name:              ipbr1
Route BW:               1000000 kbps
Committed BW:           513 kbps
Committed DCN BW:       0 kbps
Committed signaling BW: 0 kbps
IFC NRTDCH:             E-RED
IFC NRTHSDPA:           E-RED
Scheduler type:         none
PHB profile ID:         0
DSPM profile ID:        0
Mux enable:             disable
Max mux packets number: 30
Local mux UDP port:     65535
Remote mux UDP port:    65535
Mux UDP DSCP value:     46
''', 
        'fsclish -c "show networking ipbr ipbr-id 1"')
        self.add_mml_response('''

ID    Name             (kbps)    (kbps)    (kbps)  (kbps)  type          MUX
----  ---------------  --------  --------  ------  ------  ------------  -------
1     ipbr1            1000000   513       0       0	      none         disable 
2     ipbr2            1000000   1000      0       0	      none         disable 
3     ipbr3            1000000   1000      0       0	      none         disable 
4     ipbr4            1000000   1000      0       0	      none         disable 
5     ipbr5            1000000   1000      0       0	      none         disable 
6     ipbr6            1000000   1000      0       0	      none         disable 
7     ipbr7            1000000   1000      0       0	      none         disable 
8     ipbr8            1000000   1000      0       0	      none         disable 
9     ipbr9            1000000   1000      0       0	      none         disable 
10    ipbr10           1000000   1000      0       0	      none         disable 
11    ipbr11           1000000   1000      0       0	      none         disable 
13    ipbr13           1000000   1000      0       0	      none         disable 
72    ipbr72           1000000   1000      0       0	      none         disable 
900   ipbr900          1000000   1000      0       0	      none         disable 
1003  qostest1003      1000000   1000000   0       0	      none         disable 
2003  qostest2003      1000000   1000000   0       0	      none         disable 
2500  ipbr2500         10000     1000      0       0	      none         disable 
2501  ipbr2501         10000     1000      0       0	      none         disable 
---------------------------------------------------------------------------------
Total IPBR count: 162 

''', 'fsclish -c "show networking ipbr "')
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()
    def test_show_ip_based_route(self):
        result = ipbrcli.show_ip_based_route("1")
        expect_result = {'result': 'SUCCESS', 'IPBR name': 'ipbr1', 'Local mux UDP port': '65535', 'Committed signaling BW': '0', 'Remote mux UDP port': '65535', 'Scheduler type': 'none', 'IPBR ID': '1', 'Committed DCN BW': '0', 'IFC NRTDCH': 'E-RED', 'Route BW': '1000000', 'Mux UDP DSCP value': '46', 'Max mux packets number': '30', 'Mux enable': 'disable', 'DSPM profile ID': '0', 'IFC NRTHSDPA': 'E-RED', 'PHB profile ID': '0', 'Committed BW': '513'}
        self.assertEqual(result, expect_result)
    def test_show_ip_base_route_list(self):
        result = ipbrcli.show_ip_based_route()
        expect_result =  {'11': {'route_bw': '1000000', 'name': 'ipbr11', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '1000', 'sig_bw': '0', 'id': '11'}, '10': {'route_bw': '1000000', 'name': 'ipbr10', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '1000', 'sig_bw': '0', 'id': '10'}, '13': {'route_bw': '1000000', 'name': 'ipbr13', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '1000', 'sig_bw': '0', 'id': '13'}, 'total': '162', 'result': 'SUCCESS', 'Total IPBR count': '162', '900': {'route_bw': '1000000', 'name': 'ipbr900', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '1000', 'sig_bw': '0', 'id': '900'}, '1': {'route_bw': '1000000', 'name': 'ipbr1', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '513', 'sig_bw': '0', 'id': '1'}, '2003': {'route_bw': '1000000', 'name': 'qostest2003', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '1000000', 'sig_bw': '0', 'id': '2003'}, '3': {'route_bw': '1000000', 'name': 'ipbr3', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '1000', 'sig_bw': '0', 'id': '3'}, '2': {'route_bw': '1000000', 'name': 'ipbr2', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '1000', 'sig_bw': '0', 'id': '2'}, '5': {'route_bw': '1000000', 'name': 'ipbr5', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '1000', 'sig_bw': '0', 'id': '5'}, '4': {'route_bw': '1000000', 'name': 'ipbr4', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '1000', 'sig_bw': '0', 'id': '4'}, '7': {'route_bw': '1000000', 'name': 'ipbr7', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '1000', 'sig_bw': '0', 'id': '7'}, '6': {'route_bw': '1000000', 'name': 'ipbr6', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '1000', 'sig_bw': '0', 'id': '6'}, '9': {'route_bw': '1000000', 'name': 'ipbr9', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '1000', 'sig_bw': '0', 'id': '9'}, '8': {'route_bw': '1000000', 'name': 'ipbr8', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '1000', 'sig_bw': '0', 'id': '8'}, '2500': {'route_bw': '10000', 'name': 'ipbr2500', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '1000', 'sig_bw': '0', 'id': '2500'}, '1003': {'route_bw': '1000000', 'name': 'qostest1003', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '1000000', 'sig_bw': '0', 'id': '1003'}, '2501': {'route_bw': '10000', 'name': 'ipbr2501', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '1000', 'sig_bw': '0', 'id': '2501'}, '72': {'route_bw': '1000000', 'name': 'ipbr72', 'mux': 'disable', 'schedule_type': 'none', 'dcn_bw': '0', 'cmmt_bw': '1000', 'sig_bw': '0', 'id': '72'}}

        self.assertEqual(result, expect_result)

class Test_add_ipro(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response('', 'fsclish -c "add networking ipro ipbr-id 1 owner /SITPIUBRG ip-address 192.199.35.35 iface ether1_1"')
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()
    def test_add_ipro(self):
        result = ipbrcli.add_ipro("1", "192.199.35.35", "/SITPIUBRG", "ether1_1")
        self.assertEqual(result["IPRO Add"], "Fail")

class Test_delete_ipro(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response('', 'fsclish -c "delete networking ipro ipbr-id 1 owner /SITPIUBRG ip-address 192.199.35.35 iface ether1_1"')
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()

    def test_del_ipro(self):
        result = ipbrcli.delete_ipro("1", "192.199.35.35", "/SITPIUBRG", "ether1_1")
        self.assertEqual(result["IPRO Delete"], "Fail")

class Test_show_ipro(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(
'''
IPBR ID  IP address       Owner           Interface        PHB set                VRF
-------  ---------------  ---------  	---------------  ---------------------  ---------------
1        191.251.10.3     /EITPUPTRMRG-0  ethtest20        EF,AF4,AF3,AF2,AF1,BE   default
---------------------------------------------------------------------------------------------
''', 
        'fsclish -c "show networking ipro ipbr-id 1 owner /EITPUPTRMRG-0 ip-address 191.251.10.3 iface ethtest20"')
        self.add_mml_response(
'''
IPBR ID  IP address       Owner          Interface        PHB set                VRF
-------  ---------------  ---------      ---------------  ---------------------  ---------------
1         191.251.10.3    /EITPUPTRMRG-0 ethtest20        EF,AF4,AF3,AF2,AF1,BE   default
2         191.251.10.2    /EITPUPTRMRG-0 ethtest20        EF,AF4,AF3              1
---------------------------------------------------------------------------------------------
''', 
        'fsclish -c "show networking ipro  owner /EITPUPTRMRG-0"')
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()

    def test_show_ipro(self):
        result = ipbrcli.show_ipro('1', '191.251.10.3', '/EITPUPTRMRG-0', 'ethtest20')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].iface, 'ethtest20')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].ip_address, '191.251.10.3')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].owner, '/EITPUPTRMRG-0')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].phb_set.af1, 'on')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].phb_set.af2, 'on')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].phb_set.af3, 'on')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].phb_set.af4, 'on')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].phb_set.be,  'on')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].phb_set.ef,  'on')
        #self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].vrf,  'default')
    
    def test_show_ipro_list(self):
        result = ipbrcli.show_ipro('','','/EITPUPTRMRG-0','')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].ipbr_id, '1')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].iface, 'ethtest20')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].ip_address, '191.251.10.3')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].owner, '/EITPUPTRMRG-0')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].phb_set.af1, 'on')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].phb_set.af2, 'on')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].phb_set.af3, 'on')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].phb_set.af4, 'on')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].phb_set.be,  'on')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].phb_set.ef,  'on')
        self.assertEqual(result['1@191.251.10.3@ethtest20@/EITPUPTRMRG-0'].vrf,  'default')
        
        self.assertEqual(result['2@191.251.10.2@ethtest20@/EITPUPTRMRG-0'].iface, 'ethtest20')
        self.assertEqual(result['2@191.251.10.2@ethtest20@/EITPUPTRMRG-0'].ipbr_id, '2')
        self.assertEqual(result['2@191.251.10.2@ethtest20@/EITPUPTRMRG-0'].ip_address, '191.251.10.2')
        self.assertEqual(result['2@191.251.10.2@ethtest20@/EITPUPTRMRG-0'].owner, '/EITPUPTRMRG-0')
        self.assertEqual(result['2@191.251.10.2@ethtest20@/EITPUPTRMRG-0'].phb_set.af1, 'off')
        self.assertEqual(result['2@191.251.10.2@ethtest20@/EITPUPTRMRG-0'].phb_set.af2, 'off')
        self.assertEqual(result['2@191.251.10.2@ethtest20@/EITPUPTRMRG-0'].phb_set.af3, 'on')
        self.assertEqual(result['2@191.251.10.2@ethtest20@/EITPUPTRMRG-0'].phb_set.af4, 'on')
        self.assertEqual(result['2@191.251.10.2@ethtest20@/EITPUPTRMRG-0'].phb_set.be,  'off')
        self.assertEqual(result['2@191.251.10.2@ethtest20@/EITPUPTRMRG-0'].phb_set.ef,  'on')
        self.assertEqual(result['2@191.251.10.2@ethtest20@/EITPUPTRMRG-0'].vrf,  '1')

class Test_add_ip_address(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response('', \
                """fsclish -m -c "add networking  address dedicated /QNUP-0 iface ether1 ip-address 123.211.231.111" """)
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()
    def test_add_ip_address(self):
        result = ipbrcli.add_ip_address("/QNUP-0", "ether1", "123.211.231.111")
        self.assertEqual(result, "successfully")

class Test_delete_ip_address(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response('successfully', \
                """fsclish -m -c "delete networking  address dedicated /QNUP-0 iface ether1 ip-address 123.211.231.111" """)
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()
    def test_delete_ip_address(self):
        result = ipbrcli.delete_ip_address("/QNUP-0", "ether1", "123.211.231.111")
        self.assertEqual(result, "successfully")

ipbr_measurement_result = """
<PMMOResult>
    <MO>
        <DN>FPTEST-BCN_10/ip_route_id-1024</DN>
    </MO>
    <PMTarget measurementType="IP_based_route">
        <M568C0>234</M568C0>
        <M568C1>567</M568C1>
        <M568C2>325</M568C2>
        <M568C3>1234</M568C3>
        <M568C4>2341</M568C4>
        <M568C5>12312</M568C5>
        <M568C6>1212</M568C6>
        <M568C7>1231</M568C7>
        <M568C8>12312</M568C8>
        <M568C9>2321</M568C9>
        <M568C10>0</M568C10>
        <M568C11>0</M568C11>
        <M568C12>0</M568C12>
        <M568C13>0</M568C13>
        <M568C14>0</M568C14>
        <M568C15>0</M568C15>
        <M568C16>0</M568C16>
        <M568C17>0</M568C17>
        <M568C18>0</M568C18>
        <M568C19>0</M568C19>
        <M568C20>0</M568C20>
        <M568C21>0</M568C21>
        <M568C22>0</M568C22>
    </PMTarget>
</PMMOResult>
"""
class Test_get_ipbr_measurement_result(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(ipbr_measurement_result, 'cat hello_world')
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()
    def test_get_ipbr_measurement_result(self):
        result = ipbrcli.get_ipbr_measurement_result("hello_world")
        self.assertEqual(result['1024']["M568C0"], "234")
        self.assertEqual(result['1024']["M568C1"], "567")
        self.assertEqual(result['1024']["M568C2"], "325")
        self.assertEqual(result['1024']["M568C3"], "1234")
        self.assertEqual(result['1024']["M568C4"], "2341")
        self.assertEqual(result['1024']["M568C5"], "12312")
        self.assertEqual(result['1024']["M568C6"], "1212")
        self.assertEqual(result['1024']["M568C7"], "1231")
        self.assertEqual(result['1024']["M568C8"], "12312")
        self.assertEqual(result['1024']["M568C9"], "2321")
ip_show_out = """
IP addresses in default instance:
 ether1_1
   type        : dedicated
   address     : 20.30.40.50/0
   owner       : /EITPPXTest
"""
class Test_show_ip_address(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(ip_show_out, 'fsclish -c "show networking address ip-address 192.199.28.1" ')
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()
    def test_show_ip_address(self):
        result = ipbrcli.show_ip_address("192.199.28.1")
        self.assertEqual(result["type"], 'dedicated')
        self.assertEqual(result["address"], '20.30.40.50/0')
        self.assertEqual(result["owner"], '/EITPPXTest')
        self.assertEqual(result["inface"], 'ether1_1')
        
GCU_show_info = """
unit name       utype   uindex  log_add phy_add state   redund          type    MOId    attribute       MOName
VRNC-1          0x5e4   0x1     0x4fff  0x1fff  0x0     0x00000004      0x2     0       0x0
GCU-0           0x5e5   0x0     0x4d01  0x4d01  0x4a    0x00000004      0x2     0       0x0
GCU-1           0x5e5   0x1     0x4d02  0x4d02  0x0     0x00000004      0x2     0       0x0
GCU-2           0x5e5   0x2     0x4d03  0x4d03  0x4a    0x00000004      0x2     0       0x0
"""
class Test_get_GCU_info(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(GCU_show_info, 'ilfunitcli -lx')
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()
    def test_get_GCU_info(self):
        result = ipbrcli.get_GCU_info()
        self.assertEqual(result, '0x0')       
ip_in_GFCPRG_show_ADA = """
eth3
    type        : dedicated
    address     : 193.233.16.1/16
    owner       : /GFCPRG
"""
class Test_select_random_IP_address_and_recovery_group_ADA(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(ip_in_GFCPRG_show_ADA, 'fsclish -c "show networking instance default address"')
        self.add_mml_response('\n0\n', "echo $?")
        self.mml_responses_completed()
   
    def test_select_random_IP_address_and_recovery_group_ADA(self):
        result = ipbrcli.select_random_IP_address_and_recovery_group_ADA('1')
        print result[0]
        self.assertEqual(result[0].iface, "eth3")
        self.assertEqual(result[0].ip_addr, '193.233.16.1')
        self.assertEqual(result[0].rg_name, '/GFCPRG')

