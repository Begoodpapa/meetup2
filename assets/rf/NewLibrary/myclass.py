#coding=utf-8
'''
'''
__Version__ = '0.1'

'''
import robot
'''
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.String import String

import os

class MyClass(object):
    def __init__(self):
        pass

    def printMsgToSomePlace(self,msg):
        print "hello "+msg
        
    def invokesyskw(self,str1,str2):
		"""
		 This keyword is used to release specified UDP connection resource in CACPRB

		#COMMAND: iltrmcli -D -u 192.168.1.1:1024

		| Parameters | Man.| Description       |
		| str1       | Yes | IP address        |
		| str2       | Yes | UDP Port ID       |

		Example
		| invokesyskw | ${IP_address} | ${UDP_PORT} |
		"""	
		BuiltIn().run_keyword("Should Be Equal As Strings", str1, str2)


    def parse_release_result(self,str):
        #tempstr = String().run_keyword("Get Substring", str, 0, 3)
        tempstr = BuiltIn().run_keyword("Get Substring", str, 1, 3)
        print tempstr
        if ("abc" == tempstr):
            return_value = "success"
        else:
            return_value = "failure"
        
        return return_value    
        
    def invokesyskw2(self,str):
		return self.parse_release_result(str)
        
    