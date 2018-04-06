# (c) 2018 Victor Mireles for Semantic Web Company GmbH, Vienna, Austria.
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import os
from urllib.parse import urlparse
import json

storagePath = "./storage/"

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        qs = {}
        path = self.path
        print("path", path)
        if path=="/index":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'INDEX\n\n')
        else:


            alldata = dict()
            files=os.listdir(storagePath)
            for f in files:
                a = open(storagePath + f, "rt")
                for line in a:
                    ls = line.strip().split("\t")
                    time = ls[0]
                    if not time in alldata.keys():
                        alldata[time] = dict()
                    alldata[time][ls[1]] = int(ls[2])

            resp=(json.dumps(alldata, sort_keys=True))

            self.send_response(200)
            self.end_headers()
            self.wfile.write(resp.encode("utf8"))


    def do_POST(self):
        content_length = int(self.headers.get('Content-Length'))
        body = self.rfile.read(content_length).decode("utf8")
        print(body)
        filename = storagePath+str(uuid.uuid4())+".file"
        fo = open(filename, 'wt')
        fo.write(body)
        fo.close()


        self.send_response(200)
        self.end_headers()
        response = BytesIO()

        response.write(b'\n POST \n')

if 'PRODUCER_LISTENING_PORT' in os.environ:
    port = int(os.environ['PRODUCER_LISTENING_PORT'])
else:
    port = 8765
print("Server started on port", port)
httpd = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
httpd.serve_forever()
