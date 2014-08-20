#!/usr/bin/env python
# encoding=utf-8

import sys

def readfile(filepath):
	content_arr = []
	fp = open(filepath, 'r')
	while True:
		line = fp.readline()
		if not line:
			break
		content_arr.append(line.strip())
	fp.close()
	return content_arr

def maketable(content_arr):
	"""Convert content to table.

	The first line indicate the title of table"""
	content = ""
	title = content_arr[0]
	content_arr = content_arr[1:]
	content += "<b>" + title + "</b><br/>\n"
	content += "<table cellpadding=0 cellspacing=0 border=1>\n"

	i = 0
	for line in content_arr:
		col = line.strip().split('\t')
		#第一行，表头
		if i == 0:
			content += "<tr bgcolor=#eeeeee>\n"
			for content_str in col:
				content += "<td width=100><b>" + content_str +"</b></td>\n";
			content += "</tr>"
			i = i + 1
			continue
		else:
			content += "<tr>\n"
			for content_str in col:
				content += "<td align=left>" + content_str + "</td>\n"
			content += "</tr>\n"
	content += "</table><p/>\n"
	return content

def makeplain(content_arr):
	"""Convert a plain text to html, with <p> seg.
	"""
	content = ""
	content += "<p>\n"
	for line in content_arr:
		content += line
		content += "</p>\n"
	content += "<p/>\n"
	return content

def formathtml(filepath):
	"""Format a file to html form:

	The first line of this file indicate the type:
		'table' or 'plain'
	"""
	content_arr = readfile(filepath)
	if not content_arr:
		return ""

	filetype = ""
	html = ""
	if len(content_arr) > 0:
		filetype = content_arr[0]

	if filetype == "table":
		html += maketable(content_arr[1:])
	elif filetype == "plain":
		html += makeplain(content_arr[1:])

	return html



if __name__ == "__main__":
	if len(sys.argv) < 2:
		print >> sys.stderr, "need source file path"
		sys.exit(1)

	body = "<html>\n"
	body += "<head>\n<style type=\"text/css\">\n"
	body += "body {font-size: 14px; MARGIN: auto; FONT-FAMILY: arial}\n"
	body += "table {border-collapse:collapse; margin:0px, 2px; padding:2px; font-size:12px; }\n</style>\n</head>\n<body>\n"

	for i in range(1, len(sys.argv)):
		body += formathtml(sys.argv[i])

	body += "<hr size=1><br>\n";
	body += "</body>\n</html>\n";

	print body
