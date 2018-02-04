#!/bin/env python
from comm.communication import exceptions
from comm.communication import connections
from comm.communication.helper import *
from robot import utils
from robot import output

# Msg struct
#Irproff_pid(computer:family:process_id);sender_pid (computer:family:process_id.);dst_pid (computer:family:process_id.);seqnum;

def get_record_seq_num(record):
        rec = record.split(';')
        return int(rec[3])

#################################################################################
def check_seq_order_and_count(msg_list, seq_start, total_num):
        """This function to check the input msg list's msg if is in correct order
			| Parameters      | Man. | Description                                  |
			| msg_list        | Yes  | msgs                                         |  
			| seq_start       | Yes  | seq start number                             |
			| total_num       | Yes  | total msg num                                |
        	| Return value    | true or false                                       |
        """
        count     = len(msg_list)
        seq_cur   = get_record_seq_num(msg_list[0])
        if int(seq_start) != seq_cur:
          return ['failure', seq_cur, seq_start]
        if int(total_num) != count:
           return ['failure', count]
        i = 1
        while i < count - 1:
                seq_next = get_record_seq_num(msg_list[i])

                if  seq_cur  >= seq_next :
                        return ['failure', seq_cur, seq_next]
                else:
                        seq_cur = seq_next

                i += 1

        return 'success'

#################################################################################
def check_seq_and_count_for_one_link(input_file, seq_start, count):
        """ This function to check the input file's sequence order and the total num of the msgs
			| Parameters      | Man. | Description                                  |
			| input_file      | Yes  | input_file                                   |  
			| seq_start       | Yes  | seq start number                             |
			| count           | Yes  | total msg count                              |
        	| Return value    | true or false                                      
        """
        command = "cat" + " " + input_file    
        input_string = connections.execute_mml_without_check(command)

        if input_string == "":
            return 'failure: got null string'
        if len(input_string) == 0:
            return 'failure: got null string'

        input_string = input_string.strip()
        input_string = input_string.splitlines()
        if len(input_string) == 0:
                return 'failure: got null list'
        # check the sequence order
        ret = check_seq_order_and_count(input_string, seq_start, count)
        if ret[0] == 'failure' :
                return 'failure: check seq failed at %d' %ret[1]

        return 'success'

