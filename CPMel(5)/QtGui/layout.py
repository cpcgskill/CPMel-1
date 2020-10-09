#!/usr/bin/python
# -*-coding:utf-8 -*-
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
class ListItem(QListWidget):
    def __init__(self,parent = None , Flow = QListWidget.LeftToRight):
        super(ListItem,self).__init__(parent)
        self.item_szie = QSize(100,100)

        self.setFlow(Flow)
        self.setWrapping(True)
        self.setResizeMode(QListWidget.Adjust)
    def addItem(self,weidgrt):
        item = QListWidgetItem()
        item.setSizeHint(self.item_szie)
        super(ListItem,self).addItem(item)
        super(ListItem,self).setItemWidget(item,weidgrt)
class MainWindow ( QWidget ) :
    def __init__ ( self ) :
        super (MainWindow,self ).__init__ ( )
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.setWindowTitle ( '我的第一个PyQt窗口' )
        self.resize ( 800 , 600 )
        list_item = ListItem(self)
        layout.addWidget(list_item)
        for i in range(1000 ):
            list_item.addItem (QPushButton() )




if __name__ == '__main__' :
    app = QApplication ( sys.argv )
    win = MainWindow ( )
    win.show ( )
    sys.exit ( app.exec_ ( ) )
