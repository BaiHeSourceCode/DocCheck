#!/usr/bin/env python
# coding=utf-8
import rule_reader

__author__ = 'Baihe'
__date__ = '2018/1/25'
# 解析pdf的内容

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator


class PdfReader(object):
    def __init__(self, file, password=''):
        self.file = file
        self.pages = range(file.PDFPageCount)
        self.password = password

    def read_pdf(self):
        # 获取文档对象
        fp = open(self.file.pdf_file, "rb")
        # 创建一个与文档相关联的解释器
        parser = PDFParser(fp)
        # 获取PDF文档对象
        doc = PDFDocument(parser, self.password)
        # 查看是否可被解析
        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed
        else:
            # 创建PDF资源管理器
            resource = PDFResourceManager()
            # 参数分析器
            device = PDFPageAggregator(resource, laparams=LAParams())
            # 创建一个PDF解释器对象
            interpreter = PDFPageInterpreter(resource, device)
            i = 0
            layouts = []
            for page in PDFPage.get_pages(fp, self.pages):
                interpreter.process_page(page)
                layout = device.get_result()
                layouts.insert(self.pages[i], layout)
                i += 1
            return layouts
