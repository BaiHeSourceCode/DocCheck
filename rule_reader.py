#!/usr/bin/env python
# coding=utf-8
__author__ = 'Baihe'
__date__ = '2018/1/25'
# config_configparser.py 配置文件
# configparser 可以读写和解析注释文件, 但是没有写入注释的功能

import configparser


class RuleReader(object):
    def __init__(self):
        self.config = configparser.ConfigParser()

    def config_read(self, config_file_name):
        # 读取
        # self.config = configparser.ConfigParser()
        self.config.read('resources/' + config_file_name + '.ini')
        return self.config


if __name__ == "__main__":
    rr = RuleReader()
    config = rr.config_read()
    areas = config.sections()  # 配置组名, TEST
    print(areas)
    for area in areas:
        print(area)
        for key, value in config[area].items():
            print(key + ":" + value)
