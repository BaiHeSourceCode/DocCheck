#!/usr/bin/env python
# coding=utf-8
__author__ = 'Baihe'
__date__ = 2018 / 2 / 27

import db_reader


class JSD_Reader():
    def __init__(self):
        self.dbr = db_reader.DB_Reader(host="d-s48.cnpdc.com", user="p108034", pwd="123qweASD", db="CenterDB")

    def get_files(self, jsd_id):
        files = self.dbr.ExecQuery(
            "SELECT * FROM [CenterDB].[dbo].[JSD_FileMain] WHERE [JSDID]='" + jsd_id + "' AND IsDel=0")
        return files