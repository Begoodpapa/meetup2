#coding=utf-8
'''
'''
__Version__ = '0.1'

'''
import robot
from robot.libraries.BuiltIn import BuiltIn
'''
import os

class MyClass(object):
    def __init__(self):
        pass
 
    def ElementShouldBeInsideTheList(self,item,list):
        returnValue = ""
        for listitem in list:
            if (item == listitem):
                returnValue = "success"
                break
            else:
                returnValue = "failure"
			
        return returnValue