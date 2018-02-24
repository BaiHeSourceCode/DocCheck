#!/usr/bin/env python
# coding=utf-8
__author__ = 'Baihe'
__date__ = 2018 / 2 / 11
import db_reader


class JSD_FILEMAIN():
    def __init__(self, file_id, reader):
        self.FileID = file_id
        file = reader.ExecQuery(
            "SELECT * FROM [CenterDB].[dbo].[JSD_FileMain] where [FileID]='" + self.FileID + "' AND IsDel=0")[0]
        self.JSDID = file[1]
        self.FileCodeType = file[2]
        self.FileCodeType = file[2]
        self.FileCode = file[3]
        self.FileLanguage = file[4]
        self.FileVolum = file[5]
        self.FileState = file[6]
        self.FileVersion = file[7]
        self.FileType = file[8]
        self.FileLevel = file[9]
        self.InternalCode = file[10]
        self.InternalVar = file[11]
        self.InternalMode = file[12]
        self.Secret = file[13]
        self.SecretExpireDate = str(file[14]).split(' ')[0] # 获得yyyy-mm-dd
        self.SecretDes = file[15]
        self.VolumNum = file[16]
        self.TomeNum = file[17]
        self.MachineGroup = file[18]
        self.FileChTitle = file[19]
        self.FileEnTitle = file[20]
        self.FileDesignStep = file[21]
        self.FileCategory = file[22]
        self.RefFileCode = file[23]
        self.RefFileVersion = file[24]
        self.FileWorkshop = file[25]
        self.FileSubNum = file[26]
        self.EqFunCode = file[27]
        self.WPCCode = file[28]
        self.ECSCode = file[29]
        self.StockNum = file[30]
        self.ModifyReMark = file[31]
        self.A0 = int(file[32])
        self.A018 = int(file[33])
        self.A014 = int(file[34])
        self.A1 = int(file[35])
        self.A114 = int(file[36])
        self.A124 = int(file[37])
        self.A134 = int(file[38])
        self.A2 = int(file[39])
        self.A3 = int(file[40])
        self.A4 = int(file[41])
        self.SMandQY = int(file[42])
        self.JSBook = int(file[43])
        self.TGGBook = int(file[44])
        self.FileSource = file[45]
        self.FileDesignUId = file[46]
        self.FileDesignUName = file[47]
        self.FileDesignCreateDate = file[48]
        self.LastModifyDate = str(file[49]).split(' ')[0] # 获得yyyy-mm-dd
        self.IsDel = file[50]
        self.FileSize = file[51]
        self.cundanghao = file[52]
        self.cdhPath = file[53]
        self.PDFPageCount = int(file[54])
        self.PDFPageSize = file[55]
        self.GDDate = file[56]
        self.PDFTrans = file[57]
        self.InputOrjCode = file[58]
        self.InputAlterVersion = file[59]
        self.FileListName = file[60]
        self.esign = file[61]
        self.WBSCode = file[62]
        self.KZWBSCode = file[63]
        # 获取标题
        if self.FileLanguage == '中文':
            self.title = self.FileChTitle
        elif self.FileLanguage == '英语':
            self.title = self.FileEnTitle
        else:
            self.title = ''

if __name__ == "__main__":
    dbreader = db_reader.DB_Reader(host="d-s48.cnpdc.com", user="p108034", pwd="123qweASD", db="CenterDB")
    test = JSD_FILEMAIN('0000D3F8-E55D-4016-8B27-D0BF6CE7596B', dbreader)
    print(test.JSDID)
