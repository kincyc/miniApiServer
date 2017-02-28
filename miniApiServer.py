#!/usr/bin/python

# python 2.6 for legacy software compat reasons

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import random
import os
import re
import json
import string
import StringIO
import gzip

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p", "--port", dest="port_number", help="which port to listen (default: 8080)", metavar="PORT_NUMBER", default=8080, type="int")
parser.add_option("--noheaders", dest="noheaders", action="store_true", default=False, help="don't output http request headers in response json")
parser.add_option("--notext", dest="notext", action="store_true", default=False, help="don't output random text in response json")
parser.add_option("-s", "--silent", dest="silent", action="store_true", help="runs in silent mode", default=False)

(options, args) = parser.parse_args()

PORT_NUMBER = options.port_number

if not options.silent:
	print(options.notext, options.noheaders)

if not options.notext:
	# we open a text file and convert and split it into lines	
	lines = open('/usr/share/doc/python27-simplejson-3.6.5/LICENSE.txt').read().splitlines()
	words = []
	# compile regex for later
	pattern = re.compile('[\W_]+')
	# we then loop through the lines and split them into words
	for l in lines:
		# split each line into words
		for w in l.split():
			# remove all non-alphanumeric characters, capword them then append to array
			words.append(re.sub(pattern, '', string.capwords(w)))
	# this filters out all the empty words in the array
	words = filter(None, words)

#This class will handles any incoming request, regardless of path submitted 
class myHandler(BaseHTTPRequestHandler):
	# protocol_version = 'HTTP/1.1'
	
	def gzipencode(self, content):
		out = StringIO.StringIO()
		f = gzip.GzipFile(fileobj=out, mode='w', compresslevel=5)
		f.write(content)
		f.close()
		return out.getvalue()
	
	#Handler for the GET requests
	def do_GET(self):

		myJsonResponse = dict()

		# build a json response out of the words		
		if not options.notext:
			# if headers are turned off
			for x in range(0,10):
				element =random.choice(words)
				data = ""
				for x in range(0,random.randint(25000,25001)):	
					data = random.choice(words) + " " + data
			
				myJsonResponse[element] = data.strip()
			
		myTextResponse = self.gzipencode(json.dumps(myJsonResponse))

		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.send_header('Content-length',str(len(str(myTextResponse))))
		self.send_header("Content-Encoding", "gzip")
		if not options.noheaders:
		# if random text is turned off
			myJsonResponse['headers'] = {}
			for k in self.headers:
				myJsonResponse['headers'][k] =  self.headers[k]

		self.end_headers()
		
		if not options.silent:
			print(myTextResponse)
		
		# Send the html message
		self.wfile.write(myTextResponse)

	if options.silent:
		# redefines log_message to silence output
		def log_message(self, format, *args):
			return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	if not options.silent:
		print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()