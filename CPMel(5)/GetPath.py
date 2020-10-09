#!/usr/bin/python
#-*-coding:gbk -*-
'''
获得路径模块
'''
PATH = ''.join(['%s\\'%i for i in __file__.split('\\')][:-1])
MAYAPLUGPATH = '%smayaPlug\\'%PATH
INIPATH = '%siniFile\\'%PATH
TOOLPATH = '%stool\\'%PATH
DLLPATH = '%sDLL\\'%PATH
