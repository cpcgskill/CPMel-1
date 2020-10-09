#!/usr/bin/python
#-*-coding:gbk -*-
import maya.api.OpenMaya as om
def displayError(v):
    om.MGlobal.displayError(str(v))
def displayWarning(v):
    om.MGlobal.displayWarning(str(v))
def displayPrint(v):
    om.MGlobal.displayInfo(str(v))