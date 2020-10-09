#!/usr/bin/python
# encoding:gbk
# 作者：张隆鑫
# 完成时间:2020.1.17
# 最近修改时间:
'''
这是个操作maya蒙皮的模块
'''
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import functools
import pymel.core as pm
import CPMel.core as cmcore
import CPMel.tool.Universal as universal
#刚性化权重
def rigidWeighting(mesh_list = None):
    if mesh_list is None:mesh_list = [i.getShape() for i in pm.selected()]
    for i in mesh_list:
        skinNode = i.history(type='skinCluster')
        if len(skinNode)<1:
            continue
        skinNode = skinNode[0]
        inf = range(len(skinNode.getInfluence()))
        weigth = [s for t in skinNode.getWeights(i) for s in rigidList(t)]
        setWeigths(skinNode, i, inf, weigth)
    return 0
#刚性化列表只有一个为1的值其他都为0
def rigidList(in_v):
    test_max = max(in_v)
    i_id = range(len(in_v))
    try:
        max_id = in_v.index(1)
    except:
        max_id = None
        crr_v = None
        for t,id in zip(in_v, i_id):
            if crr_v is None or crr_v<t:
                crr_v = t
                max_id=id
    return [1 if i == max_id else 0 for i in i_id]
#设置蒙皮权重(skinNode, geo, weigth, inf = None)(蒙皮节点,蒙皮对象,权重,影响对象的索引数组（ps：如果没有这个的话将会默认操作所有）)
# def setWeigths(skinNode, geo, weigth, inf = None): 
#     if inf is None:
#         unWeights = [t for i in skinNode.getWeights(geo) for t in i]
#         inf = range(len(skinNode.getInfluence()))
#     else:
#         unWeights = [
#             t for i in
#             zip(*[
#                 [
#                     t for t in skinNode.getWeights(geo, i)
#                 ] for i in inf
#             ])
#             for t in i
#         ]
#     doIt = functools.partial(skinNode.setWeights, geo, inf, weigth)
#     undoIt = functools.partial(skinNode.setWeights, geo, inf, unWeights)
#     return cmcore.addCommand(doIt, undoIt)

#设置蒙皮权重(skinNode, geo, inf, weigth)(蒙皮节点,蒙皮对象,影响对象的索引数组,权重)
def setWeigths(skinNode, geo, inf, weigth):
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
    #撤销的权重
    unWeights = fn_skin.getWeights(path,comp,m_inf)

    doIt = functools.partial(fn_skin.setWeights,path,comp,m_inf,m_weigth)
    undoIt = functools.partial(fn_skin.setWeights,path,comp,m_inf,unWeights)
    return cmcore.addCommand(doIt, undoIt)
class SetWeights:
    '''
    操作蒙皮权重的类
    __init__(self,skinNode, geo)#(蒙皮节点,需要设置的被蒙皮节点影响的对象)
    setWeigths(self,inf,weigth)#设置蒙皮权重
    getWeigths(self,inf)#获得蒙皮权重
    setBlendWeights(self,weigth)#设置DQ混合权重
    getBlendWeights(self)#获得DQ权重
    示例
    import CPMel.tool.skin as skin
    reload(skin)
    skinNode,geo,inf,weights=('skinCluster1','pSphere1',[0,1],[t for i in range(382) for t in range(2) ])
    SetWeights = skin.SetWeights(skinNode,geo)
    SetWeights.getWeigths(inf)
    SetWeights.setWeigths(inf,weights)
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
        unWeights = self.fn_skin.getWeights(self.path,self.comp,m_inf)

        doIt = functools.partial(self.fn_skin.setWeights,self.path,self.comp,m_inf,m_weigth)
        undoIt = functools.partial(self.fn_skin.setWeights,self.path,self.comp,m_inf,unWeights)
        return cmcore.addCommand(doIt, undoIt)
    def getWeigths(self,inf):
        m_inf = om.MIntArray(inf)
        return self.fn_skin.getWeights(self.path,self.comp,m_inf)
    def setBlendWeights(self,weigth):
        #执行的权重
        m_weigth = om.MDoubleArray(weigth)
        #撤销的权重
        unWeights = self.fn_skin.getBlendWeights(self.path,self.comp)
        doIt = functools.partial(self.fn_skin.setBlendWeights,self.path,self.comp,m_weigth)
        undoIt = functools.partial(self.fn_skin.setBlendWeights,self.path,self.comp,unWeights)
        return cmcore.addCommand(doIt, undoIt)
    def getBlendWeights(self):
        return self.fn_skin.getBlendWeights(self.path,self.comp)