# CLI Webhook Receiver

A very small and simple CLI Webhook receiver for developpers and pentesters.

This project can be used to open a webhook receiver in a cli-only environment.

To run the receiver just run:

```
$ python3 cliwebhook.py
```

This will run the receiver on all interfaces on port 3030 by default.

### Options

Listening Port (default: 3030)

```
$ python3 cliwebhook.py -p 3031
# OR
$ python3 cliwebhook.py --port 3031
```

Listening Address (default: 0.0.0.0)

```
$ python3 cliwebhook.py -a 127.0.0.1
# OR
$ python3 cliwebhook.py --address 127.0.0.1
```

Response Content (default: This is a webhook receiver)

```
$ python3 cliwebhook.py -r '{"status": "Not Found"}'
# OR
$ python3 cliwebhook.py --response '{"status": "Not Found"}'
```

Response Code (default: 200)

```
$ python3 cliwebhook.py -c 404
# OR
$ python3 cliwebhook.py --response-code 404
```

Response Type (default: text/plain)

```
$ python3 cliwebhook.py -t 'application/json'
# OR
$ python3 cliwebhook.py --response-type 'application/json'
```
