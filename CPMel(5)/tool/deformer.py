#!/usr/bin/python
# encoding:gbk
# 作者：张隆鑫
# 完成时间:2020.1.17
# 最近修改时间:
'''
这是个操作maya变形器的模块
'''
import pymel.core as pm
import maya.cmds as mc
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
import functools
import CPMel.core as cmc
if __name__ == "__main__":
    import CPMel.tool.Universal as universal
else:
    import Universal as universal
#这是个对大部分变形器都兼容的设置权重函数(变形器节点, 需要设置的被影响的对象, 权重列表#一个组件对应一个float值)
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
    sel_list.add(DeformerNode)
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


class SetDeformerWeigth:
    """
    操作变形器权重的类
    __init__(self, DeformerNode, geo)#(变形器,需要设置的被影响的对象)
    setWeight(self,weights)#设置权重
    getWeight(self)#获得权重
    #示例
    import CPMel.tool.deformer as deformer
    reload(deformer)
    DeformerNode,geo,weights=('cluster1','pSphere1',[0 for i in pm.PyNode('pSphere1').vtx])
    setDeformerWeigth = deformer.SetDeformerWeigth(DeformerNode,geo)
    setDeformerWeigth.getWeight()
    setDeformerWeigth.setWeight(weights)
    """
    def __init__(self, DeformerNode, geo):
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
        self.path = om.MDagPath()
        self.comp = om.MObject()
        sel_list.getDagPath(0,self.path,self.comp)

        #获得变形节点
        obj = om.MObject()
        sel_list.add(DeformerNode)
        sel_list.getDependNode(1,obj)

        try:
            self.weightGeo = oma.MFnWeightGeometryFilter(obj)
        except:
            raise EOFError('输入的变形节点不是正确的对象(簇,软变形...)')
    def setWeight(self,weights):
        float_array = om.MFloatArray()
        append = float_array.append
        try:
            [append(i) for i in weights]
        except:
            raise EOFError('输入权重列表错误')

        try:
            undoIt_float_array = om.MFloatArray()
            self.weightGeo.getWeights(self.path,self.comp,undoIt_float_array)
        except:
            raise EOFError('获得原始权重列表失败')
        doIt_def = functools.partial(self.weightGeo.setWeight,self.path,self.comp,float_array)
        undoIt_def = functools.partial(self.weightGeo.setWeight,self.path,self.comp,undoIt_float_array)
        return cmc.addCommand(doIt_def,undoIt_def)
    def getWeight(self):
        try:
            float_array = om.MFloatArray()
            self.weightGeo.getWeights(self.path,self.comp,float_array)
        except:
            raise EOFError('获得权重列表失败')
        return list(float_array)


#以下被放弃#
#这是个对大部分变形器都兼容的设置权重函数(变形器节点,权重列表#一个组件对应一个float值#,组件=None)
#如果不输入组件将会默认设置变形器影响的所有对象
#对象中只要有一个组件被影响都会默认设置整个对象所以需要为整个对象的组件都输入一个权重,这是maya的特性无法修改#
# def setDeformerWeigth(DeformerNode,weights,geo=None):
#     #DeformerNode = 'softMod1'
#     #geo = None
#     #weights = [0 for i in pm.selected(fl = True)]

#     if not pm.objExists(DeformerNode):
#         om.MGlobal.displayError('错误输入的变形节点并不存在')
#         return False
#     if not isinstance(DeformerNode,basestring):
#     	DeformerNode = DeformerNode.nodeName()
#     if not geo is None:
#         if not pm.objExists(geo):
#             om.MGlobal.displayError('错误输入的对象并不存在')
#             return False
#         if not isinstance(geo,basestring):
#             geo = ['%s'%i for i in pm.ls(geo)]
#         else:
#             geo = [geo]
#     sel = om.MSelectionList()
#     obj = om.MObject()
#     path = om.MDagPath()
#     comp = om.MObject()
#     try:
#         sel.add(DeformerNode)
#     except:
#         om.MGlobal.displayError('无法找到变形节点')
#         return False
#     sel.getDependNode(0,obj)
    
#     try:
#         weightGeo = oma.MFnWeightGeometryFilter(obj)
#     except:
#         om.MGlobal.displayError('输入的变形节点不是正确的对象(簇,软变形...)')
#         return False
#     float_array = om.MFloatArray()
#     append = float_array.append
#     try:
#         [append(i) for i in weights]
#     except:
#         om.MGlobal.displayError('输入权重列表错误')
#         return False
#     sel = om.MSelectionList()
#     if not geo is None:
#         try:
#             [sel.add(i) for i in geo]
#         except:
#             om.MGlobal.displayError('无法找到变形对象')
#             return False

#         sel.getDagPath(0,path,comp)
    
#         try:
#             undoIt_float_array = om.MFloatArray()
#             weightGeo.getWeights(path,comp,undoIt_float_array)
#             doIt_def = functools.partial(weightGeo.setWeight,path,comp,float_array)
#             undoIt_def = functools.partial(weightGeo.setWeight,path,comp,undoIt_float_array)
#             cmc.addCommand(doIt_def,undoIt_def)
#         except:
#             om.MGlobal.displayError('设置权重发生错误')
#             return False
#     else:
#         comp_dict = {'mesh':'vtx','nurbsCurve':'cv','nurbsSurface':'cv','lattice':'pt'}
#         for i in range(weightGeo.numOutputConnections()):
#             weightGeo.getPathAtIndex(i,path)
#             itGeo = om.MItGeometry(weightGeo.outputShapeAtIndex(i))
#             length = itGeo.exactCount()
#             shape = path.fullPathName()
#             shape_type = mc.objectType(shape)
#             comp_type = comp_dict[shape_type]
#             for t in range(length):
#                 sel.add('%s.%s[%d]'%(shape,comp_type,itGeo.index()) )
#                 itGeo.next()
#         if sel.length() == 1:
#             sel.getDagPath(0,path,comp)
#             try:
#                 undoIt_float_array = om.MFloatArray()
#                 weightGeo.getWeights(path,comp,undoIt_float_array)
#                 doIt_def = functools.partial(weightGeo.setWeight,path,0,comp,float_array)
#                 undoIt_def = functools.partial(weightGeo.setWeight,path,0,comp,undoIt_float_array)
#                 cmc.addCommand(doIt_def,undoIt_def)
#             except:
#                 om.MGlobal.displayError('设置权重发生错误')
#                 return False
#         crr_id = 0
#         for i in range(sel.length()):
#             sel.getDagPath(i,path,comp)
#             obj_comp_size = om.MFnComponent(comp).elementCount()
#             try:
#                 undoIt_float_array = om.MFloatArray()
#                 weightGeo.getWeights(path,comp,undoIt_float_array)
                
#                 doIt_float_array = float_array[crr_id:crr_id+obj_comp_size]
                
#                 doIt_def = functools.partial(weightGeo.setWeight,path,i,comp,doIt_float_array)
#                 undoIt_def = functools.partial(weightGeo.setWeight,path,i,comp,undoIt_float_array)
#                 cmc.addCommand(doIt_def,undoIt_def)
                
#                 #weightGeo.setWeight(path,i,obj,float_array[crr_id:crr_id+obj_comp_size])
#             except:
#                 om.MGlobal.displayError('设置权重发生错误')
#                 return False
#             crr_id += obj_comp_size
#     return True