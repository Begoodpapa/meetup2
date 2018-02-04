from comm.communication import exceptions
from runall import BaseTestCase
from iltransport_subsystem_lib import il_caclib as transutil_resource
from iltransport_subsystem_lib.il_caclib import create_iub_leg_with_cac_params, \
    create_iucs_leg_with_cac_params, create_iur_leg_with_cac_params

rel_udp_success = """
Release UDP connection successfully.
IP:   10.10.10.10
Port: 1026
"""
rel_udp_failed = """

Release UDP Connection Failed
Error Code:   3150
"""
class Test_release_udp_conn_resource(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(rel_udp_success, \
                """iltrmcli -D -u 10.10.10.10:1026""")
        self.add_mml_response(rel_udp_failed, \
                """iltrmcli -D -u 10.10.10.10:1027""")
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()

    def test_release_udp_conn_resource_success(self):
        output = transutil_resource.release_udp_conn_resource("10.10.10.10", "1026")
        self.assertEqual(output.result, "success")
    def test_release_udp_conn_resource_failed(self):
        output = transutil_resource.release_udp_conn_resource("10.10.10.10", "1027")
        self.assertEqual(output.result, "failed")

rel_gtp_success = """

Release GTP Connection Success
IP:   10.10.10.10
teid: 1026
"""
rel_gtp_failed = """

Release GTP Connection Failed
Error Code:   3150
"""
class Test_release_gtp_conn_resource(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(rel_gtp_success, \
                """iltrmcli -D -g 0x1026""")
        self.add_mml_response(rel_gtp_failed, \
                """iltrmcli -D -g 0x1027""")
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()

    def test_release_gtp_conn_resource_success(self):
        output = transutil_resource.release_gtp_conn_resource("10.10.10.10", "1026")
        print "*" * 100
        print output
        print "*" * 100
        self.assertEqual(output.result, "success")

    def test_release_gtp_conn_resource_failed(self):
        output = transutil_resource.release_gtp_conn_resource("10.10.10.10", "1027")
        self.assertEqual(output.result, "failed")

rel_all_udp_success = """
Release Multi-Connection resource in CACPRB Result: Success


"""
class Test_release_all_udp_conn_resource(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(rel_all_udp_success, \
                """iltrmcli -D -u all""")
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()

    def test_release_all_gtp_conn_resource(self):
        output = transutil_resource.release_all_udp_conn_resource()
        self.assertEqual(output.result, "success")

class Test_release_all_gtp_conn_resource(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(rel_all_udp_success, \
                """iltrmcli -D -g all""")
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()

    def test_release_all_gtp_conn_resource(self):
        output = transutil_resource.release_all_gtp_conn_resource()
        self.assertEqual(output.result, "success")

class Test_release_all_conn_resource_with_owner_id(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(rel_all_udp_success, \
                """iltrmcli -D -o 1""")
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()

    def test_release_all_conn_resource_with_owner_id(self):
        output = transutil_resource.release_all_conn_resource_with_owner_id("1")
        self.assertEqual(output.result, "success")

class Test_release_all_conn_resource(BaseTestCase):

    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(rel_all_udp_success, \
                """iltrmcli -D -a""")
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()

    def test_release_all_conn_resource(self):
        output = transutil_resource.release_all_conn_resource()
        self.assertEqual(output.result, "success")
one_udp_conn_info = """
======  TRANSPORT RESOURCE INFORMATION LIST  ===================================================================
        IP_ADDR:[TEID/PORT]      TYPE      IPBR_ID      OWNER_ID      BANDWIDTH      OWNER_LOG_ADDR      VRF_ID
----------------------------------------------------------------------------------------------------------------
          192.199.39.3:1026       UDP          1           12              1000              0x1234          64
================================================================================================================
"""
class Test_inquiry_udp_conn_resource_info(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(one_udp_conn_info, \
                """iltrmcli -S -u 10.10.10.10:1026 """)
        self.add_mml_response("""
        0
        """, "echo $?")
        self.add_mml_response('BCN', 'echo $HW_PLATFORM')
        self.mml_responses_completed()

    def test_inquiry_udp_conn_resource_info(self):
        output = transutil_resource.inquiry_udp_conn_resource_info("10.10.10.10", "1026")
        self.assertEqual(output["192.199.39.3:1026"]["type"], "UDP")
        self.assertEqual(output["192.199.39.3:1026"]["ipbr_id"], "1")
        self.assertEqual(output["192.199.39.3:1026"]["owner_id"], "12")
        self.assertEqual(output["192.199.39.3:1026"]["reserve_bw"], "1000")

one_gtp_conn_info = """
======  TRANSPORT RESOURCE INFORMATION LIST  ===================================================================
        IP_ADDR:[TEID/PORT]      TYPE      IPBR_ID      OWNER_ID      BANDWIDTH      OWNER_LOG_ADDR      VRF_ID
----------------------------------------------------------------------------------------------------------------
         192.199.39.3:0x1026       GTP          1           12              1000              0x1234          64
================================================================================================================
"""
class Test_inquiry_gtp_conn_resource_info(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(one_gtp_conn_info, \
                """iltrmcli -S -g 0x1026""")
        self.add_mml_response("""
        0
        """, "echo $?")
        self.add_mml_response('BCN', 'echo $HW_PLATFORM')
        self.mml_responses_completed()

    def test_inquiry_gtp_conn_resource_info(self):
        output = transutil_resource.inquiry_gtp_conn_resource_info("10.10.10.10", "1026")
        self.assertEqual(output["192.199.39.3:1026"]["type"], "GTP")
        self.assertEqual(output["192.199.39.3:1026"]["ipbr_id"], "1")
        self.assertEqual(output["192.199.39.3:1026"]["owner_id"], "12")
        self.assertEqual(output["192.199.39.3:1026"]["reserve_bw"], "1000")

multi_udp_conn_info = """
======  TRANSPORT RESOURCE INFORMATION LIST  ===================================================================
        IP_ADDR:[TEID/PORT]      TYPE      IPBR_ID      OWNER_ID      BANDWIDTH      OWNER_LOG_ADDR      VRF_ID
----------------------------------------------------------------------------------------------------------------
          192.199.39.3:1026       UDP          1           12              1000              0x1234          64
          192.199.39.3:1027       UDP          1           12              1000              0x1234          64
================================================================================================================
"""
class Test_list_all_udp_conn_resource_info(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(multi_udp_conn_info, \
                """iltrmcli -S -u all""")
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()

    def test_list_all_udp_conn_resource_info(self):
        output = transutil_resource.list_all_udp_conn_resource_info()
        self.assertEqual(output["192.199.39.3:1026"]["type"], "UDP")
        self.assertEqual(output["192.199.39.3:1026"]["ipbr_id"], "1")
        self.assertEqual(output["192.199.39.3:1026"]["owner_id"], "12")
        self.assertEqual(output["192.199.39.3:1026"]["reserve_bw"], "1000")

        self.assertEqual(output["192.199.39.3:1027"]["type"], "UDP")
        self.assertEqual(output["192.199.39.3:1027"]["ipbr_id"], "1")
        self.assertEqual(output["192.199.39.3:1027"]["owner_id"], "12")
        self.assertEqual(output["192.199.39.3:1027"]["reserve_bw"], "1000")

multi_gtp_conn_info = """
======  TRANSPORT RESOURCE INFORMATION LIST  ===================================================================
        IP_ADDR:[TEID/PORT]      TYPE      IPBR_ID      OWNER_ID      BANDWIDTH      OWNER_LOG_ADDR      VRF_ID
----------------------------------------------------------------------------------------------------------------
          192.199.39.3:0x1026       GTP          1           12              1000              0x1234          64
          192.199.39.4:0x1026       GTP          1           12              1000              0x1234          64
================================================================================================================
"""
class Test_list_all_gtp_conn_resource_info(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(multi_gtp_conn_info, \
                """iltrmcli -S -g all""")
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()

    def test_list_all_gtp_conn_resource_info(self):
        output = transutil_resource.list_all_gtp_conn_resource_info()
        print '======================================================='
        print output
        print '======================================================='
        self.assertEqual(output["192.199.39.3:1026"]["type"], "GTP")
        self.assertEqual(output["192.199.39.3:1026"]["ipbr_id"], "1")
        self.assertEqual(output["192.199.39.3:1026"]["owner_id"], "12")
        self.assertEqual(output["192.199.39.3:1026"]["reserve_bw"], "1000")

        self.assertEqual(output["192.199.39.4:1026"]["type"], "GTP")
        self.assertEqual(output["192.199.39.4:1026"]["ipbr_id"], "1")
        self.assertEqual(output["192.199.39.4:1026"]["owner_id"], "12")
        self.assertEqual(output["192.199.39.4:1026"]["reserve_bw"], "1000")

multi_owner_conn_info = """
======  TRANSPORT RESOURCE INFORMATION LIST  ===================================================================
        IP_ADDR:[TEID/PORT]      TYPE      IPBR_ID      OWNER_ID      BANDWIDTH      OWNER_LOG_ADDR      VRF_ID
----------------------------------------------------------------------------------------------------------------
          192.199.39.3:1026       GTP          1           12              1000              0x1234          64
          192.199.39.3:1027       UDP          2           12              2000              0x1234          64
================================================================================================================
"""

all_conn_info = """
   IP_ADDR:(Port/TEID)     Type     IPBR ID     Owner ID     Reserve BW
  ---------------------   ------   ---------   ----------   ------------
    192.199.39.3:1026       GTP          1           12         1000
    192.199.39.3:1027       UDP          2           12         2000
"""
class Test_list_all_conn_resource_info(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(multi_owner_conn_info, \
                """iltrmcli -S -a""")
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()

    def test_list_all_conn_resource_info(self):
        output = transutil_resource.list_all_conn_resource_info()
        self.assertEqual(output["192.199.39.3:1026"]["type"], "GTP")
        self.assertEqual(output["192.199.39.3:1026"]["ipbr_id"], "1")
        self.assertEqual(output["192.199.39.3:1026"]["owner_id"], "12")
        self.assertEqual(output["192.199.39.3:1026"]["reserve_bw"], "1000")

        self.assertEqual(output["192.199.39.3:1027"]["type"], "UDP")
        self.assertEqual(output["192.199.39.3:1027"]["ipbr_id"], "2")
        self.assertEqual(output["192.199.39.3:1027"]["owner_id"], "12")
        self.assertEqual(output["192.199.39.3:1027"]["reserve_bw"], "2000")

create_iub_success = """
LGU started at 2010-6-4 14:22:45:887

count: 17

155 terminated, count: 77
/* commad line terminated */
   IP-RESOURCE IN-01 RESERVED SUCCESSFUL
IPv4 Addr: 20.20.20.20 : 1026
5691 lgumo1gx finished

LGU exited at 2010-6-4 14:22:45:908
"""

create_iub_failed = """
LGU started at 2010-6-7 15:33:13:106

count: 17

155 terminated, count: 77
/* commad line terminated */
   /*** IP-RESOURCE RESERVATION FAILED, EC=35f7
   ERROR REASON 0 NOTIF 0 0 0 0 ORIG 0 0 0 0

LGU exited at 2010-6-7 15:33:13:118

"""
class Test_create_iub_leg_with_cac_params(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(create_iub_success, \
                """lgutilgx RRI:USCP-0:123:IN,:,,,45:1::""")
        self.add_mml_response(create_iub_failed, \
                'lgutilgx RRI:USCP-0:123:IN,:,,,46:1::')
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()

    def test_create_iub_leg_with_cac_params_1(self):
        output = create_iub_leg_with_cac_params("123", "45")
        self.assertEqual(output.result, "success")
        self.assertEqual(output.ip, "20.20.20.20")
        self.assertEqual(output.port, "1026")
        self.assertEqual(output.leg_id, "IN-01")
        
    def test_create_iub_leg_with_cac_params_2(self):
        output = create_iub_leg_with_cac_params("123", "46")
        self.assertEqual(output.result, "failed")
        self.assertEqual(output.error_code, "35f7")

create_iucs_success = """
LGU started at 2010-6-7 15:33:40:234

count: 15
155 terminated, count: 76
/* commad line terminated */
 HAND CREATED, USE CALL_ID 2775 TO ACCESS THIS CALL
   IP-RESOURCE OUT RESERVED SUCCESSFUL  FAMILY = 4b4    RM2 HAND = 1 1
IPv4 Addr: 30.30.30.30 : 1026

 DSP-SERVICE: SERV_ID = 80000002
              VCC_ID  = ffffffff

LGU exited at 2010-6-7 15:33:40:253
"""

create_iucs_failed = """
LGU started at 2010-6-7 15:33:42:753

count: 15
155 terminated, count: 76
/* commad line terminated */
 HAND CREATED, USE CALL_ID 2777 TO ACCESS THIS CALL
   /*** IP-RESOURCE RESERVATION FAILED, EC=35f7    RM2 HAND = 3 0
   ERROR REASON 0 NOTIF 0 0 0 0 ORIG 0 0 0 0

LGU exited at 2010-6-7 15:33:42:765

"""
class Test_create_iucs_leg_with_cac_params(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(create_iucs_success, \
                'lgutilgx RRI:USCP-0::OUT,:,,,45:34:: ')
        self.add_mml_response(create_iucs_failed, \
                'lgutilgx RRI:USCP-0::OUT,:,,,46:34:: ')
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()

    def test_create_iucs_leg_with_cac_params_1(self):
        create_iucs_leg_with_cac_params("45")
        output = create_iucs_leg_with_cac_params("45")
        print output
        self.assertEqual(output.result, "success")
        self.assertEqual(output.ip, "30.30.30.30")
        self.assertEqual(output.port, "1026")
        self.assertEqual(output.call_id, "2775")
        
    def test_create_iucs_leg_with_cac_params_2(self):
        output = create_iucs_leg_with_cac_params("46")
        print output
        self.assertEqual(output.result, "failed")
        self.assertEqual(output.error_code, "35f7")  
create_iur_success = """
LGU started at 2010-6-4 14:22:45:887

count: 17

155 terminated, count: 77
/* commad line terminated */
   IP-RESOURCE IN-01 RESERVED SUCCESSFUL
IPv4 Addr: 20.20.20.20 : 1026
5691 lgumo1gx finished

LGU exited at 2010-6-4 14:22:45:908
"""

create_iur_failed = """
LGU started at 2010-6-7 15:33:13:106

count: 17

155 terminated, count: 77
/* commad line terminated */
   /*** IP-RESOURCE RESERVATION FAILED, EC=35f7
   ERROR REASON 0 NOTIF 0 0 0 0 ORIG 0 0 0 0

LGU exited at 2010-6-7 15:33:13:118

"""
class Test_create_iur_leg_with_cac_params(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(create_iur_success, \
                """lgutilgx RRI:USCP-0:123:IN,:,,,45:1::""")
        self.add_mml_response(create_iur_failed, \
                """lgutilgx RRI:USCP-0:123:IN,:,,,46:1::""")
        self.add_mml_response("""
        0
        """, "echo $?")
        self.mml_responses_completed()

    def test_create_iur_leg_with_cac_params_1(self):
        output = create_iur_leg_with_cac_params("123", "45")
        self.assertEqual(output.result, "success")
        self.assertEqual(output.ip, "20.20.20.20")
        self.assertEqual(output.port, "1026")
        self.assertEqual(output.leg_id, "IN-01")
        
    def test_create_iur_leg_with_cac_params_2(self):
        output = create_iur_leg_with_cac_params("123", "46")
        self.assertEqual(output.result, "failed")
        self.assertEqual(output.error_code, "35f7")
