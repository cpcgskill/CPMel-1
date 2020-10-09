#!/usr/bin/python
#-*-coding:gbk -*-
'''
在这个核心模块中提供了一些重要的功能
addCommand #将两个函数添加到命令队列里#
Command #尚未实现命令注册类#
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


# 命令注册类
class Command ( object ) :
    isCommand = False
    def __init__ ( self , *args , **kwargs ) :
        self._doIt ( *args , **kwargs )
        addCommand ( self._redoIt , self._undoIt )
    def _doIt ( self , *args , **kwargs ) :
        pass

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