import maya.cmds as mc
import maya.api.OpenMaya as om
import collections 
class node:
    def __init__(self,node_name):
        self.__dict__['__UUID'] = mc.ls(node_name,uid = True)
    def __setattr__(self,name,val):
        if isinstance(val,collections.Iterable) and type(val) != str:
            mc.setAttr('%s.%s'%(mc.ls(self.__dict__['__UUID'])[0],name),*val)
        else:
            mc.setAttr('%s.%s'%(mc.ls(self.__dict__['__UUID'])[0],name),val)
    def __getattr__(self,name):
        return mc.getAttr('%s.%s'%(mc.ls(self.__dict__['__UUID'])[0],name))
a = node('pSphere1')