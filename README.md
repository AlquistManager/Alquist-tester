# Alquist tester
Testing utility for Alquist dialogue manager https://github.com/AlquistManager/alquist
Alquist tester tests dialogue, if it works as you expect. Multiple tests are run at once,
and each test randomly select one possible branch of dialogue. This testing utility can be
used as stress test, if you use high number of tests at once.

## Installation
Install Python 3.
Install PyYaml
    
    pip install PyYaml

Alquist tester gets three input parameters:

- ``Alquist's URL`` It is Alquist's URL, where tested dialogue is running.
- ``Test file`` Yaml test file, where is described functionality of dialogue.
- ``Number of tests`` Number of test, which will be performed.

    py -3 http://127.0.0.1:5000/ tests\test.yaml 10

## Creating test file
Example test file is in ``tests\test.yaml``. It is test for demo dialogue https://github.com/AlquistManager/alquist/tree/master/yaml/demo.
The test files contains dialogue nodes. Dialogue node is one response of Alquist or one input of user. Dialogue nodes are named
by numbers starting by zero. Dialogue node has properties: 

- ``agent``
- ``output``\\``input``
- ``transition``

### Agent property
Agent property has two possible values: 

- ``alquist`` if dialogue node represents Alquist's output.
- ``user`` if dialogue node represents user's input.

### Output\input property
Agent property affect if you will use ``Output`` or ``Input`` property in the dialogue node. Use ``Output`` property
for ``alquist`` agent property and ``input`` for ``user`` agent property. 

#### Output property
Contains list of possible Alquist's outputs. If none of outputs from yaml equals to Alquist's output, the test ends unsuccessfully.

#### Input property
Contains list of object representing possible inputs. Input object contains two properties, ``text`` and ``transition``.
Text property contains input, which will be send to Alquist and transition describes, which node is next.

    input:    #List of possible inputs
        - text: "Yes"   #Input
          transition: 2 #Transition to next node, if this branch is selected
        - text: "No"
          transition: 6

### Transition property
Transition property is used only in the nodes with ``agent: Alquist``. It describes, which node is next. You can also insert
``return`` value. This means, that test will end in this dialogue node. If the transition field is missing, the node with next
number will be used.

## Example test file

    0:  #Dialogue number starting at zero
      agent: "alquist"  #Alqusit output node
      output:   #List of possible Alquist outputs
        - "Hi, can I ask you a question?"
    1:  #Next dialogue number
      agent: "user" #User input node
      input:    #List of possible inputs
        - text: "Yes"   #Input
          transition: 2 #Transition to next node, if this branch is selected
        - text: "No"
          transition: 6
        - text: "bla-bla-bla"
          transition: 7
    2:
      agent: "alquist"
      output:
        - "What is your favourite color?"
    3:
      agent: "user"
      input:
        - text: "Blue"
          transition: 4
        - text: "Black"
          transition: 4
        - text: "Pink"
          transition: 4
        - text: "I don't know"
          transition: 5
        - text: "I dwdwdwd'wdwwtdknwwodwd"
          transition: 5
    4:
      agent: "alquist"
      output:
        - "Wow, {{blue, black, Pink}}, really? That is super cool." #Output with multiple possibilities in the curly brackets
      transition: "return"  #Return in transition ends test
    5:
      agent: "alquist"
      output:
        - "I don't think that is a color. Try another one?"
      transition: 3
    6:
      agent: "alquist"
      output:
        - "OK, bye"
        - "I see, it was nice talking to you anyway"
        - "Oh, that is a shame, bye then"
      transition: "return"
    7:
      agent: "alquist"
      output:
        - "Sorry, I don't understand, yes or no?"
      transition: 1

## Logging
Logs are created for every test in the folder ``logs``.
