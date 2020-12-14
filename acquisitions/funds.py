#!/usr/bin/python3
import xmltodict
import sys
from lxml import objectify

# local modules
sys.path.append('..')
from alma import http
from alma import errors


class RetrieveFunds():
    def __init__(self, limit="10", offset="0", q="", library="", apikey=""):
        self.RetrieveFunds = RetrieveFunds
        
        self.base_url = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/acq/funds'
        self.url = f"{self.base_url}?limit={limit}&offset={offset}&apikey={apikey}"
        self.r = http.retrieve_xml(url=self.url, method="get")
        
        # Check for errors in Response object.
        self.errors = errors.Errors(self.r)
        
        # Parse return
        if self.errors.exist == False:
            self.xml = self.r.text
            self.dict = xmltodict.parse(self.xml)
            self.xml_bytes = bytes(self.xml, encoding="utf-8")
            self.object = objectify.fromstring(self.xml_bytes)