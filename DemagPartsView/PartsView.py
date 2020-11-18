#!/usr/bin/python
# -*- coding: cp1250 -*-
'''
Created on 17. 10. 2020
@author: Lojza
'''
"""
todo:
check boxy pro doplneni zadani o symbol procenta
poznamka s proconty pro vyhledavani
dodelat logiku
dodelat pouziti vlastniho commandu
upravit sirku zadavacich okenek
"""



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

import sqlite3
from sqlite3 import Error
from string import Template
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QRadioButton, QGroupBox, QVBoxLayout,\
    QGridLayout, QLineEdit, QPushButton, QTabWidget, QLabel, QCheckBox, QTextEdit
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
        
        self.database = r"Parts.sqlite3"
#         mainLay = QHBoxLayout() #horizontalni razeni 
        self.mainLay = QVBoxLayout() #vertikalni razeni 
        self.grpParams = QGroupBox(" Filter: ")
        self.grpOutput = QGroupBox(" Output: ")
        self.grpFoot = QGroupBox()
        
        self.grdLayParams = QGridLayout()
        self.grdLayOutput = QGridLayout()
        self.grdLayTabOutData = QGridLayout()
        self.grdLayTabOutCmd = QGridLayout()
        self.horLayFoot = QHBoxLayout()
        self.horLayFoot.addStretch(1)

        self.grpOutput.setLayout(self.grdLayOutput)
        self.grpParams.setLayout(self.grdLayParams)
        self.grpFoot.setLayout(self.horLayFoot)
        
        self.mainLay.addWidget(self.grpParams)
#         self.mainLay.addWidget(tabForm)
        self.mainLay.addWidget(self.grpOutput)
        self.mainLay.addWidget(self.grpFoot)
        
        self.lbComplete = QLabel("%")
        self.lbComplete.setStyleSheet(".QLabel{margin-left:50%; margin-right:50%}")
        self.lbAdd = QLabel("+")
        self.lbAdd.setStyleSheet(".QLabel{margin-left:50%; margin-right:50%}")
        self.lbPartName = QLabel("name: ")
        self.lePartName = QLineEdit()
        self.lePartName.setText("1B6")
        self.lbPartDescription = QLabel("description: ")
        self.lePartDescription = QLineEdit()
        self.cbPartName = QCheckBox()
        self.cbPartName.setStyleSheet(".QCheckBox{margin-left:50%; margin-right:50%}")
        self.cbPartDescription = QCheckBox()
        self.cbPartDescription.setStyleSheet(".QCheckBox{margin-left:50%; margin-right:50%}")
        self.cbCompleteName = QCheckBox()
        self.cbCompleteName.setStyleSheet(".QCheckBox{margin-left:50%; margin-right:50%}")
        self.cbCompleteDesc = QCheckBox()
        self.cbCompleteDesc.setStyleSheet(".QCheckBox{margin-left:50%; margin-right:50%}")
        self.cbCompleteDesc.setChecked(True)
        self.chClearOutput = QCheckBox("clearing")
        self.chClearOutput.setChecked(True)
        self.btClearOutput = QPushButton("clear")
        self.btCommit = QPushButton("commit")
        
        self.grdLayParams.addWidget(self.lbComplete,            0, 4, 1, 1)
        self.grdLayParams.addWidget(self.lbAdd,              0, 5, 1, 1)
        self.grdLayParams.addWidget(self.lbPartName,            1, 1, 1, 1)
        self.grdLayParams.addWidget(self.lePartName,            1, 2, 1, 2)
        self.grdLayParams.addWidget(self.cbCompleteName,        1, 4, 1, 1)
        self.grdLayParams.addWidget(self.cbPartName,            1, 5, 1, 1)
        self.grdLayParams.addWidget(self.lbPartDescription,     2, 1, 1, 1)
        self.grdLayParams.addWidget(self.lePartDescription,     2, 2, 1, 2)
        self.grdLayParams.addWidget(self.cbCompleteDesc,        2, 4, 1, 1)
        self.grdLayParams.addWidget(self.cbPartDescription,     2, 5, 1, 1)
        self.grdLayParams.addWidget(QLabel(""),                 4, 1, 1, 1)
        self.grdLayParams.addWidget(self.btCommit,              5, 5, 1, 1)
        
        self.tabsOutput = QTabWidget()
        self.tabOutputData = QWidget()
        self.teOutputData = QTextEdit()
        self.teOutputData.setMinimumWidth(600)
        self.tabOutputData.setLayout(self.grdLayTabOutData)
        self.grdLayTabOutData.addWidget(self.teOutputData,      0, 0, 10, 10)
        self.grdLayTabOutData.addWidget(self.chClearOutput,     11,8, 1,  1)
        self.grdLayTabOutData.addWidget(self.btClearOutput,     11,9 ,1,  1)
        
        self.tabOutputCmd = QWidget()
        self.teOutputCmd = QTextEdit()
        self.teOutputCmd.append("SELECT * FROM parts")
        self.btOutputCmdSend = QPushButton("send")
        self.tabOutputCmd.setLayout(self.grdLayTabOutCmd)
        self.grdLayTabOutCmd.addWidget(self.teOutputCmd,          0, 0,10,10)
        self.grdLayTabOutCmd.addWidget(self.btOutputCmdSend,      10,9, 1, 1)
        
        self.tabsOutput.addTab(self.tabOutputData, "output data")
        self.tabsOutput.addTab(self.tabOutputCmd, "DB command edit")
        self.grdLayOutput.addWidget(self.tabsOutput,              0, 0, 1, 1)
        
        self.lbDBConnect = QLabel("DB connected: ") 
        self.lbDBName = QLabel("...") 
        self.lbDBName.setStyleSheet(".QLabel{background-color: yellow}")
        self.horLayFoot.addWidget(self.lbDBConnect)
        self.horLayFoot.addWidget(self.lbDBName)
        
        self.setLayout(self.mainLay)
        self.show()
        
        self.btCommit.clicked[bool].connect(self.commitDBCommand)
        self.btClearOutput.clicked[bool].connect(self.clearOutput)
        
    def clearOutput(self):
        self.teOutputData.clear()
        
    def commitDBCommand(self):
        database = r"Parts.sqlite3"
        # create a database connection
        conn = self.create_connection(database)
        dataName = self.lePartName.text()
        dataDesc = self.lePartDescription.text()
        
        if self.chClearOutput.isChecked() == True:
            self.teOutputData.clear()
    
        sql = Template('''
            SELECT parts.partName, parts.partDescription, kinds.kindName, machines.machineName, parts.partLink
            FROM parts
            INNER JOIN kinds ON parts.partKind = kinds.kindID
            INNER JOIN machines ON parts.partMachine = machines.machineId
            WHERE parts.partName LIKE \"$pName\" and
            parts.partDescription LIKE \"$pDesc\"
            ''')
        
        cur = conn.cursor()
        #https://docs.python.org/2/library/string.html#template-strings
        if self.cbPartName.isChecked() == True and self.cbPartDescription.isChecked() == False:
            if self.cbCompleteName.isChecked() == True:
                cur.execute(sql.substitute(     pName = "%" + dataName + "%",        pDesc = "%")) 
            else:
                cur.execute(sql.substitute(     pName = dataName,                    pDesc = "%"))  
                  
        elif self.cbPartName.isChecked() == False and self.cbPartDescription.isChecked() == True:
            if self.cbCompleteDesc.isChecked() == True:
                cur.execute(sql.substitute(     pName = "%",                         pDesc = "%"+ dataDesc + "%"))
            else:
                cur.execute(sql.substitute(     pName = "%",                         pDesc = dataDesc))
                
        elif self.cbPartName.isChecked() == True and self.cbPartDescription.isChecked() == True and len(self.lePartDescription.text()) > 0:
            cur.execute(sql.substitute(         pName = "%" + dataName + "%",        pDesc = "%"+ dataDesc + "%"))
        
        
        
#         print(cur)
        
        rows = cur.fetchall()
        for row in rows:
#             print(row)
            self.teOutputData.append(str(row))
            
            
    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            self.lbDBName.setText("OK")
            self.lbDBName.setStyleSheet(".QLabel{background-color: lightgreen}")
        except Error as e:
            self.lbDBName.setText("NOK")
            self.lbDBName.setStyleSheet(".QLabel{background-color: red}")
            print(e)
        return conn
    
if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
    
    
# SELECT parts.partName, parts.partDescription, kinds.kindName, machines.machineName, parts.partLink
# FROM parts
# INNER JOIN kinds ON parts.partKind = kinds.kindID
# INNER JOIN machines ON parts.partMachine = machines.machineId
# /*WHERE parts.partDescription LIKE "%etenice%" */
# WHERE parts.partName LIKE "2SV21"