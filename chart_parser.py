#!/usr/bin/env python
# coding=utf-8
__author__ = 'Baihe'
__date__ = '2018/1/29'
# 解析pdf的图片

import pytesseract
from PIL import Image as Img
from PIL import ImageFilter

import chart_formater
import rule_reader


class ChartParser(object):
    def __init__(self, charts, file):
        self.charts = charts
        self.file = file
        rr_config = rule_reader.RuleReader()
        rr_path = rule_reader.RuleReader()
        self.config = rr_config.config_read('chart_label')
        self.path = rr_path.config_read('path')

    def parser_chart(self):
        labels = self.config.sections()
        results = []
        pageno = 0
        for chart in self.charts:
            result = {}
            cf = chart_formater.ChartFormater(chart, self.file, pageno)
            labels_filename, sign_date_filename, rate = cf.chart_resize()
            with Img.open(sign_date_filename) as sign_date_chart:
                text = pytesseract.image_to_string(sign_date_chart, lang='eng')
                self.file.SignDate = text
                result['SignDate'] = text
            with Img.open(labels_filename) as labels_chart:
                for label in labels:
                    x1 = float(self.config[label]['x1']) * self.file.dpi * rate / 25.4
                    y1 = float(self.config[label]['y1']) * self.file.dpi * rate / 25.4
                    x2 = float(self.config[label]['x2']) * self.file.dpi * rate / 25.4
                    y2 = float(self.config[label]['y2']) * self.file.dpi * rate / 25.4
                    label_chart = labels_chart.crop((x1, y1, x2, y2))
                    if int(self.path['label']['out']):
                        label_chart.save(self.path['label']['path'] + self.file.FileID + '_' + label + '.png')
                    if 'FileVersion' == label or 'FileDesignStep' == label:
                        # label_chart = label_chart.filter(ImageFilter.DETAIL)
                        text = pytesseract.image_to_string(label_chart, lang='eng', config='-psm 10')
                    elif 'title' == label:
                        # label_chart = label_chart.filter(ImageFilter.Kernel((3, 3), (1, 1, 1, 0, 0, 0, 2, 0, 2)))
                        text = pytesseract.image_to_string(label_chart, lang='chi_sim').replace('\n', '')
                    elif 'FileCategory_A' == label or 'FileCategory_B' == label or 'FileCategory_C' == label:
                        if pytesseract.image_to_string(label_chart, lang='eng', config='-psm 10') != '':
                            setattr(self.file, 'FileCategory', label.split('_')[1])
                    else:
                        text = pytesseract.image_to_string(label_chart, lang='eng')
                    result[label] = text
                    if hasattr(self.file, label):
                        setattr(self.file, label, text)
            pageno += 1
            results.append(result)
        return results
