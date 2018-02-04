"""Unit Test Cases for Libdmxmsg sending.
#  These test cases are for libdmxmsg.py testing:
#
"""

__author__ = "Pan Haiqin(haiqin.pan@nsn.com)"
__version__ = "$0.0.1$"
__date__ = "$Date: 2010/05/06 09:37:20 $"
__copyright__ = "Copyright (c) 2010 Nokia Siemens Networks, All rights reserved"


import unittest;
from runall import BaseTestCase
from comm.communication import exceptions
from illibgen_subsystem_lib.libdmxmsg import *


#######################################
# Command expect output definitions.
#
###

monitor_ret_1 = '''Start monitoring for family 193B in RU 0700.
Monitored with conditions:
Message  SR:

----------------------------------------------------
Please wait, outputting the remaining frames in buffer...

===Total output 0 frames.===
Interrupted by signal 2, cleaning and exiting.
In total 10 frames sent, 0 lost.
Monitoring buffer empty.'''

monitor_ret_2 = '''Start monitoring for family 193B in RU 0700.
Monitored with conditions:
Message  SR:

----------------------------------------------------
Please wait, outputting the remaining frames in buffer...

===Total output 0 frames.===
Interrupted by signal 2, cleaning and exiting.
In total 10 frames sent, 0 lost.
Monitoring buffer empty. '''



#################
# Unit Test Cases
#
#######################################  

class Test_send_message_to_test_process(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(monitor_ret_1, \
        '''testmon.py -p "-u 0x700 -f 0x193B -V" -c "montest -f 0xffff -- -u 0x700 -f 0x193B -p 0 -d '01 34 56 ff 01 21' -n 10 -t 1" -t 3 -r 3''')
        self.add_mml_response(monitor_ret_2, \
        '''testmon.py -p "-u 0x700 -f 0x193B -V" -c "montest -f 0xffff -- -u 0x700 -f 0x193B -p 0 -d '01 34 56 ff 01 21' -n 10" -t 3 -r 3''')
        self.add_mml_response('0', "echo $?")
        self.mml_responses_completed();

    def test_send_message_to_test_process(self):
        ret = send_message_to_test_process("0x700","0x700","0x193B","0","true")
        print ret
        print monitor_ret_1
        self.assertEqual(ret, monitor_ret_1);  
        ret = send_message_to_test_process("0x700","0x700","0x193B","0","false")
        self.assertEqual(ret, monitor_ret_2);

class Test_send_message_to_test_process_by_libdmxmsg(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(monitor_ret_1, \
        '''testmon.py -p "-u 0X700 -f 0x1941 -V" -c "msgmonstub -u 0X700 -f 0x1941 -p 0 -d '01 34 56 ff 01 21' -n 10 -t 1" -t 3 -r 3''')
        self.add_mml_response(monitor_ret_2, \
        '''testmon.py -p "-u 0X700 -f 0x1941 -V" -c "msgmonstub -u 0X700 -f 0x1941 -p 0 -d '01 34 56 ff 01 21' -n 10" -t 3 -r 3''')
        self.add_mml_response('0', "echo $?")
        self.mml_responses_completed();

        self.mml_responses_completed();

    def test_send_message_to_test_process(self):
        ret = send_message_to_test_process("0x700","0x700","0x193B","0","true")
        print ret
        print monitor_ret_1
        self.assertEqual(ret, monitor_ret_1);  
        ret = send_message_to_test_process("0x700","0x700","0x193B","0","false")
        self.assertEqual(ret, monitor_ret_2);

class Test_send_message_to_test_process_by_libdmxmsg(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(monitor_ret_1, \
        '''testmon.py -p "-u 0X700 -f 0x1941 -V" -c "msgmonstub -u 0X700 -f 0x1941 -p 0 -d '01 34 56 ff 01 21' -n 10 -t 1" -t 3 -r 3''')
        self.add_mml_response(monitor_ret_2, \
        '''testmon.py -p "-u 0X700 -f 0x1941 -V" -c "msgmonstub -u 0X700 -f 0x1941 -p 0 -d '01 34 56 ff 01 21' -n 10" -t 3 -r 3''')
        self.add_mml_response('0', "echo $?")
        self.mml_responses_completed();

    def test_send_message_to_test_process_by_libdmxmsg(self):
        ret = send_message_to_test_process_by_libdmxmsg("0X700","0X700","0x1941","0","true")
        self.assertEqual(ret, monitor_ret_1);  
        ret = send_message_to_test_process_by_libdmxmsg("0X700","0X700","0x1941","0","false")
        self.assertEqual(ret, monitor_ret_2); 

class Test_send_message_to_test_process_with_condition_by_libdmxmsg(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(monitor_ret_1, \
        '''testmon.py -p "-u 0X700 -f 0x1941 -V -c "R:"" -c "msgmonstub -u 0X700 -f 0x1941 -p 0 -d '01 34 56 ff 01 21' -n 10" -t 3 -r 3''')
        self.add_mml_response(monitor_ret_2, \
        '''testmon.py -p "-u 0X700 -f 0x1942 -V -c ":NUM=FF01"" -c "msgmonstub -u 0X700 -f 0x1942 -p 0 -d '01 34 56 ff 01 21' -n 10" -t 3 -r 3''')
        self.add_mml_response('0', "echo $?")
        self.mml_responses_completed();

    def test_send_message_to_test_process_with_condition_by_libdmxmsg(self):
        ret = send_message_to_test_process_with_condition_by_libdmxmsg("0X700","0X700","0x1941","0",'''"R:"''')
        self.assertEqual(ret, monitor_ret_1);
        ret = send_message_to_test_process_with_condition_by_libdmxmsg("0X700","0X700","0x1942","0",'''":NUM=FF01"''')
        self.assertEqual(ret, monitor_ret_2);

msg_buf = '''MONITORING TIME: 2010-05-05    23:03:30.932169    000E3949 4BE1F942
RECEIVED BY: 1941 0000 00
BOTTOM: 7002 1941 0000 00 00 00 00 EB7A 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 4002 1940 FFFF 00 01 0000 FF01 0700
01 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.932243    000E3993 4BE1F942
SENT BY: 1942 FFFF 00
BOTTOM: 4002 1942 FFFF 00 00 00 00 EB7A 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 7002 1940 FFFF 00 01 0000 FF01 0700
01 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.932409    000E3A39 4BE1F942
RECEIVED BY: 1941 0000 00
BOTTOM: 7002 1941 0000 00 00 00 00 EB7C 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 4002 1940 FFFF 00 01 0000 FF01 0700
02 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.932455    000E3A67 4BE1F942
SENT BY: 1942 FFFF 00
BOTTOM: 4002 1942 FFFF 00 00 00 00 EB7C 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 7002 1940 FFFF 00 01 0000 FF01 0700
02 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.932525    000E3AAD 4BE1F942
RECEIVED BY: 1941 0000 00
BOTTOM: 7002 1941 0000 00 00 00 00 EB7E 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 4002 1940 FFFF 00 01 0000 FF01 0700
03 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.932571    000E3ADB 4BE1F942
SENT BY: 1942 FFFF 00
BOTTOM: 4002 1942 FFFF 00 00 00 00 EB7E 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 7002 1940 FFFF 00 01 0000 FF01 0700
03 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.932640    000E3B20 4BE1F942
RECEIVED BY: 1941 0000 00
BOTTOM: 7002 1941 0000 00 00 00 00 EB80 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 4002 1940 FFFF 00 01 0000 FF01 0700
04 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.932686    000E3B4E 4BE1F942
SENT BY: 1942 FFFF 00
BOTTOM: 4002 1942 FFFF 00 00 00 00 EB80 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 7002 1940 FFFF 00 01 0000 FF01 0700
04 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.932753    000E3B91 4BE1F942
RECEIVED BY: 1941 0000 00
BOTTOM: 7002 1941 0000 00 00 00 00 EB82 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 4002 1940 FFFF 00 01 0000 FF01 0700
05 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.932799    000E3BBF 4BE1F942
SENT BY: 1942 FFFF 00
BOTTOM: 4002 1942 FFFF 00 00 00 00 EB82 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 7002 1940 FFFF 00 01 0000 FF01 0700
05 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.932867    000E3C03 4BE1F942
RECEIVED BY: 1941 0000 00
BOTTOM: 7002 1941 0000 00 00 00 00 EB84 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 4002 1940 FFFF 00 01 0000 FF01 0700
06 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.932910    000E3C2E 4BE1F942
SENT BY: 1942 FFFF 00
BOTTOM: 4002 1942 FFFF 00 00 00 00 EB84 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 7002 1940 FFFF 00 01 0000 FF01 0700
06 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.933031    000E3CA7 4BE1F942
RECEIVED BY: 1941 0000 00
BOTTOM: 7002 1941 0000 00 00 00 00 EB86 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 4002 1940 FFFF 00 01 0000 FF01 0700
07 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.933078    000E3CD6 4BE1F942
SENT BY: 1942 FFFF 00
BOTTOM: 4002 1942 FFFF 00 00 00 00 EB86 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 7002 1940 FFFF 00 01 0000 FF01 0700
07 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.933147    000E3D1B 4BE1F942
RECEIVED BY: 1941 0000 00
BOTTOM: 7002 1941 0000 00 00 00 00 EB88 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 4002 1940 FFFF 00 01 0000 FF01 0700
08 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.933192    000E3D48 4BE1F942
SENT BY: 1942 FFFF 00
BOTTOM: 4002 1942 FFFF 00 00 00 00 EB88 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 7002 1940 FFFF 00 01 0000 FF01 0700
08 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.933261    000E3D8D 4BE1F942
RECEIVED BY: 1941 0000 00
BOTTOM: 7002 1941 0000 00 00 00 00 EB8A 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 4002 1940 FFFF 00 01 0000 FF01 0700
09 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.933306    000E3DBA 4BE1F942
SENT BY: 1942 FFFF 00
BOTTOM: 4002 1942 FFFF 00 00 00 00 EB8A 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 7002 1940 FFFF 00 01 0000 FF01 0700
09 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.933373    000E3DFD 4BE1F942
RECEIVED BY: 1941 0000 00
BOTTOM: 7002 1941 0000 00 00 00 00 EB8C 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 4002 1940 FFFF 00 01 0000 FF01 0700
0A 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:30.933417    000E3E29 4BE1F942
SENT BY: 1942 FFFF 00
BOTTOM: 4002 1942 FFFF 00 00 00 00 EB8C 000E 00 00 0000 00000000
MONITORED MESSAGE: 0020 7002 1940 FFFF 00 01 0000 FF01 0700
0A 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 
'''
msg_buf_1 = '''
MONITORING TIME: 2010-05-05    23:03:13.744688    000B5CF0 4BE1F931
RECEIVED BY: 193B 0000 00
BOTTOM: 0700 193B 0000 00 00 00 00 E31F 0700 00 00 0000 00000000
MONITORED MESSAGE: 0020 0700 FC00 0000 00 11 0000 FF02 0700
01 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:13.744773    000B5D45 4BE1F931
SENT BY: 193B 0000 00
BOTTOM: 0700 193B 0000 00 00 00 00 0000 0700 00 00 0000 00000000
MONITORED MESSAGE: 0020 0700 FC00 0000 00 11 0000 FF02 0700
01 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:13.744805    000B5D65 4BE1F931
SENT BY: 193B 0000 00
BOTTOM: 7002 193B 0000 00 00 00 00 0000 0700 00 00 0000 00000000
MONITORED MESSAGE: 0020 7002 193B 0001 00 19 0000 FF02 0700
01 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:13.744955    000B5DFB 4BE1F931
RECEIVED BY: 193B 0001 00
BOTTOM: 7002 193B 0001 00 00 00 00 0000 0700 00 00 0000 00000000
MONITORED MESSAGE: 0020 7002 193B 0000 00 19 0000 FF02 0700
01 34 56 FF 01 21 00 00 00 00 00 00 00 00 00 00 

MONITORING TIME: 2010-05-05    23:03:13.744984    000B5E18 4BE1F931
RECEIVED BY: 193B 0000 00
BOTTOM: 0700 193B 0000 00 00 00 00 E320 0700 00 00 0000 00000000
MONITORED MESSAGE: 0011 0700 FC00 0000 00 11 0000 FF03 0700
00 

MONITORING TIME: 2010-05-05    23:03:13.744996    000B5E24 4BE1F931
SENT BY: 193B 0000 00
BOTTOM: 0700 193B 0000 00 00 00 00 E320 0700 00 00 0000 00000000
MONITORED MESSAGE: 0011 0700 FC00 0000 00 11 0000 FF03 0700
00 

'''
class Test_message_count_should_be_correct(BaseTestCase):

    def test_message_count_should_be_correct(self):
        ret = message_count_should_be_correct(msg_buf_1,"true")
        self.assertEqual(ret, "success");
        ret = message_count_should_be_correct(msg_buf,"false")
        self.assertEqual(ret, "success");

class Test_received_message_order_should_be_consistent_with_send(BaseTestCase):

    def test_received_message_order_should_be_consistent_with_send(self):
        ret = received_message_order_should_be_consistent_with_send(msg_buf)
        self.assertEqual(ret, "success");

class Test_address_for_received_message_should_be_correct(BaseTestCase):

    def test_address_for_received_message_should_be_correct(self):
        ret = address_for_received_message_should_be_correct("0x7002","0x7002",msg_buf)
        self.assertEqual(ret, "success");
