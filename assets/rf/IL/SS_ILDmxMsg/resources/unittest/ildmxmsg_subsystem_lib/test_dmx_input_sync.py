import unittest
from runall import BaseTestCase
from comm.communication import exceptions
from comm.communication.exceptions import ILException

from ildmxmsg_subsystem_lib.dmx_input_sync import *


dummy_str = """
successful
"""

class Test_input_sync_recv_daemon(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "mkdir -p /tmp/input_sync_daemon_log")
        self.add_mml_response(dummy_str, 'dmx_input_sync_daemon -f 22222 -n 2 -s "100:101">/tmp/input_sync_daemon_log/daemon.log 2>&1 &')
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        start_recv_daemon("22222","2","100:101")

class Test_input_sync_run_case(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxtstste -R 0")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        run_test_case("0")

class Test_input_sync_kill_daemon(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "kill -SIGINT `ps -ef|grep dmx_input_sync_daemon|grep -v grep|awk '{print $2}'`")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        kill_input_sync_daemon()






