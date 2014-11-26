#!/usr/bin/env python

import yaml
import sys
from lxml import etree
from collections import defaultdict


def usage():
    print >> sys.stderr, 'usage: python yaml2xml.py <xml_file>'


def addElement(data, parent):
    if type(data) is dict:
        for k in data:
            node = etree.SubElement(parent, k)
            addElement(data[k], node)
    elif type(data) is list:
        for e in data:
            addElement(e, parent)
    elif type(data) is str:
        parent.text = data


def element2dict(t):
    d = {}
    children = list(t)
    if children:
        dd = []
        for dc in map(element2dict, children):
            for k, v in dc.iteritems():
                dd.append({k: v})
        d = {t.tag: dd}
    if t.text:
        text = t.text.strip()
        if text:
            d[t.tag] = text
    return d


def xml2dict(tree):
    datadict = element2dict(tree.getroot())
    return datadict


def loadXmlData(fp):
    tree = etree.parse(fp)
    return tree


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    xmlfile = sys.argv[1]
    with open(xmlfile, 'r') as fp:
        tree = loadXmlData(fp)
        data = xml2dict(tree)
        print yaml.dump(data, default_flow_style=False)


if __name__ == '__main__':
    main()
