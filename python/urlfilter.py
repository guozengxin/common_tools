#!/usr/bin/env python
#encoding = utf8

import re
import sys
import getopt

def split_url(url):
    '''split domain and extra
    '''
    pos = url.find('http://')
    domain = ''
    extra = ''
    if pos >= 0:
        pos2 = url.find('/', pos + 7)
        if pos2 < 0:
            domain = url[pos + 7:]
        else:
            domain = url[pos + 7:pos2]
            extra = url[pos2:]
    else:
        pos2 = url.find('/')
        if pos2 < 0:
            domain = url
        else:
            domain = url[:pos2]
            extra = url[pos2:]

    return (domain, extra)

class UrlFilter:

    def __init__(self, di = {}):
        self._data = di

    def additem(self, domain, prefix, suffix, cate):
        '''add an item to UrlFilter, the key is domain
        '''
        if self._data.has_key(domain):
            dset = self._data[domain]
            exist = False
            for d in dset:
                if d['prefix'] == prefix and d['suffix'] == suffix:
                    exist = True
                    break

            if not exist:
                it = {'prefix':prefix, 'suffix':suffix, 'cate':cate}
                it['re'] = re.compile(suffix)
                dset.append(it)
        else:
            it = {'prefix':prefix, 'suffix':suffix, 'cate':cate}
            it['re'] = re.compile(suffix)
            self._data[domain] = [it]

    def addline(self, line):
        arr = line.strip().split('\t')
        cate = int(arr[1])
        arr = arr[0].split('#')
        if len(arr) == 2:
            (domain, prefix) = split_url(arr[0])
            self.additem(domain, prefix, arr[1], cate)
        elif len(arr) == 1:
            (domain, prefix) = split_url(arr[0])
            self.additem(domain, prefix, '', cate)
        else:
            return False

    def loaduffile(self, filepath):
        fp = open(filepath, 'r')
        lines = fp.readlines()
        if not lines:
            sys.exit(-1)
        for line in lines:
            self.addline(line)


    def lookup(self, url):
        (domain, extra) = split_url(url)
        dl = domain.split('.')
        dl = ['.' + '.'.join(dl[i:]) for i in range(1, len(dl))]
        dl = [domain] + dl
        dset = None
        for d in dl:
            if self._data.has_key(d):
                dset = self._data[d]
                for it in dset:
                    #print extra
                    #print it
                    prefix_len = len(it['prefix'])
                    if not extra.startswith(it['prefix']): continue
                    search_str = extra[prefix_len:]
                    if it['re'].search(search_str):
                        print '\t'.join([str(it['cate']), url])
                        return True
        return False

    def lookup_ret(self, url):
        (domain, extra) = split_url(url)
        dl = domain.split('.')
        dl = ['.' + '.'.join(dl[i:]) for i in range(1, len(dl))]
        dl = [domain] + dl
        dset = None
        for d in dl:
            if self._data.has_key(d):
                dset = self._data[d]
                for it in dset:
                    #print extra
                    #print it
                    prefix_len = len(it['prefix'])
                    if not extra.startswith(it['prefix']): continue
                    search_str = extra[prefix_len:]
                    if it['re'].search(search_str):
                        #print '\t'.join([str(it['cate']), url])
                        return it['cate']
        return None

def usage():
    print '''    -h, --help     show this help
    -l          indicate urlfilter file
    '''


def process_argv(argv):
    '''process the command options
    '''
    try:
        short_args = 'hl:'
        long_args = ['help']
        opts, args = getopt.getopt(argv, short_args, long_args)
    except getopt.GetoptError, e:
        print >> sys.stderr, e
        usage()
        sys.exit(-1)

    conf_item = {}
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif o == '-l':
            conf_item['uffile'] = a

    if not conf_item.has_key('uffile'):
        print >> sys.stderr, 'need uffile'
        usage()
        sys.exit(-1)

    return conf_item

def urlfilter(args):
    conf_item = process_argv(args)
    uf = UrlFilter()
    uffile = conf_item['uffile']
    uf.loaduffile(uffile)

    while True:
        line = sys.stdin.readline()
        if not line:
            break
        uf.lookup(line.strip())

if __name__ == '__main__':
    urlfilter(sys.argv[1:])
