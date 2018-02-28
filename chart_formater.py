#!/usr/bin/env python
# coding=utf-8
__author__ = 'Baihe'
__date__ = 2018 / 2 / 7
import cv2
import rule_reader
import os

class ChartFormater:
    def __init__(self, page):
        self.page = page
        # self.rate = 1.0
        self.config = rule_reader.RuleReader('chart_size').config
        self.path = rule_reader.RuleReader('path').config
        if self.page.chart_size in ['3H', '3V', '4H', '4V']:
            self.edge = 5
        else:
            self.edge = 10

        self.std_w = int(int(self.config[self.page.chart_size]['x']) * self.page.dpi / 25.4)
        self.std_h = int(int(self.config[self.page.chart_size]['y']) * self.page.dpi / 25.4)

        self.label_x = 140 + self.edge
        self.label_y = 91 + self.edge
        # self.label_y = 85 + self.edge 这里本来应该修改为85的，但是懒得弄了，就这样吧
        self.record_x = 140 + self.edge
        self.record_y1 = 91 + self.edge + page.record_count * 6
        self.record_y2 = 85 + self.edge

    def chart_resize(self):
        # 图片预处理
        # chart = self.pre_process_img()
        chart = self.page.chart
        # 保存签字日期图片
        sign_date = self.cut_sign_date(chart)
        # 获取图框及压缩比例
        frame, self.page.rate = self.cut_frame(chart)
        # 获取图框截图
        labels = self.cut_labels(frame)
        # 保存多版本信息
        if self.page.record_count == 0:
            return labels, sign_date, '', self.page.rate
        else:
            record = self.cut_record(frame)
            return labels, sign_date, record, self.page.rate

    # pre_process_img不再使用，改为在read_chart中实现
    def pre_process_img(self):
        # 读取一页图纸图片
        chart_bgr = cv2.imread(self.page.img_path)
        # 转换为黑白
        chart_gray = cv2.cvtColor(chart_bgr, cv2.COLOR_BGR2GRAY)
        # 二值化处理
        ret, chart_binary = cv2.threshold(chart_gray, 127, 255, cv2.THRESH_BINARY_INV)
        return chart_binary

    def find_frame_by_point(self, chart_binary, w, h):
        left = 0
        up = 0
        right = 0
        for y in range(h):
            for x in range(w):
                if chart_binary[y][x] == 0:
                    left = x
                    up = y
                    break
            if chart_binary[y][x] == 0:
                break
        for y in range(h):
            for x in range(w):
                if chart_binary[y][w - x - 1] == 0:
                    right = x
                    break
            if chart_binary[y][w - x - 1] == 0:
                break
        down = int((w - left - right) * self.std_h / self.std_w + up)
        return left, up, right, down

    def cut_record(self, frame):
        left = int(self.record_x * self.page.dpi / 25.4)
        top = int(self.record_y1 * self.page.dpi / 25.4)
        right = int(self.edge * self.page.dpi / 25.4)
        bottom = int(self.record_y2 * self.page.dpi / 25.4)
        record = frame[int((self.std_h-top) * self.page.rate):int((self.std_h-bottom) * self.page.rate),
                 int((self.std_w-left)*self.page.rate):int((self.std_w-right)*self.page.rate)]
        # 生成内容信息截图
        if self.path['labels']['out']:
            if not os.path.exists(self.page.labels_path):
                os.makedirs(self.page.labels_path)
            cv2.imwrite(self.page.labels_path + str(self.page.page_no) + '_record.png', record)
        return record

    def cut_sign_date(self, chart_binary):
        w, h = chart_binary.shape[::-1]
        sign_date_cut = chart_binary[h - 78:h, w - 240:w]
        if self.path['labels']['out']:
            if not os.path.exists(self.page.labels_path):
                os.makedirs(self.page.labels_path)
            cv2.imwrite(self.page.labels_path + str(self.page.page_no) + '_date.png', sign_date_cut)
        return sign_date_cut

    def cut_labels(self, frame):
        # 获取图框所在位置
        label_x_p = int(self.label_x * self.page.dpi / 25.4)
        label_y_p = int(self.label_y * self.page.dpi / 25.4)
        # 获取图框边缘大小
        edge_p = int(self.edge * self.page.dpi / 25.4)
        # 截取labels
        labels = frame[int((self.std_h - label_y_p) * self.page.rate):int((self.std_h - edge_p) * self.page.rate),
                 int((self.std_w - label_x_p) * self.page.rate):int((self.std_w - edge_p) * self.page.rate)]
        # 生成内容信息截图
        if self.path['labels']['out']:
            if not os.path.exists(self.page.labels_path):
                os.makedirs(self.page.labels_path)
            cv2.imwrite(self.page.labels_path + str(self.page.page_no) + '.png', labels)
        return labels

    def cut_frame(self, chart):
        # 获取图片大小
        w, h = chart.shape[::-1]
        # 根据图片找到图框边界
        left, up, right, down = self.find_frame_by_point(chart, w, h)
        # 获取图框与原始页面的比例大小
        rate = (self.std_w - right - left) / self.std_w
        # 截取图框
        frame = chart[up:down, left:w - right]
        return frame, rate
