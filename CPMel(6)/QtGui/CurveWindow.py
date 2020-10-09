#!/usr/bin/python
# -*-coding:utf-8 -*-
import sys

try :
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
except ImportError :
    try :
        from PySide2.QtGui import *
        from PySide2.QtCore import *
        from PySide2.QtWidgets import *
    except ImportError :
        try :
            from PySide.QtGui import *
            from PySide.QtCore import *
            from PySide.QtWidgets import *
        except :
            print ( 'ImportError' )


class CurveExpWindow ( QWidget ) :
    '''
    曲线表达式控件
    __init__( self , parent=None , rect_color = QColor(...) , exp_color=QColor(...) )#(父对象,背景颜色,表达式区域颜色,笔颜色)

    setExp(self,exp)#设置表达式
    setPenColor(self,color)#设置笔颜色
    setPen(self,pen)#设置笔
    upPoly(self)#更新视图多边形
    '''

    def __init__ ( self , parent = None , rect_color = QColor ( *(120 ,) * 3 ) , exp_color = QColor ( *(50 ,) * 3 ) ,
                   pen_color = QColor ( *(0 ,) * 3 ) ) :
        super ( CurveExpWindow , self ).__init__ ( parent )
        # 背景颜色
        self.rect_color = rect_color
        # 表达式区域颜色
        self.exp_color = exp_color
        # 曲线表达式
        self._exp = lambda i : i
        # 多边形
        self._poly = None
        # 笔颜色
        self._pen = QPen ( pen_color )
        #
        self.w = self.width ( )
        self.h = self.height ( )
        # 更新多边形
        self.upPoly ( )

    def setExp ( self , exp ) :
        self._exp = exp
        self.update ( )

    def setPenColor ( self , color ) :
        self._pen = QPen ( color )
        self.update ( )

    def setPen ( self , pen ) :
        self._pen = pen
        self.update ( )

    def upPoly ( self ) :
        poly = QPolygonF ( )
        self.w = self.width ( )
        self.h = self.height ( )
        for i in range ( self.w ) :
            # poly << QPointF ( i , self.h - self._exp ( 1 - float ( i ) / (self.w - 1) ) * self.h )
            # 兼容PySide2
            poly.append ( QPointF ( i , self.h - self._exp ( 1 - float ( i ) / self.w ) * self.h ) )
        poly.append ( QPointF ( self.w , self.h ) )
        poly.append ( QPointF ( 0 , self.h ) )
        self._poly = poly

    def paintEvent ( self , event ) :
        painter = QPainter ( )
        painter.begin ( self )

        painter.setRenderHint ( QPainter.Antialiasing , True )

        painter.setPen ( self._pen )
        painter.setBrush ( QBrush ( self.rect_color ) )
        painter.drawRect ( self.rect ( ) )

        painter.setBrush ( QBrush ( self.exp_color ) )
        # 在宽度和高度修改时更新多边形
        if self.w != self.width ( ) or self.h != self.height ( ) :
            self.upPoly ( )
        painter.drawPolygon ( self._poly )


class BezierCurveWindow ( QWidget ) :
    '''
    Bezier曲线窗口
    __init__(self,parent=None)
    setlinePen ( self , pen )# 设置线笔
    setGridPen ( self , pen )# 设置网格笔
    setRectBeush ( self , brush ) # 设置背景brush
    setStartDirection ( self , direction ) # 设置开始方向（start , end）
    setGridLineSize ( self , size )#设置网格线数量
    upStartEndCv ( self ) #更新开始结束点
    initMidPoint ( self ) #初始化中间点
    upStretchingMidPoint ( self )#更新中间点的拉伸空间
    upMidPoint ( self ) #根据中间拉伸空间点更新中间点
    pointToStretchingSpace ( self , pointf ) #将一个当前控件空间点转化到拉伸空间点
    stretchingSpaceToPoint ( self , pointf ) #将一个拉伸空间点转化到当前控件空间点
    '''
    start , end = range ( 2 )

    def __init__ ( self , parent = None ) :
        super ( BezierCurveWindow , self ).__init__ ( parent )

        #线笔
        self._line_pen = QPen ( QColor ( *(0 ,) * 3 ) , 3 )
        #网格笔
        self._grid_pen = QPen ( QColor ( *(52 ,) * 3 ) , 2 )
        #背景brush
        self._rect_brush = QBrush ( QColor ( *(125 ,) * 3 ) )
        #开始方向（start , end）
        self._start_direction = self.start
        #网格线数量
        self._grid_line_size = 10
        #开始、中间A、中间B、结束点
        self._start_point = None
        self._mid_point_A = None
        self._mid_point_B = None
        self._end_point = None
        #中间俩个的在拉伸空间内的点想x、y皆为0~1
        self._stretching_mid_point_A = None
        self._stretching_mid_point_B = None
        #目前w、h
        self._w = None
        self._h = None
        #更新开始结束点
        self.upStartEndCv ( )
        #初始化中间点
        self.initMidPoint ( )
        # 更新中间点的拉伸空间
        self.upStretchingMidPoint ( )
    # 设置线笔
    def setlinePen ( self , pen ) :
        self._line_pen = pen
        self.update ( )
    # 设置网格笔
    def setGridPen ( self , pen ) :
        self._grid_pen = pen
    # 设置背景brush
    def setRectBeush ( self , brush ) :
        self._rect_brush = brush
    # 设置开始方向（start , end）
    def setStartDirection ( self , direction ) :
        self._start_direction = direction
        self.update ( )
    #设置网格线数量
    def setGridLineSize ( self , size ) :
        self._grid_line_size = size
    #更新开始结束点
    def upStartEndCv ( self ) :
        self._w = self.width ( )
        self._h = self.height ( )
        if self._start_direction == self.start :
            self._start_point = QPointF ( 0 , self._h )
            self._end_point = QPointF ( self._w , 0 )
        else :
            self._start_point = QPointF ( 0 , 0 )
            self._end_point = QPointF ( self._w , self._h )
    #初始化中间点
    def initMidPoint ( self ) :
        self._mid_point_A = (self._start_point * 2 + self._end_point) / 3
        self._mid_point_B = (self._start_point + self._end_point * 2) / 3
    #更新中间点的拉伸空间
    def upStretchingMidPoint ( self ) :
        self._stretching_mid_point_A = self.pointToStretchingSpace ( self._mid_point_A )
        self._stretching_mid_point_B = self.pointToStretchingSpace ( self._mid_point_B )
    #根据中间拉伸空间点更新中间点
    def upMidPoint ( self ) :
        self._mid_point_A = self.stretchingSpaceToPoint ( self._stretching_mid_point_A )
        self._mid_point_B = self.stretchingSpaceToPoint ( self._stretching_mid_point_B )
    #将一个当前控件空间点转化到拉伸空间点
    def pointToStretchingSpace ( self , pointf ) :
        return QPointF ( pointf.x ( ) / self.width ( ) , pointf.y ( ) / self.height ( ) )
    #将一个拉伸空间点转化到当前控件空间点
    def stretchingSpaceToPoint ( self , pointf ) :
        return QPointF ( pointf.x ( ) * self.width ( ) , pointf.y ( ) * self.height ( ) )

    def paintEvent ( self , event ) :
        #更新中间点
        self.upMidPoint ( )

        painter = QPainter ( )
        painter.begin ( self )
        painter.setRenderHint ( QPainter.Antialiasing , True )

        #绘制背景
        painter.setPen ( Qt.NoPen )
        painter.setBrush ( self._rect_brush )
        painter.drawRect ( self.rect ( ) )

        #绘制网格
        painter.setPen ( self._grid_pen )
        painter.setBrush ( Qt.NoBrush )
        for i in range ( 1 , self._grid_line_size + 1 ) :
            val = i / (self._grid_line_size + 1)
            painter.drawLine ( QPointF ( 0 , val * self.height ( ) ) ,
                               QPointF ( self.width ( ) , val * self.height ( ) ) )
            painter.drawLine ( QPointF ( val * self.width ( ) , 0 ) ,
                               QPointF ( val * self.width ( ) , self.height ( ) ) )

        #如果大小变化就更新开始结束点
        if self._w != self.width ( ) or self._h != self.height ( ) :
            self.upStartEndCv ( )
        #绘制线
        path = QPainterPath ( self._start_point )
        path.cubicTo ( self._mid_point_A , self._mid_point_B , self._end_point )
        painter.setPen ( self._line_pen )
        painter.setBrush ( Qt.NoBrush )
        painter.drawPath ( path )


if __name__ == '__main__' :
    app = QApplication ( sys.argv )
    win = BezierCurveWindow ( )
    win.resize ( 800 , 800 )
    # win.setStartDirection ( win.end )
    win.initMidPoint()
    win.show ( )
    sys.exit ( app.exec_ ( ) )
