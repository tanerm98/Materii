#!/usr/bin/env python3

import requests

POST = requests.post
GET = requests.get

SESSION = requests.Session()
POST_SESSION = SESSION.post
GET_SESSION = SESSION.get


def print_response(response_dict):
    for element in response_dict:
        print("{}: {}".format(element, response_dict[element]))

def ex1():
    URL = "https://sprc.dfilip.xyz/lab1/task1/check"
    HEADERS = {"secret2": "SPRCisBest"}
    PARAMS = {"nume": "Mustafa Taner", "grupa": "341C1"}
    DATA = {"secret": "SPRCisNice"}

    req_check = POST(url=URL, data=DATA, params=PARAMS, headers=HEADERS)

    response = {
        "CHECK response code": req_check,
        "CHECK response text": req_check.text
    }
    print_response(response)

def ex2():
    URL = "https://sprc.dfilip.xyz/lab1/task2"
    DATA = {"username" : "sprc", "password" : "admin", "nume" : "Mustafa Taner"}

    req_check = POST(url=URL, json=DATA)

    response = {
        "CHECK response code": req_check,
        "CHECK response text": req_check.text
    }
    print_response(response)

def ex3():
    # login
    URL = "https://sprc.dfilip.xyz/lab1/task3/login"
    DATA = {"username": "sprc", "password": "admin", "nume": "Mustafa Taner"}

    req_check = POST_SESSION(url=URL, json=DATA)

    response = {
        "CHECK response code": req_check,
        "CHECK response text": req_check.text
    }
    print_response(response)

    # check
    URL = "https://sprc.dfilip.xyz/lab1/task3/check"

    req_check = GET_SESSION(url=URL, json=DATA)

    response = {
        "CHECK response code": req_check,
        "CHECK response text": req_check.text
    }
    print_response(response)

def main():
    ex1()
    ex2()
    ex3()

if __name__ is main():
    main()
