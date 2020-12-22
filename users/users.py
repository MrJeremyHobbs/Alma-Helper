#!/usr/bin/python3
from alma_helper import http
from alma_helper import errors
from lxml import objectify
import xmltodict

# Documentation
# https://developers.exlibrisgroup.com/alma/apis/users/

class GetUserDetails():
    def __init__(self, user_id, user_id_type="all_unique", view="full", expand="none", 
                 source_institution_code= "", apikey=""):
            self.GetUserDetails = GetUserDetails

            self.base_url = f'https://api-na.hosted.exlibrisgroup.com/almaws/v1/users/{user_id}'
            self.url = f'{self.base_url}?user_id_type={user_id_type}&view={view}&expand={expand}&apikey={apikey}'

            self.r = http.retrieve_xml(url=self.url, method="get")
            self.xml = self.r.text

            # Check for errors in Response object.
            self.errors = errors.Errors(self.r)

            # Parse return
            if self.errors.exist is False:
                self.xml = self.r.text
                self.dict = xmltodict.parse(self.xml, dict_constructor=dict)
                self.xml_bytes = bytes(self.xml, encoding="utf-8")
                self.object = objectify.fromstring(self.xml_bytes)
                
                self.found = True
            else:
                self.found = False

class UpdateUserDetails():
    def __init__(self, user_id, user_id_type="all_unique", send_pin_number_letter="false", 
                 recalculate_roles="false", source_institution_code= "", user_xml="", apikey=""):
            self.UpdateUserDetails = UpdateUserDetails
            self.base_url = f'https://api-na.hosted.exlibrisgroup.com/almaws/v1/users/{user_id}'
            self.url = f'{self.base_url}?user_id_type={user_id_type}&send_pin_number_letter={send_pin_number_letter}&recalculate_roles={recalculate_roles}&apikey={apikey}'

            self.r = http.retrieve_xml(url=self.url, method="put", xml=user_xml)
            #print(self.r)
            self.xml = self.r

            # Check for errors in Response object.
            self.errors = errors.Errors(self.r)

            # Parse return
            if self.errors.exist is False:
                self.xml = self.r
                self.dict = xmltodict.parse(self.xml, dict_constructor=dict)
                self.xml_bytes = bytes(self.xml, encoding="utf-8")
                self.object = objectify.fromstring(self.xml_bytes)