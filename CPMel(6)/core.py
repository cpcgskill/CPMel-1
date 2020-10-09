#!/usr/bin/python
#-*-coding:gbk -*-
'''
在这个核心模块中提供了一些重要的功能
addCommand #将两个函数添加到命令队列里#
Command #命令类#
'''
import importMayaPlug
import maya.cmds as mc
import abc

#将两个函数添加到命令队列里
def addCommand(doIt, undoIt):
    if callable(doIt) and callable(undoIt):
        try:
            mc.CPMeldoIt(d=id(doIt), ud=id(undoIt))
            return 0
        except:
            return 1
    else:
        return 1

class Command ( object ) :
    '''
    命令类
    isCommand #命令是否被创建默认False
    __init__(self,*args,**key) #所有初始化操作应该在此创建
    _redoIt(self) #重做的操作
    _undoIt（self） #撤销的操作
    示例：
        class TestCommand(Command):
            isCommand = True
            def __init__(self, print_a_str, print_b_str):
                print "doIt"
                self.print_a_str = print_a_str
                self.print_b_str = print_b_str
                self._carryOut()
            def _redoIt ( self ) :
                print self.print_a_str
            def _undoIt ( self ) :
                print self.print_b_str
    '''
    isCommand = False
    def _carryOut( self ) :
        addCommand ( self._redoIt , self._undoIt )
    def _redoIt ( self ) :
        pass
    def _undoIt ( self ) :
        pass
#获得所有注册的命令
def getCommand():
    class_list = list()
    crr_class_list = [Command]
    test_list = list()
    while len(crr_class_list)>0:
        for i in crr_class_list:
            test_list = i.__subclasses__()
            [class_list.append(i) for i in test_list]
        crr_class_list = test_list
    return [i for i in class_list if i.isCommand]