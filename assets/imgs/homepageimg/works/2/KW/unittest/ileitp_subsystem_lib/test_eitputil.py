import unittest
from runall import BaseTestCase

from comm.communication import exceptions
from comm.communication.exceptions import ILException
from ileitp_subsystem_lib.eitputil import *

class Test_eitputil_profiling(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)


    def _get_command(self, eipu_name, cmd):
        return 'ssh -oStrictHostKeyChecking=no %s eitpste -f pprofiling %s' % (eipu_name.lower(), cmd)
        
        
    def test_show_eitp_profiling1(self):
        output = '''
Status is | ENABLE_EGRESS | ENABLE_INGRESS |
+---+----------------------------------+------------------------+---------------------+---------------------+
|id |function                          |branch-0                |branch-1             |branch-2             |
|   |                                  |ave   |max   |num       |ave   |max   |num    |ave   |max   |num    |
+---+----------------------------------+------------------------+---------------------+---------------------+
|0  |main_fastdist_handle_frame        |3212  |9648  |705       |0     |0     |0      |0     |0     |0      |
+---+----------------------------------+------------------------+---------------------+---------------------+
|1  |main_fpn_process_input            |3967  |10648 |805       |0     |0     |0      |0     |0     |0      |
+---+----------------------------------+------------------------+---------------------+---------------------+
ave:average cycle; max:maximun cycle; num: calling number.
        '''
        eipu_name = 'EIPU-0'
        command = self._get_command(eipu_name, 'show')
        self.add_mml_response(output, command)
        self.mml_responses_completed()

        result = eitputil_profiling_show(eipu_name)
        
        self.assertEqual(result.status,'ENABLED')
        self.assertEqual(result.egress_ave, 3212)
        self.assertEqual(result.egress_max, 9648)
        self.assertEqual(result.egress_num, 705)
        self.assertEqual(result.ingress_ave, 3967)
        self.assertEqual(result.ingress_max, 10648)
        self.assertEqual(result.ingress_num, 805)

        
    def test_show_eitp_profiling2(self):
        output = '''
Status is | DISABLED |
+---+----------------------------------+------------------------+---------------------+---------------------+
|id |function                          |branch-0                |branch-1             |branch-2             |
|   |                                  |ave   |max   |num       |ave   |max   |num    |ave   |max   |num    |
+---+----------------------------------+------------------------+---------------------+---------------------+
ave:average cycle; max:maximun cycle; num: calling number.
        '''
        eipu_name = 'EIPU-0'
        command = self._get_command(eipu_name, 'show')
        self.add_mml_response(output, command)
        self.mml_responses_completed()

        result = eitputil_profiling_show(eipu_name)
        
        self.assertEqual(result.status,'DISABLED')
            
                
    def test_enable_eitp_profiling(self):
        output = 'Path profiling is enabled.'
        eipu_name = 'EIPU-0'

        command = self._get_command(eipu_name, 'enable')
        self.add_mml_response(output, command)
        command = self._get_command(eipu_name, 'disable')
        self.add_mml_response(output, command)
        self.mml_responses_completed()

        result = eitputil_profiling_enable(eipu_name)        
        self.assertEqual(result, 'True')

        result = eitputil_profiling_disable(eipu_name)        
        self.assertEqual(result, 'False')

        
    def test_disable_eitp_profiling(self):
        output = 'Path profiling is disabled.'
        eipu_name = 'EIPU-0'

        command = self._get_command(eipu_name, 'disable')
        self.add_mml_response(output, command)
        command = self._get_command(eipu_name, 'enable')
        self.add_mml_response(output, command)
        self.mml_responses_completed()

        result = eitputil_profiling_disable(eipu_name)        
        self.assertEqual(result, 'True')

        result = eitputil_profiling_enable(eipu_name)        
        self.assertEqual(result, 'False')


class Test_eitputil_mux(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)

    def test_mux_show_stat(self):
        output = '''
ipbr out_mux          out_muxed        in_mux           in_muxed         in_disc
==== ================ ================ ================ ================ ================
1    334              10000            334              10000            0    
    '''
        ipbr_id = 1
        command = 'eitputil mux show stat ' + str(ipbr_id)
        self.add_mml_response(output, command)
        self.mml_responses_completed()

        result = eitputil_mux_show_stat(ipbr_id)
        self.assertEqual(result.ipbr_id, ipbr_id)
        self.assertEqual(result.out_mux, 334)
        self.assertEqual(result.out_muxed, 10000)
        self.assertEqual(result.in_mux, 334)
        self.assertEqual(result.in_muxed, 10000)
        self.assertEqual(result.in_disc, 0)
       
       
class Test_eitputil_gtp(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.result1 = '''
IuPS measurement counters:
------------------------------------------------------
RNC IP address:                        31.31.31.31
SGSN IP address:                       191.233.102.1
Total input packets:                   75395496
Total input UDP bytes:                 11007742416
Total input IP error bytes:            33
Total input UDP error bytes:           4818
Input TC conversational bytes:         11007742416
Input TC stream bytes:                 0
Input TC interactive bytes:            0
Input TC background bytes:             0
Total output IP packets:               86195499
Total output UDP bytes:                12584542854
Total output IP error bytes:           0
Total output UDP error bytes:          0
Output TC conversational bytes:        12584542854
Output TC stream bytes:                0
Output TC interactive bytes:           0
Output TC background bytes:            0
Echo request received:                 0
Echo response received:                0
Echo response sent:                    0
Error indications received:            0
Error indications sent:                0
Extension header notification received:0

    '''

    def test_gtp_get_iups_counters(self):
        eipu_name = 'EIPU-0'
        ipaddr = 'all'
        command = 'ssh -oStrictHostKeyChecking=no %s eitpste  gtp get iups counters ip-address %s' % (eipu_name.lower(), ipaddr)
        self.add_mml_response(self.result1, command)
        self.mml_responses_completed()

        result = eitputil_gtp_get_iups_counters(eipu_name)
        self.assertEqual(result.eipu, eipu_name)
        self.assertEqual(result.rnc_ip, '31.31.31.31')
        self.assertEqual(result.sgsn_ip, '191.233.102.1')
        self.assertEqual(result.in_ip_packets, '75395496')
        self.assertEqual(result.in_udp_bytes, '11007742416')
        self.assertEqual(result.in_ip_err, '33')
        self.assertEqual(result.in_udp_err, '4818')
        self.assertEqual(result.in_tc_conversational, '11007742416')
        self.assertEqual(result.in_tc_stream, '0')
        self.assertEqual(result.in_tc_interactive, '0')
        self.assertEqual(result.in_tc_background, '0')        
        self.assertEqual(result.out_ip_packets, '86195499')
        self.assertEqual(result.out_udp_bytes, '12584542854')
        self.assertEqual(result.out_ip_err, '0')
        self.assertEqual(result.out_udp_err, '0')
        self.assertEqual(result.out_tc_conversational, '12584542854')
        self.assertEqual(result.out_tc_stream, '0')
        self.assertEqual(result.out_tc_interactive, '0')
        self.assertEqual(result.out_tc_background, '0')
        self.assertEqual(result.echo_request_received, '0')
        self.assertEqual(result.echo_response_received, '0')
        self.assertEqual(result.echo_rresponse_sent, '0')
        self.assertEqual(result.error_indication_received, '0')
        self.assertEqual(result.error_indication_sent, '0')
        self.assertEqual(result.ext_hdr_notif_received, '0')
