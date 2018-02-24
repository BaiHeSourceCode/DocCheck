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

if __name__ == "__main__":
    dbr = db_reader.DB_Reader(host="d-s48.cnpdc.com", user="p108034", pwd="123qweASD", db="CenterDB")
    jsdfm = jsd_filemain.JSD_FILEMAIN('63b52f0b-6bd0-4bd6-af50-f4a0de83b2d5', dbr)
    doc = file.Document(jsdfm)
    dl = DownLoader()
    local_pdf = dl.get_pdf(doc)
    # 如果是cad
    if doc.pdf_type == 0:
        print("this is a cad")
        cr = chart_reader.ChartReader(doc)
        charts = cr.read_chart()
        cp = chart_parser.ChartParser(charts, doc)
        doc.info = cp.parser_chart()
    # 如果是 word
    else:
        print("this is a word")
        word_reader = pdf_reader.PdfReader(doc)
        word_layouts = word_reader.read_pdf()
        word_parser = pdf_parser.Parser()
        doc.info = word_parser.word2pdf_parser(word_layouts, doc)

    print(doc.info)

    dc = DocumentChecker(doc)
    dc.check(jsdfm)
