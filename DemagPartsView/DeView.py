#!/usr/bin/python
# -*- coding: cp1250 -*-
'''
Created on 18. 10. 2020
@author: Lojza
'''

import sys
import sqlite3
from sqlite3 import Error
from string import Template
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QApplication, QTextEdit)
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class Example(QWidget):
    def __init__(self):
        super().__init__()
#         self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
#         self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMinMaxButtonsHint)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        
        self.lbFind = QLabel("name: ")
        self.lePart = QLineEdit()
        self.txOut = QTextEdit()
        self.lbParts = QLabel("parts: ")
        self.btFind = QPushButton("find")
        
        grid = QGridLayout()
        self.setLayout(grid)
        
        grid.addWidget(self.lbFind,     0, 0, 1, 1)
        grid.addWidget(self.lePart,     0, 1, 1, 1)
        grid.addWidget(self.btFind,     0, 9 ,1, 1)
        grid.addWidget(self.lbParts,    1, 0, 1, 1)
        grid.addWidget(self.txOut,      1, 1, 9, 9)
        
        
        
        self.move(300, 150)
        self.setWindowTitle('DeView')
        self.show()
        self.setPalette(QtGui.QPalette(QtGui.QColor(200, 180, 180)))
        
        self.btFind.clicked[bool].connect(self.insertDataIntoDB)
        
#         self.insertDataIntoDB("1D")
        
    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        return conn
    
    
#     def insertDataIntoDB(self, data):
    def insertDataIntoDB(self):
        database = r"Parts.sqlite3"
        # create a database connection
        conn = self.create_connection(database)
        cur = conn.cursor()
    
        data = self.lePart.text()
    
        sql = Template('''
            SELECT parts.partName, parts.partDescription, kinds.kindName, machines.machineName, parts.partLink
            FROM parts
            INNER JOIN kinds ON parts.partKind = kinds.kindID
            INNER JOIN machines ON parts.partMachine = machines.machineId
            WHERE parts.partName LIKE \"%$what%\" ''')
            

        print(sql)
        cur = conn.cursor()
        cur.execute(sql.substitute(what = data)) #https://docs.python.org/2/library/string.html#template-strings
            
        rows = cur.fetchall()
        for row in rows:
            print(row)
            self.txOut.append(str(row))

        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())        