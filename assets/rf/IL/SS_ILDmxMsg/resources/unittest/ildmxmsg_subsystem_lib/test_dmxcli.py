import unittest
from runall import BaseTestCase
from comm.communication import exceptions
from comm.communication.exceptions import ILException

from ildmxmsg_subsystem_lib.dmxcli import *

dummy_str = """
successful
"""

class Test_Dmxcli(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxcli -s 0:ad9c:0 -r 1700:44d:0 -b 1 -i 1 -n 10 -l 200 -m 0 -t 30")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        make_dmx_sending("0:ad9c:0","1700:44d:0","1","1","10","200","0","30")

class Test_Dmxcli_Group(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxcli -s 0:ad9c:0 -r 1700:45b:0 -b 1 -i 1 -n 10 -l 200 -m 0 -t 30 -G FFB,4,0,100,1300,1700 -B 1 -I 1 -N 1 -A 0")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        make_dmx_sending("0:ad9c:0","1700:45b:0","1","1","10","200","0","30","FFB,4,0,100,1300,1700","1","1","1","0")
