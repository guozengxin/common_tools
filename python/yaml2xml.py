# encoding=utf-8

import yaml
import sys
from lxml import etree


def usage():
    print >> sys.stderr, 'usage: python yaml2xml.py <yaml_file>'


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


def dict2xml(data):
    xmlNode = None
    if type(data) is not dict:
        print >> sys.stderr, 'must has a root node'
    elif len(data) != 1:
        print >> sys.stderr, 'root node must be just on node'
    else:
        for k in data:
            xmlNode = etree.Element(k)
            addElement(data[k], xmlNode)
            break
    if xmlNode is not None:
        return etree.tostring(xmlNode, pretty_print=True)
    else:
        return None


def loadYamlData(fp):
    data = yaml.load(fp)
    return data


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    yamlfile = sys.argv[1]
    with open(yamlfile, 'r') as fp:
        data = loadYamlData(fp)
        print data
        print dict2xml(data)


if __name__ == '__main__':
    main()
