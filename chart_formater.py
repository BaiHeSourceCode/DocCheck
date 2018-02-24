#!/usr/bin/env python
# coding=utf-8
__author__ = 'Baihe'
__date__ = 2018 / 2 / 7
import cv2
import rule_reader


class ChartFormater:
    def __init__(self, chart, file, pageno):
        self.chart = chart
        self.file = file
        self.pageno = pageno
        rr_config = rule_reader.RuleReader()
        rr_path = rule_reader.RuleReader()
        self.config = rr_config.config_read('chart_size')
        self.path = rr_path.config_read('path')
        if self.file.PDFPageSize in ['3H', '3V', '4H', '4V']:
            self.edge = 5
        else:
            self.edge = 10
        self.label_x = 140 + self.edge
        self.label_y = 91 + self.edge

    def chart_resize(self):
        # 读取一页图纸图片
        chart_bgr = cv2.imread(self.chart)
        # 转换为黑白
        chart_gray = cv2.cvtColor(chart_bgr, cv2.COLOR_BGR2GRAY)
        # 二值化处理
        ret, chart_binary = cv2.threshold(chart_gray, 127, 255, cv2.THRESH_BINARY_INV)
        # 获取图片大小
        w, h = chart_binary.shape[::-1]
        # 保存签字日期图片
        sign_date_cut = chart_binary[h - 78:h, w - 240:w]
        sign_date_filename = self.file.labels_path + self.file.FileID + str(self.pageno) + '_date.png'
        cv2.imwrite(sign_date_filename, sign_date_cut)

        # 根据图片找到图框边界
        left, up, right, down, std_w, std_h = self.find_frame_by_point(chart_binary, w, h)
        # 截取图框
        cut = chart_binary[up:down, left:w-right]
        # 获取图框与原始页面的比例大小
        rate = (std_w-right-left) / std_w
        # if self.path['cut']['out']:
        #     cv2.imwrite(self.path['cut']['path'] + self.file.FileID + '.png', cut)
        # 获取图框所在位置
        label_x_p = int(self.label_x * self.file.dpi / 25.4)
        label_y_p = int(self.label_y * self.file.dpi / 25.4)
        # 获取图框边缘大小
        edge_p = int(self.edge * self.file.dpi / 25.4)
        # 截取labels
        labels = cut[int((std_h-label_y_p) * rate):int((std_h-edge_p)*rate), int((std_w-label_x_p) * rate):int((std_w-edge_p)*rate)]
        # 生成内容信息截图
        labels_filename = self.file.labels_path + self.file.FileID + str(self.pageno) + '.png'
        cv2.imwrite(labels_filename, labels)
        return labels_filename,sign_date_filename, rate

    def find_frame_by_point(self, chart_binary, w, h):
        left = 0
        up = 0
        right = 0
        for y in range(h):
            for x in range(w):
                if chart_binary[y][x] == 255:
                    left = x
                    up = y
                    break
            if chart_binary[y][x] == 255:
                break        
        for y in range(h):
            for x in range(w):
                if chart_binary[y][w - x - 1] == 255:
                    right = x
                    break
            if chart_binary[y][w - x - 1] == 255:
                break
        std_w = int(int(self.config[self.file.PDFPageSize]['x']) * self.file.dpi / 25.4)
        std_h = int(int(self.config[self.file.PDFPageSize]['y']) * self.file.dpi / 25.4)
        down = int((w - left - right) * std_h / std_w + up)
        return left, up, right, down, std_w, std_h

