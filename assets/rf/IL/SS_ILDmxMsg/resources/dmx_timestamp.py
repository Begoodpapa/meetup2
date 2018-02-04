from comm.communication import exceptions
from comm.communication import connections
from comm.communication.helper import *
from robot import utils
from robot import output 
from robot.libraries.BuiltIn import BuiltIn

import re

        
def Check_Enter_ioctl_Timestamp(log_file, start_index, check_option):
    cmd = "grep " + "ts_ioctl" + " " + log_file + " |awk -F \" \" \'{print $2}\' |awk -F \":\" \'{print $2}\' |awk -F \"-\" \'{print $1}\'"
    output = connections.execute_mml_without_check( cmd )
    timer_s = output.strip().splitlines()
    s_line_count = len(timer_s)
    print timer_s
    cmd = "grep " + "ts_ioctl" + " " + log_file + " |awk -F \" \" \'{print $2}\' |awk -F \":\" \'{print $2}\' |awk -F \"-\" \'{print $2}\'"
    output = connections.execute_mml_without_check( cmd )
    timer_ms = output.strip().splitlines()
    ms_line_count = len(timer_ms)
    print timer_ms
    index_s = int(start_index)
    if ms_line_count < (index_s + 2):
        return 'failure: not received enough message'
    s_gap = int(timer_s[index_s+1]) - int(timer_s[index_s])
    print "s gap is: %d \n" %s_gap
    ms_gap = int(timer_ms[index_s+1]) - int(timer_ms[index_s])
    print "ms gap is: %d \n" %ms_gap
    
    if check_option == 'INCRE':
        if s_gap > 0:
            return "successful"
        else:        
            if ms_gap > 0:
                return "successful"
            else:
                return "error"
    if check_option == 'RANDOM':
        if s_gap == 0 and ms_gap == 0:
            return "successful"
        else:
            return "error"
    
    

def Check_Enter_POW_INT_Timestamp(log_file, check_index, check_option):
    cmd = "grep " + "ts_intrrupt" + " " + log_file + " |awk -F \" \" \'{print $1}\' |awk -F \":\" \'{print $2}\' |awk -F \"-\" \'{print $1}\'"
    output = connections.execute_mml_without_check( cmd )
    timer_s = output.strip().splitlines()
    s_line_count = len(timer_s)
    print timer_s
    cmd = "grep " + "ts_intrrupt" + " " + log_file + " |awk -F \" \" \'{print $1}\' |awk -F \":\" \'{print $2}\' |awk -F \"-\" \'{print $2}\'"
    output = connections.execute_mml_without_check( cmd )
    timer_ms = output.strip().splitlines()
    ms_line_count = len(timer_ms)
    print timer_ms
    index_s = int(check_index)

    if check_option == 'INCRE':
        if ms_line_count < (index_s + 2):
            return 'Check INCRE: not received enough message'
        s_gap = int(timer_s[index_s+1]) - int(timer_s[index_s])
        print "s gap is: %d \n" %s_gap
        if s_gap > 0:
            return "successful"
        else:
            ms_gap = int(timer_ms[index_s+1]) - int(timer_ms[index_s])
            print "ms gap is: %d \n" %ms_gap
            if ms_gap > 0:
                return "successful"
            else:
                return "error"
    if check_option == 'RANDOM':
        if ms_line_count < (index_s + 2):
            return 'Check RANDOM: not received enough message'
        s_gap = int(timer_s[index_s+1]) - int(timer_s[index_s])
        ms_gap = int(timer_ms[index_s+1]) - int(timer_ms[index_s])
        print "s gap is: %d \n" %s_gap
        if s_gap == 0 and ms_gap == 0:
            return "successful"
        else:
            return "error"

    if check_option == 'ZERO':
        if ms_line_count < (index_s + 1):
            return 'Check ZERO: not received enough message'
        if int(timer_s[index_s]) == 0 and int(timer_ms[index_s]) == 0:
            return "successful"
        else:
            return "error"

def Check_Timestamp_Order(log_file, check_option, check_index, expect_gap_s):
    cmd = "grep " + "ts_intrrupt" + " " + log_file + " |awk -F \" \" \'{print $1}\' |awk -F \":\" \'{print $2}\' |awk -F \"-\" \'{print $1}\'"
    output = connections.execute_mml_without_check( cmd )
    pow_timer_s = output.strip().splitlines()
    pow_s_line_count = len(pow_timer_s)
    print "POW Timer S: "
    print pow_timer_s
    cmd = "grep " + "ts_intrrupt" + " " + log_file + " |awk -F \" \" \'{print $1}\' |awk -F \":\" \'{print $2}\' |awk -F \"-\" \'{print $2}\'"
    output = connections.execute_mml_without_check( cmd )
    pow_timer_ms = output.strip().splitlines()
    pow_ms_line_count = len(pow_timer_ms)
    print "POW Timer MS: "
    print pow_timer_ms

    cmd = "grep " + "ts_ioctl" + " " + log_file + " |awk -F \" \" \'{print $2}\' |awk -F \":\" \'{print $2}\' |awk -F \"-\" \'{print $1}\'"
    output = connections.execute_mml_without_check( cmd )
    ioctl_timer_s = output.strip().splitlines()
    ioctl_s_line_count = len(ioctl_timer_s)
    print "IOCTL Timer S: "
    print ioctl_timer_s
    cmd = "grep " + "ts_ioctl" + " " + log_file + " |awk -F \" \" \'{print $2}\' |awk -F \":\" \'{print $2}\' |awk -F \"-\" \'{print $2}\'"
    output = connections.execute_mml_without_check( cmd )
    ioctl_timer_ms = output.strip().splitlines()
    ioctl_ms_line_count = len(ioctl_timer_ms)
    print "IOCTL Timer MS: "
    print ioctl_timer_ms
    
    cmd = "grep " + "ts_inqueue" + " " + log_file + " |awk -F \" \" \'{print $3}\' |awk -F \":\" \'{print $2}\' |awk -F \"-\" \'{print $1}\'"
    output = connections.execute_mml_without_check( cmd )
    inq_timer_s = output.strip().splitlines()
    inq_s_line_count = len(inq_timer_s)
    print "INQUEUE Timer S: "
    print inq_timer_s
    cmd = "grep " + "ts_inqueue" + " " + log_file + " |awk -F \" \" \'{print $3}\' |awk -F \":\" \'{print $2}\' |awk -F \"-\" \'{print $2}\'"
    output = connections.execute_mml_without_check( cmd )
    inq_timer_ms = output.strip().splitlines()
    inq_ms_line_count = len(inq_timer_ms)
    print "INQUEUE Timer MS: "
    print inq_timer_ms
        
    index_s = int(check_index)
    if inq_ms_line_count < (index_s + 1):
        return 'failure: not received enough message'
    expect_gap = int(expect_gap_s)
###compare pow timer before queue timer###
    gap = int(inq_timer_s[index_s]) - int(pow_timer_s[index_s])
    print "pow timer before queue timer %d s" %gap
    if check_option == 'POWINQ':        
        if gap >= expect_gap:
            return "successful"
        else:
            return "error"
    else:        
        if gap <= 0:
            if gap == 0:
                ms_gap = int(inq_timer_ms[index_s]) - int(pow_timer_ms[index_s])
                if ms_gap > 0:
                    print "pow timer before queue timer %d ms" %ms_gap
                else:
                    print "error: pow timer equal queue timer at s, but after ms"
                    return "error"
            else:
                print "error: pow timer after queue timer at s"
                return "error"
###compare ioctl timer before pow timer###                    
    if check_option == 'IOFIRST':
        gap = int(pow_timer_s[index_s]) - int(ioctl_timer_s[index_s])
        print "IOFIRST: ioctl timer before pow timer %d s" %gap
        if gap >= expect_gap:            
            return "successful"
        else:
            return "error"

###compare ioctl timer afte queue timer###
    if check_option == 'IOLAST':
        gap = int(ioctl_timer_s[index_s]) - int(inq_timer_s[index_s])
        print "IOLAST: queue timer before ioctl timer %d s" %gap
        if gap >= expect_gap:            
            return "successful"
        else:
            return "error"
            
    print "no option"
    return "error"
