from comm.communication import exceptions
from comm.communication import connections
from comm.communication.helper import *
import re

def make_dmx_sending(sender, receiver, burst='', interval='', number='', length='', workmode='', timeout='', 
                     group_addr='', change_burst='', change_interval='', change_number='', change_context=''):
    """
    This keyword is to return execution result contain "successful" when transmisson all messages between sender and receiver success
    #COMMAND: dmxcli 

    | Parameters       | Man. | Description                                       |
    | sender           | Yes  |sender address                                     |
    | receiver         | Yes  |receiver address                                   |
    | burst            | No   |The number of message sent without interval        |
    | interval         | No   |The interval between burst, measured with ms       |
    | number           | No   |The number of bursts                               |
    | length           | No   |The length of message                              |
    | workmode         | No   |Work mode:"1" echo, "0" not echo                   |   
    | timeout          | No   |Time out                                           |   
    | group_addr       | No   |Group address to be config                         |   
    | change_burst     | No   |The number of group address change without interval|
    | change_interval  | No   |The interval between change_burst, measured with ms|   
    | change_number    | No   |The number of group address change bursts          |   
    | change_context   | No   |Change group address context "1" or number "0"     | 
    | Return value     | command execution result contain "successful" if success |

    Example
    | make_dmx_sending |0:ad9c:0|1700:44d:0|100|1|10|100|0|100|FFB,3,0,100,200|2|50|2|1|
    """
    command = "dmxcli -s "+sender+" -r "+receiver
    if burst != '':
        command += " -b " + burst
    if interval != '':
        command += " -i " + interval    
    if number != '':                      
        command += " -n " + number    
    if length != '':                   
        command += " -l " + length 
    if workmode != '':
        command += " -m " + workmode
    if timeout != '':
        command += " -t " + timeout 
    if group_addr != '':                      
        command += " -G " + group_addr    
    if change_burst != '':                   
        command += " -B " + change_burst 
    if change_interval != '':                      
        command += " -I " + change_interval    
    if change_number != '':                   
        command += " -N " + change_number 
    if change_context != '':                      
        command += " -A " + change_context   

    out = connections.execute_mml_without_check(command)
    return out

