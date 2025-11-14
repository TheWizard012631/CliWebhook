from json import loads
from socket import inet_aton
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

def die(msg=None):
    if msg!=None:print(msg)
    parser.print_help()
    exit()

parser = ArgumentParser(
    prog='CliWebhook.py',
    description='Small and simple CLI webhook receiver for developpers and pentesters',
    formatter_class=ArgumentDefaultsHelpFormatter
)

parser.add_argument('-p', '--port', type=int, required=False, help='Listening port', default=3030)
parser.add_argument('-a', '--address', type=str, required=False, help='Listening address', default='0.0.0.0')
parser.add_argument('-r', '--response', type=str, required=False, help='Response content', default='This is a webhook receiver')
parser.add_argument('-c', '--response-code', type=int, required=False, help='Response code', default=200)
parser.add_argument('-t', '--response-type', type=str, required=False, help='Response type', default='text/plain')
parser.add_argument('-e', '--response-headers', type=str, required=False, help='Headers to add to response in json format ex: {"X-Forwarded-For": "localhost"}', default='{}')
args = parser.parse_args()

PORT = args.port
ADDRESS = args.address
RESPONSE = args.response.encode('utf-8')
RESPONSE_CODE = args.response_code
RESPONSE_TYPE = args.response_type

try:
    RESPONSE_HEADERS = loads(args.response_headers)
    if type(RESPONSE_HEADERS) != dict: raise
except:
    die("Error: argument response-headers is not a valid json dictionary")

try:
    inet_aton(ADDRESS)
except:
    die(f"Error: argument address '{ADDRESS}' is not a valid ip address")

if (PORT < 1 or PORT > 65535):
    die(f"Error: argument port '{PORT}' is not a valid port")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass

    def do_GET(self):
        print(f'{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")} -> New {self.command} request from {":".join(map(str,self.client_address))} '.ljust(88, '-'))
        print('v'*88)

        print(f'{self.raw_requestline.decode("utf-8")}', end='')
        print(f'{self.headers.as_string()}', end='')

        length = self.headers.get('Content-Length')
        if (length != None):
            print(self.rfile.read(int(length)).decode('utf-8'))
        print('^'*88)

        if (self.wfile.writable):
            self.send_response(RESPONSE_CODE)
            self.send_header("Content-type", RESPONSE_TYPE)
            for k,v in RESPONSE_HEADERS.items():
                self.send_header(k,v)
            self.end_headers()
            self.wfile.write(RESPONSE)

    def do_OPTIONS(self):
        RESPONSE_HEADERS['Access-Control-Allow-Origin'] = '*'
        RESPONSE_HEADERS['Access-Control-Allow-Methods'] = 'GET,HEAD,POST,PUT,DELETE,GET'
        RESPONSE_HEADERS['Access-Control-Allow-Headers'] = 'authorization, content-type'
        RESPONSE_HEADERS['Access-Control-Max-Age'] = '1800'
        self.do_GET()

    # do_GET = handle
    do_PUT = do_GET
    do_POST = do_GET
    do_HEAD = do_GET
    do_PATCH = do_GET
    do_TRACE = do_GET
    do_DELETE = do_GET
    do_CONNECT = do_GET

httpd = HTTPServer((ADDRESS, PORT), Handler)
print('Welcome to your CLI HTTP webhook receiver')
print(f'Listening on {ADDRESS}:{PORT}')

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print('Exiting ...')
    httpd.shutdown()
