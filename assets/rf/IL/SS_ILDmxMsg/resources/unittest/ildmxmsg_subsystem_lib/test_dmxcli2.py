import unittest
from runall import BaseTestCase
from comm.communication import exceptions
from comm.communication.exceptions import ILException

from  ildmxmsg_subsystem_lib.dmxcli2 import *


dummy_str = """
successful
"""

class Test_Dmxcli2_Sending(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxcli2 -U 100,0,200")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmxcli2_sending("-U 100,0,200")

class Test_Dmxcli2_Query_unit_status(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxcli2 -Q 127")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmxcli2_Query_unit_status("127")

class Test_Dmxcli2_Update_unit_status(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxcli2 -U 127")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmxcli2_Update_unit_status("127")

class Test_Dmxcli2_Query_own_phys_addr(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxcli2 -o")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmxcli2_Query_own_phys_addr()

class Test_Dmxcli2_Update_unit_state(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxcli2 -u 127=1")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmxcli2_Update_unit_state("127","1")

class Test_Dmxcli2_Update_unit_co(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxcli2 -c 127=0x1")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmxcli2_Update_unit_co("127","1","0")

class Test_Dmxcli2_Query_comp_table(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxcli2 -q 127,1")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmxcli2_Query_comp_table("127","1")

class Test_Dmxcli2_Query_Phys_Addr(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxcli2 -t 127,1")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmxcli2_Query_Phys_Addr("127","1")

class Test_Dmxcli2_Query_and_Fill(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxcli2 -p 127")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmxcli2_Query_and_Fill("127")

class Test_Dmxcli2_send_msg(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxcli2 -s 127")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmxcli2_send_msg("127")

class Test_Dmxcli2_recv_msg(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxcli2 -r 127")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmxcli2_recv_msg("127")

class Test_Dmxcli2_launch_command(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxcli2 command 888")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmxcli2_launch_command("command","888")

class Test_Dmxcli2_Config_comp_table(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxcli2 -C 1F0,4FF0,FF7,0,100")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmxcli2_Config_comp_table("1F0","4FF0","FF7","0","100")

class Test_Dmxcli2_Config_grp_addr_1(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxcli2 -G FF7,1,0x102")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmxcli2_Config_grp_addr_1("FF7","2","100")

class Test_Dmxcli2_Config_grp_addr_2(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(dummy_str, "dmxcli2 -G FF7,2,2,0x101")
        self.mml_responses_completed()
    def test_make_dmx_sending(self):
        dmxcli2_Config_grp_addr_2("FF7","2","100","1")
