#!/usr/bin/env python
# -*- coding: utf-8

import BaseHTTPServer
import codecs
import markdown
import os.path
import SimpleHTTPServer
import sys

class H(SimpleHTTPServer.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        print self.path
        if self.path.endswith('.md'):
            fs_path = self.path[1:]
            input_file = codecs.open(fs_path, mode="r", encoding="utf8")
            mdtext = input_file.read()
            input_file.close()
            
            html = markdown.Markdown().convert(mdtext)
            self.end_headers()
            self.wfile.write("""<html><head>
                <link href="/scripts/github-md2html_bundle_github.css" media="screen"  rel="stylesheet" type="text/css" />
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                </head><body class="logged_in page-blob  linux env-production">
                <div class="subnavd" id="main"> 
                <div class="site"> 
                <div class="slider"> 
                <div class="frames"> 
                <div class="frame frame-center"> 
                <div id="files"> 
                <div class="file"> 
                <div class="blob instapaper_body"> 
                <div class="wikistyle"> 
            """)
            
            html_string = html.encode('utf-8')
            html_string = str(html_string)
            self.wfile.write(html_string)
            
            self.wfile.write("""
                </div>
                </div>
                </div>
                </div>
                </div>
                </div>
                </div>
                </div>
                </div>
                </body></html>
            """)
        elif self.path.startswith('/hgdeoro/py-arduino-proxy/raw/'):
            # /hgdeoro/py-arduino-proxy/raw/<ANY_BRANCH>/
            splitted = self.path.split('/')
            # '' $ hgdeoro $ py-arduino-proxy $ raw $ <ANY_BRANCH> $ many $ paths $ elements
            splitted = splitted[5:]
            self.path = '/' + '/'.join(splitted)
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

def main():
    if not os.path.exists('scripts/github-md2html_bundle_github.css'):
        print "ERROR: Couldn't find 'scripts/github-md2html_bundle_github.css'."
        print "Maybe you aren't running this scripts from the base directory of the project..."
        sys.exit(1)
    
    httpd = BaseHTTPServer.HTTPServer(('', 8055), H)
    print "Listeting on http://localhost:8055/"
    httpd.serve_forever()

if __name__ == '__main__':
    main()
