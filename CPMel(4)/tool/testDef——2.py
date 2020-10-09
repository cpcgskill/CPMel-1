#!/usr/bin/python
#-*-coding:gbk -*-
import pymel.core as pm
import maya.cmds as mc
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
import functools
import CPMel.core as cmc
import CPMel.tool.Universal as universal

#DeformerNode,geo,weights=('cluster1','pSphere1',[0 for i in pm.PyNode('pSphere1').vtx])
def setDeformerWeigth(DeformerNode,geo,weights):
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
    path = om.MDagPath()
    comp = om.MObject()
    sel_list.getDagPath(0,path,comp)

    #获得变形节点
    obj = om.MObject()
    sel.add(DeformerNode)
    sel_list.getDependNode(1,obj)

    try:
        weightGeo = oma.MFnWeightGeometryFilter(obj)
    except:
        raise EOFError('输入的变形节点不是正确的对象(簇,软变形...)')

    float_array = om.MFloatArray()
    append = float_array.append
    try:
        [append(i) for i in weights]
    except:
        raise EOFError('输入权重列表错误')

    try:
        undoIt_float_array = om.MFloatArray()
        weightGeo.getWeights(path,comp,undoIt_float_array)
    except:
        raise EOFError('获得原始权重列表失败')
    doIt_def = functools.partial(weightGeo.setWeight,path,comp,float_array)
    undoIt_def = functools.partial(weightGeo.setWeight,path,comp,undoIt_float_array)
    return cmc.addCommand(doIt_def,undoIt_def)