#!/usr/bin/env python
# encoding=utf8

import sys
from urlparse import urlparse

tldFile = '/search/guozengxin/tools/python/tld.dat'


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


@singleton
class Url(object):

    def __init__(self):
        self.tld = {}
        tldFp = open(tldFile, 'r')
        for line in tldFp:
            self.tld[line.strip().lower()] = 1
        tldFp.close()

    def getHost(self, url):
        urlResult = urlparse(url)
        return urlResult.netloc

    def getDomain(self, url):
        host = self.getHost(url)
        if host is None:
            return None
        parts = host.split('.')
        if len(parts) < 2:
            return None
        domain = None
        if parts[-2] in self.tld:
            domain = '.'.join(parts[-3:])
        else:
            domain = '.'.join(parts[-2:])
        return domain


def usage(name):
    print '''
python %s [gethost|getdomain] < urlFile
    ''' % (name)


def main():
    if len(sys.argv) == 1:
        usage(sys.argv[0])
        sys.exit(1)
    flag = sys.argv[1]
    if flag == 'gethost':
        urlObj = Url()
        for line in sys.stdin:
            print urlObj.getHost(line.strip())
    elif flag == 'getdomain':
        urlObj = Url()
        for line in sys.stdin:
            print urlObj.getDomain(line.strip())
    else:
        usage(sys.argv[0])
        sys.exit(1)

if __name__ == '__main__':
    main()
    # url = 'http://www.baidu.com.cn/abc'
    # print Url().getDomain(url)
