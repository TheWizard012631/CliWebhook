# CLI Webhook Receiver

A very small and simple CLI Webhook receiver for developpers and pentesters.

This project can be used to open a webhook receiver in a cli-only environment.

To run the receiver just run:

```
$ python cliwebhook.py
```

This will run the receiver on all interfaces on port 3030 by default.

### Options

Listening Port (default: 3030)

```
$ python cliwebhook.py -p 3031
# OR
$ python cliwebhook.py --port 3031
```

Listening Address (default: 0.0.0.0)

```
$ python cliwebhook.py -a 127.0.0.1
# OR
$ python cliwebhook.py --address 127.0.0.1
```

Response Content (default: This is a webhook receiver)

```
$ python cliwebhook.py -r '{"status": "Not Found"}'
# OR
$ python cliwebhook.py --response '{"status": "Not Found"}'
```

Response Code (default: 200)

```
$ python cliwebhook.py -c 404
# OR
$ python cliwebhook.py --response-code 404
```

Response Type (default: text/plain)

```
$ python cliwebhook.py -t 'application/json'
# OR
$ python cliwebhook.py --response-type 'application/json'
```
