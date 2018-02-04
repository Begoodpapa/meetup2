from comm.communication import exceptions
from comm.communication import connections
from comm.communication.helper import *

def convert_to_string_list(list):
	ss = []
	for i in list:
		sub_list = i.split(" ")
		ss.append([ int(i,16) for i in sub_list if i != ''])
	return ss

def query_result_ordinal(start):
	return map(lambda x:x+start, [0,2,5,8,11])

def linux_for_every_addr_list_the_found_address_tuple_should_match_itself(list):
	nl = convert_to_string_list(list)
	rec = nl[0]
	log_addr = rec[1]
	result = connections.execute_mml_without_check('dmx_generic_stub query_logic_addr %x' % log_addr).split("\r\n")[2]
	query_list = [int(dummp,16) for i, dummp in enumerate(result.split(' ')) if i in set(query_result_ordinal(1))]
	print query_list
	if rec !=  query_list:
		return "Fail"
	return "Pass"

def se_for_every_addr_list_the_found_address_tuple_should_match_itself(list):
	nl = convert_to_string_list(list)
	rec = nl[0]
	log_addr = rec[1]
	result = connections.execute_mml_without_check('dmx_generic_stub se_query_logic_addr 5B5D:44d:0 %x' % log_addr).split("\r\n")[1]
	query_list = [int(dummp,16) for i, dummp in enumerate(result.split(' ')) if i in set(query_result_ordinal(4))]
	print query_list
	if rec !=  query_list:
	        return "Fail"
	return "Pass"
