import unittest
from runall import BaseTestCase

from comm.communication import exceptions
from ilnaseva_subsystem_lib.name_server import *

list_service_pid_of_name_server_output="""
Computer   : 4FFE
Family     : 0646
Process Id : 0000
Focus      :   00
Group number    : 0000
Delivery   : 3000
Attr       :   09
"""

get_service_pid_of_name_server_output="""
Computer   : 4FFE
Family     : 0646
Process id : 0000
Focus      :   00
Group      : 0000
Delivery   : 3000
Attr       :   09
"""
list_service_content_of_name_server_output="""
# nasext lc "read_params_as"

CONTENTS OF NAMETABLE


Index         : 0000
Service name  : read_params_as
Real location : 0200
Computer      : 4002
Family        : 0438
Process Id    : 0000
Focus         : 00
Group service : 0
Local service : 0
Replaceable   : 0
Msg group     : 0000
Delivery      : 3000
Attributes    : 09
Number of use : 00000000
Token         : 0
In use        : 1
Can show      : 1"""
list_service_name_of_name_server_output="""# nasext ls read_params_as
LIST SERVICES
Service_Name:read_params_as"""
update_service_pid_of_name_server_output='Update ok'
add_service_pid_of_name_server_output='Add ok'
remove_service_pid_of_name_server_output='Remove ok'
cat_alarm_file_output = 'SP=13'

class Test_get_service_pid_of_name_server(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.add_mml_response(list_service_pid_of_name_server_output, 'nasext lp test')
        self.add_mml_response(get_service_pid_of_name_server_output, 'nasext g test')
        self.add_mml_response(add_service_pid_of_name_server_output, 'nasext a test_server,4002,123,0,0,0,0,0,0,0,0')
        self.add_mml_response(update_service_pid_of_name_server_output, 'nasext u test_server,4002,123,0,0,0,0,0,0,0,0')
        self.add_mml_response(get_service_pid_of_name_server_output, 'cat /root/naseva_pending.log')
        self.add_mml_response(remove_service_pid_of_name_server_output, 'nasext r test_server,4002,123,0,0')
        self.add_mml_response(list_service_content_of_name_server_output, 'nasext lc read_params_as')
        self.add_mml_response(list_service_name_of_name_server_output, 'nasext ls read_params_as')
        self.add_mml_response(cat_alarm_file_output, 'cat test')
        self.add_mml_response('0', 'echo $?')
        self.mml_responses_completed()

    def test_get_service_pid_of_name_server(self):
        result = get_service_pid_of_name_server('test')
        self.assertEquals(result.Family, '0646')
        self.assertEquals(result.Computer, '4FFE')
        self.assertEquals(result.Process, '0000')
        self.assertEquals(result.Group, '0000')
        self.assertEquals(result.Attr, '09')

    def test_opt_service_of_name_server(self):
        result = opt_service_of_name_server('add',['test_server','4002','123','0','0','0','0','0','0','0','0'])
        self.assertEquals(result, True)

        result = opt_service_of_name_server('update',['test_server','4002','123','0','0','0','0','0','0','0','0'])
        self.assertEquals(result, True)

        result = opt_service_of_name_server('remove',['test_server','4002','123','0','0','0','0','0','0','0','0'])
        self.assertEquals(result, True)

    def test_get_pending_result_of_name_server(self):
        result = get_pending_result_of_name_server()
        self.assertEquals(result.Family, '0646')
        self.assertEquals(result.Computer, '4FFE')
        self.assertEquals(result.Process, '0000')
        self.assertEquals(result.Group, '0000')
        self.assertEquals(result.Attr, '09')

    def test_list_service_pid_of_name_server(self):
        result = list_service_pid_of_name_server('test')
        self.assertEquals(result[0].Computer, '4FFE')
        self.assertEquals(result[0].Process, '0000')
        self.assertEquals(result[0].Group, '0000')
        self.assertEquals(result[0].Attr, '09')

    def test_list_service_content_of_name_server(self):
        result = list_content_of_name_server('read_params_as')
        self.assertEquals(result.Name, 'read_params_as')
        self.assertEquals(result.Computer, '4002')
        self.assertEquals(result.Family, '0438')
        self.assertEquals(result.Process, '0000')
        self.assertEquals(result.Focus, '00')
        self.assertEquals(result.Group, '0')
        self.assertEquals(result.Attr, '09')
        self.assertEquals(result.Delivery, '3000')
        self.assertEquals(result.GroupNum, '0000')
        self.assertEquals(result.Replace, '0')

    def test_list_service_name_of_name_server(self):
        result = list_name_of_name_server('read_params_as')
        self.assertEquals(result.Name, 'read_params_as')
    def test_check_alarm_of_name_server(self):
       result = check_alarm_of_name_server('test')
