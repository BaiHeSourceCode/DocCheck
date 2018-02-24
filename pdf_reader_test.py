#!/usr/bin/env python
# coding=utf-8
__author__ = 'Baihe'
__date__ = 2018 / 2 / 22

# !/usr/bin/env python
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
from pdfminer.layout import LTTextBoxHorizontal


class PdfReader(object):

    def read_pdf(self, pdf_file, pages):
        # 获取文档对象
        fp = open(pdf_file, "rb")
        # 创建一个与文档相关联的解释器
        parser = PDFParser(fp)
        # 获取PDF文档对象
        doc = PDFDocument(parser)
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
            for page in PDFPage.get_pages(fp, pages):
                interpreter.process_page(page)
                layout = device.get_result()
                for x in layout:
                    if isinstance(x, LTTextBoxHorizontal):
                        print(x)
                layouts.insert(pages[i], layout)
                i += 1
            return layouts




if __name__ == "__main__":
    reader = PdfReader()
    layouts = reader.read_pdf('d:/6.pdf', range(3))
    #print(layouts)
