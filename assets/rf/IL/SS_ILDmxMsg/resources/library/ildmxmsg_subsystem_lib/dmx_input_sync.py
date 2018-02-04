from comm.communication import exceptions
from comm.communication import connections
from comm.communication.helper import *
import re

def start_recv_daemon(daemon_family, expected_msg_num, expected_msg_seq):
    """
    This keyword is to start the daemon in user land to receive msg

    #COMMAND:

    | Parameters       | Man. | Description                                       |
    | daemon_family    | Yes  |daemon family                                      |
    | expected_msg_num | Yes  |expected received msg number                       |
    | expected_msg_seq | Yes  |expected received msg sequence               	  |

    Example
    | start_recv_daemon |22222|2|100:101|
    """
    command = 'mkdir -p /tmp/input_sync_daemon_log'
    connections.execute_mml_without_check(command)

    command = 'dmx_input_sync_daemon -f '+daemon_family+' -n '+expected_msg_num+' -s "'+expected_msg_seq+'"'+">/tmp/input_sync_daemon_log/daemon.log 2>&1 &"
    connections.execute_mml_without_check(command)

def run_test_case(case_id):
    """
    This keyword is to run a test case

    #COMMAND:

    | Parameters       | Man. | Description                                       |
    | case_id          | Yes  |test case id                                       |

    Example
    | run_test_case |0 |
    """
    command = 'dmxtstste -R ' + case_id

    connections.execute_mml_without_check(command)


def kill_input_sync_daemon():
    """
    This keyword is kill monitor process and remove log file

    Example
    | kill_input_sync_daemon|
    """

    command = "kill -SIGINT `ps -ef|grep dmx_input_sync_daemon|grep -v grep|awk '{print $2}'`"
    connections.execute_mml_without_check(command)

