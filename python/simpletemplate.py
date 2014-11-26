#!/usr/bin/env python
# coding=utf-8

import sys
import re
import os.path
import logging
import StringIO
from lxml import etree

logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(levelname)s] %(message)s', datefmt='%Y%m%d %H:%M:%S')


class SimpleTemplate:
    '''Simple Template of lxml etree
    '''
    def __init__(self):
        self.__alltpl = {}

    def loadTpl(self, tplselector, tpldir):
        '''加载所有模板文件
        '''
        fp = open(tplselector, 'r')
        while True:
            line = fp.readline()
            if not line:
                break
            arr = line.strip().split('\t')
            urlregex = re.compile(arr[0])
            tplfile = arr[1]
            tplpath = os.path.join(tpldir, tplfile)
            self.__loadUrlTpl(urlregex, tplpath)

    def __loadUrlTpl(self, regex, tplpath):
        '''加载模板文件
        '''
        fp = open(tplpath, 'r')
        data = fp.read()
        xsltdoc = etree.XML(data)
        transform = etree.XSLT(xsltdoc)
        self.__alltpl[regex] = transform

    def selectTransform(self, url):
        for regex, t in self.__alltpl.items():
            if regex.match(url):
                return t
        return None

    def parse(self, url, data, encode=None):
        '''分析网页数据
        '''
        if encode is None:
            encode = self.fetch_encoding(data)
        parser = etree.HTMLParser(encoding=encode)
        tree = etree.parse(StringIO.StringIO(data), parser)
        transform = self.selectTransform(url)
        purl = "'" + url + "'"
        if transform:
            result = transform(tree, **{'url': purl})
            return str(result)
        else:
            return None

    def fetch_encoding(self, data):
        '''从原网页html中分析网页的encoding
        '''
        # pattern = re.compile('content=\"[\w/]+;\bcharset=(\w+)\"')
        encode = None
        pattern = re.compile('content=\"[\w/]+;\W+charset=(.*?)\"')
        m = pattern.search(data)
        if m:
            encode = m.group(1).strip()

        if encode is None:
            pattern = re.compile('<meta.*charset=\"(.*)\"')
            m = pattern.search(data)
            if m:
                encode = m.group(1).strip()

        if encode is None:
            pattern = re.compile('<meta.*charset=(.*)')
            m = pattern.search(data)
            if m:
                encode = m.group(1).strip()

        if encode == 'gb2312' or encode == 'gbk':
            encode = 'gb18030'

        if encode is None:
            encode = 'gb18030'

        return encode


def main():
    tplpath = sys.argv[1]
    st = SimpleTemplate('data/base/page_tpl')
    st.loadTpl(tplpath)

if __name__ == '__main__':
    main()
