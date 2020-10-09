#!/usr/bin/python
#-*-coding:gbk -*-
import maya.OpenMaya as om
import pymel.core as pm
import CPMel.outputMaya as outputmaya
class CPGetMeshConnect():
    '''
    用于获得多边形连接信息
    属性
        _is_c_path(是否已经输入路径)
        _vtx_to_e （顶点对应边的字典）
        _e_to_vtx （边对应顶点的字典）
        _vtx_to_vtx （顶点对应顶点的字典）
    方法：
        c_vtx_to_e (self)（创建顶点对应边的字典）
        c_e_to_vtx (self)（创建边对应顶点的字典）
        c_vtx_to_vtx (self)（创建顶点对应顶点的字典）
        get_vtx_to_e_connect (self)（获得顶点对应边的字典）
        get_e_to_vtx_connect (self)（获得边对应顶点的字典）
        get_vtx_to_vtx_connect (self)（获得顶点对应顶点的字典）
        get_vtx_path （self,vtx_id）（获得一个顶点与所有顶点的表面路径距离）#这是个繁重的任务#
    '''
    _is_c_path = False
    _vtx_to_e = False
    _e_to_vtx = False
    _vtx_to_vtx = False

    def __init__(self, obj=False):
        if obj:
            sel = om.MSelectionList()
            sel.add(obj)
            self.path = om.MDagPath()
            sel.getDagPath(0, self.path)
            self._is_c_path = TabError
        else:
            om.MGlobal.displayError('No set mesh name')

    def c_vtx_to_e(self):
        if not self._is_c_path:
            om.MGlobal.displayError('No set mesh name')
            return 0
        it_vtx = om.MItMeshVertex(self.path)
        self._vtx_to_e = dict()
        for i in range(it_vtx.count()):
            int_list = om.MIntArray()
            it_vtx.getConnectedEdges(int_list)
            self._vtx_to_e[i] = int_list
            it_vtx.next()

    def c_e_to_vtx(self):
        if not self._is_c_path:
            om.MGlobal.displayError('No set mesh name')
            return 0
        if not self._vtx_to_e:
            self.c_vtx_to_e()
        self._e_to_vtx = dict()
        for i in self._vtx_to_e:
            for t in self._vtx_to_e[i]:
                if not t in self._e_to_vtx:
                    self._e_to_vtx[t] = list()
                self._e_to_vtx[t].append(i)

    def c_vtx_to_vtx(self):
        if not self._is_c_path:
            om.MGlobal.displayError('No set mesh name')
            return 0
        if not self._e_to_vtx:
            self.c_e_to_vtx()
        self._vtx_to_vtx = \
            {i: list(
                {s for t in self._vtx_to_e[i] for s in self._e_to_vtx[t]} - {i}
            )
                for i in self._vtx_to_e}
        # 原型
        # for i in self._vtx_to_e:
        #     vtx_to_vtx_set = {s for t in self._vtx_to_e[i] for s in self._e_to_vtx[t]}
        #     self._vtx_to_vtx[i] = list(vtx_to_vtx_set - {i})

    def get_vtx_to_e_connect(self):
        if not self._vtx_to_e:
            self.c_vtx_to_e()
        return self._vtx_to_e

    def get_e_to_vtx_connect(self):
        if not self._e_to_vtx:
            self.c_e_to_vtx()
        return self._e_to_vtx

    def get_vtx_to_vtx_connect(self):
        if not self._vtx_to_vtx:
            self.c_vtx_to_vtx()
        return self._vtx_to_vtx

    def get_vtx_path(self, vtx_id):
        if not self._is_c_path:
            om.MGlobal.displayError('No set mesh name')
            return 0
        if not self._vtx_to_vtx:
            self.c_vtx_to_vtx()
        if not vtx_id in self._vtx_to_vtx:
            om.MGlobal.displayError('point ID no in connect lsit')
            return 0
        # 对象路径字典
        vtx_path = dict()
        # 将当前需要操作的点列表设置为输入ID对应的连接列表
        crr_id_list = [vtx_id]
        # 默认将输入点设置为已有的点
        Already_id_list = list()
        # 不使用.操作符来访问效率会有提高
        append = Already_id_list.append
        # 计数
        size = 0
        # 计数上限
        size_len_max = len(self._vtx_to_vtx)
        # 循环只要当前点id列表小于1 或者 计数大于等于计数上限就停止
        while len(crr_id_list) > 0 and size < size_len_max:
            test_id_dict = dict()
            [append(i) for i in crr_id_list]
            for i in crr_id_list:
                test_id_dict[i] = [t for t in self._vtx_to_vtx[i] if not t in Already_id_list]
                vtx_path[i] = size
            crr_id_list = [t for i in test_id_dict for t in test_id_dict[i]]
            size += 1
        return vtx_path
#逆向平滑
def reverseSmoothing(obj_list = None):
    for obj in obj_list if not obj_list is None else pm.selected():
        outputmaya.displayPrint('正在逆向平滑:%s'%obj.nodeName())
        pm.select(obj.vtx[-1])
        pm.mel.ConvertSelectionToEdges()
        pm.mel.SelectEdgeLoopSp()
        pm.mel.polySelectEdgesEveryN('edgeRing',2)
        pm.mel.SelectEdgeLoopSp()
        pm.mel.SelectEdgeLoopSp()
        pm.mel.SelectEdgeLoopSp()
        pm.mel.polySelectEdgesEveryN('edgeRing',2)
        pm.polyDelEdge(cv=True,ch=False)
        outputmaya.displayPrint('逆向平滑 %s 完成'%obj.nodeName())