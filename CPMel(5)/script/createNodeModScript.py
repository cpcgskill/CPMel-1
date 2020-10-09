#!/usr/bin/python
#-*-coding:gbk -*-
'''
这个模块中提供了createNodeMod模块的静态创建的自动代码生成
环境:maya2018及maya2018标准python
'''
import pymel.core as pm
node_list_str = 'except:\n'
for i in pm.allNodeTypes(ia = False):
    node_list_str+='    def %s(*args,**kwargs):\n        return createNode(\'%s\',*args,**kwargs)\n'%(i,i)
print node_list_str