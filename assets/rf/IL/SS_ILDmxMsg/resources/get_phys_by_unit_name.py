from comm.communication import exceptions
from comm.communication import connections
from comm.communication.helper import *
import re, time
from robot import utils
from robot import output

def get_pindex_from_phys_addr(record):
   rec = re.split('\s+', record)
   length = len(rec[2])
   pid = rec[2][length-2:length]
   return pid

def get_pid_from_phys_addr(record):
   rec = re.split('\s+', record)
   length = len(rec[2])
   pid = rec[2][length-4:length]
   return pid

def get_mo_name(record):
   rec = re.split('\s+', record)
   tmp = rec[5].split('/')
   return tmp[1]

def get_phys_addr_by_node_name(input_unit_name):
   """This function used to get unit type by input unit name.
      If success retuen the correct pid, else return 0xffff
	   | Parameters      | Man. | Description                                  |
	   | input_unit_name | Yes  | unit name                                    |
   """
   cmd = 'ilclifunit -u'
   input_string = connections.execute_mml(cmd)

   if len(input_string) == 0 :
      return int("ffff", 16)

   input_string = input_string.strip()
   input_string = input_string.splitlines()

   count = len(input_string)
   i = 3;
   while i < count :
      if input_string[i] != "" :
         #print input_string[i]
         unit_name = get_mo_name(input_string[i])
         if unit_name == input_unit_name:
            unit_pid = get_pid_from_phys_addr(input_string[i])
            #print 'unit:%s==%s' %(unit_name, unit_pid)
            return int(unit_pid, 16)
         i += 1
      else :
         return int("ffff", 16)

   return int("ffff", 16)

def get_processor_index_by_node_name(input_unit_name):
   """This function used to get unit type by input unit name.
      If success retuen the correct pid, else return 0xffff
	   | Parameters      | Man. | Description                                  |
	   | input_unit_name | Yes  | unit name                                    |
   """
   cmd = 'ilclifunit -u'
   input_string = connections.execute_mml(cmd)

   if len(input_string) == 0 :
      return int("ffff", 16)

   input_string = input_string.strip()
   input_string = input_string.splitlines()

   count = len(input_string)
   i = 3;
   while i < count :
      if input_string[i] != "" :
         #print input_string[i]
         unit_name = get_mo_name(input_string[i])
         if unit_name == input_unit_name:
            unit_pid = get_pindex_from_phys_addr(input_string[i])
            #print 'unit:%s==%s' %(unit_name, unit_pid)
            return int(unit_pid, 16)
         i += 1
      else :
         return int("ffff", 16)
   
   return int("ffff", 16)
