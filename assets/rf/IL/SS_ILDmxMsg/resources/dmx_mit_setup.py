from comm.communication import exceptions
from comm.communication import connections
from comm.communication.helper import *
import re, time
from robot import utils
from robot import output

def exec_cmd(command):
   return connections.execute_mml_without_check(command)

def lock_rg_and_ru():
   command = 'fshascli -lnEF /*QN* /*RG* /SGWNetMgr /SS7SGU /ConfMgmtActivator'
   exec_cmd(command)

def unlock_rg_and_ru():
   command = 'fshascli -unEF /*QN* /*RG* /SGWNetMgr /SS7SGU /ConfMgmtActivator'
   exec_cmd(command)

def reboot_other_nodes():
   node_list = exec_cmd('fslistnodes | grep -i PU | grep -v CFPU').splitlines()
   print node_list
   for node in node_list:
      cmd='ssh ' + node + ' reboot'
      exec_cmd(cmd)

def reload_nodes_dmxmsg_module(node_list):
   #node_list = exec_cmd('fslistnodes | grep -i PU').splitlines()
   print node_list
   for node in node_list:
      cmd='ssh ' + node + ' configModuleRG.sh restart'
      exec_cmd(cmd)


def check_other_nodes_up(node_list):
   #node_list = exec_cmd('fslistnodes | grep -i PU | grep -v CFPU').splitlines()
   print node_list

   nodes=''
   for node in node_list:
       nodes +=  '/' + node.strip('\r\n') + ' '

   cmd = 'fshascli  -s ' + nodes
   result=exec_cmd(cmd)

   if result.find('IDLE') == -1:
      return 'yes'
   else:
      return 'no'


def get_dmxmsg_ko_md5sum():
   command = 'fsswcli -c '
   build_version=exec_cmd(command).strip('\n\r')

   command = 'uname -r'
   kernel_version=exec_cmd(command).strip('\n\r')

   # get wnd dmxmsg ko md5sum
   out = '\n---wnd---\n'
   ko_path='/mnt/images/' + build_version + '/mips64/wnd/lib/modules/' + kernel_version + '/drivers/net/dmxmsg/dmxmsg*.ko'
   command = 'md5sum ' + ko_path
   out += exec_cmd(command)

   # get std dmxmsg ko md5sum
   out += '\n---std---\n'
   std_kernel_version=exec_cmd('ssh uspu-0 "uname -r"').strip('\n\r')
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
   build_version=exec_cmd(command).strip('\n\r')

   command = 'uname -r'
   kernel_version=exec_cmd(command).strip('\n\r')

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
   command = 'cp -f /mnt/images/' + build_version + '/mips64/wnd/opt/nokiasiemens/SS_ILFT/bin/dmxmsg*.ko ' + path_prefix + '/'
   out += exec_cmd(command)

   #backup std orignal images.
   #TODO: how to get std type node's kernel version samply??
   std_kernel_version=exec_cmd('ssh uspu-0 "uname -r"').strip('\n\r')
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
   command = 'cp  -f /mnt/images/' + build_version + '/mips64/std/opt/nokiasiemens/SS_ILFT/bin/dmxmsg*.ko ' + path_prefix + '/'
   out += exec_cmd(command)

   #command = 'fshascli -rn  /'
   #out += exec_cmd(command)

   return out



def recover_mit_env():
   """ This keyword is to recover the MIT cases testing env.
       1. Restore orignal dmxmsg ko images;
       2. Reboot whole cluster;
   """
   command = 'fsswcli -c'
   build_version=exec_cmd(command).strip('\n\r')

   command = 'uname -r'
   kernel_version=exec_cmd(command).strip('\n\r')

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
   kernel_version=exec_cmd('ssh uspu-0 "uname -r"').strip('\n\r')
   path_prefix='/mnt/images/' + build_version + '/mips64/std/lib/modules/' + kernel_version + '/drivers/net/dmxmsg'
   command = 'cp -f ' +  path_prefix + '_orig_bak/dmxmsg*.ko ' + path_prefix + '/'
   out += exec_cmd(command)

   #command = 'fshascli -rn  /'
   #out += exec_cmd(command)
   return out



