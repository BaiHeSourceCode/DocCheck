#!/usr/bin/env python
# coding=utf-8
__author__ = 'Baihe'
__date__ = '2018/1/29'
# 读取pdf的图片
import rule_reader
from wand.image import Image
from wand.color import Color



class ChartReader(object):
    def __init__(self, file):
        self.file = file
        rr = rule_reader.RuleReader()
        self.config = rr.config_read('chart_size')

    def read_chart(self):
        charts = []
        try:
            # 获取pdf图纸文件 ,pdf存储在local_pdf中， 规则为local_path + file.FileID + '.pdf'
            with Image(filename=self.file.pdf_file, resolution=int(self.file.dpi)) as pages:
                pages.background_color = Color("white")
                pages.alpha_channel = 'flatten'
                page_no = 0
                # 访问图纸的每一页，并将其另存为图片对象
                for page in pages.sequence:
                    page = Image(image=page)
                    # 获取图纸大小
                    self.file.PDFPageSize = self.size_of_chart(page)
                    chart_name = self.file.chart_path + self.file.FileID + str(page_no) + '.jpg'
                    page.save(filename=chart_name)
                    charts.append(chart_name)
                    page_no += 1

        finally:
            return charts

    def size_of_chart(self, page):
        sizes = self.config.sections()
        chart_x = page.size[0]
        chart_y = page.size[1]
        off = 50
        for size in sizes:
            # pixel= mm * dpi / 25.4
            size_x = int(self.config[size]['x']) * self.file.dpi / 25.4
            size_y = int(self.config[size]['y']) * self.file.dpi / 25.4
            if chart_x > size_x - off < size_x + off and chart_y > size_y - off < size_y + off:
                return size
        return ''

    def to_mm(self, pixel):
        return int(pixel * 25.4 / self.file.dpi)

    def to_pixel(self, mm):
        return int(mm * self.file.dpi / 25.4)


