#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import urllib.parse
# Reference: https://docs.python.org/3/library/urllib.parse.html
from urllib.parse import urlparse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        ''' Build request, connect to server and send the GET request '''
        url_string = urlparse(url)
        port = url_string.port
        if port == None:
            port = 80
        host = url_string.hostname
        path = url_string.path
        if len(path) == 0:
            path = '/'
        request = f"GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nConnection: close\r\n\r\n"
        self.connect(host, port)
        self.sendall(request)

        ''' Read incoming data from the request, parse the code and body '''
        incoming_data = self.recvall(self.socket)
        code = int(incoming_data.split()[1])
        body = incoming_data.split('\r\n\r\n')[1]
        self.socket.close()
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        ''' Build request, connect to server and send the POST request '''
        url_string = urlparse(url)
        port = url_string.port
        if port == None:
            port = 80
        host = url_string.hostname
        path = url_string.path
        if len(path) == 0:
            path = '/'
        self.connect(host, port)
        
        # Test for sent data. If None, send POST request without any arguments.
        if args == None:
            body = ""
            content = "0"
        # Test for sent data. If yes, send POST request with arguments.
        else:
            body = urllib.parse.urlencode(args)
            content = str(len(body))

        request = f"POST {path} HTTP/1.1\r\nHost: {host}Content-Type: application/x-www-form-urlencoded\r\nContent-Length: {content}\r\nConnection: close\r\n\r\n{body}\r\n"
        self.sendall(request)

        ''' Read incoming data from the request, parse the code and body '''
        incoming_data = self.recvall(self.socket)
        code = int(incoming_data.split()[1])
        body = incoming_data.split('\r\n\r\n')[1]
        self.socket.close()
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
