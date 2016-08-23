import json
import sys

import requests
import yaml

from random import randint

url = sys.argv[1]
context = {}
state = "init"
session = ""
response_text = ""


def parse():
    with open("test.yaml", 'r') as stream:
        try:
            loaded_yaml = yaml.load(stream)
            return loaded_yaml
        except yaml.YAMLError as exc:
            print(exc)


def send_post(url, text, context, state, session):
    payload = {'text': text, 'context': context, 'state': state, 'session': session}
    headers = {'content-type': 'application/json'}
    return requests.post(url, data=json.dumps(payload), headers=headers)


def execute_test(loaded_yaml):
    i = 0
    while i < len(loaded_yaml):
        if loaded_yaml[i]["agent"] == "user":
            if isinstance(loaded_yaml[i]["input"], list):
                randomly_selected = select_random_input(loaded_yaml[i]["input"])
                text_to_send = randomly_selected["text"]
                i = randomly_selected["transition"] - 1
            else:
                text_to_send = loaded_yaml[i]["input"]
            response = send_post(url, text_to_send, context, state, session)
            save_info_from_response(response)
            print(response.json())
        elif loaded_yaml[i]["agent"] == "alquist":
            if not (loaded_yaml[i]["text"] == response_text):
                print("Mistake in the node " + state)
                break
        i += 1


def save_info_from_response(response):
    global context
    global state
    global session
    global response_text
    context = response.json()['context']
    state = response.json()['state']
    session = response.json()['session']
    response_text = response.json()['text']


def select_random_input(inputs):
    index = randint(0, len(inputs) - 1)
    return inputs[index]


if __name__ == '__main__':
    loaded_yaml = parse()
    execute_test(loaded_yaml)
