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


# parse and load yaml
def parse():
    with open("test.yaml", 'r') as stream:
        try:
            loaded_yaml = yaml.load(stream)
            return loaded_yaml
        except yaml.YAMLError as exc:
            print(exc)


# sends post to Alquist and return its response
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
            print(text_to_send)
            # take transition, if presented
            if 'transition' in randomly_selected:
                i = randomly_selected["transition"] - 1
            response = send_post(url, text_to_send, context, state, session)
            save_info_from_response(response)
            print(response.json()["text"])
        # if it is Alquist's turn
        elif loaded_yaml[i]["agent"] == "alquist":
            # check last response
            if not (test_response_test(response_text, loaded_yaml[i]["text"])):
                # we founded mistake
                print(
                    'There is mistake in the state ' + state + '. Response text "' + response_text + '" was unexpected.')
                return False
        i += 1
    return True


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


def test_response_test(response_text, text_from_yaml):
    if isinstance(text_from_yaml, list):
        for text in text_from_yaml:
            if response_text == text:
                return True
        return False
    else:
        return response_text == text_from_yaml


if __name__ == '__main__':
    # load yaml
    loaded_yaml = parse()
    # test the dialogue
    result = execute_test(loaded_yaml)
    if result == True:
        print("Dialogue ended successfully")
