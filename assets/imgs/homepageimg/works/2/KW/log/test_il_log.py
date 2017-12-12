import unittest
from runall import BaseTestCase
import sys
sys.path.append("../../library/")
from illog_subsystem_lib.il_log import *
from comm.communication import exceptions

echo_out = """
0

"""

log_out_success ="""
FAM PROC FOC: TISERO 11 22 33
WRITE TIME  : 2009-1-4 07:49:01:512 UNIT: OMU-1     NUM: 2
PARAMETERS  : T CPL TEXT    COUNT: 26
USER TEXT   :
USER DATA   : dxsyslog:|dxsyslog case 2: 0x123456789
"""

log_out_norecord = """
no such log
"""

log_out_wrong = """
unknown input, -h for help
"""


class Test_interrogate_log(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(log_out_success, "ILlogdisp  unit=OMU-1 famid=11 proc=22 focus=33 level=test > tmp.txt")
        self.add_mml_response("""
        0
        ""","echo $?")
        self.add_mml_response(log_out_norecord, "ILlogdisp  unit=XYZ  ")
        self.add_mml_response("""
        0
        ""","echo $?")
        self.add_mml_response(log_out_wrong, "ILlogdisp  XYZ  ")
        self.add_mml_response("""
        0
        ""","echo $?")
        self.mml_responses_completed()
    def test_interrogate_log(self):
        result = interrogate_log("tmp.txt", "", "unit=OMU-1", "famid=11 proc=22 focus=33", "level=test")
        self.assertEqual(result, log_out_success)
        result = interrogate_log("", "", "unit=XYZ")
        self.assertEqual(result, log_out_norecord)
        result = interrogate_log("", "", "XYZ")
        self.assertEqual(result, log_out_wrong)












