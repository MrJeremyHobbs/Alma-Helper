#!/usr/bin/python3
from alma import http
from alma import errors
from lxml import objectify
import xml.etree.ElementTree as ET
import requests
import xmltodict
import sys

class ManageMembers():
    def __init__(self, set_id="", id_type="", op="", payload_xml="", apikey=""):
        self.ManageMembers = ManageMembers
        self.headers = {'Content-Type': 'application/xml'}
        self.r = requests.post(f'https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/sets/{set_id}?id_type={id_type}&op={op}&apikey={apikey}', data=payload_xml,headers=self.headers)
        self.xml = self.r.text

        # check for invalid api key
        if self.xml == "Invalid API Key":
            self.successful = False
            self.error_msg = "Invalid API Key."
            return

        # create dict and check for errors
        self.dict = xmltodict.parse(self.xml)

        if self.r.status_code != 200:
            self.successful = False
            self.error_msg = self.dict['web_service_result']['errorList']['error'].get('errorMessage')
        else:
            self.successful = True


class RetrieveSetMembers():
    def __init__(self, set_id="", limit="", offset="", apikey=""):
        self.RetrieveSetMembers = RetrieveSetMembers
        
        self.set_id = set_id
        self.limit = limit
        self.offset = offset
        self.apikey = apikey

        self.members = []
        self.all_members = {}

        self.url = f'https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/sets/{self.set_id}/members?limit={str(self.limit)}&offset={str(offset)}&apikey={self.apikey}'
        self.r = requests.get(self.url)
        self.xml = self.r.text

        # check for invalid api key
        if self.xml == "Invalid API Key":
            self.successful = False
            self.error_msg = "Invalid API Key."
            return

        # create dict and check for errors
        self.dict = xmltodict.parse(self.xml)

        if self.r.status_code != 200:
            self.successful = False
            self.error_msg = self.dict['web_service_result']['errorList']['error'].get('errorMessage')
            self.total_members = "0"
        else:
            self.successful = True
            self.total_members = self.dict['members']['@total_record_count']
            self.members.append(self.dict)

            self.get_all()

    # get all members of set in a dictionary
    def get_all(self):
        offset = int(self.total_members)

        _all_members = []
        self.barcodes = []

        while len(_all_members) < int(self.total_members): 
            offset -= 100

            if offset < 0:
                offset = 0

            print(f"Retrieving records ({offset}-{offset+100} of {self.total_members}) ...")

            url = f'https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/sets/{self.set_id}/members?limit={str(self.limit)}&offset={str(offset)}&apikey={self.apikey}'
            r = requests.get(url)

            xml = r.text
            member_dict = xmltodict.parse(xml)

            # create list of members and barcodes
            for d in member_dict['members']['member']:
                _all_members.append(d)
                self.barcodes.append(d['description'])

        # de-dupe barcodes
        print(f"Removing duplicate barcodes ...")
        self.barcodes = set(self.barcodes)

        # set up dictionary of members
        self.all_members = {}
        self.all_members['@total_record_count'] = len(_all_members)
        self.all_members['members'] = _all_members