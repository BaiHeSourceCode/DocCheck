#!/usr/bin/env python
# coding=utf-8
__author__ = 'Baihe'
__date__ = '2018/1/29'
# 读取pdf的图片
import rule_reader
from wand.image import Image
from wand.color import Color
import cv2
import numpy as np
import chart_page
import time


class ChartReader(object):
    def __init__(self, file):
        self.file = file
        self.config = rule_reader.RuleReader('chart_size').config

    def read_chart(self):
        charts = []
        try:
            # 获取pdf图纸文件 ,pdf存储在local_pdf中， 规则为local_path + file.FileID + '.pdf'
            with Image(filename=self.file.pdf_file, resolution=int(self.file.dpi)) as page_imgs:
                page_no = 0
                # 访问图纸的每一页，并将其另存为图片对象
                for img in page_imgs.sequence:
                    img = Image(image=img)
                    img.background_color = Color("white")
                    img.alpha_channel = 'flatten'
                    img.format = 'png'
                    img.threshold(0.6)
                    img_buffer = np.asarray(bytearray(img.make_blob()), dtype=np.uint8)
                    cv2_img = cv2.imdecode(img_buffer, cv2.IMREAD_GRAYSCALE)
                    ret, cv2_img = cv2.threshold(cv2_img, 127, 255, cv2.THRESH_BINARY)

                    # 获取图纸大小
                    chart_size = self.size_of_chart(img)
                    page = chart_page.Page(self.file, page_no, chart_size, cv2_img)
                    yield page
                    if self.file.config['chart']['out']:
                        img.save(filename=self.file.chart_path + self.file.FileID + str(page_no) + 'wand.png')
                    if self.file.config['chart']['out']:
                        cv2.imwrite(self.file.chart_path + self.file.FileID + str(page_no) + 'cv2.png', cv2_img)
                    charts.append(page)
                    # yield chart_name
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


