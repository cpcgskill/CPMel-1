#!/usr/bin/python
#-*-coding:gbk -*-
try:
    import mesh
except ImportError:
    print 'ImportError:mesh'
try:
    import skin
except ImportError:
    print 'ImportError:skin'
try:
    import soft
except ImportError:
    print 'ImportError:soft'
try:
    import deformer
except ImportError:
    print 'ImportError:deformer'