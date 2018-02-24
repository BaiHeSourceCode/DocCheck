#!/usr/bin/env python
# coding=utf-8
__author__ = 'Baihe'
__date__ = 2018 / 2 / 8

import db_reader
ms = db_reader.DB_Reader(host="d-s48.cnpdc.com", user="p108034", pwd="123qweASD", db="CenterDB")
resList = ms.ExecQuery("SELECT  DISTINCT FileChTitle FROM [CenterDB].[dbo].[JSD_FileMain] where FileChTitle!=''")
dictionary = set(' ')
for title in resList:
    # chars = list(title)
    for i in range(len(title[0]), 0, -1):
        # if title[0][i-1] >= u'\u4e00' and title[0][i-1] <= u'\u9fa5':
        dictionary.add(title[0][i-1])
print(dictionary)

