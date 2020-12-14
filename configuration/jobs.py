#!/usr/bin/python3
from alma import http
from alma import errors
from lxml import objectify
import xml.etree.ElementTree as ET
import requests
import xmltodict
import sys

class SubmitJob():
    def __init__(self, op="", job_id="", payload_xml="", apikey=""):
        self.SubmitJob = SubmitJob
        self.headers = {'Content-Type': 'application/xml'}
        self.r = requests.post(f'https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/jobs/{job_id}?op={op}&apikey={apikey}', data=payload_xml, headers=self.headers)
        self.xml = self.r.text

        # check for invalid api key
        if self.xml == "Invalid API Key":
            self.found = False
            self.error_msg = "Invalid API Key."
            return

        # create dict and check for errors
        self.dict = xmltodict.parse(self.xml)

        if self.r.status_code != 200:
            self.found = False
            self.error_msg = self.dict['web_service_result']['errorList']['error'].get('errorMessage')
        else:
            self.found = True

