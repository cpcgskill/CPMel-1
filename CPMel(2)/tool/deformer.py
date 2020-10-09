#!/usr/bin/python
#-*-coding:gbk -*-
import pymel.core as pm
import maya.cmds as mc
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
import functools
import CPMel.core as cmc

#这是个对大部分变形器都兼容的设置权重函数(变形器节点,权重列表#一个组件对应一个float值#,组件=None)
#如果不输入组件将会默认设置变形器影响的所有对象
#对象中只要有一个组件被影响都会默认设置整个对象所以需要为整个对象的组件都输入一个权重,这是maya的特性无法修改#
def setDeformerWeigth(DeformerNode,weights,geo=None):
    #DeformerNode = 'softMod1'
    #geo = None
    #weights = [0 for i in pm.selected(fl = True)]

    if not pm.objExists(DeformerNode):
        om.MGlobal.displayError('错误输入的变形节点并不存在')
        return False
    if not isinstance(DeformerNode,basestring):
    	DeformerNode = DeformerNode.nodeName()
    if not geo is None:
        if not pm.objExists(geo):
            om.MGlobal.displayError('错误输入的对象并不存在')
            return False
        if not isinstance(geo,basestring):
            geo = ['%s'%i for i in pm.ls(geo)]
        else:
            geo = [geo]
    sel = om.MSelectionList()
    obj = om.MObject()
    path = om.MDagPath()
    comp = om.MObject()
    try:
        sel.add(DeformerNode)
    except:
        om.MGlobal.displayError('无法找到变形节点')
        return False
    sel.getDependNode(0,obj)
    
    try:
        weightGeo = oma.MFnWeightGeometryFilter(obj)
    except:
        om.MGlobal.displayError('输入的变形节点不是正确的对象(簇,软变形...)')
        return False
    float_array = om.MFloatArray()
    append = float_array.append
    try:
        [append(i) for i in weights]
    except:
        om.MGlobal.displayError('输入权重列表错误')
        return False
    sel = om.MSelectionList()
    if not geo is None:
        try:
            [sel.add(i) for i in geo]
        except:
            om.MGlobal.displayError('无法找到变形对象')
            return False

        sel.getDagPath(0,path,comp)
    
        try:
            undoIt_float_array = om.MFloatArray()
            weightGeo.getWeights(path,comp,undoIt_float_array)
            doIt_def = functools.partial(weightGeo.setWeight,path,comp,float_array)
            undoIt_def = functools.partial(weightGeo.setWeight,path,comp,undoIt_float_array)
            cmc.addCommand(doIt_def,undoIt_def)
        except:
            om.MGlobal.displayError('设置权重发生错误')
            return False
    else:
        comp_dict = {'mesh':'vtx','nurbsCurve':'cv','nurbsSurface':'cv','lattice':'pt'}
        for i in range(weightGeo.numOutputConnections()):
            weightGeo.getPathAtIndex(i,path)
            itGeo = om.MItGeometry(weightGeo.outputShapeAtIndex(i))
            length = itGeo.exactCount()
            shape = path.fullPathName()
            shape_type = mc.objectType(shape)
            comp_type = comp_dict[shape_type]
            for t in range(length):
                sel.add('%s.%s[%d]'%(shape,comp_type,itGeo.index()) )
                itGeo.next()
        if sel.length() == 1:
            sel.getDagPath(0,path,comp)
            try:
                undoIt_float_array = om.MFloatArray()
                weightGeo.getWeights(path,comp,undoIt_float_array)
                doIt_def = functools.partial(weightGeo.setWeight,path,0,comp,float_array)
                undoIt_def = functools.partial(weightGeo.setWeight,path,0,comp,undoIt_float_array)
                cmc.addCommand(doIt_def,undoIt_def)
            except:
                om.MGlobal.displayError('设置权重发生错误')
                return False
        crr_id = 0
        for i in range(sel.length()):
            sel.getDagPath(i,path,comp)
            obj_comp_size = om.MFnComponent(comp).elementCount()
            try:
                undoIt_float_array = om.MFloatArray()
                weightGeo.getWeights(path,comp,undoIt_float_array)
                
                doIt_float_array = float_array[crr_id:crr_id+obj_comp_size]
                
                doIt_def = functools.partial(weightGeo.setWeight,path,i,comp,doIt_float_array)
                undoIt_def = functools.partial(weightGeo.setWeight,path,i,comp,undoIt_float_array)
                cmc.addCommand(doIt_def,undoIt_def)
                
                #weightGeo.setWeight(path,i,obj,float_array[crr_id:crr_id+obj_comp_size])
            except:
                om.MGlobal.displayError('设置权重发生错误')
                return False
            crr_id += obj_comp_size
    return True