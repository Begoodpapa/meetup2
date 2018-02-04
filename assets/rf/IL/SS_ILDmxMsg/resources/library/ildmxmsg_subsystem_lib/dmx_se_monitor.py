from comm.communication import exceptions
from comm.communication import connections
from comm.communication.helper import *
import re

def start_se_monitor(target_phy, target_fam, condition_str, monitored_msg_num):
    """
    This keyword is to return execution result contain "successful" when transmisson all messages between sender and receiver success
    #COMMAND:

    | Parameters       | Man. | Description                                       |
    | target_phy       | Yes  |target physical address                            |
    | target_fam       | Yes  |target family address                              |
    | condition_str    | Yes  |monitor condition string                           |
    | monitored_msg_num| Yes  |monitored message number                           |

    Example
    | start_se_monitor |1700|44d|[src_phy]=1700|monitor.log|2
    """
    command = 'mkdir -p /tmp/monitor_log'
    connections.execute_mml_without_check(command)

    command = '/opt/nsn/SS_ILFT/bin/dmxmsg_monitor_daemon -p '+target_phy+' -f '+target_fam+' -n '+monitored_msg_num+' -c "'+condition_str+'"'+">/tmp/monitor_log/dmxmsg_monitor_daemon.log 2>&1 &"

    connections.execute_mml_without_check(command)


def get_se_monitored_msg_num():
    """
    This keyword is to return number of monitored msg

    Example
    | get_se_monitored_msg_num |
    """

    command = "cat /tmp/monitor_log/dmxmsg_monitor_daemon.log|grep BOTTOM|wc -l"

    out = connections.execute_mml_without_check(command)
    msg_number = out.strip()
    return msg_number

def remove_monitor_and_log_file():
    """
    This keyword is kill monitor process and remove log file

    Example
    | remove_monitor_and_log_file |
    """

    command = "kill -SIGINT `ps -ef|grep dmxmsg_monitor_daemon|grep -v grep|awk '{print $2}'`"
    connections.execute_mml_without_check(command)

    command = "rm -rf /tmp/monitor_log"
    connections.execute_mml_without_check(command)

