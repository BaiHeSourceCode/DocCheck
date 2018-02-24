#!/usr/bin/env python
# coding=utf-8
__author__ = 'Baihe'
__date__ = 2018 / 2 / 9
import os


def get_file_list(path, list_name):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            get_file_list(file_path, list_name)
        elif os.path.splitext(file_path)[1] == '.pdf':
            list_name.append(file_path)