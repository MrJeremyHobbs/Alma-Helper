#!/usr/bin/python3
import requests

def retrieve_xml(url="", method="get", params=""):
    method = method.lower()
    
    if method == "get":
        r = requests.get(url, params)
        return r

    if method == "post":
        pass

    if method == "put":
        pass

    if method == "delete":
        pass

    if method == "patch":
        pass
    
    else:
        return None