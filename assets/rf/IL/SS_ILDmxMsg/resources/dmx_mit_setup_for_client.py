#!/usr/bin/python

import atexit
import errno
import getopt
import os
import re
import sys
import commands
import string
import glob

"""
from comm.communication import exceptions
from comm.communication import connections
from comm.communication.helper import *
import re, time
from robot import utils
from robot import output
"""

def exec_cmd(command):
   (status, output) = commands.getstatusoutput(command)
   print 'exec : ', command
   '''
   if status != 0:
          _str="Failed to execute command: %s\n%s\n" % (command, output)
          print "ERROR:", _str
          sys.exit(status)
   '''
   return output
   
def reboot_nodes():
   node_list = exec_cmd('fslistnodes | grep -i PU | grep -v CFPU').splitlines()
   print node_list
   for node in node_list:
      cmd='ssh ' + node + ' reboot'
      exec_cmd(cmd)
      
def get_dmxmsg_ko_md5sum():
   command = 'fsswcli -c '
   build_version=exec_cmd(command).strip('\n')
   
   command = 'uname -r'
   kernel_version=exec_cmd(command).strip('\n')

   # get wnd dmxmsg ko md5sum
   out = '\n---wnd---\n'
   ko_path='/mnt/images/' + build_version + '/mips64/wnd/lib/modules/' + kernel_version + '/drivers/net/dmxmsg/dmxmsg*.ko'
   command = 'md5sum ' + ko_path
   out += exec_cmd(command)
   
   # get std dmxmsg ko md5sum
   out += '\n---std---\n'
   std_kernel_version=exec_cmd('ssh uspu-0 "uname -r"').strip('\n')
   ko_path='/mnt/images/' + build_version + '/mips64/std/lib/modules/' + std_kernel_version + '/drivers/net/dmxmsg/dmxmsg*.ko'
   command = 'md5sum ' + ko_path
   out += exec_cmd(command)

   # get wnd MIT dmxmsg ko md5sum
   out += '\n---wnd MIT---\n'  
   command = 'ssh cfpu-0 "md5sum /opt/nokiasiemens/SS_ILFT/bin/dmxmsg*.ko"'
   out += exec_cmd(command)

   # get wnd MIT dmxmsg ko md5sum
   out += '\n---std MIT---\n'  
   command = 'ssh uspu-0 "md5sum /opt/nokiasiemens/SS_ILFT/bin/dmxmsg*.ko"'
   out += exec_cmd(command)
   
   return out


def check_backup_dir_exist(dir_path):
   command = 'stat ' + dir_path
   output = exec_cmd(command)
   
   if output.find('No such file or directory') == -1:  #not found the error info, so it exist
      return 'exist'
   else:
      return 'not_exist'      

def setup_mit_env():
   """ This keyword is to setup the DMXMSG MIT cases testing env. 
       Step1. Backup orignal dmxmsg ko images;
       Step2. Install MIT version dmxmsg ko images;
       Step3. Reboot whole cluster;
   """
   command = 'fsswcli -c '
   build_version=exec_cmd(command).strip('\n')
   
   command = 'uname -r'
   kernel_version=exec_cmd(command).strip('\n')

   #make dest path writeable
   command = 'mount -o rw,remount /mnt/images/' + build_version + '/mips64/wnd/'
   out = exec_cmd(command)
   command = 'mount -o rw,remount /mnt/images/' + build_version + '/mips64/std/'
   out += exec_cmd(command)
   
   #backup wnd orignal images
   path_prefix='/mnt/images/' + build_version + '/mips64/wnd/lib/modules/' + kernel_version + '/drivers/net/dmxmsg'

   #check if the backup dir is exist, 
   output = check_backup_dir_exist(path_prefix + '_orig_bak/')
   if output == 'exist':
      out += "wnd backup dir exist, skip backup step.\n"
   else:
      command = 'mkdir -p ' + path_prefix + '_orig_bak'
      out += exec_cmd(command)
      command = 'cp  ' +  path_prefix + '/dmxmsg*.ko ' + path_prefix + '_orig_bak/'
      out += exec_cmd(command)
      
   #replace with wnd mit images
   command = 'cp -f /mnt/images/' + build_version + '/mips64/wnd/opt/nsn/SS_ILFT/bin/dmxmsg*.ko ' + path_prefix + '/' 
   out += exec_cmd(command)   
   
   
   
   #backup std orignal images. 
   #TODO: how to get std type node's kernel version samply??
   std_kernel_version=exec_cmd('ssh uspu-0 "uname -r"').strip('\n')
   path_prefix='/mnt/images/' + build_version + '/mips64/std/lib/modules/' + std_kernel_version + '/drivers/net/dmxmsg'
   output = check_backup_dir_exist(path_prefix + '_orig_bak/')
   if output == 'exist':
      out += "std backup dir exist, skip backup step.\n"
   else:
      command = 'mkdir -p ' + path_prefix + '_orig_bak'
      out += exec_cmd(command)
      command = 'cp -f ' +  path_prefix + '/dmxmsg*.ko ' + path_prefix + '_orig_bak/'
      out += exec_cmd(command)

   #replace with wnd mit images
   command = 'cp  -f /mnt/images/' + build_version + '/mips64/std/opt/nsn/SS_ILFT/bin/dmxmsg*.ko ' + path_prefix + '/' 
   out += exec_cmd(command)  

   #command = 'fshascli -rn  /'
   #out += exec_cmd(command)
   
   #print output
   return out



def recover_mit_env():
   """ This keyword is to recover the MIT cases testing env. 
       1. Restore orignal dmxmsg ko images;
       2. Reboot whole cluster;
   """
   command = 'fsswcli -c'
   build_version=exec_cmd(command).strip('\n')
   
   command = 'uname -r'
   kernel_version=exec_cmd(command).strip('\n')
      
   #make dest path writeable
   command = 'mount -o rw,remount /mnt/images/' + build_version + '/mips64/wnd/'
   out = exec_cmd(command)
   command = 'mount -o rw,remount /mnt/images/' + build_version + '/mips64/std/'
   out += exec_cmd(command)
   
   # Restore wnd dmxmsg images
   path_prefix='/mnt/images/' + build_version + '/mips64/wnd/lib/modules/' + kernel_version + '/drivers/net/dmxmsg'
   command = 'cp -f ' +  path_prefix + '_orig_bak/dmxmsg*.ko ' + path_prefix + '/'
   out += exec_cmd(command)   
   
   # Restore std dmxmsg images
   kernel_version=exec_cmd('ssh uspu-0 "uname -r"').strip('\n')
   path_prefix='/mnt/images/' + build_version + '/mips64/std/lib/modules/' + kernel_version + '/drivers/net/dmxmsg'
   command = 'cp -f ' +  path_prefix + '_orig_bak/dmxmsg*.ko ' + path_prefix + '/'
   out += exec_cmd(command)   

   #command = 'fshascli -rn  /'
   #out += exec_cmd(command)
   return out
   
   
def usage():
   print "Usage:"
   print "   dmx_mit_setup.py --install"
   print "   dmx_mit_setup.py --recover"



def test_main():
   command = ""
   if len(sys.argv) > 1:
     command=sys.argv[1].lower()
   else:
      print 'Error: Invalid argument'
      usage()
      return -1
   
   
   print command

   if command == '--install' :
      print get_dmxmsg_ko_md5sum()
      print setup_mit_env()
      print get_dmxmsg_ko_md5sum()
   elif command == '--recover':
      print get_dmxmsg_ko_md5sum()
      print recover_mit_env()
      print get_dmxmsg_ko_md5sum()
   elif command == '--reboot':
      reboot_nodes()
   else: 
      print 'Error: Unknow command : ', command   
    
    
if __name__ == "__main__": test_main()

