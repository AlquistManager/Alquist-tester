import json
import sys

import requests

if __name__ == '__main__':
    print("I am tester")


def send_post(url, text, context, node, session):
    payload = {'text': text, 'context': context, 'node': node, 'session': session}
    headers = {'content-type': 'application/json'}
    requests.post(url, data=json.dumps(payload), headers=headers)
