#!/usr/bin/env python
# coding=utf-8
import chart_parser
from doc_checker import DocumentChecker
from pdf_downloader import DownLoader

__author__ = 'Baihe'
__date__ = '2018/1/25'

import db_reader
import file
import jsd_filemain
import pdf_parser
import pdf_reader
import chart_reader
import jsd_files_reader

if __name__ == "__main__":
    dbr = jsd_files_reader.JSD_Reader()
    for jsd_record in dbr.get_files('371abe47-7c9d-660a-a4-8f232def95436a'):
        jsdfm = jsd_filemain.JSD_FILEMAIN(jsd_record)
        doc = file.Document(jsdfm)
        dl = DownLoader()
        local_pdf = dl.get_pdf(doc)
        # 如果是cad
        if doc.pdf_type == 0:
            print("this is a cad")
            cr = chart_reader.ChartReader(doc)
            info = []
            for page in cr.read_chart():
                cp = chart_parser.ChartParser(page)
                page.info = cp.parser_chart()
                dc = DocumentChecker(page)
                dc.check(jsdfm)
                info.append(page.info)
            print(info)
        # 如果是 word
        else:
            print("this is a word")
            word_reader = pdf_reader.PdfReader(doc)
            word_layouts = word_reader.read_pdf()
            word_parser = pdf_parser.Parser()
            doc.info = word_parser.word2pdf_parser(word_layouts, doc)
            dc = DocumentChecker(doc)
            dc.check(jsdfm)
        print(doc.info)
