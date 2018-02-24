#!/usr/bin/env python
# coding=utf-8
__author__ = 'Baihe'
__date__ = '2018/1/25'
# 根据pdf的layout，再加上template的格式解析模板内容


from pdfminer.layout import LTTextBoxHorizontal
import rule_reader


class Parser(object):
    def __init__(self):
        self.config = rule_reader.RuleReader().config_read('template')

    def word2pdf_parser(self, layouts, file) -> dict:
        areas = self.config.sections()
        # 按照页面访问layout
        for page in range(file.PDFPageCount):
            info = {}
            layout = layouts[page]
            for x in layout:
                if isinstance(x, LTTextBoxHorizontal):
                    # TODO 临时处理表格中两个单元格合并为一个的情况，后续再处理
                    content = x.get_text().replace('版本/Rev:', '').replace('版本', '').replace('Rev', '').replace('Status','').replace('状态', '')
                    for area in areas:
                        # 判断area是否属于该页面，page从0开始，属于才处理
                        if self.config[area]['page'] == str(page + 1) or self.config[area]['page'] == 'all':
                            x_plot = (x.x0 + x.x1) / 2
                            y_plot = (x.y0 + x.y1) / 2
                            x_max = int(self.config[area]['xmax'])
                            x_min = int(self.config[area]['xmin'])
                            y_max = int(self.config[area]['ymax'])
                            y_min = int(self.config[area]['ymin'])
                            # 判断x是否属于area
                            if x_min < x_plot < x_max and y_min < y_plot < y_max:
                                # print("page:" + str(page) + " area:" + area + ":" + content)
                                # 处理需要合并表单内容的数据，如跨行的标题。
                                if 'rev_record' == self.config[area]['name'] and content != '':
                                    if info.get(area):
                                        info[area] = info[area] + '||' + content.replace('\n', '').replace(' ', '')
                                    else:
                                        info[area] = content.replace('\n', '').replace(' ', '')
                                elif 'title' == self.config[area]['name'] and content != '':
                                    if info.get(area):
                                        info[area] = info[area] + content.replace('\n', '').replace(' ', '')
                                    else:
                                        info[area] = content.replace('\n', '').replace(' ', '')
                                # 非特殊情况直接记录结果
                                else:
                                    info[self.config[area]['name']] = content.replace('\n', '').replace(' ', '')

                                # 为file对象的元数据赋值
                                if 'FileType_FileDesignStep' == area:
                                    combine_att = content.split('\n')
                                    setattr(file, 'FileType', combine_att[0].replace('\n', '').replace(' ', ''))
                                    setattr(file, 'FileDesignStep', combine_att[1].replace('\n', '').replace(' ', ''))
                                content = content.replace('\n', '').replace(' ', '')
                                if 'FileCategory' == self.config[area]['name'] and content != '':
                                    setattr(file, 'FileCategory', area.split('_')[1])
                                elif 'Secret' == area:
                                    if content == '普通商密':
                                        setattr(file, 'Secret', 'R')
                                    elif content == '核心商密':
                                        setattr(file, 'Secret', 'C')
                                elif 'SecretExpireDate' == area:
                                    if content != '':
                                        setattr(file, 'SecretExpireDate',
                                                content.replace('解密时间：', '').replace('/', '-'))
                                elif hasattr(file, area):
                                    setattr(file, area, content)
            file.result.append(info)
        return file.result
