#!/usr/bin/env python
# coding=utf-8
__author__ = 'Baihe'
__date__ = '2018/1/29'
# 解析pdf的图片

import pytesseract
from PIL import Image as Img
import chart_formater
import rule_reader


class ChartParser(object):
    def __init__(self, page):
        self.page = page
        self.config = rule_reader.RuleReader('chart_label').config
        self.path = rule_reader.RuleReader('path').config
        self.rconfig = rule_reader.RuleReader('chart_record').config


    def parser_chart(self):
        labels = self.config.sections()
        record_sections = self.rconfig.sections()
        page_info = {}
        cf = chart_formater.ChartFormater(self.page)
        # labels_filename, sign_date, record, rate = cf.chart_resize()
        labels_img, sign_date_img, record_img, rate = cf.chart_resize()
        with Img.fromarray(sign_date_img) as sign_date_chart:
            text = pytesseract.image_to_string(sign_date_chart, lang='eng')
            self.page.SignDate = text
            # 截取格式为yyyy-mm的签字信息
            page_info['SignDate'] = text[0:7]

        with Img.fromarray(labels_img) as labels_chart:
            for label in labels:
                x1 = float(self.config[label]['x1']) * self.page.dpi * rate / 25.4
                y1 = float(self.config[label]['y1']) * self.page.dpi * rate / 25.4
                x2 = float(self.config[label]['x2']) * self.page.dpi * rate / 25.4
                y2 = float(self.config[label]['y2']) * self.page.dpi * rate / 25.4
                label_chart = labels_chart.crop((x1, y1, x2, y2))
                if int(self.path['label']['out']):
                    label_chart.save(self.path['label']['path'] + self.page.FileID + '_' + str(self.page.page_no) +
                                     '_' + label + '.png')
                if 'FileVersion' == label or 'FileDesignStep' == label:
                    text = pytesseract.image_to_string(label_chart, lang='eng', config='-psm 10')
                elif 'title' == label:
                    text = pytesseract.image_to_string(label_chart, lang='chi_sim').replace('\n', '')
                elif 'FileCategory_A' == label or 'FileCategory_B' == label or 'FileCategory_C' == label:
                    if pytesseract.image_to_string(label_chart, lang='eng', config='-psm 10') != '':
                        setattr(self.page, 'FileCategory', label.split('_')[1])
                elif 'LastModifyDate' == label:
                    text = pytesseract.image_to_string(label_chart, lang='eng').replace('.', '-').replace('。', '-')
                    page_info[label] = text
                else:
                    text = pytesseract.image_to_string(label_chart, lang='eng')
                    page_info[label] = text
                if hasattr(self.page, label):
                    setattr(self.page, label, text)

        if self.page.record_count != 0:
            with Img.fromarray(record_img) as record_chart:
                # 每个record高是6cm
                row_infos = []
                for row in range(self.page.record_count+1):
                    row_info = {}
                    for sec in record_sections:
                        x1 = float(self.rconfig[sec]['x1']) * self.page.dpi * rate / 25.4
                        y1 = (float(self.rconfig[sec]['y1']) + row * 6) * self.page.dpi * rate / 25.4
                        x2 = float(self.rconfig[sec]['x2']) * self.page.dpi * rate / 25.4
                        y2 = (float(self.rconfig[sec]['y2']) + row * 6) * self.page.dpi * rate / 25.4
                        record_label = record_chart.crop((x1, y1, x2, y2))
                        if int(self.path['label']['out']):
                            record_label.save(self.path['label']['path'] + self.page.FileID + '_' +
                                              str(self.page.page_no) + '_' + str(row) + '_' + sec + '.png')
                        if 'FileVersion' == sec:
                            text = pytesseract.image_to_string(record_label, lang='eng', config='-psm 10')
                        else:
                            text = pytesseract.image_to_string(record_label, lang='eng')
                        row_info[sec] = text
                    row_infos.append(row_info)
                # 打印record信息
                # print(row_infos)
                self.page.records = row_infos
                # 存储最新版信息
                for k in row_infos[0]:
                    v = row_infos[0][k]
                    if k == 'LastModifyDate':
                        v = v.replace('.', '-').replace('。', '-')
                        # 截取格式为yyyy-mm的版本信息
                        v = v[0:7]
                    page_info[k] = v
                    if hasattr(self.page, k):
                        setattr(self.page, k, v)
        return page_info
