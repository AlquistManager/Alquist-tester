import json
import re
import sys
import requests
import yaml

from random import randint

from Tester import Tester

url = sys.argv[1]
context = {}
state = "init"
session = ""
response_text = ""
isUserTurn = True


# parse and load yaml
def parse():
    with open("test.yaml", 'r') as stream:
        try:
            loaded_yaml = yaml.load(stream)
            return loaded_yaml
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == '__main__':
    # load yaml
    loaded_yaml = parse()
    # test the dialogue
    threads = [None] * 10
    i = 0
    for thread in threads:
        thread = Tester(url, loaded_yaml, "Tester" + str(i))
        thread.start()
        i += 1
