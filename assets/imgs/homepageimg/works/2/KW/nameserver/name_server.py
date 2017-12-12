import re
import time
import math

from comm.communication import connections
from comm.communication import exceptions
from comm.communication.helper import *
from comm.communication.helper import CommonItem, CommonDict

result_file = '/root/naseva_pending.log'
def opt_service_of_name_server(opt_type,list):
    """This keyword is to add, update, remove or pending request service of name server.

    #COMMAND: nasext

    | Parameters | Man. | Description |
    | opt_type    | yes  |'add','remove','update' or 'pending_req'
    | list       | Yes  | Service Info List:server_name,computer,family,process_id,focus,group_service,local_service,replaceable,group_number,delivery,attr |

    | Return value | The result of the operation. |

    Example
    | Opt Service Of Name Server | 'add' | ['test_server','4002','123','0','0','0','0','0','0','0','0']
    | Opt Service Of Name Server | 'update' | ['test_server','4002','123','0','0','0','0','0','0','0','0']
    """
    opt_dict = {'add': ['Add ok',11,'a'],\
               'remove': ['Remove ok',5,'r'],\
               'update': ['Update ok',11,'u'],\
               'pending_req':['',1,'p']
              }
    list = list[:opt_dict[opt_type][1]]
    expect_result = opt_dict[opt_type][0]
    command = ",".join(list)
    command = "nasext "+opt_dict[opt_type][2]+" "+command

    if opt_type == 'pending_req':
        command = command + ',100,1 >' + result_file + '&'
    output = connections.execute_mml(command)
    if output.count(expect_result) != 0:
        return True
    return False

def send_pending_request_of_name_service(service_name,family_id='9999',timeout='100',sync='0'):
    """This keyword is to send pending request service of name server.

    #COMMAND: nasext

    | Parameters      | Man. | Description |
    | service_name    | yes  | name of service user want to request |
    | family_id       | No   | Family id of the PRB registration pending service |
    | timeout         | No   | Timer for the pending request.Default hex |
    | sync            | No   | Synchronized or asynchronized waiting method for request service  |

    | Return value | The result of the operation. |

    """
    command = 'nasext -f ' + family_id + ' p ' + service_name + ',' + timeout + ',' + sync + ' >' + result_file + '&'
    output = connections.execute_mml(command)
    return output.strip().split()[-1]

def get_pending_result_of_name_server():
    """This keyword is to get the pending request result from the result file

    #COMMAND: cat file

    | Parameters | Man. | Description |

    | Return value |call detail information (CommonItem)
     can support the following attributes:
         *service_pid.Computer
         *service_pid.Family
         *service_pid.Process
         *service_pid.Focus
         *service_pid.Group
         *service_pid.Delivery
         *service_pid.Attr

    Example
    |${result}  | Get Pending Result Of Name Server |

    """
    command = 'cat ' + result_file
    output = connections.execute_mml(command)

    item = '\s*Computer\s*:\s*(\w+)\s*Family\s*:\s*(\w+)\s*Process\s*id\s*:\s*(\w+)\s*Focus\s*:\s*(\w+)\s*Group\s*:\s*(\w+)\s*Delivery\s*:\s*(\w+)\s*Attr\s*:\s*(\w+)\s*'
    match = re.search(item, output)
    if match is not None:
        service_pid = CommonItem()
        service_pid.Computer = match.group(1)
        service_pid.Family = match.group(2)
        service_pid.Process = match.group(3)
        service_pid.Focus = match.group(4)
        service_pid.Group = match.group(5)
        service_pid.Delivery = match.group(6)
        service_pid.Attr = match.group(7)
        return service_pid
    else:
        exceptions.raise_ILError("ILCommandExecuteError", output)

def list_content_of_name_server (service_name):
    """This keyword is to get the service pid by the service name

    #COMMAND: nasext g service_name

    | Parameters | Man. | Description |
    | service_name      | Yes  | The name of the service
    | Return value |call detail information (CommonItem)
     can support the following attributes:
         *service_pid.Computer
         *service_pid.Family
         *service_pid.Process
         *service_pid.Focus
         *service_pid.Group
         *service_pid.Delivery
         *service_pid.Attr

    Example
    | Get Service Pid Of Name Server | test_service |

    """
    command = "nasext lc "+ service_name
    output = connections.execute_mml(command)

    item ='Index\s*:\s*(\d+)\w+\s+Service name  :\s*([a-zA-Z0-9\-_]+)\s*Real location :\s*(\d+)\s*Computer      :\s*(\w+)\s*Family        :\s*(\d+)\s*Process Id    :\s*(\d+)\s*Focus         :\s*(\d+)\s*Group service :\s*(\d+)\s*Local service :\s*(\d+)\s*Replaceable   :\s*(\d+)\s*Msg group     :\s*(\d+)\s*Delivery      :\s*(\d+)\s*Attributes    :\s*(\d+)\s*Number of use :\s*(\d+)\s*Token         :\s*(\d+)\s*In use        :\s*(\d+)\s*Can show      :\s*(\d+)'
    match = re.search(item, output)
    print match
    if match is not None:
        service_pid = CommonItem()
        service_pid.Name = match.group(2)
        service_pid.Computer = match.group(4)
        service_pid.Family = match.group(5)
        service_pid.Process = match.group(6)
        service_pid.Focus = match.group(7)
        service_pid.Group = match.group(8)
        service_pid.Local = match.group(9)
        service_pid.Replace = match.group(10)
        service_pid.GroupNum = match.group(11)
        service_pid.Delivery = match.group(12)
        service_pid.Attr = match.group(13)
        return service_pid
    else:
        exceptions.raise_ILError("ILCommandExecuteError", output)
def list_name_of_name_server(service_name):
    """This keyword is to get the service pid by the service name

    #COMMAND: nasext ls service_name

    | Parameters | Man. | Description |
    | service_name      | Yes  | The name of the service
    | Return value |call detail information (CommonItem)

    Example
    | Get Service Pid Of Name Server | test_service |

    """
    command = "nasext ls "+ service_name
    output = connections.execute_mml(command)

    item ="""Service_Name:([a-zA-Z0-9\-_]+)"""
    match = re.search(item, output)

    if match is not None:
        service_pid = CommonItem()
        service_pid.Name = match.group(1)
        return service_pid
    else:
        exceptions.raise_ILError("ILCommandExecuteError", output)
def get_service_pid_of_name_server(service_name):
    """This keyword is to get the service pid by the service name

    #COMMAND: nasext g service_name

    | Parameters | Man. | Description |
    | service_name      | Yes  | The name of the service
    | Return value |call detail information (CommonItem)
     can support the following attributes:
         *service_pid.Computer
         *service_pid.Family
         *service_pid.Process
         *service_pid.Focus
         *service_pid.Group
         *service_pid.Delivery
         *service_pid.Attr

    Example
    | Get Service Pid Of Name Server | test_service |

    """
    command = "nasext g "+ service_name
    output = connections.execute_mml(command)

    item = '\s*Computer\s*:\s*(\w+)\s*Family\s*:\s*(\w+)\s*Process\s*id\s*:\s*(\w+)\s*Focus\s*:\s*(\w+)\s*Group\s*:\s*(\w+)\s*Delivery\s*:\s*(\w+)\s*Attr\s*:\s*(\w+)\s*'
    match = re.search(item, output)
    if match is not None:
        service_pid = CommonItem()
        service_pid.Computer = match.group(1)
        service_pid.Family = match.group(2)
        service_pid.Process = match.group(3)
        service_pid.Focus = match.group(4)
        service_pid.Group = match.group(5)
        service_pid.Delivery = match.group(6)
        service_pid.Attr = match.group(7)
        return service_pid
    else:
        exceptions.raise_ILError("ILCommandExecuteError", output)

def list_service_pid_of_name_server(service_name):
    """This keyword is to list the service PID of the speceified serivce name

    #COMMAND: nasext lp service_name

    | Parameters | Man. | Description |
    | service_name      | Yes  | The name of the service

    | Return value |call detail information (CommonItem)
     can support the following attributes:
         *service_pid.Computer
         *service_pid.Family
         *service_pid.Process
         *service_pid.Focus
         *service_pid.Group
         *service_pid.Delivery
         *service_pid.Attr

    Example
    | List Service Pid Of Name Server | test_service |

    """
    command = "nasext lp "+ service_name
    output = connections.execute_mml(command)
    item = '\s*Computer\s*:\s*(\w+)\s*Family\s*:\s*(\w+)\s*Process\s*Id\s*:\s*(\w+)\s*Focus\s*:\s*(\w+)\s*Group\s*number\s*:\s*(\w+)\s*Delivery\s*:\s*(\w+)\s*Attr\s*:\s*(\w+)\s*'
    items = re.findall(item, output)
    if items is None:
        exceptions.raise_ILError("ILCommandExecuteError", output)

    result = []
    for item in items:
        service_pid = CommonItem()
        service_pid.Computer = item[0]
        service_pid.Family = item[1]
        service_pid.Process = item[2]
        service_pid.Focus = item[3]
        service_pid.Group = item[4]
        service_pid.Delivery = item[5]
        service_pid.Attr = item[6]
        result.append(service_pid)
    return result

def check_alarm_of_name_server(file_name):
    """This keyword is to add service of name server.

    #COMMAND: cat file_name

    | Parameters | Man. | Description |
    | file_name       | Yes  | The alarm file
    | Return value | name server alarm exists in the file or not |

    Example
    | Check Alarm Of Name Server | test.txt |

    """
    command = "cat "+ file_name
    output = connections.execute_mml(command)

    if output.count('SP=13') == 0:
        exceptions.raise_ILError("ILCommandExecuteError", output)

def add_service_of_name_server(service):
    """This keyword is to add service of name server.
    
    Note: "ilnascli a" is a hidden function of cli.

    #COMMAND: ilnascli a

    | Parameters | Man. | Description |
    | service    | Yes  | Service Info List:server_name,computer,family,process_id,focus,group_service,local_service,replaceable,group_number,delivery,attr |

    | Return value | The result of the operation. |

    Example
    | Add Service Of Name Server | ['test_server','4002','123','0','0','0','0','0','0','0','0']
    """
    
    service_info = ",".join(service)
    command = "ilnascli a " + service_info

    output = connections.execute_mml(command)
    if output.count('execute command successfully') != 0:
    	return True
    else:
    	return False

if __name__ == "__main__":
        pass
