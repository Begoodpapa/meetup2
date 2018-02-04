from comm.communication import exceptions
from comm.communication import connections
from comm.communication.helper import *
import re

#***********************************************************************
#Usage: dmxcli2 [options]
#    1. dmxcli2 -h / -?                 :Show this help message.
#    2. dmxcli2 -s comp.fam             :Send a message to dest pid.
#    3. dmxcli2 -r comp[.fam[.timeout]] :Receive a message from pid.
#         e.g.  -r 0.ad9c               :Receive from 0.ad9c.0. Wait for ever.
#         e.g.  -r 1.?.1000             :Receive from computer 1 and any family. Timeout 1000MS.
#         e.g.  -r ?.?.50               :Receive from any computer and any family. Timeout 50MS.
#    4. dmxcli2 -m wosp_logic_addr      :Check last warming message.
#         e.g.  -m 7002                 :Must be WOSP logical address.
#    5. dmxcli2 -w wosp_logic_addr      :Check WO message is faster than SP.
#         e.g.  -w 7002                 :Must be WOSP logical address.
#    6. dmxcli2 -u unit_addr=unit_state :Update RU state. Addr and state are all hexadecimal.
#         e.g.  -u 0100=F               :Unit_addr must be physical address. 0xF means UNIT_STATE_T_WO_C.
#    7. dmxcli2 -c unit_addr=co_uaddr   :Update RU co-unit address. (Hexadecimal)
#         e.g.  -c 0100=0200            :Both address must be physical addr.
#    8. dmxcli2 -U uaddr,ustate,counit  :Update RU state and co-unit at one time.
#         e.g.  -U 100,0,200            :Set RU 100's state to WO, and co-unit addr is 200.
#    9. dmxcli2 -C unit,log,wosp,wo,sp  :Config logical address. This will modify the computer table.
#         e.g.  -C 1F0,4FF0,FF7,0,100   :Config logical address 7FF0.
#    10.dmxcli2 -G grp,num,addr1,...    :Config group address. This will modify the group table.
#         e.g.  -G FF7,2,0,100          :Config group address FF7.
#    11.dmxcli2 -Q unit_addr            :Query unit state by unit address.
#         e.g.  -Q 0100                 :Query unit state of 0x0100. Return value will be 'State,CoUnit'.
#    12.dmxcli2 -q RUType[,n]           :Query RU computer table info. Such as logical addr, Physical address, ...
#               Optional 'n'            :0=All, 1=PhysAddr, 2=LogAddr, 3=Log_GroupAddr, 4=Group_LogAddr, 5=Processor_index.
#         e.g.  -q Unit_Type,0          :Query all info about unit type.
#    13.dmxcli2 -o                      :Query own physical address.
#
#    [Sep 29 2009 18:34:15]
#
#***********************************************************************

def dmxcli2_sending( options ):

    """
    This keyword is to return execution result contains "**SUCCESS**" when funcs implemented successful.
    #COMMAND: dmxcli2 

   Usage: dmxcli2 [options]
    1. dmxcli2 -h / -?                 :Show this help message.
    2. dmxcli2 -s comp.fam             :Send a message to dest pid.
    3. dmxcli2 -r comp[.fam[.timeout]] :Receive a message from pid.
         e.g.  -r 0.ad9c               :Receive from 0.ad9c.0. Wait for ever.
         e.g.  -r 1.?.1000             :Receive from computer 1 and any family. Timeout 1000MS.
         e.g.  -r ?.?.50               :Receive from any computer and any family. Timeout 50MS.
    4. dmxcli2 -m wosp_logic_addr      :Check last warming message.
         e.g.  -m 7002                 :Must be WOSP logical address.
    5. dmxcli2 -w wosp_logic_addr      :Check WO message is faster than SP.
         e.g.  -w 7002                 :Must be WOSP logical address.
    6. dmxcli2 -u unit_addr=unit_state :Update RU state. Addr and state are all hexadecimal.
         e.g.  -u 0100=F               :Unit_addr must be physical address. 0xF means UNIT_STATE_T_WO_C.
    7. dmxcli2 -c unit_addr=co_uaddr   :Update RU co-unit address. (Hexadecimal)
         e.g.  -c 0100=0200            :Both address must be physical addr.
    8. dmxcli2 -U uaddr,ustate,counit  :Update RU state and co-unit at one time.
         e.g.  -U 100,0,200            :Set RU 100's state to WO, and co-unit addr is 200.
    9. dmxcli2 -C unit,log,wosp,wo,sp  :Config logical address. This will modify the computer table.
         e.g.  -C 1F0,4FF0,FF7,0,100   :Config logical address 7FF0.
    10.dmxcli2 -G grp,num,addr1,...    :Config group address. This will modify the group table.
         e.g.  -G FF7,2,0,100          :Config group address FF7.
    11.dmxcli2 -Q unit_addr            :Query unit state by unit address.
         e.g.  -Q 0100                 :Query unit state of 0x0100. Return value will be 'State,CoUnit'.
    12.dmxcli2 -q RUType[,n]           :Query RU computer table info. Such as logical addr, Physical address, ...
               Optional 'n'            :0=All, 1=PhysAddr, 2=LogAddr, 3=Log_GroupAddr, 4=Group_LogAddr, 5=Processor_index.
         e.g.  -q Unit_Type,0          :Query all info about unit type.
    13.dmxcli2 -o                      :Query own physical address.

    Example
    | dmxcli2_sending |-s 0.ad9c.0|
    """
    command = "dmxcli2 " + options
    out = connections.execute_mml_without_check( command )
    return out

def dmxcli2_Query_unit_status( unit_addr ):
    """
    This keyword is to return unit state by querying unit address.
    #COMMAND: dmxcli2 -Q unit_addr

    | Parameters  | Man. | Description  |
    | unit_addr   | Yes  | unit address |

    | Return value |retuen unit address, state, CoUnit |

    Example
    | ${result}  |  dmxcli2 -Q  0100|

    """
    command = "dmxcli2 -Q " + unit_addr
    out = connections.execute_mml_without_check( command )
    out2 = out.strip().splitlines()
    return out2[0]

def dmxcli2_Update_unit_status( unit_status ):
    """This keyword is to Update RU state and co-unit at one time.
    #COMMAND: dmxcli2 -U unit_addr

    | Parameters  | Man. | Description  |
    | unit_addr   | Yes  | unit address |

    | Return value |retuen unit state, Co RU State|

    Example
    | ${result}  |  dmxcli2 -U  0100 |

    """
    command = "dmxcli2 -U " + unit_status
    out = connections.execute_mml_without_check( command )
    return out

def dmxcli2_Query_own_phys_addr():
    """This keyword is Query own physical address.
    #COMMAND: dmxcli2 -o 

    | Parameters  | Man. | Description  |

    | Return value |retuen RU state|

    Example
    | ${result}  |  dmxcli2 -o |

    """
    command = "dmxcli2 -o"
    out = connections.execute_mml_without_check( command )
    out2 = out.strip().splitlines()
    return out2[0]

def dmxcli2_Update_unit_state( unit_addr, unit_state ):
    """This keyword is Update RU state. Addr and state are all hexadecimal.
    #COMMAND: dmxcli2 -u  unit_addr=unit_state

    | Parameters  | Man. | Description  |
    | unit_addr   | Yes  | unit address |
    | unit_state  | Yes  | unit state   |
		
    | Return value | no return values|

    Example
    | ${result}  |  dmxcli2 -u 0100=0 |

    """
    command = "dmxcli2 -u " + unit_addr + "=" + unit_state
    out = connections.execute_mml_without_check( command )
    return out

def dmxcli2_Update_unit_co( unit_addr, processor_index, uindex_offset ):
    """This keyword is Update RU state. Addr and state are all hexadecimal.
    #COMMAND: dmxcli2 -c  unit_addr=unit_state

    | Parameters       | Man. | Description        |
    | unit_addr        | Yes  | unit address       |
    | processor_index  | Yes  | processor index    |
    | uindex_offset    | Yes  | uindex offset	   |
    | Return value | return "FAILURE" or "SUCCESS" |

    Example
    | ${result}  |  dmxcli2 -c 0100=0 |

    """
    processor_index = "0x" + processor_index
    uindex_offset = "0x" + uindex_offset
    sum = int( processor_index, 16 ) + int( uindex_offset, 16 )
    sum = hex( sum )
    print sum
    co_unit_addr = str( sum )
    print co_unit_addr
    command = "dmxcli2 -c " + str( unit_addr ) + "=" + co_unit_addr
    print command
    out = connections.execute_mml_without_check( command )
    return out

def dmxcli2_Query_comp_table( unit_type, num ):
    """This keyword is Update RU state. Addr and state are all hexadecimal.
    #COMMAND: dmxcli2 -q  unit_addr[,num]

    | Parameters       | Man. | Description                                                                      |
    | unit_type        | Yes  | unit type                                                                        |
	| num              | Yes  |0=All, 1=PhysAddr, 2=LogAddr, 3=Log_GroupAddr, 4=Group_LogAddr, 5=Processor_index |
	
    | Return value     | RU computer table info. Such as logical addr, Physical address|
	
    Example
    | ${result}  |  dmxcli2 -q 0100,1 |
	
    """
    command = "dmxcli2 -q " + unit_type + "," + num
    out = connections.execute_mml_without_check( command )
    out2 = out.strip().splitlines()
    return out2[0]

def dmxcli2_Query_Phys_Addr( unit_type, unit_index ):
    """This keyword Query physical address by ru name and index.
    #COMMAND: dmxcli2 -t unit_type,unit_index

    | Parameters       | Man. | Description       |
    | unit_type        | Yes  | unit type         |
	| unit_index       | Yes  | unit index        |
	
    | Return value     | RU Physical address|
	
    Example
    | ${result}  |  dmxcli2 -t unit_type,unit_index |
	
    """
    command = "dmxcli2 -t " + unit_type + "," + unit_index
    out = connections.execute_mml_without_check( command )
    out2 = out.strip().splitlines()
    return out2[0]

def dmxcli2_Query_and_Fill( pid ):
    """This keyword Query and replace physical addr.
    #COMMAND: dmxcli2 -p  pid

    | Parameters       | Man. | Description       |
    | pid              | Yes  | pid               |
	
    | Return value     | RU Physical address      |
	
    Example
    | ${result}  |  dmxcli2 -p pid                |
	
    """
    command = "dmxcli2 -p " + pid
    out = connections.execute_mml_without_check( command )
    out2 = out.strip().splitlines()
    return out2[0]

def dmxcli2_send_msg( pid_to ):
    """This keyword Send a message to dest pid.
    #COMMAND: dmxcli2 -s comp.fam

    | Parameters       | Man. | Description              |
    | pid_to           | Yes  | comp.fam                 |
	
    | Return value     | **SUCCESS** of **FAILURE**      |
	
    Example
    | ${result}  |  dmxcli2 -s comp.fam                  |
	
    """
    command = "dmxcli2 -s " + pid_to
    out = connections.execute_mml_without_check( command )
    return out

def dmxcli2_recv_msg( pid_from ):
    """This keyword Receive a message from pid.
    #COMMAND: dmxcli2  -r comp[.fam[.timeout]] 

    | Parameters       | Man. | Description              |
    | pid_from         | Yes  | comp[.fam[.timeout]]     |
	
    | Return value     | **SUCCESS** of **FAILURE**      |
	
    Example
    | ${result}  |  dmxcli2 -r comp.fam                  |
	
    """
    command = "dmxcli2 -r " + pid_from
    out = connections.execute_mml_without_check( command )
    return out

def dmxcli2_launch_command( cmd, param ):
    command = "dmxcli2 " + cmd + " " + param
    out = connections.execute_mml_without_check( command )
    return out

def dmxcli2_Config_comp_table( utype, logaddr, wospaddr, woaddr, spaddr ):
    """This keyword Config logical address. This will modify the computer table.
    #COMMAND: dmxcli2 -C unit,log,wosp,wo,sp

    | Parameters       | Man. | Description              |
    | utype            | Yes  | RU Type                  |
    | logaddr          | Yes  | logical address.         |
    | wospaddr         | Yes  | WOSP address             |
    | woaddr           | Yes  | WO address               |
    | spaddr           | Yes  | SP address               |
	
    | Return value     | **SUCCESS** of **FAILURE**      |
	
    Example
    | ${result}  | dmxcli2 -C 1F0,4FF0,FF7,0,100         |
	
    """
    command = "dmxcli2 -C " + utype + "," + logaddr + "," + wospaddr + "," + woaddr + "," + spaddr
    out = connections.execute_mml_without_check( command )
    return out

def dmxcli2_Delete_comp_table( logaddr ):
    """This keyword Delete logical address. This will modify the computer table.
    #COMMAND: dmxcli2 -D log

    | Parameters       | Man. | Description              |
    | logaddr          | Yes  | logical address.         |
	
    | Return value     | **SUCCESS** of **FAILURE**      |
	
    Example
    | ${result}  | dmxcli2 -D 4FF0         |
	
    """
    command = "dmxcli2 -C 0," + logaddr + ",FFFF,FFFF,FFFF"
    out = connections.execute_mml_without_check( command )
    return out

def dmxcli2_Config_grp_addr_1( grp_addr, processor_index, uindex_offset ):
    """This keyword Config group address. This will modify the group table.
    #COMMAND: dmxcli2 -G grp,num,addr1,

    | Parameters       | Man. | Description              |
    | grp_addr         | Yes  | Group Address            |
    | processor_index  | Yes  | processor index          |
    | uindex_offset    | Yes  | uindex offset            |
	
    | Return value     | **SUCCESS** of **FAILURE**      |
	
    Example
    | ${result}  | dmxcli2 -G FF7,2,0,100.               |
	
    """
    processor_index = "0x" + processor_index
    uindex_offset = "0x" + uindex_offset
    sum = int( processor_index, 16 ) + int( uindex_offset, 16 )
    sum = hex( sum )
    addr = str( sum )
    print addr
    command = "dmxcli2 -G " + str( grp_addr ) + ",1," + addr
    out = connections.execute_mml_without_check( command )
    return out

def dmxcli2_Config_grp_addr_2( grp_addr, phys_addr1, processor_index, uindex_offset ):
    """This keyword Config group address. This will modify the group table.
    #COMMAND: dmxcli2 -G grp,num,addr1,

    | Parameters       | Man. | Description              |
    | grp_addr         | Yes  | Group Address            |
    | phys_addr1       | Yes  | phys address             |          	
    | processor_index  | Yes  | processor index          |
    | uindex_offset    | Yes  | uindex offset            |
	
    | Return value     | **SUCCESS** of **FAILURE**      |
	
    Example
    | ${result}  | dmxcli2 -G FF7,2,0,100.               |
	
    """
    processor_index = "0x" + processor_index
    uindex_offset = "0x" + uindex_offset
    sum = int( processor_index, 16 ) + int( uindex_offset, 16 )
    sum = hex( sum )
    addr2 = str( sum )
    print addr2
    command = "dmxcli2 -G " + str( grp_addr ) + ",2," + str( phys_addr1 ) + "," + addr2
    out = connections.execute_mml_without_check( command )
    return out

def dmxcli2_Swo_prepare( unit_addr, unit_state, type):
    """This keyword Prepare swo. Addr and state are all hexadecimal.
    #COMMAND: dmxcli2 -P unit_addr=unit_state,swo_type

    | Parameters       | Man. | Description                                             |
    | unit_addr        | Yes  | RU address                                              |
    | unit_state       | Yes  |  0xF means UNIT_STATE_T_WO_C. Use control switchover    |          	
    | type             | Yes  | control, faulty                                         |
	
    | Return value     | **SUCCESS** of **FAILURE**      |
	
    Example
    | ${result}  | dmxcli2 -P 0100=F,contr               |
	
    """
    command = "dmxcli2 -P " + unit_addr + "=" + unit_state +","+type 
    out = connections.execute_mml_without_check( command )
    return out

