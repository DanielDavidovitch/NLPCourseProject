from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
from sentiment_analyzer import getProbAndLabel, Label

class HttpServer_reviewAnalyzer(BaseHTTPRequestHandler):
    _DB_PATH = 'data.json'

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
            with open(self._DB_PATH) as f:
                data = json.load(f)
                self.wfile.write(bytes(json.dumps(data), 'utf8'))
        else:
            params = parse_qs(urlparse(self.path).query)
            if params and params['movie']:
                with open(self._DB_PATH) as f:
                    data = json.load(f)
                    for movie in data['reviewList']:
                        if int(movie['id']) == int(params['movie'][0]):
                            print (movie)
                            self.wfile.write(bytes(json.dumps(movie), 'utf8'))
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

        # Convert the assurnace level to a rate on scale of 1 to 10
        rate = int(round(probAndLabel['final_prob'] * 10))
        # The rate needs to be iversed if the label is NEGATIVE, so the rate will be lower
        # as the assurnace of negative grows
        if probAndLabel['final_label'] == Label.NEGATIVE.name:
            rate = 10 - rate
        probAndLabel['rate'] = rate

        # Save the review in the JSON
        self._save_review(json.loads(post_data)['id'], review, rate)

        # Send the response to the client
        self._set_headers()
        self.wfile.write(bytes(json.dumps(probAndLabel), 'utf8'))

    def _save_review(self, movie_id, review, rate):
        with open(self._DB_PATH) as f:
            data = json.load(f)

        review_list = data['reviewList']
        # Find the index of the movie with the given ID
        for index in range(len(review_list)):
            if int(review_list[index]['id']) == movie_id:
                break
        else:
            # If the given movie ID wasn't found raise an exception
            raise Exception("Given movie ID {} doesn't exist in the DB".format(movie_id))

        # Insert the review and its rating
        review_list[index]['reviews'].append({'rate': rate, 'review': review})

        # Save to file
        with open(self._DB_PATH, 'w') as f:
            json.dump(data, f)


def run(server_class=HTTPServer, handler_class=HttpServer_reviewAnalyzer, port=8081):
    print ('starting server...')
    server_address = ('localhost', port)
    httpd = server_class(server_address, handler_class)
    print ('Starting httpd...')
    httpd.serve_forever()

run()
