import unittest
from runall import BaseTestCase

from comm.communication import exceptions
from comm.communication.exceptions import ILException
from ileitp_subsystem_lib.bootmem import *

class Test_bootmem_show(BaseTestCase):
    def setUp(self):
        BaseTestCase.setUp(self)

    def _get_command(self, node_name, cmd):
        return 'ssh -oStrictHostKeyChecking=no %s bootmem show %s' % (node_name.lower(), cmd)
        
    def test_show_free(self):
        output = '''
Printing bootmem block list, descriptor: 0x48108,  head is 0xf572a0
Descriptor version: 3.0
Block address: 0xf572a0, size: 0x20, next: 0xf57330
Block address: 0xf57330, size: 0x50, next: 0xf573e0
Block address: 0xf573e0, size: 0x20, next: 0xf5c810
Block address: 0xf5c810, size: 0x70, next: 0xf668f0
Block address: 0xf668f0, size: 0x10, next: 0xfee760
Block address: 0xfee760, size: 0x113a0, next: 0x4d72410
Block address: 0x4d72410, size: 0x70, next: 0x4f4ac90
Block address: 0x4f4ac90, size: 0x70, next: 0x4fd2b60
Block address: 0x4fd2b60, size: 0x2c6a0, next: 0x8087e60
Block address: 0x8087e60, size: 0x781a0, next: 0x81c09c0
Block address: 0x81c09c0, size: 0x7840, next: 0x81c8300
Block address: 0x81c8300, size: 0x37d00, next: 0x9387e60
Block address: 0x9387e60, size: 0x781a0, next: 0xff337e0
Block address: 0xff337e0, size: 0x20, next: 0xffbb660
Block address: 0xffbb660, size: 0x41d20, next: 0xfffdbd0
Block address: 0xfffdbd0, size: 0x30, next: 0x1483628a0
Block address: 0x1483628a0, size: 0x60, next: 0x154d0d880
Block address: 0x154d0d880, size: 0xab2f2780, next: 0x410000000
Block address: 0x410000000, size: 0xf800000, next: 0x0        
        '''
        node_name = 'UsPu-0'
        command = self._get_command(node_name, 'free')
        self.add_mml_response(output, command)
        self.mml_responses_completed()

        result = bootmem_get_max_free_size(node_name)
        
        self.assertEqual(result['address'], '0x154d0d880')
        self.assertEqual(result['size'], '0xab2f2780')
        self.assertEqual(result['next'], '0x410000000')


    def test_show_named(self):
        output = '''
List of currently allocated named bootmem blocks:
Name: __uboot_code_data, address: 0x41f800000, size: 0x00800000, index: 0
Name: idle-core-loop, address: 0x000ffff0, size: 0x00000010, index: 1
Name: __bootloader_env, address: 0x04fff200, size: 0x00000e00, index: 2
Name: cvmx-debug-globals, address: 0x00edd890, size: 0x0002d550, index: 3
Name: __pci_console, address: 0x0fffd380, size: 0x00000850, index: 4
Name: cvmx_mgmt_port, address: 0x08100000, size: 0x000c0940, index: 5
Name: cvmx_qlm_jtag, address: 0x00fffb00, size: 0x00000500, index: 6
Name: cvmx-app-hotplug-block, address: 0x00f0ade0, size: 0x00008020, index: 7
Name: cvmx_cmd_queues, address: 0x00f12e00, size: 0x00007800, index: 8
Name: USUP_SHM_FSDSTUB, address: 0x04c00000, size: 0x00172410, index: 9
Name: CAVIUM_MCORE_SHMEM, address: 0x36000000, size: 0x18000000, index: 10
Name: bucket, address: 0x26000000, size: 0x08000000, index: 11
Name: DMA_HOLE, address: 0xf0000000, size: 0x10000000, index: 12
Name: __reserved_ramdisk, address: 0x05000000, size: 0x02000000, index: 13
Name: FASTDIST_STAT_MEM, address: 0x00f1a600, size: 0x0003cca0, index: 14
Name: cvmx_timer, address: 0x00f57300, size: 0x00000030, index: 15
Name: USUP_SHM_FASTDIST, address: 0x146800000, size: 0x01b628a0, index: 16
Name: UPSIM_DIAGNOSTIC_SHM, address: 0x00f57380, size: 0x00000060, index: 17
Name: PATH-PROFILING, address: 0x00f57400, size: 0x00005410, index: 18
Name: dmxmsg, address: 0x00f5c880, size: 0x00004000, index: 19
Name: FASTDIST_CONFIG_MEM, address: 0x00f60880, size: 0x00000080, index: 20
Name: USUPSIM_UP_INFO_POOL, address: 0x0fc00000, size: 0x002ab980, index: 21
Name: USUPSIM_HSCF_INFO_POOL, address: 0x00f60900, size: 0x00000500, index: 22
Name: USUPSIM_CONN_STAT_POOL, address: 0x148362900, size: 0x001b7780, index: 23
Name: USUPSIM_CONN_STAT_SERV_POOL, address: 0x14851a080, size: 0x003e4180, index: 24
Name: USUPSIM_HANGING_INFO_POOL, address: 0x00f60e00, size: 0x00000280, index: 25
Name: USUPSIM_SERV_RES_POOL, address: 0x1488fe200, size: 0x0015f900, index: 26
Name: USUPSIM_CONN_RES_POOL, address: 0x148a5db00, size: 0x00bd3580, index: 27
Name: UP_EXC_SHMEM, address: 0x00f61080, size: 0x00005400, index: 28
Name: UPSIM_FD_CF_SHMEM, address: 0x00f66480, size: 0x00000470, index: 29
Name: UPSIM_FD_TIMER_INIT_SHM, address: 0x149631080, size: 0x0a930800, index: 30
Name: hwa8000001400391a0, address: 0x00f66900, size: 0x00087e60, index: 31
Name: hwa8000001400392a0, address: 0x04f4ad00, size: 0x00087e60, index: 32
Name: hwa8000001400393a0, address: 0x08000000, size: 0x00087e60, index: 33
Name: hwa80000011fd01ea0, address: 0x09300000, size: 0x00087e60, index: 34
Name: hwa80000011fd01aa0, address: 0x0feab980, size: 0x00087e60, index: 35
Name: hwa80000011fd019a0, address: 0x0ff33800, size: 0x00087e60, index: 36
        '''
        node_name = 'UsPu-0'
        command = self._get_command(node_name, 'named all')
        self.add_mml_response(output, command)
        self.mml_responses_completed()

        result = bootmem_get_max_named_index(node_name)
        
        self.assertEqual(result['name'], 'hwa80000011fd019a0')
        self.assertEqual(result['address'], '0x0ff33800')
        self.assertEqual(result['size'], '0x00087e60')
        self.assertEqual(result['index'], '36')
