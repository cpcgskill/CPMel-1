#!/usr/bin/python
#-*-coding:utf-8 -*-
import sys
try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
except ImportError:
    try:
        from PySide2.QtGui import *
        from PySide2.QtCore import *
        from PySide2.QtWidgets import *
    except ImportError :
        try:
            from PySide.QtGui import *
            from PySide.QtCore import *
            from PySide.QtWidgets import *
        except:
            print('ImportError')
class ProgressBar ( QWidget ) :
    def __init__ ( self, size = QSize(500,500)) :
        super (ProgressBar, self).__init__ ()
        self.resize (size)
        self.setWindowFlags ( Qt.FramelessWindowHint )
        self.setAttribute ( Qt.WA_TranslucentBackground )  # 设置窗口背景透明

        self._alen = 0.7
        self._is_left_button = False
        self._s_pos = QPoint(0,0)
        self._e_pos = QPoint(0,0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint ( QPainter.Antialiasing , True )

        painter.setPen (Qt.NoPen)
        painter.setBrush(QBrush(QColor(0,0,0,1)))
        painter.drawRect(self.rect())

        painter.setPen(QPen(QColor(70, 147, 236),5))
        painter.setBrush(QBrush(QColor(218, 167, 72)))
        painter.drawPie( self.rect().adjusted(10,10,-10,-10) , 0 , self._alen * 360 * 16 )
    def mousePressEvent(self, event):
        if event.buttons ( ) == Qt.LeftButton :
            self._s_pos = QCursor.pos ( )
            self._is_left_button = True
            self.update()
    def mouseMoveEvent(self, event):
        if self._is_left_button:
            self._e_pos = QCursor.pos ( )
            self.move(self.pos()+self._e_pos-self._s_pos)
            self._s_pos = self._e_pos
            self.update ( )
    def mouseReleaseEvent(self, QMouseEvent):
        self._is_left_button = False
if __name__ == '__main__' :
    app = QApplication ( sys.argv )
    win = ProgressBar ( )
    win.show ( )
    sys.exit ( app.exec_ ( ) )