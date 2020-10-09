#!/usr/bin/python
#-*-coding:gbk -*-
'''
导入maya插件模块
'''
import os
import re
import maya.cmds as mc
import maya.api.OpenMaya as om
import GetPath as GetPath

path_list = [i for i in os.listdir('%s\\mayaPlug'%GetPath.PATH) if not re.match('__',i)]
for i in path_list:
    try:
        om.MGlobal.displayInfo('CPMel:正在加载%s'%i)
        mc.loadPlugin('%s\\mayaPlug\\%s'%(GetPath.PATH,i))
        om.MGlobal.displayInfo('CPMel:成功加载%s'%i)
    except:
        om.MGlobal.displayInfo ( 'CPMel:加载失败%s' % i )