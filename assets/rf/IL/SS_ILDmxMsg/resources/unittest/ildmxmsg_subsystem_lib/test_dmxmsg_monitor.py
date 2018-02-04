import unittest
from runall import BaseTestCase
from comm.communication import exceptions
from comm.communication.exceptions import ILException

from ildmxmsg_subsystem_lib.dmx_se_monitor import *


dummy_str = """
hello_word
"""

dummy_int = """
0
"""



class Test_Start_Se_Monitor(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "mkdir -p /tmp/monitor_log")
        self.add_mml_response(dummy_str, '/opt/nsn/SS_ILFT/bin/dmxmsg_monitor_daemon -p 5888 -f 1101 -n 2 -c "[src_phy]=5888">/tmp/monitor_log/dmxmsg_monitor_daemon.log 2>&1 &')
        self.mml_responses_completed()
    def test_start_se_monitor(self):
        start_se_monitor("5888","1101","[src_phy]=5888","2")

class Test_Get_Se_Monitored_Msg_Num(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_int, "cat /tmp/monitor_log/dmxmsg_monitor_daemon.log|grep BOTTOM|wc -l")
        self.mml_responses_completed()
    def test_get_se_monitored_msg_num(self):
        result = get_se_monitored_msg_num()

class Test_Remove_Monitor_And_Log_File(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "kill -SIGINT `ps -ef|grep dmxmsg_monitor_daemon|grep -v grep|awk '{print $2}'`")
        self.add_mml_response(dummy_str, "rm -rf /tmp/monitor_log")
        self.mml_responses_completed()
    def test_remove_monitor_and_log_file(self):
        remove_monitor_and_log_file()
