#!/usr/bin/python
# -*- coding: cp1250 -*-
'''
Created on 17. 10. 2020
@author: Lojza
'''


""" aplikace pro plneni databaze s dilama z textaku, ktery bude obsahovat nakopirovana data z pdf navodu """

import sqlite3
import sys
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def insertDataIntoDB(data):
    database = r"Parts.sqlite3"
    # create a database connection
    conn = create_connection(database)
    cur = conn.cursor()

#     sql = ''' INSERT INTO part(partId,partKind,partName,partDescription,partLink) VALUES(?,?,?,?,?) '''
    sql = ''' INSERT INTO parts(partKind,partName,partDescription,partMachine,partLink) VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, data)
        conn.commit()

        return cur.lastrowid
    except:
        pass

sourceFileName = "hydraulika.txt"
# sourceFileName = "elektrika.txt"
# sourceFileName = "pneumatika.txt"



sourceFile = open(sourceFileName, "r")

for line in sourceFile:
    li = line.strip().split(" ")
    name = li[0]
    desc = li[1:]

    expName = name.replace("-", "")
    expDesc = line.replace(name, "").strip()
#     print(expName)
#     print(expDesc)
#     expData = (1, expName, expDesc, "") #hydraulika
#     expData = (2, expName, expDesc, "") #elektrika

    typ = 0
    if str.find(sourceFileName, "hydraulika.txt") == 0:
        typ = 1
    elif str.find(sourceFileName, "elektrika.txt") == 0:
        typ = 2
    elif str.find(sourceFileName, "pneumatika.txt") == 0:
        typ = 3

#     expData = (typ, expName, expDesc, 1, "")     #intElect2 180
#     expData = (typ, expName, expDesc, 2, "")     #Concept 80
#     expData = (typ, expName, expDesc, 3, "")     #Systec 50
#     expData = (typ, expName, expDesc, 4, "")     #Systec multi 160
#     expData = (typ, expName, expDesc, 5, "")     #El-Exis SP 300
#     expData = (typ, expName, expDesc, 6, "")     #IntElect 220
#     expData = (typ, expName, expDesc, 7, "")     #Systec 1500
    expData = (typ, expName, expDesc, 8, "")       #IntElect 160 smart
    
    insertDataIntoDB(expData)   
    
