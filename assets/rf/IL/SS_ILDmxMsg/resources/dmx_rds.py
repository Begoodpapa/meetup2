from comm.communication import exceptions
from comm.communication import connections
from comm.communication.helper import *
import re, time
from robot import utils
from robot import output

    
def Generic_Get_Rds_Link_Info(addr):
    cmd = "dmx_generic_stub get_rds_link_info " + addr
    output = connections.execute_mml( cmd )
    print output
    cmd += " >/tmp/generic.txt"
    connections.execute_mml( cmd )
    return
    
def Generic_Get_Rds_Sequence_Num(addr):
    Generic_Get_Rds_Link_Info(addr)
    cmd = "grep Frame_seq /tmp/generic.txt | cut -f 2 -d :"   
    output = connections.execute_mml( cmd )
    output = output.strip()
    return output

        
def Get_Rds_Sliding_Window_Size():    
    cmd = "cat /proc/dmxmsg/rds_tx_win_size"
    output = connections.execute_mml( cmd )
    size = output.strip()
    return size

def Get_Rds_Tx_Queue_Size():    
    cmd = "cat /proc/dmxmsg/rds_tx_queue_limit"
    output = connections.execute_mml( cmd )
    size = output.strip()
    return size
    
def Get_Rds_Tx_Queue_Extra_Size():    
    cmd = "cat /proc/dmxmsg/rds_tx_queue_extra_limit"
    output = connections.execute_mml( cmd )
    size = output.strip()
    return size

def Get_Rds_max_state_query_count():
    cmd = "cat /proc/dmxmsg/rds_max_state_query_count"
    output = connections.execute_mml( cmd )
    size = output.strip()
    return size

def Set_Rds_Sliding_Window_Size(size): 
    if size != '':   
        cmd = "echo %s >/proc/dmxmsg/rds_tx_win_size" %size
        output = connections.execute_mml( cmd )
    Get_Rds_Sliding_Window_Size()
    return    

def Set_Rds_Tx_Queue_Size(size):    
    if size != '':  
        cmd = "echo %s >/proc/dmxmsg/rds_tx_queue_limit" %size
        output = connections.execute_mml( cmd )
    Get_Rds_Tx_Queue_Size()
    return   
    
def Set_Rds_Tx_Queue_Extra_Size(size):    
    if size != '':  
        cmd = "echo %s >/proc/dmxmsg/rds_tx_queue_extra_limit" %size
        output = connections.execute_mml( cmd )
    Get_Rds_Tx_Queue_Extra_Size()
    return
      
def Set_Rds_max_state_query_count(size):
    if size != '':
        cmd = "echo %s >/proc/dmxmsg/rds_max_state_query_count" %size
        output = connections.execute_mml( cmd )
    Get_Rds_max_state_query_count()
    return

g_tx_items = 20
g_rx_items = 10   
def Get_Rds_Tx_Link_Table(node_phy_addr):
    """This keyword is to get rds_link_tbl info
	    | Parameters      | Man. | Description                                  |
        | node_phy_addr   | Yes  | node physical address                        |
    """

    cmd = 'cat /proc/dmxmsg/rds_link_tbl'
    output = connections.execute_mml( cmd )
    result = output.strip()
#    print "output is:%s" % output
#    print "result is:%s" % result
    statistic_list = CommonItem()
    
    linktable_exist_flag = 0
    if len(result) > 0:        
  
        re_item_peer = '(?<=PEER:)\w{4}\s*'
        re_item = '\s*[a-z\s.]+\s*(\d+)\s*' 
        peer_node = re.findall( re_item_peer, result )
        link_data = re.findall( re_item, result )
        
        if link_data is not None:
            for count in range(len(peer_node)) : 
                if int(peer_node[count].strip(),16) == int(node_phy_addr,16): 
                    i = (g_tx_items + g_rx_items - 1)* count
                    statistic_list.tx_frame_seq = link_data[i]
                    i += 1
                    statistic_list.tx_retr_timeout = link_data[i]
                    i += 1
                    statistic_list.tx_retr_frame = link_data[i]
                    i += 1
                    statistic_list.tx_recv_ack = link_data[i]
                    i += 1
                    statistic_list.tx_recv_retr_req = link_data[i]
                    i += 1
                    statistic_list.tx_dropped_ack = link_data[i]
                    i += 1
                    statistic_list.tx_dropped_retr_req = link_data[i]
                    i += 1
                    statistic_list.tx_win_start = link_data[i]
                    i += 1
                    statistic_list.tx_win_end = link_data[i]
                    i += 1
                    i += 1
                    statistic_list.tx_win_full = link_data[i]
                    i += 1
                    statistic_list.tx_queue_push_full = link_data[i]
                    i += 1
                    statistic_list.tx_sleep = link_data[i]
                    i +=6
                    statistic_list.tx_con_retr_timeout = link_data[i]
                    i +=1
                    statistic_list.tx_state_query_count = link_data[i]
                    linktable_exist_flag = 1
                    break

    if linktable_exist_flag == 0:
        statistic_list.tx_frame_seq = 0
        statistic_list.tx_retr_timeout = 0
        statistic_list.tx_retr_frame = 0
        statistic_list.tx_recv_ack = 0
        statistic_list.tx_recv_retr_req = 0
        statistic_list.tx_dropped_ack = 0
        statistic_list.tx_dropped_retr_req = 0
        statistic_list.tx_win_start = 0
        statistic_list.tx_win_end = 0
        statistic_list.tx_win_full = 0
        statistic_list.tx_queue_push_full = 0
        statistic_list.tx_sleep = 0
        statistic_list.tx_con_retr_timeout = 0
        statistic_list.tx_state_query_count = 0
    return statistic_list

def Get_Rds_Rx_Link_Table(node_phy_addr):
    """This keyword is to get rds_link_tbl info
		| Parameters      | Man. | Description                                  |
        | node_phy_addr   | Yes  | node physical address                        |
    """

    cmd = 'cat /proc/dmxmsg/rds_link_tbl'
    output = connections.execute_mml( cmd )
    result = output.strip()
 
    statistic_list = CommonItem()
    linktable_exist_flag = 0
    if len(result) > 0:        
        re_item_peer = '(?<=PEER:)\w{4}\s*'
        re_item = '\s*[a-z\s.]+\s*(\d+)\s*' 
        peer_node = re.findall( re_item_peer, result )
        link_data = re.findall( re_item, result )

        if link_data is not None:
            for count in range(len(peer_node)) : 
                if int(peer_node[count].strip(),16) == int(node_phy_addr,16): 
                    i = (g_tx_items + g_rx_items - 1)* count + g_tx_items
                    statistic_list.rx_exp_frame_seq = link_data[i]
                    i += 1
                    statistic_list.rx_acked = link_data[i]
                    i += 1
                    statistic_list.rx_retr_req = link_data[i]
                    i += 1
                    statistic_list.rx_ack_err = link_data[i]
                    i += 1
                    statistic_list.rx_retr_req_err = link_data[i]
                    i += 1
                    statistic_list.rx_delayed_ack_timeout = link_data[i]
                    i += 1
                    statistic_list.rx_lost_frames = link_data[i]
                    i += 1
                    statistic_list.rx_dup_frame = link_data[i]
                    linktable_exist_flag = 1
                    break
                
    if linktable_exist_flag == 0:
        statistic_list.rx_exp_frame_seq = 0
        statistic_list.rx_acked = 0
        statistic_list.rx_retr_req = 0
        statistic_list.rx_ack_err = 0
        statistic_list.rx_retr_req_err = 0
        statistic_list.rx_delayed_ack_timeout = 0
        statistic_list.rx_lost_frames = 0
        statistic_list.rx_dup_frame = 0
    return statistic_list

                                   
def Compare_tx_link_talble_value(org_value, cur_value, frame_seq = '', retr_timeout = '', retr_frame = '', recv_ack = '', recv_retr_req = '',
                                 dropped_ack = '', dropped_retr_req = '', win_start = '', win_end = '',
                                 win_full = '', sleep = '', queue_push_full = ''):    
    """This keyword is to check tx link table value
		| Parameters             | Man. | Description                        |
        | org_value              | Yes  | orig value                         |
		| cur_value              | Yes  | current value                      |
		| exp_frame_seq          | No   | expect frame seq                   |
		| acked                  | No   | acked                              |
		| retr_req               | No   | retransfor req physical            |
	    | ack_err                | No   | ack err                            |
		| retr_req_err           | No   | retransfor req err                 |
		| delayed_ack_timeout    | No   | delayed ack timeout                |
		| lost_frames            | No   | lost frames                        |
		| dup_frame              | No   | duppliacte frames                  |
    """
    result = 1
    if frame_seq != '':
        cur_frame_seq = int(cur_value.tx_frame_seq)
        print "current frame sequence is: %s\n" % cur_frame_seq
        if cur_frame_seq != int(frame_seq):
            print "   ---   Expect value is:%s \n\n" % frame_seq
            result = 0
    if retr_timeout != '':
        if int(cur_value.tx_retr_timeout) < int(org_value.tx_retr_timeout):
            off_retr_timeout = int(cur_value.tx_retr_timeout) + 65536 - int(org_value.tx_retr_timeout)
        else:
            off_retr_timeout = int(cur_value.tx_retr_timeout) - int(org_value.tx_retr_timeout)
        print "retrans timeout is: %s \n" % off_retr_timeout
        if off_retr_timeout != int(retr_timeout):
            print "   ---   Expect value is:%s \n\n" % retr_timeout
            result = 0
        
    if retr_frame != '':    
        if int(cur_value.tx_retr_frame) < int(org_value.tx_retr_frame):
            off_retr_frame = int(cur_value.tx_retr_frame) + 65536 - int(org_value.tx_retr_frame)
        else:
            off_retr_frame = int(cur_value.tx_retr_frame) - int(org_value.tx_retr_frame)
        print "retrans frame is: %s \n" % off_retr_frame
        if off_retr_frame < int(retr_frame):
            print "   ---   Expect value is:%s \n\n" % retr_frame
            result = 0

    if recv_ack != '':    
        if int(cur_value.tx_recv_ack) < int(org_value.tx_recv_ack):
            off_recv_ack = int(cur_value.tx_recv_ack) + 65536 - int(org_value.tx_recv_ack)
        else:
            off_recv_ack = int(cur_value.tx_recv_ack) - int(org_value.tx_recv_ack)
        print "receive ack is: %s \n" % off_recv_ack
        if off_recv_ack < int(recv_ack):
            print "   ---   Expect value is:%s \n\n" % recv_ack
            result = 0
       
    if recv_retr_req != '':    
        if int(cur_value.tx_recv_retr_req) < int(org_value.tx_recv_retr_req):
            off_recv_retr_req = int(cur_value.tx_recv_retr_req) + 65536 - int(org_value.tx_recv_retr_req)
        else:
            off_recv_retr_req = int(cur_value.tx_recv_retr_req) - int(org_value.tx_recv_retr_req)
        print "receive retrans request is: %s \n" % off_recv_retr_req
        if off_recv_retr_req != int(recv_retr_req):
            print "   ---   Expect value is:%s \n\n" % recv_retr_req
            result = 0
      
    if dropped_ack != '':    
        if int(cur_value.tx_dropped_ack) < int(org_value.tx_dropped_ack):
            off_dropped_ack = int(cur_value.tx_dropped_ack) + 65536 - int(org_value.tx_dropped_ack)
        else:
            off_dropped_ack = int(cur_value.tx_dropped_ack) - int(org_value.tx_dropped_ack)
        print "dropped ack is: %s \n" % off_dropped_ack
        if off_dropped_ack < int(dropped_ack):
            print "   ---   Expect value is:%s \n\n" % dropped_ack
            result = 0
      
    if dropped_retr_req != '':    
        if int(cur_value.tx_dropped_retr_req) < int(org_value.tx_dropped_retr_req):
            off_dropped_retr_req = int(cur_value.tx_dropped_retr_req) + 65536 - int(org_value.tx_dropped_retr_req) 
        else:
            off_dropped_retr_req = int(cur_value.tx_dropped_retr_req) - int(org_value.tx_dropped_retr_req)
        print "dropped retrans request is: %s \n" % off_dropped_retr_req
        if off_dropped_retr_req != int(dropped_retr_req):
            print "   ---   Expect value is:%s \n\n" % dropped_retr_req
            result = 0
     
    if win_start != '':    
        cur_win_start = int(cur_value.tx_win_start)
        print "window start is: %s \n" % cur_win_start
        if cur_win_start != int(win_start):
            print "   ---   Expect value is:%s \n\n" % win_start
            result = 0
    if win_end != '':    
        cur_win_end = int(cur_value.tx_win_end)
        print "window end is: %s \n" % cur_win_end
        if cur_win_end != int(win_end):
            print "   ---   Expect value is:%s \n\n" % win_end
            result = 0

    if win_full != '':    
        if int(cur_value.tx_win_full) < int(org_value.tx_win_full):
            off_win_full = int(cur_value.tx_win_full) + 65536 - int(org_value.tx_win_full)
        else:
            off_win_full = int(cur_value.tx_win_full) - int(org_value.tx_win_full)
        print "sliding window full count is: %s \n" % off_win_full
        if off_win_full < int(win_full):
            print "   ---   Expect value is:%s \n\n" % win_full
            result = 0

    if sleep != '':    
        if int(cur_value.tx_sleep) < int(org_value.tx_sleep):
            off_sleep = int(cur_value.tx_sleep) + 65536 - int(org_value.tx_sleep)
        else:
            off_sleep = int(cur_value.tx_sleep) - int(org_value.tx_sleep)
        print "Tx queue count is: %s \n" % off_sleep
        if off_sleep < int(sleep):
            print "   ---   Expect value is:%s \n\n" % sleep
            result = 0  
            
    if queue_push_full != '':    
        if int(cur_value.tx_queue_push_full) < int(org_value.tx_queue_push_full):
            off_queue_push_full = int(cur_value.tx_queue_push_full) + 65536 - int(org_value.tx_queue_push_full)
        else:
            off_queue_push_full = int(cur_value.tx_queue_push_full) - int(org_value.tx_queue_push_full)
        print "Tx queue extra count is: %s \n" % off_queue_push_full
        if off_queue_push_full < int(queue_push_full):
            print "   ---   Expect value is:%s \n\n" % queue_push_full
            result = 0
                            
    if result == 1:    
        return "successful"
    else:    
        return "error"

def Compare_rx_link_talble_value(org_value, cur_value, exp_frame_seq = '', acked = '', retr_req = '', ack_err = '', retr_req_err = '',
                                 delayed_ack_timeout = '', lost_frames = '', dup_frame = ''): 
    """This keyword is to check rx link table value
		| Parameters             | Man. | Description                        |
        | org_value              | Yes  | orig value                         |
		| cur_value              | Yes  | current value                      |
		| exp_frame_seq          | No   | expect frame seq                   |
		| acked                  | No   | acked                              |
		| retr_req               | No   | retransfor req physical            |
	    | ack_err                | No   | ack err                            |
		| retr_req_err           | No   | retransfor req err                 |
		| delayed_ack_timeout    | No   | delayed ack timeout                |
		| lost_frames            | No   | lost frames                        |
		| dup_frame              | No   | duppliacte frames                  |
    """
    result = 1
    if exp_frame_seq != '':
        cur_exp_frame_seq = int(cur_value.rx_exp_frame_seq)
        print "expect frame sequence is: %s \n" % cur_exp_frame_seq
        if cur_exp_frame_seq != int(exp_frame_seq):
            print "   ---   Expect value is:%s \n\n" % exp_frame_seq
            result = 0
    if acked != '':    
        if int(cur_value.rx_acked) < int(org_value.rx_acked):
            off_acked = int(cur_value.rx_acked) + 65536 - int(org_value.rx_acked)
        else:
            off_acked = int(cur_value.rx_acked) - int(org_value.rx_acked)
        print "acked is: %s \n" % off_acked
        if off_acked < int(acked):
            print "   ---   Expect value is:%s \n\n" % acked
            result = 0
    if retr_req != '':    
        if int(cur_value.rx_retr_req) < int(org_value.rx_retr_req):
            off_retr_req = int(cur_value.rx_retr_req) + 65536 - int(org_value.rx_retr_req)
        else:
            off_retr_req = int(cur_value.rx_retr_req) - int(org_value.rx_retr_req)
        print "retrans request is: %s \n" % off_retr_req
        if off_retr_req != int(retr_req):
            print "   ---   Expect value is:%s \n\n" % retr_req
            result = 0
    if ack_err != '':    
        if int(cur_value.rx_ack_err) < int(org_value.rx_ack_err):
            off_ack_err = int(cur_value.rx_ack_err) + 65536 - int(org_value.rx_ack_err)
        else:
            off_ack_err = int(cur_value.rx_ack_err) - int(org_value.rx_ack_err)
        print "ack error is: %s \n" % off_ack_err
        if off_ack_err != int(ack_err):
            print "   ---   Expect value is:%s \n\n" % ack_err
            result = 0
    if retr_req_err != '':    
        if int(cur_value.rx_retr_req_err) < int(org_value.rx_retr_req_err):
            off_retr_req_err = int(cur_value.rx_retr_req_err) + 65536 - int(org_value.rx_retr_req_err)
        else:
            off_retr_req_err = int(cur_value.rx_retr_req_err) - int(org_value.rx_retr_req_err)
        print "retrans request error is: %s \n" % off_retr_req_err
        if off_retr_req_err != int(retr_req_err):
            print "   ---   Expect value is:%s \n\n" % retr_req_err
            result = 0            
    if delayed_ack_timeout != '':    
        if int(cur_value.rx_delayed_ack_timeout) < int(org_value.rx_delayed_ack_timeout):
            off_delayed_ack_timeout = int(cur_value.rx_delayed_ack_timeout) + 65536 - int(org_value.rx_delayed_ack_timeout)
        else:
            off_delayed_ack_timeout = int(cur_value.rx_delayed_ack_timeout) - int(org_value.rx_delayed_ack_timeout)
        print "delayed ack timeout is: %s \n" % off_delayed_ack_timeout
        if off_delayed_ack_timeout != int(delayed_ack_timeout):
            print "   ---   Expect value is:%s \n\n" % delayed_ack_timeout
            result = 0            
    if lost_frames != '':    
        if int(cur_value.rx_lost_frames) < int(org_value.rx_lost_frames):
            off_lost_frames = int(cur_value.rx_lost_frames) + 65536 - int(org_value.rx_lost_frames)
        else:
            off_lost_frames = int(cur_value.rx_lost_frames) - int(org_value.rx_lost_frames)
        print "lost frames is: %s \n" % off_lost_frames
        if off_lost_frames != int(lost_frames):
            print "   ---   Expect value is:%s \n\n" % lost_frames
            result = 0            
    if dup_frame != '':    
        if int(cur_value.rx_dup_frame) < int(org_value.rx_dup_frame):
            off_dup_frame = int(cur_value.rx_dup_frame) + 65536 - int(org_value.rx_dup_frame)
        else:
            off_dup_frame = int(cur_value.rx_dup_frame) - int(org_value.rx_dup_frame)
        print "duplicate frames is: %s \n" % off_dup_frame
        if off_dup_frame < int(dup_frame):
            print "   ---   Expect value is:%s \n\n" % dup_frame
            result = 0            
            
    if result == 1:    
        return "successful"
    else:    
        return "error"




    
