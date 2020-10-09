#!/usr/bin/python
#-*-coding:gbk -*-
import mayaPlug
import maya.cmds as mc
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
#尚未实现命令注册类
class Command(object):
    pass