from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
from sentiment_analyzer import getProbAndLabel

class HttpServer_reviewAnalyzer(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'origin, x-csrftoken, content-type, accept')
        self.end_headers()
    
    def do_GET(self):
        self._set_headers()
        if self.path == '/':
            with open('data.json') as f:
                data = json.load(f)
                self.wfile.write(bytes(json.dumps(data),'utf8'))
        else:
            params = parse_qs(urlparse(self.path).query)
            if params and params['movie']:
                with open('data.json') as f:
                    data = json.load(f)
                    for movie in data['reviewList']:
                        if int(movie['id']) == int(params['movie'][0]):
                            print (movie)
                            self.wfile.write(bytes(json.dumps(movie),'utf8'))
                            return        
        return
    
    def do_POST(self):
        print('do post')
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print(post_data)
        review = json.loads(post_data)['review']
        print(review)
        probAndLabel = getProbAndLabel(review)
        print (probAndLabel)
        self._set_headers()
        self.wfile.write(bytes(json.dumps(probAndLabel),'utf8'))
        return

        # getProbAndLable()



def run(server_class=HTTPServer, handler_class=HttpServer_reviewAnalyzer, port=8081):
    print ('starting server...')
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()

run()