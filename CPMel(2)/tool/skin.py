#!/usr/bin/python
#-*-coding:gbk -*-
import pymel.core as pm
import functools
import pymel.core as pm
import CPMel.core as cmcore
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
        setWeigths(skinNode, i, weigth, inf)
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
def setWeigths(skinNode, geo, weigth, inf = None): 
    if inf is None:
        unWeights = [t for i in skinNode.getWeights(geo) for t in i]
        inf = range(len(skinNode.getInfluence()))
    else:
        unWeights = [
            t for i in
            zip(*[
                [
                    t for t in skinNode.getWeights(geo, i)
                ] for i in inf
            ])
            for t in i
        ]
    doIt = functools.partial(skinNode.setWeights, geo, inf, weigth)
    undoIt = functools.partial(skinNode.setWeights, geo, inf, unWeights)
    return cmcore.addCommand(doIt, undoIt)
