#!/usr/bin/env python
#encoding=utf8

import sys

if __name__ == '__main__':
	ori_docid = sys.argv[1]
	ori_docid = ori_docid.replace('-', '')
	docid = ori_docid[::-1]
	d = ''
	for i in range(0, len(docid), 2):
		d += docid[i:i+2][::-1]
	print d
