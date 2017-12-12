import re

from comm.communication import exceptions
from comm.communication import connections

def interrogate_log(tmp_file='', param='', unit='', famid='', level='' ):
    """This keyword is to interrogate log

    #COMMAND: ILlogdisp

    | Parameters | Man. | Description |
    | tmp_file   | No  | tmp file to store the interrogate result, need be deleted after case execute
    | command param | No | command param, such as: -h or --help
    | unit       | No  | unit type |
    | famid      | No  | family id combination, such as: famid=1 or famid=1 proc=2 or famid=1 proc=2 focus=3 |
    | level      | No  | log level, including: crit, err, test, info |

    | Return value | Successful: True, Failure: False |

    Example
    | ${result} | interrogate_log | unit=OMU famid=1,2 proc=2 focus=3 | level=crit,info |
    | Should Be True | ${result} |

    """
    if tmp_file != '':
        command = "ILlogdisp %s %s %s %s > %s" % (param, unit, famid, level, tmp_file)
    else:
        command = "ILlogdisp %s %s %s %s" % (param, unit, famid, level)

#    print command
    out = connections.execute_cli(command)

    return out

def copy_file(file1, file2):
    """This keyword is to copy file1 to file2 us cp command

    #COMMAND: cp

    | Parameters | Man. | Description |
    | file1   | Yes | source file name
    | file2   | Yes | destination name

    | Return value | Successful: True, Failure: False |

    Example
    | ${result} | copy_file | test.txt | test.bak |
    | Should Be True | ${result} |

    """
    #just copying file/folder but not symbol links
    command = "cp -rfL %s %s" % (file1, file2)
    out = connections.execute_mml_without_check(command, 'y')
    if out.count("Read-only file system")!=0:
       connections.execute_mml("mount -o rw,remount /mnt/sysimg")
       connections.execute_cli(command, 'y')
    
    return True

def empty_file(file):
    """This keyword is to copy file1 to file2 us cp command

    #COMMAND: :>

    | Parameters | Man. | Description |
    | file   | Yes | file name that will be cleared

    | Return value | Successful: True, Failure: False |

    Example
    | ${result} | clear_file | test.txt |
    | Should Be True | ${result} |

    """

    command = ":> %s " % (file)
    out = connections.execute_cli(command)

    return True

def remove_file(file):
    """*DEPRECATED* Please use 'delete_file' to instead of.
    This keyword is to remove file1 to file2 us cp command

    #COMMAND: rm -rf

    | Parameters | Man. | Description |
    | file   | Yes | file name that will be removed

    | Return value | Successful: True, Failure: False |

    Example
    | ${result} | clear_file | test.txt |
    | Should Be True | ${result} |

    """

    command = "rm -rf %s " % (file)
    out = connections.execute_cli(command)

    return True

if __name__ == "__main__":
    interrogate_log("tmp.txt", "", "unit=OMU-1", "famid=11 proc=22 focus=33", "level=test")
