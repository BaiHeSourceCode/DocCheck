#!/usr/bin/env python
# coding=utf-8
__author__ = 'Baihe'
__date__ = 2018 / 2 / 27
import rule_reader
import cv2


class ChartMarker:
    def __init__(self):
        self.config = rule_reader.RuleReader('chart_label_frame').config
        self.chart_path = rule_reader.RuleReader('path').config

    def mark_errors(self, page, errors):
        for error in errors:
            print(error)
            if error in self.config.sections():
                print("in")
                print(page.labels_path)
                img_name = page.labels_path + str(page.page_no) + '.png'
                img = cv2.imread(img_name)
                pt1 = (
                int(float(self.config[error]['x1']) * 300 / 24.5), int(float(self.config[error]['y1']) * 300 / 24.5))
                pt2 = (
                int(float(self.config[error]['x2']) * 300 / 24.5), int(float(self.config[error]['y2']) * 300 / 24.5))
                cv2.rectangle(img, pt1, pt2, (0, 0, 255), 3)
                cv2.imwrite(img_name, img)
