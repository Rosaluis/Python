#!/usr/bin/python
# -*- coding: cp1250 -*-
'''
Created on 17. 10. 2020
@author: Lojza
'''
from PyQt5.Qt import QLabel, QCheckBox

""" databaze dilu ktere skopiruju z dokumentaci jednotlivych stroju, 
    obsahovat bude:
    jmeno - 2SH1
    popis - ventil k ...
    odkaz - odkaz na onenote stranku, kde k tomu budu treba mit nejake poznamky
    typ stroje na kterem to jde najit - trochu problem, nelze prochazet vsechno
    jestli je to elektricky, hydraulicky, nebo pneumaticky dil
    
    aplikace bude zobrazovat automaticky i z jake je to casti stroje
    aplikace bude moci filtrovat - editace sql dotazu 
    aplikace bude moci exportovat studijni soubor do anki - nice to have, rychlejsi bude export do csv a tam to promazat a 
    naimportovat do anki 
"""
# 1 - Napájecí a řídící systém
# 2 - Zavírací jednotka SE
# 3 -Vstřikovací jednotka EE
# 4 - Pohon šneku
# 5 - Neobsazeno
# 6 -Vytápění vstřikovacího válce
# 250 - QC výhybka
# Příklad:
# Cívka -2Y1 ventilu 2SH1

#!/usr/bin/python
# -*- coding: utf-8 -*-

# import sys


# from PyQt5 import QtGui


# from PyQt5 import QtCore
# from PyQt5.QtWidgets import QApplication, QGridLayout, QDialog,QTabWidget, QComboBox, QCheckBox ,QGroupBox ,QVBoxLayout, QWidget, QLabel, QLineEdit, QDialogButtonBox
# from PyQt5.QtGui import QIcon
# 
# # from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QApplication, QToolBar)
# from PyQt5.QtCore import Qt
# 
# class Example(QWidget):
#     def __init__(self):
#         super().__init__()
# #         self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
# #         self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMinMaxButtonsHint)
#         self.setWindowFlags(Qt.WindowCloseButtonHint)
#         
#         
#         
#         self.initUI()
# 
#     def initUI(self):
# 
#         grid = QGridLayout()
#         self.setLayout(grid)
#         
# #         self.lbCountDown.setFont(QtGui.QFont('Verdana bold', 50))
#         # QtGui.QWidget.__init__(self, parent, QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.WindowMinimizeButtonHint)
#         # self.btGogogo.setStyleSheet(".QPushButton {background-color: yellow; padding: 2px}")
# 
# #         self.leMaxInSpd.setStyleSheet(".QLineEdit {background-color: yellow}")
#         
# 
# #         grid.addWidget(self.lbMaxInSpd,     0, 0, 1, 2)
# #         grid.addWidget(self.leMaxInSpd,     0, 2, 1, 1)
#         
#         
#         
#         self.move(300, 150)
#         self.setWindowTitle('PartView')
#         self.show()
#         self.setPalette(QtGui.QPalette(QtGui.QColor(80, 120, 240)))
#         
#         
#         
#         
# #         self.connect(self.btCalk, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))
# #         self.btPreCalk.clicked[bool].connect(self.calcTeorInjectSpeed)
# #         self.btCalk.clicked[bool].connect(self.calcInjectSpeed)
#         
# #         jak se sakra dela s tabulatorama
# 
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())


from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QRadioButton, QGroupBox, QVBoxLayout,\
    QGridLayout, QLineEdit, QPushButton, QDialogButtonBox
import sys
from PyQt5.QtCore import Qt

class Window(QWidget):
    def __init__(self):
        super().__init__()
#         self.top = 200
#         self.left = 500
#         self.width = 400
#         self.height = 300
        self.setWindowTitle("Parts viewer")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
#         self.setWindowIcon(QtGui.QIcon("icon.png"))
#         self.setGeometry(self.left, self.top, self.width, self.height)
        

#         mainLay = QHBoxLayout() #horizontalni razeni 
        mainLay = QVBoxLayout() #vertikalni razeni 
        grpParams = QGroupBox(" Parametry: ")
        grpHistory = QGroupBox(" Historie hledání: ")
#         grpParams.setFont(QtGui.QFont("Sanserif", 15))
        mainLay.addWidget(grpParams)
        mainLay.addWidget(grpHistory)
        
#         grdLayParams = QVBoxLayout()
        grdLayParams = QGridLayout()
        grdLayHistory = QGridLayout()
        
        
        lbDBConnect = QLabel("DB připojena: ") 
        btDBConnect = QPushButton("OK") 
        btDBConnect.setEnabled(False)
        btDBConnect.setStyleSheet(".QPushButton {background-color: lightgreen}")
        lbPartNumber = QLabel("číslo: ")
        lePartNumber = QLineEdit()
        lbPartName = QLabel("název: ")
        lePartName = QLineEdit()
        lbStroj = QLabel("stroj: ")
        leStroj = QLineEdit()
        cbPartNumber = QCheckBox()
        cbPartName = QCheckBox()
        cbStroj = QCheckBox()
        grdLayParams.addWidget(lbDBConnect,     0, 0, 1, 2)
        grdLayParams.addWidget(btDBConnect,     0, 3, 1, 1)
        grdLayParams.addWidget(lbPartNumber,    1, 1, 1, 1)
        grdLayParams.addWidget(lePartNumber,    1, 2, 1, 2)
        grdLayParams.addWidget(cbPartNumber,    1, 4, 1, 1)
        grdLayParams.addWidget(lbPartName,      2, 1, 1, 1)
        grdLayParams.addWidget(lePartName,      2, 2, 1, 2)
        grdLayParams.addWidget(cbPartName,      2, 4, 1, 1)
        grdLayParams.addWidget(lbStroj,         3, 1, 1, 1)
        grdLayParams.addWidget(leStroj,         3, 2, 1, 2)
        grdLayParams.addWidget(cbStroj,         3, 4, 1, 1)
        
        
        btHistoryPast = QPushButton(" <- ")
        btHistoryNext = QPushButton(" -> ")
        btHistoryPast.setEnabled(False)
        btHistoryNext.setEnabled(False)
        grdLayHistory.addWidget(btHistoryPast,  0, 0, 1, 1)
        grdLayHistory.addWidget(btHistoryNext,  0, 1, 1, 1)
        grpParams.setLayout(grdLayParams)
        grpHistory.setLayout(grdLayHistory)
        grpHistory.setVisible(False)
        
        
        self.setLayout(mainLay)
        self.show()



if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
    