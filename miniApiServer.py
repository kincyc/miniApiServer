#!/usr/bin/python

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import random
import os
import re
import json
import string

PORT_NUMBER = 8080

# we open a text file and convert and split it into lines
lines = open('/usr/share/doc/vmware-tools/open_source_licenses.txt').read().splitlines()

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
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.end_headers()
		
		# build a json response out of the words
		myJsonResponse = dict()
		for x in range(0,10):
			element =random.choice(words)
			data = ""
			for x in range(0,random.randint(0,20)):	
				data = random.choice(words) + " " + data
		
			myJsonResponse[element] = data.strip()

		myJsonResponse['headers'] = {}
		for k in self.headers:
			myJsonResponse['headers'][k] =  self.headers[k]
		
		print(myJsonResponse)
		
		# Send the html message
		self.wfile.write(json.dumps(myJsonResponse))
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
