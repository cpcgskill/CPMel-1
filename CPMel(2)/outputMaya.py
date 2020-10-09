#!/usr/bin/python
#-*-coding:gbk -*-
'''
提供几个对maya输出的函数避免每一次都要导入OpenMaya
'''
import maya.api.OpenMaya as om
def displayError(v):
    om.MGlobal.displayError(str(v))
def displayWarning(v):
    om.MGlobal.displayWarning(str(v))
def displayPrint(v):
    om.MGlobal.displayInfo(str(v))