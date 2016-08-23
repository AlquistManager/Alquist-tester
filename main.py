import sys
import yaml

from tester import *

url = sys.argv[1]
file = sys.argv[2]
number_of_testers = int(sys.argv[3])
context = {}
state = "init"
session = ""
response_text = ""
isUserTurn = True


# parse and load yaml
def parse():
    with open(file, 'r') as stream:
        try:
            loaded_yaml = yaml.load(stream)
            return loaded_yaml
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == '__main__':
    # load yaml
    loaded_yaml = parse()
    # create threads
    threads = [None] * number_of_testers
    i = 0
    # run each thread
    for thread in threads:
        thread = Tester(url, loaded_yaml, i)
        thread.start()
        i += 1
