#!/usr/bin/env python
# coding=utf-8
import rule_reader

__author__ = 'Baihe'
__date__ = 2018 / 2 / 11
import re


class Document():
    def __init__(self, jsd_file):
        self.config = rule_reader.RuleReader('path').config
        # 文件路径
        self.url = self.get_url(jsd_file.FileListName)
        self.pdf_file = self.config['pdf']['path'] + jsd_file.FileID + '.pdf'
        # 文件是cad还是word转的pdf, 0是cad，1是word
        if jsd_file.SMandQY + jsd_file.JSBook + jsd_file.TGGBook == 0:
            self.pdf_type = 0
            self.chart_path = self.config['chart']['path'] + jsd_file.FileID + '/'
            self.labels_path = self.config['labels']['path'] + jsd_file.FileID + '/'
            self.chart_size = ''
        else:
            self.pdf_type = 1
            self.chart_path = ''
            self.labels_img = ''
        # 文件id信息
        self.FileID = jsd_file.FileID
        self.JSDID = jsd_file.JSDID
        # 获取语种
        self.FileLanguage = ''  # jsd_file.FileLanguage
        self.title = ''

        # 获取文件编码
        self.FileCode = ''  # jsd_file.FileCode
        # 获取内部编码
        self.InternalCode = ''  # jsd_file.InternalCode
        # 获取版本信息
        self.FileVersion = ''  # jsd_file.FileVersion
        # 获取文件类型
        self.FileType = ''  # jsd_file.FileType
        # 获取密级信息
        self.Secret = 'F'  # jsd_file.Secret
        self.SecretExpireDate = '1900-01-01'  # jsd_file.SecretExpireDate
        # 获取参考文件
        # TODO word参考文件待定
        self.RefFileCode = ''  # jsd_file.RefFileCode
        self.RefFileVersion = ''  # jsd_file.RefFileVersion
        # 获取文件类别 C-new;B-modify;A-identical
        self.FileCategory = ''  # jsd_file.FileCategory
        # 图纸尺寸
        self.PDFPageSize = ''  # jsd_file.PDFPageSize
        # 文件页数
        # TODO 获取页数
        self.PDFPageCount = jsd_file.PDFPageCount
        # 子项
        self.FileSubNum = ''  # jsd_file.FileSubNum
        # 卷标
        self.FileVolum = ''  # jsd_file.FileVolum
        # 状态
        self.FileState = ''  # jsd_file.FileState
        # 设计阶段
        self.FileDesignStep = ''
        # 归档日期
        self.LastModifyDate = ''
        self.SignDate = '1900-01-01'
        self.dpi = 300
        # 记录解析的元数据信息
        self.info = []
        self.records = []
        self.record_count = self.get_record_count(str(jsd_file.FileVersion))
        # 记录比对元数据结果
        self.result = []  # self.FileDesignStep = jsd_file.FileDesignStep  # self.VolumNum = jsd_file.VolumNum  # self.TomeNum = jsd_file.TomeNum  # self.MachineGroup = jsd_file.MachineGroup  # self.FileWorkshop = jsd_file.FileWorkshop  # self.EqFunCode = jsd_file.EqFunCode  # self.WPCCode = jsd_file.WPCCode  # self.ECSCode = jsd_file.ECSCode  # self.StockNum = jsd_file.StockNum  # self.ModifyReMark = jsd_file.ModifyReMark  # self.A0 = jsd_file.A0  # self.A018 = jsd_file.A018  # self.A014 = jsd_file.A014  # self.A1 = jsd_file.A1  # self.A114 = jsd_file.A114  # self.A124 = jsd_file.A124  # self.A134 = jsd_file.A134  # self.A2 = jsd_file.A2  # self.A3 = jsd_file.A3  # self.A4 = jsd_file.A4  # self.SMandQY = jsd_file.SMandQY  # self.JSBook = jsd_file.JSBook  # self.TGGBook = jsd_file.TGGBook  # self.FileSource = jsd_file.FileSource  # self.FileDesignUId = jsd_file.FileDesignUId  # self.FileDesignUName = jsd_file.FileDesignUName  # self.FileDesignCreateDate = jsd_file.FileDesignCreateDate  # self.LastModifyDate = jsd_file.LastModifyDate  # self.IsDel = jsd_file.IsDel  # self.FileSize = jsd_file.FileSize  # self.cundanghao = jsd_file.cundanghao  # self.cdhPath = jsd_file.cdhPath  # self.GDDate = jsd_file.GDDate  # self.PDFTrans = jsd_file.PDFTrans  # self.InputOrjCode = jsd_file.InputOrjCode  # self.InputAlterVersion = jsd_file.InputAlterVersion  # self.FileListName = jsd_file.FileListName  # self.esign = jsd_file.esign  # self.WBSCode = jsd_file.WBSCode  # self.KZWBSCode = jsd_file.KZWBSCode
        jsd_file.formate_LastModifyDate(self.pdf_type)

    # def get_path(self, file_url):
    #     # TODO 把相关目录信息写入配置文件
    #     start = re.search('/TransFolder/CSign/', file_url).end()
    #     end = re.search('.pdf', file_url).end()
    #     head = '\\\\nas-website1.cnpdc.com\\TransFolder\\CSign\\'
    #     file_path = file_url[start:end].replace('/', '\\')
    #     print(head+file_path)
    #     return head+file_path

    def get_url(self, file_url):
        # TODO 把相关目录信息写入配置文件
        start = re.search('http:', file_url).start()
        end = re.search('.pdf', file_url).end()
        file_path = file_url[start:end]
        return file_path

    def get_record_count(self, s):
        char = s[0]
        if char.isalpha():
            return ord(char)-65
        elif char.isdecimal():
            return int(s)
        else:
            print("version not found")
            return 0
