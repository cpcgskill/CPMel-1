#!/usr/bin/python
# encoding:gbk
# 作者：张隆鑫
# 完成时间:2019.7.29
# 最近修改时间:
'''
属性：
方法：
函数：
SoftModificationToWeight 软修改转权重计算权重节点返回每个值为（点id，点权重）
SoftModificationToJointWeight 软修改转关节权重输入（关节，模型，蒙皮节点）
访问示例：
选择模型组件
SoftModificationToWeight()
选择模型组件
SoftModificationToJointWeight(关节,模型,蒙皮节点)
'''
import maya.OpenMaya as om
import pymel.core as pm


def SoftModificationToWeight ( ) :
    richSel = om.MRichSelection ( )
    om.MGlobal.getRichSelection ( richSel )
    richSelList = om.MSelectionList ( )
    richSel.getSelection ( richSelList )
    component = om.MObject ( )
    richSelList.getDagPath ( 0 , om.MDagPath ( ) , component )
    componentFn = om.MFnSingleIndexedComponent ( component )
    return [ (componentFn.element ( i ) , componentFn.weight ( i ).influence ( )) for i in
             range ( 0 , componentFn.elementCount ( ) ) ]


def SoftModificationToJointWeight ( Joint , mesh , skin ) :
    idSkin = SoftModificationToWeight ( )
    [ pm.skinPercent ( skin , mesh.vtx [ i [ 0 ] ] , transformValue = (Joint , i [ 1 ]) ) for i in idSkin ]
    return 0
