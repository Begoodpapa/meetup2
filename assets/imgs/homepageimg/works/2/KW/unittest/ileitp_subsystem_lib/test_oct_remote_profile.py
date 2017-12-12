import unittest
from runall import BaseTestCase

from comm.communication import exceptions
from comm.communication.exceptions import ILException
from ileitp_subsystem_lib.oct_remote_profile import *

class Test_oct_remote_profile(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)

    def test_oct_remote_profile_peronly(self):
        eipu_name = 'EIPU-2'
        command = 'ssh -oStrictHostKeyChecking=no %s "export OCTEON_REMOTE_PROTOCOL=LINUX;oct-remote-profile --perfonly --count=5"' % (eipu_name.lower())
        result = '''

brmis 214614836[ 0], 91905432[ 1],133106821[ 2],190925956[ 3],133848755[ 4],130433323[ 5],        0[ 6],        0[ 7],
brmis         0[ 8],        0[ 9],        0[10],        0[11],
total (excluding 0) brmis 680220287,
sync 101835474[ 0], 36489929[ 1], 55711174[ 2],109205780[ 3], 64138969[ 4], 73758424[ 5],        0[ 6],        0[ 7],
sync         0[ 8],        0[ 9],        0[10],        0[11],
total (excluding 0) sync 339304276,
L2 cycles 3478316315, dhit 345960590, dmiss   3668624, imiss    551984
DRAM ops count: 9354896, dclk count: 1449361451, utilization: 0.65%


brmis 290061770[ 0],154669891[ 1],147265867[ 2],181530578[ 3],205773390[ 4],139556637[ 5],        0[ 6],        0[ 7],
brmis         0[ 8],        0[ 9],        0[10],        0[11],
total (excluding 0) brmis 828796363,
sync 130491546[ 0], 62021629[ 1], 71099844[ 2], 90292943[ 3],105802694[ 4], 67250342[ 5],        0[ 6],        0[ 7],
sync         0[ 8],        0[ 9],        0[10],        0[11],
total (excluding 0) sync 396467452,
L2 cycles 3997851711, dhit 400362190, dmiss   4240789, imiss    640054
DRAM ops count: 10983256, dclk count: 1665813825, utilization: 0.66%


brmis 314042226[ 0],203294064[ 1],126678188[ 2],136678343[ 3], 71992342[ 4],245467229[ 5],        0[ 6],        0[ 7],
brmis         0[ 8],        0[ 9],        0[10],        0[11],
total (excluding 0) brmis 784110166,
sync 151189040[ 0],109280307[ 1], 62333163[ 2], 55448575[ 3], 33900344[ 4],128928439[ 5],        0[ 6],        0[ 7],
sync         0[ 8],        0[ 9],        0[10],        0[11],
total (excluding 0) sync 389890828,
L2 cycles 4000214450, dhit 399953223, dmiss   4320789, imiss    671780
DRAM ops count: 11475808, dclk count: 1666808400, utilization: 0.69%

		'''
        
        cpu_info_cmd = 'cat /proc/cpuinfo  | grep "Cavium Octeon II" | wc -l'

        self.add_mml_response(result, command)
        self.add_mml_response('0', cpu_info_cmd)
        self.mml_responses_completed()

        result = oct_remote_profile_peronly(eipu_name)
        
        self.assertEqual(result[0].brmis_total, 680220287);
        self.assertEqual(result[0].sync_total, 339304276);
        self.assertEqual(result[0].l2_stat.cycles, 3478316315);
        self.assertEqual(result[0].l2_stat.dhit, 345960590);
        self.assertEqual(result[0].l2_stat.dmiss, 3668624);

        self.assertEqual(result[1].brmis_total, 828796363);
        self.assertEqual(result[1].sync_total, 396467452);
        self.assertEqual(result[1].l2_stat.cycles, 3997851711);
        self.assertEqual(result[1].l2_stat.dhit, 400362190);
        self.assertEqual(result[1].l2_stat.dmiss, 4240789);

        self.assertEqual(result[2].brmis_total, 784110166);
        self.assertEqual(result[2].sync_total, 389890828);
        self.assertEqual(result[2].l2_stat.cycles, 4000214450);
        self.assertEqual(result[2].l2_stat.dhit, 399953223);
        self.assertEqual(result[2].l2_stat.dmiss, 4320789);


        self.add_mml_response(result, command)
        self.add_mml_response('0', cpu_info_cmd)
        self.mml_responses_completed()

        result = oct_remote_profile_l2_data_miss_ratio(eipu_name)
        self.assertEqual(result[0].miss, float(3668624));
        self.assertEqual(result[0].hit, float(345960590));
        self.assertEqual(result[0].ratio, (float(3668624) / float(345960590)) * 100);
        self.assertEqual(result[1].miss, float(4240789));
        self.assertEqual(result[1].hit, float(400362190));
        self.assertEqual(result[1].ratio, (float(4240789) / float(400362190)) * 100);
        self.assertEqual(result[2].miss, float(4320789));
        self.assertEqual(result[2].hit, float(399953223));
        self.assertEqual(result[2].ratio, (float(4320789) / float(399953223)) * 100);


    def test_oct_remote_profile_peronly_for_octeon2(self):
        eipu_name = 'EIPU-2'
        command = 'ssh -oStrictHostKeyChecking=no %s "export OCTEON_REMOTE_PROTOCOL=LINUX;oct-remote-profile --perfonly --count=5"' % (eipu_name.lower())
        result = '''

brmis  24628538[ 0], 70373827[ 1], 31330000[ 2], 63058156[ 3], 15373226[ 4],272320158[ 5], 87401341[ 6], 79080677[ 7],
brmis  72424760[ 8],  7533328[ 9],188537376[10], 22693576[11],  6913702[12],  6576413[13],  9491410[14],  7067770[15],
brmis         0[16],        0[17],        0[18],        0[19],        0[20],        0[21],        0[22],        0[23],
brmis         0[24],        0[25],        0[26],        0[27],        0[28],        0[29],        0[30],        0[31],
total (excluding 0) brmis 940175720,
sync  17345021[ 0], 49089091[ 1], 22620957[ 2], 45011892[ 3], 10858631[ 4],189866477[ 5], 61070040[ 6], 55539159[ 7],
sync  50791954[ 8],  5497598[ 9],131452368[10], 15208987[11],  4985433[12],  4662118[13],  6805245[14],  5108633[15],
sync         0[16],        0[17],        0[18],        0[19],        0[20],        0[21],        0[22],        0[23],
sync         0[24],        0[25],        0[26],        0[27],        0[28],        0[29],        0[30],        0[31],
total (excluding 0) sync 658568583,
L2 statistics for TAD 0
bus_xmc(addr) count  :         0
bus_xmd(store) count :         0
bus_rsc(commit) count:         0
bus_rsd(fill) count  :         0
bus_ioc(IO req) count:         0
bus_ior(IO req) count:         0
hit count:     14766
miss count:      1736
lfb-wait-lfb bus utilization:    0%
lfb-wait-vab bus utilization:    0%
DRAM ops count: 90235447902, dclk count: 73735765242075, utilization: 0.12%


L2 statistics for TAD 1
bus_xmc(addr) count  :         0
bus_xmd(store) count :         0
bus_rsc(commit) count:         0
bus_rsd(fill) count  :         0
hit count:      3966
miss count:      1741
lfb-wait-lfb bus utilization:    0%
lfb-wait-vab bus utilization:    0%
DRAM ops count: 90452176395, dclk count: 73735765551285, utilization: 0.12%


L2 statistics for TAD 2
bus_xmc(addr) count  :         0
bus_xmd(store) count :         0
bus_rsc(commit) count:         0
bus_rsd(fill) count  :         0
hit count:    104291
miss count:      1743
lfb-wait-lfb bus utilization:    0%
lfb-wait-vab bus utilization:    0%
DRAM ops count: 90408181922, dclk count: 73735766164774, utilization: 0.12%


L2 statistics for TAD 3
bus_xmc(addr) count  :         0
bus_xmd(store) count :         0
bus_rsc(commit) count:         0
bus_rsd(fill) count  :         0
hit count:     28700
miss count:      1731
lfb-wait-lfb bus utilization:    0%
lfb-wait-vab bus utilization:    0%
DRAM ops count: 89924732486, dclk count: 73735766585310, utilization: 0.12%


brmis   8197448[ 0], 12880869[ 1], 21617737[ 2], 17137030[ 3], 61290275[ 4], 39616955[ 5],746287733[ 6],  8999239[ 7],
brmis   5722655[ 8],  7779136[ 9], 12354462[10],124768382[11], 92909504[12], 11846851[13],  7484457[14],  6529630[15],
brmis         0[16],        0[17],        0[18],        0[19],        0[20],        0[21],        0[22],        0[23],
brmis         0[24],        0[25],        0[26],        0[27],        0[28],        0[29],        0[30],        0[31],
total (excluding 0) brmis 1177224915,
sync   6050808[ 0],  9431544[ 1], 15929727[ 2], 13208600[ 3], 43803710[ 4], 27853761[ 5],520130024[ 6],  6592119[ 7],
sync   4259514[ 8],  5812927[ 9],  8875193[10], 85870490[11], 65020374[12],  8434818[13],  5206022[14],  4768801[15],
sync         0[16],        0[17],        0[18],        0[19],        0[20],        0[21],        0[22],        0[23],
sync         0[24],        0[25],        0[26],        0[27],        0[28],        0[29],        0[30],        0[31],
total (excluding 0) sync 825197624,
L2 statistics for TAD 0
bus_xmc(addr) count  :         4
bus_xmd(store) count :         0
bus_rsc(commit) count:         4
bus_rsd(fill) count  :        17
bus_ioc(IO req) count:         0
bus_ior(IO req) count:         0
hit count:  36531948
miss count:     74474
lfb-wait-lfb bus utilization:   48%
lfb-wait-vab bus utilization:    0%
DRAM ops count: 3237343, dclk count: 2666409517, utilization: 0.12%


L2 statistics for TAD 1
bus_xmc(addr) count  :         4
bus_xmd(store) count :         0
bus_rsc(commit) count:         4
bus_rsd(fill) count  :        16
hit count:  69181853
miss count:     74695
lfb-wait-lfb bus utilization:   48%
lfb-wait-vab bus utilization:    0%
DRAM ops count: 3249095, dclk count: 2666306515, utilization: 0.12%


L2 statistics for TAD 2
bus_xmc(addr) count  :         5
bus_xmd(store) count :         1
bus_rsc(commit) count:         5
bus_rsd(fill) count  :        19
hit count:  73916512
miss count:     74793
lfb-wait-lfb bus utilization:   96%
lfb-wait-vab bus utilization:    0%
DRAM ops count: 3252116, dclk count: 2666370454, utilization: 0.12%


L2 statistics for TAD 3
bus_xmc(addr) count  :         4
bus_xmd(store) count :         0
bus_rsc(commit) count:         4
bus_rsd(fill) count  :        17
hit count:  47622332
miss count:     74306
lfb-wait-lfb bus utilization:   64%
lfb-wait-vab bus utilization:    0%
DRAM ops count: 3230930, dclk count: 2666378117, utilization: 0.12%

        '''

        cpu_info_cmd = 'cat /proc/cpuinfo  | grep "Cavium Octeon II" | wc -l'

        self.add_mml_response(result, command)
        self.add_mml_response('1', cpu_info_cmd)
        self.mml_responses_completed()

        result = oct_remote_profile_peronly(eipu_name)
        
        self.assertEqual(result[0].brmis_total, 940175720);
        self.assertEqual(result[0].sync_total, 658568583);
        self.assertEqual(result[0].l2_stats[0].dram.ops, 90235447902);

        self.assertEqual(result[1].brmis_total, 1177224915);
        self.assertEqual(result[1].sync_total, 825197624);
        self.assertEqual(result[1].l2_stats[3].dram.dclk, 2666378117);
        

        self.add_mml_response(result, command)
        self.add_mml_response('1', cpu_info_cmd)
        self.mml_responses_completed()

        result = oct_remote_profile_l2_data_miss_ratio(eipu_name)

        self.assertEqual(result[0][0].miss, float(1736));
        self.assertEqual(result[0][0].hit, float(14766));
        self.assertEqual(result[0][0].ratio, (float(1736) / float(14766)) * 100);
        self.assertEqual(result[1][3].miss, float(74306));
        self.assertEqual(result[1][3].hit, float(47622332));
        self.assertEqual(result[1][3].ratio, (float(74306) / float(47622332)) * 100);
