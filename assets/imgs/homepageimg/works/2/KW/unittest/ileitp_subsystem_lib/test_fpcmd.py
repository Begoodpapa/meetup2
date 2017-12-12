import unittest
from runall import BaseTestCase

from comm.communication import exceptions
from comm.communication.exceptions import ILException
from ileitp_subsystem_lib.fpcmd import *

class Test_fpcmd_dump_cpu_usage(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)

    def test_dump_cpu_usage(self):
        eipu_name = 'EIPU-2'
        command = 'ssh -oStrictHostKeyChecking=no %s fpcmd dump-cpu-usage' % (eipu_name.lower())
        result = '''
Fast path CPU usage:
cpu: %busy     cycles (in 400092800 usec)
  0:    0%          0
  1:    0%          0
  2:    0%          0
  3:    0%          0
  4:    0%          0
  5:    0%          0
  6:   80%    1102930
  7:   25%      22134
  8:   30%     328633
  9:   33%      12674
 10:   22%       5736
 11:   11%     473098
 12:    0%          0
 13:    0%          0
 14:    0%          0
 15:    0%          0
 16:    0%          0
 17:    0%          0
 18:    0%          0
 19:    0%          0
 20:    0%          0
 21:    0%          0
 22:    0%          0
 23:    0%          0
 24:    0%          0
 25:    0%          0
 26:    0%          0
 27:    0%          0
 28:    0%          0
 29:    0%          0
 30:    0%          0
 31:    0%          0
average cycles/IPv4 and IPv6 forwarded packet: --- (1945205/0)
		'''
        
        self.add_mml_response(result, command)
        self.mml_responses_completed()

        result = fpcmd_dump_cpu_usage(eipu_name)
        
        self.assertEqual(result[0].cpu_id, 6);
        self.assertEqual(result[0].busy, 80);
        self.assertEqual(result[0].cycles, 1102930);
        self.assertEqual(result[1].cpu_id, 7);
        self.assertEqual(result[1].busy, 25);
        self.assertEqual(result[1].cycles, 22134);
        self.assertEqual(result[2].cpu_id, 8);
        self.assertEqual(result[2].busy, 30);
        self.assertEqual(result[2].cycles, 328633);
        self.assertEqual(result[3].cpu_id, 9);
        self.assertEqual(result[3].busy, 33);
        self.assertEqual(result[3].cycles, 12674);
        self.assertEqual(result[4].cpu_id, 10);
        self.assertEqual(result[4].busy, 22);
        self.assertEqual(result[4].cycles, 5736);
        self.assertEqual(result[5].cpu_id, 11);
        self.assertEqual(result[5].busy, 11);
        self.assertEqual(result[5].cycles, 473098);

        self.add_mml_response(result, command)
        self.mml_responses_completed()

        cpu_usage = [80, 25, 30, 33, 22, 11]
        total = sum(cpu_usage)
        result = fpcmd_get_average_cpu_usage(eipu_name)
        self.assertEqual(result, total / len(cpu_usage));

