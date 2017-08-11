# -*- coding:utf-8 -*-

import os

class CodeTracer(object):

    def __init__(self):
        self._invaild_file_list = list()
        self._wait_for_judge = list()
        self._query_dir = os.path.abspath(os.path.pardir)
        self._report_list = list()
        self._report_name = 'code_judge_report.txt'

        # 删除原有
        with open(self._report_name, 'w') as _file:
            pass

    def start_deal(self):
        '''
        程序入口，外界与该模块的接口
        :return: nothing
        '''
        self._file_filter(self._query_dir)
        self._deliver_mission()
        self._show_report()

    def _file_filter(self, _name):
        '''
        文件过滤
        :param _name: 文件名 str
        :return: nothing
        '''
        if os.path.isfile(_name):
            # 过滤规则 后续放到外部文件中处理
            if _name.endswith('.pyc') \
                or _name.endswith('.xml') \
                or _name.endswith('.iml'):
                self._invaild_file_list.append(_name)
            elif _name.endswith('.py'):
                self._wait_for_judge.append(_name)

        elif os.path.isdir(_name):
            for _dir in os.listdir(_name):
                # 跳过本身
                if _dir == 'CodeStyleJudge':
                    continue
                self._file_filter(os.path.join(_name, _dir))

    def _record_result_of_filter(self):
        '''
        将文件过滤后的结果写入到测试报告
        :return: nothing
        '''
        with open('code_judge_report.txt', 'a+') as _file:
            _file.write('invaild file: \n')
            for _filename in self._invaild_file_list:
                _file.write(_filename + '\n')
            _file.write('file for testing: \n')
            for _filename in self._wait_for_judge:
                _file.write(_filename + '\n')
            _file.write('-' * 40 + '\n')

    def _deliver_mission(self):
        '''
        任务分发
        :return: nothing
        '''
        for _file in self._wait_for_judge:
            self._single_file_code_style_judge(_file)

    def _show_report(self):
        '''
        将结果写入测试报告
        :return: nothing
        '''
        with open('code_judge_report.txt', 'a+') as _file:
            for _report in self._report_list:
                _file.write(str(_report) + '\n')

    def _single_file_code_style_judge(self, _file_name):
        '''
        对单个文件进行扫描
        :param _file_name: 文件名 str
        :return: nothing
        '''
        print 'Begin scaning {} ...'.format(_file_name)

        with open(_file_name) as _file:
            _line_num = 0
            for _line in _file.readlines():
                _line_num += 1
                _line = _line.lstrip().rstrip()

                if _line == 1 and _line != '# -*- coding: utf-8 -*-':
                    self._report_list.append((_file_name, _line_num, 'utf8 header', 'lack of utf8 tag'))
                if _line:
                    if len(_line) > 120:
                        self._report_list.append((_file_name, _line_num, 'line length', 'too long'))
                        print _line
                    if '#' in _line:
                        self._commit_judge(_line, _line_num, _file_name)
                    if _line.startswith('def'):
                        self._def_judge(_line, _line_num, _file_name)
                    elif _line.startswith('class'):
                        self._class_judge(_line, _line_num, _file_name)

        print 'Finished scaning {}. \n'.format(_file_name)

    # 函数鉴定
    def _def_judge(self, _line, _line_num, _file_name):
        if _line.isupper():
            self._report_list.append((_file_name, _line_num, 'def name', 'should be lowcase'))

    # 类鉴定
    def _class_judge(self, _line, _line_num, _file_name):
        if _line.split()[1][0].islower():
            self._report_list.append((_file_name, _line_num, 'class name', 'first letter should be upper'))

        if '_' in _line:
            self._report_list.append((_file_name, _line_num, 'class name', 'should not contain underline'))

    # 注释鉴定
    def _commit_judge(self, _line, _line_num, _file_name):
        if _line.startswith('#'):
            try:
                if _line[1] not in (' ', '  '):
                    self._report_list.append((_file_name, _line_num, 'comment', 'should be a blank after #'))
            except Exception, e:
                print (_file_name, _line_num, e)
        else:
            self._report_list.append((_file_name, _line_num, 'comment', 'should put comments another line'))
