from socket import inet_aton
from datetime import datetime
from argparse import ArgumentParser
from http.server import BaseHTTPRequestHandler, HTTPServer

def die(msg=None):
    if msg!=None:print(msg)
    parser.print_help()
    exit()

parser = ArgumentParser(
    prog='CliWebhook.py',
    description='Small and simple CLI webhook receiver for developpers and pentesters',
)

parser.add_argument('-p', '--port', type=int, help='Listening port', default=3030, required=False)
parser.add_argument('-a', '--address', type=str, help='Listening address', default='0.0.0.0', required=False)
parser.add_argument('-r', '--response', type=str, help='Response content', default='This is a webhook receiver', required=False)
parser.add_argument('-c', '--response-code', type=int, help='Response code', default=200, required=False)
parser.add_argument('-t', '--response-type', type=str, help='Response type', default='text/plain', required=False)
args = parser.parse_args()

PORT = args.port
ADDRESS = args.address
RESPONSE = args.response.encode('utf-8')
RESPONSE_CODE = args.response_code
RESPONSE_TYPE = args.response_type

try:
    inet_aton(ADDRESS)
except:
    die(f"Error: argument address '{ADDRESS}' is not a valid ip address")

if (PORT < 1 or PORT > 65535):
    die(f"Error: argument port '{PORT}' is not a valid port")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        print(f'{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")} -> New {self.command} request from {self.client_address[0]}:{self.client_address[1]} '.ljust(88, '-'))
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
            self.end_headers()
            self.wfile.write(RESPONSE)

    do_PUT = do_GET
    do_POST = do_GET
    do_HEAD = do_GET
    do_PATCH = do_GET
    do_TRACE = do_GET
    do_DELETE = do_GET
    do_OPTIONS = do_GET
    do_CONNECT = do_GET

httpd = HTTPServer((ADDRESS, PORT), Handler)
print('Welcome to your CLI HTTP webhook receiver')
print(f'Listening on {ADDRESS}:{PORT}')

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print('Exiting ...')
    httpd.shutdown()
