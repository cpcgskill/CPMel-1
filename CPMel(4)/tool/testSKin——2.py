#!/usr/bin/python
#-*-coding:gbk -*-
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import functools
import pymel.core as pm
import CPMel.core as cmcore
import CPMel.tool.Universal as universal
skinNode, geo, weigth, inf = ('skinCluster1','pSphere1',[t for i in pm.PyNode('pSphere1').vtx for t in range(2)],[0,1])

#获得一个组件列表
cmp_list = [universal.intoComponents(i) for i in universal.translateToName(geo)]
#检查组件列表的数量
if len(cmp_list)<1:
    raise EOFError('geo没有任何对象')
#建立一个组件选择列表
sel_list = om.MSelectionList()
[sel_list.add(i) for i in cmp_list]
if int(sel_list.length())>1:
    raise EOFError('%s 不在一个mesh或者其他对象上'%geo)
    return 1
path,comp = sel_list.getComponent(0)
sel_list.add(skinNode)
skinNode = sel_list.getDependNode(1)

fn_skin = oma.MFnSkinCluster(skinNode)
m_inf = om.MIntArray(inf)
m_weigth = om.MDoubleArray(weigth)
unWeights = fn_skin.getWeights(path,comp,m_inf)

doIt = functools.partial(fn_skin.setWeights,path,comp,m_inf,m_weigth)
undoIt = functools.partial(fn_skin.setWeights,path,comp,m_inf,unWeights)
cmcore.addCommand(doIt, undoIt)

fl_array = fn_skin.getBlendWeights(path,comp)
fn_skin.setBlendWeights(path,comp,fl_array)



class SetWeights:
    '''
    操作蒙皮权重的类
    setWeigths(self,inf,weigth)#设置蒙皮权重
    getWeigths(self,inf)#获得蒙皮权重
    setBlendWeights(self,weigth)#设置DQ混合权重
    getBlendWeights(self)#获得DQ权重
    '''
    def __init__(self,skinNode, geo):
        #获得一个组件列表
        cmp_list = [universal.intoComponents(i) for i in universal.translateToName(geo)]
        #检查组件列表的数量
        if len(cmp_list)<1:
            raise EOFError('geo没有任何对象')
        #建立一个组件选择列表
        sel_list = om.MSelectionList()
        [sel_list.add(i) for i in cmp_list]
        if int(sel_list.length())>1:
            raise EOFError('%s 不在一个mesh或者其他对象上'%geo)
            return 1
        self.path,self.comp = sel_list.getComponent(0)
        sel_list.add(skinNode)
        skinNode = sel_list.getDependNode(1)

        self.fn_skin = oma.MFnSkinCluster(skinNode)
    def setWeigths(self,inf,weigth):
        m_inf = om.MIntArray(inf)
        #执行的权重
        m_weigth = om.MDoubleArray(weigth)
        #撤销的权重
        unWeights = fn_skin.getWeights(self.path,self.comp,m_inf)

        doIt = functools.partial(self.fn_skin.setWeights,self.path,self.comp,m_inf,m_weigth)
        undoIt = functools.partial(self.fn_skin.setWeights,self.path,self.comp,m_inf,unWeights)
        return cmcore.addCommand(doIt, undoIt)
    def getWeigths(self,inf):
        m_inf = om.MIntArray(inf)
        return fn_skin.getWeights(self.path,self.comp,m_inf)
    def setBlendWeights(self,weigth):
        #执行的权重
        m_weigth = om.MDoubleArray(weigth)
        #撤销的权重
        unWeights = fn_skin.getBlendWeights(self.path,self.comp)
        doIt = functools.partial(self.fn_skin.setBlendWeights,self.path,self.comp,m_weigth)
        undoIt = functools.partial(self.fn_skin.setBlendWeights,self.path,self.comp,unWeights)
        return cmcore.addCommand(doIt, undoIt)
    def getBlendWeights(self):
        return fn_skin.getBlendWeights(self.path,self.comp)