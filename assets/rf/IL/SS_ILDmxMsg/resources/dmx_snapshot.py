from comm.communication import exceptions
from comm.communication import connections
from comm.communication.helper import *
from robot import utils
from robot import output 
from robot.libraries.BuiltIn import BuiltIn

import re

def Get_Send_Msg_Num_Every_Time(total_num, peer_cout):
    result = int(total_num, 10) / int(peer_cout,10)
    return str(result)

def Get_Send_Msg_Num_Last_Time(total_num, peer_cout):
    result = int(total_num) % int(peer_cout)
    return str(result)

def Check_Snapshot_Time_Scape_Less_Then_Expected_Value(log_file, end_str, expect_time):
    cmd = "grep '" + end_str + "' " + log_file
    output = connections.execute_mml_without_check( cmd )
    end_log = output.strip()
    if len(end_log) == 0:
        print "There is no end log"
        result = 0   
    else:
        stack_time = end_log.split(',')[3]
        print stack_time
        time_value = stack_time.split('=')[1]
        if int(time_value) < int(expect_time):
            result = 1
        else:
            print "time value is: %s, expect_time is: %s\n" % (time_value,expect_time)
            result = 0
    if result == 1:
        return "successful"
    else:
        return "error"

def Get_Snapshot_Family_Count(log_file, recv_fam):
    cmd = "grep " + "'kernel: dmxmsg: snapshot:'" + " " + log_file + " | " + "grep " + "'next:[0-9A-F]\{4\}, PID:[0-9A-F]\{4\}:0\{0,3\}'" + recv_fam + "':[0-9A-F]\{4\},'" + " | wc -l"
    dumplog = connections.execute_mml_without_check( cmd )
    log_count = dumplog.strip()
    return str(log_count)

def Get_Snapshot_Log_Count(log_file):
    log_count = 0
    cmd = "grep " + "'kernel: dmxmsg: snapshot:'" + " " + log_file
    output = connections.execute_mml_without_check( cmd )
    log_count = len(output.strip().splitlines())
    if log_count == 0:
        print "There is no snapshot log"
    return str(log_count)

def Get_Snapshot_Signal_Msg_Count(log_file, signal_num):
    cmd = "grep " + "'kernel: dmxmsg: snapshot:'" + " " + log_file
    output = connections.execute_mml_without_check( cmd )
    dumplog_list = output.strip().splitlines()
    log_cout = len(dumplog_list)
    msg_num = 0
    i = 0
    signal_hex_number = int(signal_num)
    while i < log_cout :
        log_item = dumplog_list[i].strip()
        re_item = "(?<=number:)\d*%X," % signal_hex_number
        match = re.findall( re_item, log_item ) 
        if match:
            doc_len = len(log_item.split(','))
            msg_num_str = log_item.split(',')[doc_len-1]
            msg_num = msg_num_str.strip().split(' ')[1]
            return msg_num
        i += 1
    print "There is no log with number 0x%X" %signal_hex_number
    return msg_num

def Get_Snapshot_Sender_And_Signal_Count(log_file, send_fam, signal_num):
    cmd = "grep " + "'kernel: dmxmsg: snapshot:'" + " " + log_file
    output = connections.execute_mml_without_check( cmd )
    dumplog_list = output.strip().splitlines()
    log_cout = len(dumplog_list)
    msg_num = 0
    i = 0
    signal_hex_number = int(signal_num)
    while i < log_cout :
        log_item = dumplog_list[i].strip()
        re_item_sig = "(?<=number:)\d*%X," % signal_hex_number
        match_sig = re.findall( re_item_sig, log_item ) 
        if match_sig:
            re_item_fam = "(?<=PID:\d{4}:)\d*%s:\d{4}, attr:" % send_fam
            match_fam = re.findall( re_item_fam, log_item )
            if match_fam:
                doc_len = len(log_item.split(','))
                msg_num_str = log_item.split(',')[doc_len-1]
                msg_num = msg_num_str.strip().split(' ')[1]
                return msg_num
        i += 1
    print "There is no log with sender family 0x%x, number 0x%X " % (send_fam, signal_hex_number)
    return msg_num

def Get_Snapshot_Top_Five_PID_Count(log_file, recv_fam): 
    cmd = "grep " + "'kernel: dmxmsg: snapshot:'" + " " + log_file
    output = connections.execute_mml_without_check( cmd )
    dumplog_list = output.strip().splitlines()
    log_cout = len(dumplog_list)
    msg_num = 0
    i = 0
    while i < log_cout :
        log_item = dumplog_list[i].strip()
        re_item_top = "\s*Top 5 PRBs in RU\s*"
        match_top = re.findall( re_item_top, log_item ) 
        if match_top:
            print "find top 5 prb log \n"
            re_item_fam = "(?<=\(0x%s\)=)\d*" % recv_fam
            match_fam = re.findall( re_item_fam, log_item )
            if match_fam:
                return match_fam[0].strip()
        i += 1
    print "There is no top log with receiver family 0x%s" % recv_fam
    return msg_num

def Convert_To_Up_Case(input_str):
    return input_str.upper()

def modify_syslog_conf(file_context, output_file):
    output = file_context.splitlines()
    i = 0
    line_no = 0
    new_line= ""
    for line in output:
       if (line.lower().find('syslog_log')) > 0:
          line_seg=line.split(',')
          new_line = line_seg[0] + "," + line_seg[1]
          line_no = i
       i += 1
    
    output[line_no] = new_line
    
    command = 'echo >' + output_file 
    connections.execute_mml_without_check(command)

    for line in output:      
        command = "echo '" + line  + "' >> " + output_file 
        connections.execute_mml_without_check(command)
