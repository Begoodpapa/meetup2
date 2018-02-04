import unittest
from runall import BaseTestCase
from comm.communication import exceptions
from comm.communication.exceptions import ILException

from ildmxmsg_subsystem_lib.dmx_input_sync_ex import *


dummy_str = """
echo $?
"""

class Test_dmx_generic_stub_recv(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmx_generic_stub recv d903 >generic_log.txt & ")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmx_generic_stub_recv("d903","generic_log.txt")

class Test_dmx_generic_stub_wait_to_recv(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmx_generic_stub recv d903 -w >generic_log.txt&")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmx_generic_stub_wait_to_recv("d903","generic_log.txt")

class Test_dmx_generic_stub_send(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmx_generic_stub send d903 3456 -n 10 -s 5 -p 2 -i 0")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmx_generic_stub_send("d903","3456","10","5","2","0")

class Test_dmx_generic_stub_drop_msg(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmx_generic_stub drop_msg  d903 -n 10")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmx_generic_stub_drop_msg("d903","10")


