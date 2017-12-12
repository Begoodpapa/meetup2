from struct import *
from string import *

import re
import string
import math
import os

from comm.communication.helper import *
from comm.communication import exceptions
from comm.communication import connections


def __is_octeon_cpu():
    command = 'cat /proc/cpuinfo  | grep "Cavium Octeon II" | wc -l'
    output = connections.execute_mml_without_check(command)
    result = str(output).strip()
    if result == '0':
        return True
    else:
        return False

def oct_remote_profile_peronly(unit_name, sampling=5):
    """
    This keyword is to profile se performance.

    #COMMAND: ssh eipu-0 oct-remote-profile --perfonly

    | Parameters | Man.| Description    |
    | unit_name  | Yes | unit name      |
    | sampling   | No  | sampling count |

    | Return value | command execution result |
    octeon: 
      * [brmis[12], brmis_total, sync[12], sync_total, l2_stat[cycles, dhit, dmiss, imiss], dram[ops, dclk, util]]
    octeon II:
      * [brmis[32], brmis_total, sync[32], sync_total, l2_stat[4*[bus[xmc, xmd, rsc, rsd, ioc, ior], hit, miss, bus_util[lfb_wait_lfb, lfb_wait_vab], dram[ops, dclk, util]]]
      
    Example
    | ${result} | Oct Remote Profile Peronly | ${unit_name} |
    
    """
	
    command = 'ssh -oStrictHostKeyChecking=no %s "%s%d"' % (unit_name.lower(), 'export OCTEON_REMOTE_PROTOCOL=LINUX;oct-remote-profile --perfonly --count=', sampling)
    output = connections.execute_mml_without_check(command)
    
    items = re.findall(r'\d*\.?\d+',  output)    
    
    result = []
    n = 0
    brims_sync_num = 32
    item_min_num = 126
    if __is_octeon_cpu():
        brims_sync_num = 12 
        item_min_num = 57 
    
    l2_stat_num = 4
    
    while (n + item_min_num) <= len(items):
        item = CommonItem()
        item.brmis = []
        for i in range(brims_sync_num):
            item.brmis.append(int(items[n]))
            n += 2
            
        item.brmis_total_excluding = int(items[n])
        n += 1

        item.brmis_total = int(items[n])
        n += 1
                
        item.sync = []
        for i in range(brims_sync_num):
            item.sync.append(int(items[n]))
            n += 2
    
        item.sync_total_excluding = int(items[n])
        n += 1
        
        item.sync_total = int(items[n])
        n += 1
        
        if __is_octeon_cpu():
            print "OCTEON+"
            n += 1
            item.l2_stat = CommonItem()
            item.l2_stat.cycles = int(items[n])
            n += 1
    
            item.l2_stat.dhit = int(items[n])
            n += 1
    
            item.l2_stat.dmiss = int(items[n])
            n += 1
    
            item.l2_imiss = int(items[n])
            n += 1
            
            item.dram = CommonItem()
            item.dram.ops = int(items[n])
            n += 1
            
            item.dram.dclk = int(items[n])
            n += 1
            
            item.dram.util = float(items[n])
            n += 1
        else:
            print "OCTEONII"
            item.l2_stats = []
            for i in range(l2_stat_num):
                l2_stat = CommonItem()
                n += 2
                l2_stat.bus = CommonItem()
                l2_stat.bus.xmc = int(items[n])
                n += 1
                l2_stat.bus.xmd = int(items[n])
                n += 1
                l2_stat.bus.rsc = int(items[n])
                n += 1
                l2_stat.bus.rsd = int(items[n])
                n += 1
                if i == 0:
                    l2_stat.bus.ioc = int(items[n])
                    n += 1
                    l2_stat.bus.ior = int(items[n])
                    n += 1
                l2_stat.hit = int(items[n])
                n += 1
                l2_stat.miss = int(items[n])
                n += 1

                l2_stat.bus_util = CommonItem()
                l2_stat.bus_util.lfb_wait_lfb = float(items[n])
                n += 1
                l2_stat.bus_util.lfb_wait_vab = float(items[n])
                n += 1

                l2_stat.dram = CommonItem()
                l2_stat.dram.ops = int(items[n])
                n += 1
                
                l2_stat.dram.dclk = int(items[n])
                n += 1
                
                l2_stat.dram.util = float(items[n])
                n += 1

                item.l2_stats.append(l2_stat)
                
        result.append(item)
    
    return result


def oct_remote_profile_l2_data_miss_ratio(unit_name, sampling=5):
    """
     This keyword is to get L2 cache data miss ratio.

    | Parameters | Man.| Description   |
    | unit_name  | Yes | unit name     |
    | sampling   | No  | sampling count |

    | Return value | command execution result |

    Example
    | ${result} | Oct Remote Profile L2 Data Miss Ratio | ${unit_name} |
    
    """
	
    output = oct_remote_profile_peronly(unit_name, sampling)
    result = []
    
    if __is_octeon_cpu():
        for item in output:
            l2_miss = CommonItem()
            l2_miss.miss = float(item.l2_stat.dmiss)
            l2_miss.hit = float(item.l2_stat.dhit) 
            l2_miss.ratio = (l2_miss.miss / l2_miss.hit) * 100
            result.append(l2_miss)
    else:
        for item in output:
            l2_miss_list = []
            for l2_stat in item.l2_stats:
                l2_miss = CommonItem()
                l2_miss.miss = float(l2_stat.miss)
                l2_miss.hit = float(l2_stat.hit) 
                l2_miss.ratio = (l2_miss.miss / l2_miss.hit) * 100
                l2_miss_list.append(l2_miss)
            result.append(l2_miss_list)
        
    return result
