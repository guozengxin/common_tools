#!/usr/bin/env python
#coding=utf-8

import pdb
import sys
import urllib2
import time
import logging
from urllib2 import HTTPError, URLError
from gzipSupport import ContentEncodingProcessor

logging.basicConfig(level = logging.INFO, format = '[%(asctime)s %(levelname)s] %(message)s', datefmt='%Y%m%d %H:%M:%S')

class SimpleSpider:
	'''simple spider
	'''
	def __init__(self):
		self.__headers = {}
		self.__interval = 1
		self.__fetchlist = []
		self.__parse = None
		self.__args = None


	def setseeds(self, seeds):
		self.__fetchlist.extend(seeds)

	def addheader(self, header):
		if type(header) == str:
			pos = header.find(':')
			if pos > 0:
				key = header[:pos].strip()
				value = header[pos+1:].strip()
				self.__headers[key] = value
			else:
				return False
		elif type(header) == dict:
			self.__headers.update(header)

	def setinterval(self, interval):
		self.__interval = interval

	def setargs(self, args):
		'''设置参数，这些参数将传入parse函数
		'''
		self.__args = args

	def setparse(self, parse):
		self.__parse = parse

	def start(self):
		'''start fetcher
		'''
		while True:
			if len(self.__fetchlist) == 0:
				break
			url = self.__fetchlist.pop()
			response = self.http_get_response(url)
			if response is not None:
				logging.info('fetch-success url %s' % (url))
				urls = self.__parse(response, args=self.__args)
				for url in urls:
					if url not in self.__fetchlist:
						self.__fetchlist.append(url)
			else:
				logging.info('fetch-fail url %s' % (url))
			time.sleep(self.__interval)

	def http_get_response(self, url, referer = None):
		'''get html response from web'''
		response = None
		encoding_support = ContentEncodingProcessor
		opener = urllib2.build_opener(encoding_support, urllib2.HTTPHandler)
		try:
			headers = self.__headers
			if referer is not None:
				headers['Referer'] = referer
			request = urllib2.Request(url, headers = headers)
			response = opener.open(request, timeout=20)
		except HTTPError, e:
			sys.stderr.write(str(e) + '\n')
		except URLError, e:
			sys.stderr.write(str(e) + '\n')
		except IOError, e:
			sys.stderr.write(str(e) + '\n')
		return response

	def http_get(self, url, referer = None):
		'''get html file from web'''
		data = None
		response = http_get_response(url, referer)
		if response:
			try:
				data = response.read()
			except:
				sys.stderr.write('unnkown error in http_get')
		return data
