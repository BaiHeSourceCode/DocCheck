#!/usr/bin/env python
# coding=utf-8
import rule_reader
import chart_marker
__author__ = 'Baihe'
__date__ = 2018 / 2 / 12


class DocumentChecker:
    def __init__(self, file):
        self.file = file
        self.errors = []
        # 文件是cad还是word转的pdf, 0是cad，1是word
        if file.pdf_type == 0:
            self.rule = rule_reader.RuleReader('check_chart').config
        elif file.pdf_type == 1:
            self.rule = rule_reader.RuleReader('check_doc').config
        else:
            print('configuration failed')

    def check(self, meta):
        for e in self.rule.sections():
            if hasattr(meta, self.rule[e]['meta']):
                mdata = str(getattr(meta, self.rule[e]['meta'])).replace(' ', '')
                if hasattr(self.file, self.rule[e]['file']):
                    fdata = str(getattr(self.file, self.rule[e]['file'])).replace(' ', '')
                    if mdata == fdata:
                        print(e + ":ok")
                    else:
                        print(e + ": not ok")
                        print('error:')
                        print('meta is ' + mdata)
                        print('but file is ' + fdata)
                        self.errors.append(e)
                else:
                    print('error:')
                    print('file attribute not found!')
            else:
                print('error:')
                print('metadata attribute not found!')
        if self.file.pdf_type == 0:
            # print(self.errors)
            cm = chart_marker.ChartMarker()
            cm.mark_errors(self.file, self.errors)
