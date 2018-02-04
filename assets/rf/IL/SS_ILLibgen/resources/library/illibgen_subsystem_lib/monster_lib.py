from comm.communication import exceptions
from comm.communication import connections
from comm.communication.helper import *
from comm.communication import misc
from illibgen_subsystem_lib.parsemon import *
import re
import os
import random
import time


class givaxi_message:
    """ givaxi_interface_messages: include one c5c5 header + multi c6c6 headers
        Detail document for the interface on sharenet:https://sharenet-ims.inside.nokiasiemensnetworks.com/Overview/D423765679
        current support version 10
    """
    def __init__(self):
        self.c5c5_header = c5c5_header()
        self.c6c6_headers = []
        self.c6c6_headers_count = 0

    def set_c5c5_header_from_file(self,file_items):
    	self.c5c5_header.set_value_from_file(file_items)

    def set_c6c6_header_from_file(self,file_items):
        one_c6c6_header = c6c6_header()
        one_c6c6_header.set_value_from_file(file_items)
        self.c6c6_headers.append(one_c6c6_header)
        self.c6c6_headers_count = len(self.c6c6_headers)
        return (self.c6c6_headers_count - 1)
        
    def check_c6c6_headers_count(self, c6c6_count):
    	if self.c6c6_headers_count <> int(c6c6_count):
    	    exceptions.raise_ILError("ILCommandExecuteError", "The c6c6 headers count is not %s." % c6c6_count)
    
    def check_c6c6_headers_value(self, phy_addr, log_addr, m_t_agent_type, m_t_montype, m_t_spare):
    	for i in range(self.c6c6_headers_count):
            self.c6c6_headers[i].check_value(phy_addr, log_addr, m_t_agent_type, m_t_montype, m_t_spare)
            
    def print_value(self):
    	self.c5c5_header.print_value()
    	for i in range(self.c6c6_headers_count):
            self.c6c6_headers[i].print_value()

class c5c5_header:
    """ one c5c5 header of givaxi_interface_message:
        
    """
    def __init__(self):
        self.header_t_identifier = "c5c5"
        self.header_t_length = "XXXX"
        self.header_t_message_type = "0200"
        self.header_t_version = "000a"
        self.char = ""

    def set_value_from_file(self,file_items):
    	nindex = 0
        self.header_t_identifier = file_items[nindex][2:4] + file_items[nindex][0:2]
        nindex = nindex + 1
        self.header_t_length = file_items[nindex][2:4] + file_items[nindex][0:2] 
        char_length = (int(self.header_t_length,16) - 8) / 2
        nindex = nindex + 1
        self.header_t_message_type = file_items[nindex][2:4] + file_items[nindex][0:2]
        nindex = nindex + 1
        self.header_t_version = file_items[nindex][2:4] + file_items[nindex][0:2]
        nindex = nindex + 1
        while (char_length > 0):
            schar = file_items[nindex]
            nindex = nindex + 1
            char_length = char_length - 1
            schar1 = chr(int(schar[0:2],16))
            schar2 = chr(int(schar[2:4],16))
            self.char = self.char + schar1 + schar2
            
    def check_value(self, message_type, version):
        if (self.header_t_identifier <> "c5c5"):
            exceptions.raise_ILError("ILCommandExecuteError", "The header_t_identifier is not c5c5.")
        if (self.header_t_message_type <> message_type):
            exceptions.raise_ILError("ILCommandExecuteError", "The header_t_message_type is not %s." % message_type)
        if (self.header_t_version <> version):
            exceptions.raise_ILError("ILCommandExecuteError", "The header_t_version is not %s." % version)
        	
    def print_value(self):
        print "c5c5 header:"
        print "header_t_identifier: %s" % (self.header_t_identifier)
    	print "header_t_length: %s" % (self.header_t_length)
    	print "header_t_message_type: %s" % (self.header_t_message_type)
    	print "header_t_version: %s" % (self.header_t_version)
    	print "char: %s" % (self.char)

class c6c6_header:
    """ one c6c6 header of givaxi_interface_message:
        
    """
    def __init__(self):
        self.monheader_t_ident = "c6c6"
        self.monheader_t_length = "XXXX"
        self.monheader_t_unitmbaddr = "ffff"
        self.monheader_t_unitlgaddr = "ffff"
        self.monheader_t_agenttype_t = "01"
        self.monheader_t_montype = "81"
        self.monheader_t_spare = "0000"
        self.monheader_t_messagecounter = "00000000"
        self.zippedheader_t_uncompressedlength = "00000000"

    def set_value_from_file(self,file_items): 
    	nindex = 0
     	self.monheader_t_ident = file_items[nindex][2:4] + file_items[nindex][0:2]
        nindex = nindex + 1
        self.monheader_t_length = file_items[nindex][2:4] + file_items[nindex][0:2] 
        nindex = nindex + 1
        self.monheader_t_unitmbaddr = file_items[nindex][2:4] + file_items[nindex][0:2] 
        nindex = nindex + 1
        self.monheader_t_unitlgaddr = file_items[nindex][2:4] + file_items[nindex][0:2] 
        nindex = nindex + 1
        self.monheader_t_agenttype_t = file_items[nindex][0:2]
        self.monheader_t_montype = file_items[nindex][2:4]
        nindex = nindex + 1
        self.monheader_t_spare = file_items[nindex][2:4] + file_items[nindex][0:2]
        nindex = nindex + 1
        self.monheader_t_messagecounter = file_items[nindex+1][2:4] + file_items[nindex+1][0:2] + file_items[nindex][2:4]+file_items[nindex][0:2]
        nindex = nindex + 2
        self.zippedheader_t_uncompressedlength = file_items[nindex+1][2:4] + file_items[nindex+1][0:2] + file_items[nindex][2:4]+file_items[nindex][0:2]

    def check_value(self, phy_addr, log_addr, m_t_agent_type, m_t_montype, m_t_spare):
    	if (self.monheader_t_ident <> "c6c6"):
            exceptions.raise_ILError("ILCommandExecuteError", "The monheader_t_ident is not c6c6.")
        if (self.monheader_t_unitmbaddr <> phy_addr[2:6]):
            exceptions.raise_ILError("ILCommandExecuteError", "The monheader_t_unitmbaddr is not %s." % phy_addr[2:6])
        if (self.monheader_t_unitlgaddr <> log_addr[2:6]):
            exceptions.raise_ILError("ILCommandExecuteError", "The monheader_t_unitlgaddr is not %s." % log_addr[2:6])
        if (self.monheader_t_agenttype_t <> m_t_agent_type):
            exceptions.raise_ILError("ILCommandExecuteError", "The monheader_t_agenttype_t is not %s." % m_t_agent_type)
        if (self.monheader_t_montype <> m_t_montype):
            exceptions.raise_ILError("ILCommandExecuteError", "The monheader_t_montype is not %s." % m_t_montype)
        if (self.monheader_t_spare <> m_t_spare):
            exceptions.raise_ILError("ILCommandExecuteError", "The monheader_t_spare is not %s." % m_t_spare)
        						
    def print_value(self):
     	print "c6c6 header:"
    	print "monheader_t_ident: %s" % (self.monheader_t_ident)
    	print "monheader_t_length: %s" % (self.monheader_t_length)
    	print "monheader_t_unitmbaddr: %s" % (self.monheader_t_unitmbaddr)
    	print "monheader_t_unitlgaddr: %s" % (self.monheader_t_unitlgaddr)
    	print "monheader_t_agenttype_t: %s" % (self.monheader_t_agenttype_t)
    	print "monheader_t_montype: %s" % (self.monheader_t_montype)
    	print "monheader_t_spare: %s" % (self.monheader_t_spare)
    	print "monheader_t_messagecounter: %s" % (self.monheader_t_messagecounter)
    	print "zippedheader_t_uncompressedlength: %s" % (self.zippedheader_t_uncompressedlength)


def create_monster_workdir(out_dir):
    """This keyword is to create monster work directory to save monitored data.
    
    | Parameters   | Man. | Description            |
    | out_dir      | Yes  | the directory under var/log |
    
    | Return value | none |
    
    Example
    | create monster workdir |  monster_test |
    
    """
    command = 'mkdir -p /var/log/%s ' % (out_dir)
    out = connections.execute_cli(command) 
    command = 'rm -f /var/log/%s/*.*' % (out_dir)
    out = connections.execute_cli(command)

def clear_monster_workdir(out_dir):
    """This keyword is to clear monster work directory.
    
    | Parameters   | Man. | Description            |
    | out_dir      | Yes  | the directory under var/log |
    
    | Return value | none |
    
    Example
    | clear monster workdir |  monster_test |
    
    """
    command = 'rm -f /var/log/%s/*.*' % (out_dir)
    out = connections.execute_cli(command)	
    
def remove_monster_workdir(out_dir):
    """This keyword is to remove monster work directory.
    
    | Parameters   | Man. | Description              |
    | out_dir      | Yes  | the directory under var/log |
    
    | Return value | none |

    Example
    | remove monster workdir |  monster_test |
    
    """
    command = 'rm -f -r /var/log/%s' % (out_dir)
    out = connections.execute_cli(command)
        
def start_monster_at_background_with_compress_mode(computer_id,family_id,out_dir,out_file,message_number,compress_mode,ssize='0',ssequence='0',snicevalue=''):
    """This keyword is to start monster monitoring at background with data compress mode.
    
    | Parameters   | Man. | Description            |
    | computer_id  | Yes  | the computer address   |
    | family_id    | Yes  | the target family to monitor and send message  |
    | out_dir      | Yes  | the directory under var/log |
    | out_file     | Yes  | the output file name   |
    | message_number| Yes | the monitored message nubmer |
    | compress_mode    | Yes  | file output format -b, -o, -g -e |
    | ssize        | No   | split file size limit(unit:Mbytes)|
    | ssequence    | No   | split file up limit sequence |
    | snice value  | No   | nice value |
    
    | Return value | the process id |

    Example
    | result | start monster at background |  0x700 | 0x1B58 | /var/log/test.mgi | 8000 | -e |

    -b <file>
       Stores messages in DX binary format to given file.
    -o <file>
       Stores monitoring data in Linux LIBGEN format to given file.
    -g <file>
      Stores monitoring data in Linux LIBGEN format with compression to
      given file. The file should be uncompressed with gunzip. 
    -e <file>
      Stores monitoring data to given file which follows GIVAXI interface
      The file externtion is .mgi and can be read by Emil. 
    """
    command = 'rm -f /var/log/%s/%s*.*' % (out_dir, out_file)
    out = connections.execute_cli(command)
    if (ssize == '0'):    
        command = '-u %s -f %s -c "SR:NUM=%s" %s /var/log/%s/%s&' % (computer_id,family_id,message_number,compress_mode, out_dir,out_file)
    else:
    	ssize_parameter = '-S %s -N %s -F' % (ssize, ssequence)
    	command = '-u %s -f %s -c "SR:NUM=%s" %s /var/log/%s/%s %s&' % (computer_id,family_id,message_number,compress_mode, out_dir,out_file, ssize_parameter)
    if (snicevalue <> ''):
    	command = 'monster' + ' -P ' + str(snicevalue) + ' ' + command
    else:
    	command = 'monster ' + command
    	
    out = connections.execute_cli(command)
    #return the monster process id
    result_list = out.split()
    result_list_len = len(result_list)
    for i in range(result_list_len):
    	if result_list[i].count('[') > 0 and result_list[i].count(']') > 0:
            return result_list[i+1].strip()
    #sleep 0.5 to make sure monitoring session connected
    time.sleep(0.5)
    return result_list[1].strip()
    
def start_message_sending_for_monster_compress_test(msg_number, msg_size, msg_count):
    """This keyword is to send messages test to test prob for monster compress feature
    
    | Parameters   | Man. | Description              |
    | msg_nubmer   | Yes  | the message number       |
    | msg_size     | Yes  | the message size         |    
    | msg_count    | Yes  | the total message count  |
    
    | Return value | None |

    Example
    | start message sending for monster compress test |  1000 | 8000 | 10 |
    """
    command = 'dmxsend -- -h %s,*,C385,0,0,0,0,%s -b xkFB4,BB' % (msg_size,msg_number)
    msg_count = int(msg_count)
    for i in range(msg_count):
    	out = connections.execute_mml_without_check(command)
    	
def stop_monsters_and_wait_for_exit(monster_pids):
    """This keyword is to stop monster process and wait for monster process totally exit
    | Parameters    | Man. | Description                   |
    | monster_pids  | Yes  | the running monster pid list  |
    
    | Return value  | none |
    
    Example
    | stop monster and wait for exit |  [12345, 23221] |
    """
    monster_pids_len = len(monster_pids)
    for i in range(monster_pids_len):
        command = "kill -2 %s" % (monster_pids[i])
        out = connections.execute_mml_without_check(command)
    timeout = 20
    monster_stop_count = 0
    for i in range(timeout):
        if (out.count('Done') == monster_pids_len):
            print "monster process is fully finished and file is saved."
            break
        command = "sleep 0.3"
        out += connections.execute_mml_without_check(command)

def start_monster_performance_test(test_round, interval_time):
    command = "cd /opt/nokiasiemens/testutils"
    out = connections.execute_mml_without_check(command)
    for i in range(int(test_round)):
        command = "perftest.py sthread.ini &"
        out = connections.execute_mml_without_check(command)
        time.sleep(int(interval_time))
    
def compressed_files_can_be_unzipped_successfully(dir_name,files_name):
    """This keyword is to unzip the compressed files using gzip
           
    | Parameters   | Man. | Description              |
    | dir_name   | Yes  | the directory name       |
    | files_name  | Yes  | the array of files name            |
    
    | Return value | new_files_name |

    Example
    | compressed files can be unzipped successfully |   monster_test | ["test0.gz","test1.gz"] |
    """
    error_log = "not in gzip format"
    new_files_name = []
    files_len = len(files_name)
    for i in range(files_len):
    	_file_should_exist(dir_name,files_name[i])
    	command = "gzip -l /var/log/%s/%s" % (dir_name,files_name[i])
    	output = connections.execute_mml_without_check(command)
    	if (output.count(error_log)>0):
    		exceptions.raise_ILError("ILCommandExecuteError", "The compressed file can not be unzipped.")
    	command = "gzip -d -f /var/log/%s/%s" % (dir_name,files_name[i])
    	output = connections.execute_mml_without_check(command)
    	if (output.count(error_log)>0):
    		exceptions.raise_ILError("ILCommandExecuteError", "The compressed file can not be unzipped.")
    	new_files_name.append(files_name[i].replace('.gz', ''))
    return new_files_name
def convert_file_names_for_split_file_mode(file_name, split_count):
    """This keyword is to return a file name list for split file mode.
    | Parameters   | Man. | Description              |
    | file_name    | Yes  | the file name            |
    | split_count  | Yes  | how many split files should be generated |
    
    | Return value | a file name list for example ["test1-000.bin", "test1-001.bin", "test1-002.bin" |
    
    Example
    | convert file names for split file mode | "test1.bin" | 3 |
    """
    split_files = file_name.split(".")
    new_file_names = []
    for i in range (int(split_count)):
        new_file_names.append(split_files[0] + "-00" + str(i) + "." + split_files[1])
    return new_file_names

def check_bin_header_is_correct(dir_name, files_name):
    """This keyword is to check whether the LIBGEN bin header is correct or not.
    | Parameters   | Man. | Description              |
    | dir_name     | Yes  | the directory name       |
    | files_name   | Yes  | the array of files name  |
    
    | Return value | None |
    
    Example
    | check bin header is correct | monster_test | ["test1-000.bin","test1-001.bin"] | 
    """
    bin_header_context = "0000000 0000 000c 0003 0000 0000 0000"
    file_count = len(files_name)
    for i in range (file_count):
        command = "hexdump -n 16 /var/log/" + dir_name + "/" + files_name[i]
        output = connections.execute_mml_without_check(command)
        if (output.count(bin_header_context) <=0 ):
            exceptions.raise_ILError("ILCommandExecuteError", "The LIBGEN bin header is not correct for file: %s." % files_name[i])
            
def messages_can_be_read_successfully_from_file(dir_name,files_name,test_prb,message_number,total_message_count,header_only='0'):
    """This keyword is to use readste to read the monitored files and check message prb, message number, total message count is correct.
    | Parameters   | Man. | Description              |
    | dir_name     | Yes  | the directory name       |
    | files_name   | Yes  | the array of files name  |
    | test_prb     | Yes  | test prb number          |
    | message_number  | Yes  | message number        |
    | total_message_count   | Yes  | total message count         |
    
    | Return value | None |
    
    Example
    | message can be read successfully from file |   monster_test | ["test1","test2"] | C385 | 8000 | 10 |
    """
    files_name_len = len(files_name)
    check_test_prb = 0
    check_message_number = 0
    check_message_count = 0
    test_prb = test_prb[2:6]
    received_test_prb = "RECEIVED BY: %s" % (test_prb)
    for i in range(files_name_len):
        file_name = files_name[i]
    	_file_should_exist(dir_name,file_name)
    	file_name = "/var/log/%s/%s" % (dir_name,file_name)
    	if (header_only == '1'):
    		command = "readste -H -i %s" % (file_name)
    	else:
    	    command = "readste -i %s" % (file_name)
    	output = connections.execute_mml_without_check(command)
    	l = get_msg_from_buf(output)
    	msg_list = [parse_msg(i) for i in l]
    	for msg in msg_list:
            if msg['recv']['computer'] <> int(test_prb,16):
                print msg['recv']['computer'], int(test_prb,16)
                exceptions.raise_ILError("ILCommandExecuteError", "The monitored message family is not %s." % test_prb)
            if msg['msg']['number'] <> int(message_number,16):
                print msg['msg']['number'], int(message_number,16)
                exceptions.raise_ILError("ILCommandExecuteError", "The monitored message number is not %s." % message_number)
        check_message_count = check_message_count + len(msg_list)
        print 'msg count: ', check_message_count
    if (check_message_count <> int(total_message_count)):
        exceptions.raise_ILError("ILCommandExecuteError", "The total message count is not %s." % total_message_count)
    	
def message_count_is_correct_in_the_monitored_files(dir_name,files_name,total_message_count):
    """This keyword is to use readste to check the message count is correct for the monitored files.
    | Parameters   | Man. | Description              |
    | output_dir   | Yes  | the directory name       |
    | output_files  | Yes  | the array of files name            |
    | total_message_count   | Yes  | total message count         |
    
    | Return value | None |
    
    Example
    | message count is correct in the monitored files |   monster_test | ["test1","test2"] | 300 |
    """
    files_name_len = len(files_name)
    check_message_count = 0
    for i in range(files_name_len):
    	_file_should_exist(dir_name,files_name[i])
    	file_name = "/var/log/%s/%s" % (dir_name,files_name[i])
    	command = "readste -i %s -a summary" % (file_name)
    	output = connections.execute_mml_without_check(command)
    	result_list = output.splitlines()
    	result_list_len = len(result_list)
    	for i in range(result_list_len):
    	    if result_list[i].count('message frames'):
    	        check_message_count = check_message_count + int(result_list[i].split()[0])
    print 'Total message count in files is: %s.' % (str(check_message_count))
    if (check_message_count <> int(total_message_count)):
        exceptions.raise_ILError("ILCommandExecuteError", "The monitored message count is not correct.")
	   	
def get_headers_from_monster_output_file(dir_name, file_name):
    """This keyword is to get the headers from monster output file
           
    | Parameters   | Man. | Description              |
    | output_dir   | Yes  | the directory name       |
    | output_file  | Yes  | the file name            |
    
    | Return value | a givaxi header(c5c5, multi x c6c6) |

    Example
    | ${header} | get_headers_from_monster_output_file |   monster_test | test.mgi |
    """
    #_file_should_exist(dir_name, file_name)
    output_givaxi_message = givaxi_message()
    temp_file = "givaxi_file_temp.mgi"
    command = "rm -f /var/log/%s/%s" % (dir_name,temp_file)
    connections.execute_mml_without_check(command)
    command = "cp -f /var/log/%s/%s /var/log/%s/%s" % (dir_name,file_name,dir_name,temp_file)
    connections.execute_mml_without_check(command)
    #dump the c5c5 header
    header_items = _dump_header_content_according_header_length(dir_name,temp_file,"c5c5")
    output_givaxi_message.set_c5c5_header_from_file(header_items)
    header_length = str(int(output_givaxi_message.c5c5_header.header_t_length,16))
    ##remove the c5c5 header from the file
    data_left =_remove_data_from_file(header_length, dir_name, temp_file)
    
    if (data_left == 1):
    	c6c6_header_left = 1
    else:
    	c6c6_header_left = 0
    	
    while (c6c6_header_left == 1):
    	header_items = _dump_header_content_according_header_length(dir_name,temp_file,"c6c6")
    	c6c6_index = output_givaxi_message.set_c6c6_header_from_file(header_items)
    	header_length = str(int(output_givaxi_message.c6c6_headers[c6c6_index].monheader_t_length,16))
    	##remove the c6c6 header and data from the file
    	data_left = _remove_data_from_file(header_length, dir_name, temp_file)
    	if (data_left == 0):
    	    c6c6_header_left = 0
    
    output_givaxi_message.print_value()
    
    command = "rm -f /var/log/%s/%s" % (dir_name,temp_file)
    connections.execute_mml(command)
    
    return output_givaxi_message
    
def monster_output_file_format_is_correct_according_givaxi_monitoring_interface(dir_name, file_name,omu_phy_address,omu_log_address):
    """This keyword is to check that the file is saved correctly according to givaxi monitoring interface
           
    | Parameters   | Man. | Description              |
    | output_dir   | Yes  | the directory name       |
    | output_file  | Yes  | the file name            |
    | omu_phy_address | Yes  | the omu physical address |
    | omu_log_address | Yes  | the omu logical address  |
    
    | Return value | all headers length(c5c5, c6c6) |

    Example
    | monster output file format is correct according to givaxi monitoring interface |   monster_test | test.mgi | 0x0100 | 0x4002 |
    """
    headers_length = []
    _file_should_exist(dir_name, file_name)
    output_givaxi_message = givaxi_message()
    temp_file = "givaxi_file_temp.mgi"
    command = "rm -f /var/log/%s/%s" % (dir_name,temp_file)
    connections.execute_mml_without_check(command)
    command = "cp -f /var/log/%s/%s /var/log/%s/%s" % (dir_name,file_name,dir_name,temp_file)
    connections.execute_mml_without_check(command)
    #dump the c5c5 header
    header_items = _dump_header_content_according_header_length(dir_name,temp_file,"c5c5")
    output_givaxi_message.set_c5c5_header_from_file(header_items)
    header_length = str(int(output_givaxi_message.c5c5_header.header_t_length,16))
    headers_length.append(header_length)
    ##remove the c5c5 header from the file
    data_left =_remove_data_from_file(header_length, dir_name, temp_file)
    
    if (data_left == 1):
    	c6c6_header_left = 1
    else:
    	c6c6_header_left = 0
    	exceptions.raise_ILError("ILCommandExecuteError", "There are no c6c6 headers found in the file.")
    	
    while (c6c6_header_left == 1):
    	header_items = _dump_header_content_according_header_length(dir_name,temp_file,"c6c6")
    	c6c6_index = output_givaxi_message.set_c6c6_header_from_file(header_items,omu_phy_address,omu_log_address)
    	header_length = str(int(output_givaxi_message.c6c6_headers[c6c6_index].monheader_t_length,16))
    	headers_length.append(header_length)
    	##remove the c6c6 header and data from the file
    	data_left = _remove_data_from_file(header_length, dir_name, temp_file)
    	if (data_left == 0):
    		c6c6_header_left = 0
    
    output_givaxi_message.print_value()
    
    command = "rm -f /var/log/%s/%s" % (dir_name,temp_file)
    connections.execute_mml(command)
    
    return headers_length

def output_files_headers_should_be_correct_according_to_givaxi_interface_format(givaxi_header, c6c6_count, h_t_msg_type, h_t_version, phy_addr, log_addr, m_t_agent_type, m_t_montype, m_t_spare):    
    """This keyword is to check if header content is correct
           
    | Parameters        | Man. | Description                 |
    | givaxi_header     | Yes  | the header contents object  |
    | c6c6_count        | Yes  | the c6c6 header count       |
    | h_t_msg_type      | Yes  | the c5c5 header message type|
    | h_t_version       | Yes  | the c5c5 header version     |
    | phy_addr          | Yes  | the c6c6 header physical address|
    | log_addr          | Yes  | the c6c6 header logical address |
    | m_t_agent_type    | Yes  | the c6c6 header agent type |
    | m_t_montype       | Yes  | the c6c6 header mon type   |
    | m_t_spare         | Yes  | the c6c6 header spare      |
    
    | Return value | None |
    
    """
    givaxi_header.c5c5_header.check_value(h_t_msg_type, h_t_version)
    givaxi_header.check_c6c6_headers_count(c6c6_count)
    givaxi_header.check_c6c6_headers_value(phy_addr, log_addr, m_t_agent_type, m_t_montype, m_t_spare)	

def check_top_output_for_monster(pid, suser):
    """This keyword is to check the top output for one monster
           
    | Parameters   | Man. | Description              |
    | pid          | Yes  | the monster process id   |
    | suser        | Yes  | the user name            |
    
    | Return value | all the threads nice value |
    
    ['\x1b[m\x0f', '2840', 'root', '20', '0', '28052', '6688', '6396', 'S', '0.0', '0.6', '0:00.01', 'monster', '\x1b[m\x0f']
    PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND                                              
    28497 root      20   0 28052 6680 6400 S  0.0  0.6   0:00.01 monster                                              
    28499 root      20   0 28052 6680 6400 S  0.0  0.6   0:00.00 monster                                              
    28500 root      20   0 28052 6680 6400 S  0.0  0.6   0:00.02 monster 
    """    
    command = "top -H -n 1 -p %s" % (pid)
    out = connections.execute_cli(command)
    #return the NICE values
    nice_values = []
    result_list = out.splitlines()
    result_list_len = len(result_list)
    for i in range(result_list_len):
    	if result_list[i].count('PID USER      PR  NI') > 0:
    		for j in range(3):
    		    strings = result_list[i+j+1].split()
    		    print strings
    		    strings_len = len(strings)
    		    for k in range(strings_len):
    			    if (strings[k].count(suser) > 0):
    				    nice_values.append(strings[k+2])
    return nice_values

def nice_value_should_be_correct(top_nice_values, nice_value):
    result = 0
    nice_values_len = len(top_nice_values)
    for i in range(nice_values_len):
        if (top_nice_values[i] == nice_value):
            result = 1
    if (result == 0):
    	exceptions.raise_ILError("ILCommandExecuteError", "The nice value is not correct.")

def monster_should_start_failed_with_invalid_nice_value(invalid_nice_value):
    #Error: invalid -P parameter, the nice value should be in range [-20, 19]
    command = 'monster -P %s' % (invalid_nice_value)
    out = connections.execute_mml_without_check(command)
    result_list = out.splitlines()
    result_list_len = len(result_list)
    for i in range(result_list_len):
    	print result_list[i]
    	if result_list[i].count('Error: invalid -P parameter, the nice value should be valid') > 0:
    		result = result_list[i]
    		return result
    exceptions.raise_ILError("ILCommandExecuteError", "The error output is not found for invalid nice value.")

def monster_add_one_non_root_user_and_switch_to_this_user():
    command = "useradd nroot -u 1111 -g 14 -d /home/monster_nice -s /bin/bash -m"
    out = connections.execute_mml_without_check(command)
    command = "su root"
    out = connections.execute_mml_without_check(command)

def monster_switch_to_root_user_and_remove_non_root_user():
    command = "exit"
    out = connections.execute_mml_without_check(command)
    command = "userdel nroot -r"
    out = connections.execute_mml_without_check(command)

def monster_should_start_ok_for_defined_nice_value(nice_value, suser, file_id):
    if (nice_value == 'default'):
        command = 'monster'
    else:
        command = 'monster' + ' -P ' + nice_value
    if (suser == 'root'):
    	command = command + ' -o monster_' + str(file_id) + '.bin &'
    else:
    	command = command + ' &'
    out = connections.execute_cli(command)
    #return the monster process id
    result_list = out.split()
    result_list_len = len(result_list)
    for i in range(result_list_len):
    	if result_list[i].count('[') > 0 and result_list[i].count(']') > 0:
            return result_list[i+1].strip()
    return result_list[1].strip()
			
def monster_should_start_failed_for_non_root_user_with_negative_nice_value(negative_nice_value):
    #Warning, setpriority(tid: 9930) to -5 failed: Permission denied
    result = ''
    command = 'monster -P %s' % (negative_nice_value)
    out = connections.execute_mml_without_check(command)
    result_list = out.splitlines()
    result_list_len = len(result_list)
    for i in range(result_list_len):
    	print result_list[i]
    	print result_list[i].count('Permission denied')
    	if (result_list[i].count('Permission denied') > 0):
    	    result = result_list[i]
    	    return result
    #if (result == ''):
     #   exceptions.raise_ILError("ILCommandExecuteError", "The error output is not found for negative nice value for non root user.")
	
	
def _file_should_exist(dir_name, file_name):
    """This keyword is to check if the file exists
           
    | Parameters   | Man. | Description              |
    | dir_name     | Yes  | the directory name       |
    | file_name    | Yes  | the file name            |
    
    | Return value | file_length |
    
    """
    file_length = 0
    command = "ll /var/log/%s/%s" % (dir_name, file_name)
    out = connections.execute_cli(command)
    if (out.count('No such file or directory')>0):
        exceptions.raise_ILError("ILCommandExecuteError", "The compressed file is not saved.")
    else:
    	file_length = out.split()[4]
    print file_length
    return file_length
    
def _dump_header_content_according_header_length(dir_name,file_name,header_type):
    """This keyword is to dump header content according to the defined length in the file header
           
    | Parameters   | Man. | Description              |
    | dir_name     | Yes  | the directory name       |
    | file_name    | Yes  | the file name            |
    | header_type  | Yes  | c5c5 or c6c6             |
    
    | Return value | dumped file items list |
    
    """
    if (header_type == "c5c5"):
        command = "hexdump -n 4 /var/log/%s/%s" % (dir_name,file_name)
        output = connections.execute_mml_without_check(command)
        file_items = _get_file_content_from_hexdump_output(output)
        header_t_length = str(int(file_items[1][2:4]+file_items[1][0:2],16))
    else:
    	header_t_length = "20"
    command = "hexdump -n %s /var/log/%s/%s" % (header_t_length, dir_name,file_name)
    output = connections.execute_mml_without_check(command)
    file_items = _get_file_content_from_hexdump_output(output)    
    return file_items
    
def _get_file_content_from_hexdump_output(output):
    result_list = output.split()
    result_list_len = len(result_list)
    file_item_length = 0
    file_items = []
    for i in range(result_list_len):
      	if (len(result_list[i])<=4):
            file_items.append(result_list[i])
            file_item_length = file_item_length + 1
    return file_items
    
def _remove_data_from_file(data_length, dir_name, file_name):
    """This keyword will remove the data from a file

    | return value | whether file has data left |
    """
    left_data = 0
    command = "rm -f /var/log/%s/temp*" % (dir_name)
    connections.execute_mml_without_check(command)
    file_length = _file_should_exist(dir_name, file_name)
    split_size = int(file_length) / 2 + 1
    print split_size
    suffix_length = 255
    split_file_name = file_name
    while ((split_size > int(data_length)) and (suffix_length > 15)):
    	command = "split -a 1 -b %s /var/log/%s/%s /var/log/%s/temp%s" % (str(split_size), dir_name, split_file_name, dir_name, hex(suffix_length)[2:4])
    	connections.execute_mml_without_check(command)
    	command = "rm -f /var/log/%s/%s" % (dir_name, split_file_name)
    	connections.execute_mml_without_check(command)
    	split_file_name = "temp%sa" % (hex(suffix_length)[2:4])
    	file_length = _file_should_exist(dir_name, split_file_name)
    	split_size = int(file_length) / 2 + 1
    	suffix_length = suffix_length - 1
    command = "split -a 1 -b %s /var/log/%s/%s /var/log/%s/temp0" % (data_length, dir_name, split_file_name, dir_name)
    connections.execute_mml_without_check(command)
    command = "rm -f /var/log/%s/%s" % (dir_name, split_file_name)
    connections.execute_mml_without_check(command)
    command = "ll /var/log/%s/temp*" % (dir_name)
    connections.execute_mml_without_check(command)
    header_file = "temp0a"
    command = "rm -f /var/log/%s/%s" % (dir_name, header_file)
    connections.execute_mml_without_check(command)
    command = "ll /var/log/%s/temp*" % (dir_name)
    output = connections.execute_mml_without_check(command)
    if (output.count('No such file or directory') == 0 ):
    	command = "rm -f /var/log/%s/%s" % (dir_name, file_name)
    	connections.execute_mml_without_check(command)
    	command = "cat /var/log/%s/temp* > /var/log/%s/%s" % (dir_name, dir_name, file_name)
    	connections.execute_mml_without_check(command)
    	command = "rm -f /var/log/%s/temp*" % (dir_name)
    	connections.execute_mml_without_check(command)
    	left_data = 1
    return left_data

def get_the_zip_file_from_c6c6_file(one_givaxi_header, output_dir,output_file):
    """This keyword will remove the c6c6/c5c5 file header and move the compressed data to a zip file
    
    | return value | new files name list |
    """
    new_files_name_list = []
    c5c5_header_length = one_givaxi_header.c5c5_header.header_t_length
    command = "rm -f /var/log/%s/newfile*" % (output_dir)
    connections.execute_mml_without_check(command)
    for i in range(one_givaxi_header.c6c6_headers_count):
    	#remove the header
    	header_length = str(int(c5c5_header_length,16) + 20)
    	_remove_data_from_file(header_length,output_dir, output_file)
    	#get the data to a zip file
    	data_length = str(int(one_givaxi_header.c6c6_headers[i].monheader_t_length,16) - 20)
    	command = "split -a 4 -b %s /var/log/%s/%s /var/log/%s/temp" % (data_length, output_dir, output_file, output_dir)
    	connections.execute_mml_without_check(command)
    	command = "ll /var/log/%s/temp*" % (output_dir)
    	connections.execute_mml_without_check(command)
    	data_file = "tempaaaa"
    	new_file_name = "newfile%s.bin.gz" % (str(i))
    	command = "cp /var/log/%s/%s /var/log/%s/%s" % (output_dir, data_file, output_dir, new_file_name)
    	connections.execute_mml_without_check(command)
    	command = "ll /var/log/%s" % (output_dir)
    	connections.execute_mml_without_check(command)
    	command = "rm -f /var/log/%s/temp*" % (output_dir)
    	connections.execute_mml_without_check(command)
    	#remove the data
    	_remove_data_from_file(data_length,output_dir, output_file)
    	new_files_name_list.append(new_file_name)
    	c5c5_header_length = "0"
    return new_files_name_list

def start_monster_monitoring_on_special_node(computer_id,family_id,node_name):
    """ This keywork is to Start Monster Process On Sepcail Node To Monitor Specail Family.

    #COMMAND: monster -u 0x700 -f 0x193B
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | node-name        | No   | monster will be started up on which node    |
    | Return value     | session id for the started monitor session  |

    Example
    | ${result} | start monster monitoring on special node | 0x700  | 0x193B |
    """
    
    return start_command_on_cloned_connection(_start_monster_monitoring,computer_id,family_id,node_name)

def execute_command_on_cloned_conn(in_cmd,node_name):
    """ This keywork is to Start Monster Process On Sepcail Node To Monitor Specail Family.

    #COMMAND: monster -u 0x700 -f 0x193B
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | node-name        | No   | monster will be started up on which node    |
    | Return value     | session id for the started monitor session  |

    Example
    | ${result} | start monster monitoring on special node | 0x700  | 0x193B |
    """

    return start_command_on_cloned_connection(_execute_cmd_only,in_cmd,node_name)

def _start_monster_monitoring(computer_id,family_id,node_name):
    """ This keywork is to start the command on the cloned session

    #COMMAND: monster -u 0x700 -f 0x193B
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | node-name        | Yes  | monster will be started up on which node    |

    Example
    | ${result} | _start monster monitoring  | 0x700  | 0x193B | CLA-0 |
    """

    command = "ssh -o StrictHostKeyChecking=no " + node_name
    connections.execute_mml_without_check(command)

    command = 'monster -u %s -f %s'%(computer_id,family_id)
    connections.get_current_connection().write(command)

def _execute_cmd_only(in_cmd,node_name,*in_args):
    """ This keywork is to start the command on the cloned session

    #COMMAND: monster -u 0x700 -f 0x193B
    
    | Parameters       | Man. | Description                                 |
    | comptuer_id      | Yes  | target computer address                     |
    | family_id        | Yes  | target family address                       |
    | node-name        | Yes  | monster will be started up on which node    |

    Example
    | ${result} | _start monster monitoring  | 0x700  | 0x193B | CLA-0 |
    """
    command = "ssh -o StrictHostKeyChecking=no " + node_name
    connections.execute_mml_without_check(command)

    if len(in_args) > 0:
        command = in_cmd % (in_args)
    else:
        command = in_cmd
    connections.get_current_connection().write(command)

def stop_monster_and_get_result(id):
    """ This keywork is to Stop Monster And Get Result.
    #COMMAND: none
    
    | Parameters       | Man. | Description                                 |
    | id               | Yes  | the started session id                      |

    | Return value     | command str, the catched message string            |
    Example
    | ${result} | stop monster and get result | ${id} |
    """
    result = stop_command_on_connection(id)
    print result
    return result
        
if __name__=="__main__":
    print "\n %s: If you see this, it means this py file has no compiling error.\n" % (sys.argv[0])
