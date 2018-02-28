#!/usr/bin/env python
# coding=utf-8
import rule_reader

__author__ = 'Baihe'
__date__ = 2018 / 2 / 11
import re


class Page():
    def __init__(self, file, page_no, chart_size, img):

        """页面信息"""
        self.FileID = file.FileID
        self.JSDID = file.JSDID
        self.page_no = page_no
        self.chart_size = chart_size
        self.pdf_type = 0
        # self.img_path = img_path
        self.config = rule_reader.RuleReader('path').config
        self.chart_path = file.chart_path
        self.labels_path = file.labels_path
        self.rate = 1.0
        self.chart = img

        '''元数据信息'''
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
        # 获取密级信息 图纸暂不考虑
        # self.Secret = 'F'  # jsd_file.Secret
        # self.SecretExpireDate = '1900-01-01'  # jsd_file.SecretExpireDate
        # 获取参考文件
        self.RefFileCode = ''  # jsd_file.RefFileCode
        self.RefFileVersion = ''  # jsd_file.RefFileVersion
        # 获取文件类别 C-new;B-modify;A-identical
        self.FileCategory = ''  # jsd_file.FileCategory
        # 图纸尺寸
        self.PDFPageSize = ''  # jsd_file.PDFPageSize
        # 文件页数，页数暂不考虑
        # self.PDFPageCount = file.PDFPageCount
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
        self.record_count = file.record_count
        # 记录比对元数据结果
        self.result = []
