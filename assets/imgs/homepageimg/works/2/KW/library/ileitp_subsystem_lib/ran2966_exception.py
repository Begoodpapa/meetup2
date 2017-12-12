#!/usr/bin/python
import commands
import os
import time

from comm.communication import connections

def ran2966_check_exception_file(file_name):
   file_prefix="/srv/Log/crash/"
   file_name=file_prefix+file_name
   ret_info={}
   cmd = 'tar xzvf %s -C %s' % (file_name,file_prefix)
   result = connections.execute_mml_without_check(cmd)
   res_file = file_prefix + result.split('\r\n')[1]
   cmd = "grep 'release information' %s" % (res_file)
   result = connections.execute_mml_without_check(cmd)
   if(len(result)>0):
      ret_info['rel_version']=result.split(':')[1]
   else:
      print ret_info
      return false
   cmd = "grep 'subsystem version' %s" % (res_file)
   result = connections.execute_mml_without_check(cmd)
   if(len(result)>0):
      ret_info['sub_version']=result.split(':')[1]
   else:
      print ret_info
      return false
   cmd = "grep 'stack' %s" % (res_file)
   result = connections.execute_mml_without_check(cmd)
   if(len(result)>0):
      ret_info['stack_info']='true'
   else:
      ret_info['stack_info']='false'
      print ret_info
      return False
   print ret_info
   return True

def ran2966_get_latest_exception_file():
   cmd = "ls -ltr /srv/Log/crash/ | tail -n 1 | awk {'print $9'}"
   result = connections.execute_mml_without_check(cmd)
   return result.split('\r\n')[1]

def ran2966_get_exceptionfile_count():
   cmd = 'ls -l /srv/Log/crash | grep ^- | wc -l'
   result = connections.execute_mml_without_check(cmd)
   return result.split('\r\n')[1]

