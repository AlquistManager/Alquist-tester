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


# tests dialogue
def execute_test(loaded_yaml):
    i = 0
    # while we are not at the end of yaml
    while i < len(loaded_yaml):
        # if it is user's turn
        if loaded_yaml[i]["agent"] == "user":
            # select one input at random
            randomly_selected = select_random_input(loaded_yaml[i]["input"])
            # take text and transition
            text_to_send = randomly_selected["text"]
            # take transition, if presented
            if hasattr(randomly_selected, "transition"):
                i = randomly_selected["transition"] - 1
            response = send_post(url, text_to_send, context, state, session)
            save_info_from_response(response)
            print(response.json())
        # if it is Alquist's turn
        elif loaded_yaml[i]["agent"] == "alquist":
            if not (loaded_yaml[i]["text"] == response_text):
                print("Mistake in the node " + state)
                break
        i += 1


# save context, state, session and response from Alquist's request
def save_info_from_response(response):
    global context
    global state
    global session
    global response_text
    context = response.json()['context']
    state = response.json()['state']
    session = response.json()['session']
    response_text = response.json()['text']


# select one input at random
def select_random_input(inputs):
    index = randint(0, len(inputs) - 1)
    return inputs[index]


if __name__ == '__main__':
    # load yaml
    loaded_yaml = parse()
    # test the dialogue
    execute_test(loaded_yaml)
