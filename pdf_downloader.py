#!/usr/bin/env python
# coding=utf-8
import rule_reader
from requests_ntlm import HttpNtlmAuth
import requests

__author__ = 'Baihe'
__date__ = 2018 / 2 / 12

class DownLoader():
    def __init__(self, username='cnpdc\\p108034', password='123qweASD'):
        self.username = username
        self.password = password

    def get_pdf(self, file):
        res = self.load(file)
        with open(file.pdf_file, 'wb') as temp_file:
            temp_file.write(res.content)
        return file.pdf_file


    def load(self, file):
        if file.url is None:
            return None
        res = requests.get(file.url, auth=HttpNtlmAuth(self.username, self.password))
        if res.status_code != 200:
            print("acess error")
            return None
        return res