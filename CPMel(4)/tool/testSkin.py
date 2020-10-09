import maya.OpenMaya as om
import maya.cmds as mc

geo = 'pSphere1'
#检查对象的类型
def conversionComponent(geo):
	if not mc.objExists(geo):
		raise EOFError('%s 对象不存在'%geo)
	#检查geo是否不是组件
	if not geo in '.':
		#检查是否有形态节点
		if mc.objectType(geo) == 'transform':
			geo_shape = mc.listRelatives(geo,s=1)
			if len(geo_shape)>0:
				geo = geo_shape[0]
			else:
				raise EOFError('%s 对象没有形态节点'%geo)
		#如果有形态节点就将geo转化成组件
		if mc.objectType(geo) == 'mesh':
			geo = '%s.vtx[*]'%geo
		elif mc.objectType(geo) == 'nurbsCurve':
			geo = '%s.cv[*]'%geo
		elif mc.objectType(geo) == 'nurbsSurface':
			geo = '%s.cv[*]'%geo
		elif mc.objectType(geo) == 'lattice':
			geo = '%s.pt[*]'%geo
		else:
			raise EOFError('%s 对象无法转化成已知组件类型'%geo)
	return geo