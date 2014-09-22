#!/usr/bin/env python
# encoding=gb18030

import sys
import getopt
import htmlfetcher
from htmlparser import HtmlXPathParser
import colorprint

outputEncoding = 'gb18030'


def usage():
    print '''iciba.py [--daemon|-h|word]'''


def parseOpt(args):
    config = {'daemon': False}
    try:
        opts, args = getopt.getopt(args, 'hd', ['help', 'daemon'])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-d', '--daemon'):
            config['daemon'] = True
        else:
            assert False, "unhandled option"
    return config, args


def getFirstText(tree, encoding=outputEncoding):
    try:
        if type(tree) is list:
            t = tree[0].text
        else:
            t = tree.text
        if t is not None:
            return t.encode(encoding)
        else:
            return ''
    except IndexError:
        return ''


def printResult(word, result):
    tColor = 'green'
    vColor = 'cyan'
    print word
    if len(result['prons']) > 0:
        print '发音'
        for t, v in result['prons']:
            colorprint.colorPrint('  %s' % t, tColor, attr=1)
            colorprint.colorPrint('%s' % v, vColor, attr=4)
        print
    if len(result['groupPos']) > 0:
        print '释义'
        for t, v in result['groupPos']:
            colorprint.colorPrint('  %s' % t, tColor, attr=1)
            colorprint.colorPrint(v, vColor, attr=4)
            print
    if len(result['netContent']) > 0:
        print '网络'
        colorprint.colorPrint('  %s' % result['netContent'], vColor, attr=1)


def parseHtml(data):
    result = {'prons': [], 'groupPos': [], 'netContent': []}
    parser = HtmlXPathParser()
    parser.feed(data, encode='utf-8')
    dictMainDiv = parser.etlist_xpath('//div[@id="dict_main"]')[0]
    tmpParser = HtmlXPathParser()
    tmpParser.feed_etree(dictMainDiv)
    pronsList = tmpParser.etlist_xpath('.//span[@class="fl"]')
    for prons in pronsList:
        pronsType = getFirstText(prons).strip('\r\n\t')
        pronsStr = getFirstText(prons.xpath('.//strong[@lang]')).strip()
        if pronsStr == '':
            pronsStr = getFirstText(prons.xpath('.//strong'))
        else:
            pronsStr = '[' + pronsStr + ']'
        if len(pronsType) == 0 and len(pronsStr) == 0:
            continue
        result['prons'].append([pronsType, pronsStr])
    groupPosList = tmpParser.etlist_xpath('.//div[@class="group_pos"]/p')
    for groupPos in groupPosList:
        posType = getFirstText(groupPos.xpath('.//strong'))
        if posType is None:
            continue
        posContent = ''
        contentList = groupPos.xpath('.//label/text()')
        for c in contentList:
            posContent += c.encode(outputEncoding)
        if len(posType) == 0 and len(posContent) == 0:
            continue
        result['groupPos'].append([posType, posContent])
    netContentList = tmpParser.etlist_xpath('.//div[@class="net_paraphrase"]/ul/li')
    netContent = ''
    for nc in netContentList:
        netContent += nc.text.encode('gb18030').strip()
    result['netContent'] = netContent

    return result


def translate(word):
    url = 'http://www.iciba.com/' + word.decode('gbk').encode('utf8')
    home = 'http://www.iciba.com/'
    data = htmlfetcher.http_get(url, referer=home)
    if data is None:
        print >> sys.stderr, 'Fetch result from iciba.com failed!'
    else:
        result = parseHtml(data)
        printResult(word, result)


def main():
    config, args = parseOpt(sys.argv[1:])
    if config['daemon']:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            word = line.strip()
            translate(word)
            sys.stdout.flush()
            sys.stderr.flush()
    else:
        if len(args) == 0:
            usage()
            sys.exit()
        word = args[0]
        translate(word)


if __name__ == '__main__':
    main()
