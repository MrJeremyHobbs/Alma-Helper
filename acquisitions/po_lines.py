#!/usr/bin/python3
import xmltodict
import sys

# local modules
sys.path.append('..')
from alma import http
from alma import errors

class GetPoLine():
    def __init__(self, po_line_id, apikey=apikey):
        self.base_url = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/acq/po-lines'
        self.url = f"{self.base_url}/{po_line_id}?apikey={apikey}"
        self.r = http.retrieve_xml(url=self.url, method="get")
        
        # Check for errors in Response object.
        self.errors = errors.Errors(self.r)
        
        # Parse return
        if self.errors.exist == False:
            self.xml = self.r.text
            self.dict = xmltodict.parse(self.xml)
            self.fund_code = self.dict['po_line']['fund_distributions']['fund_distribution']['fund_code'].get('#text', None)
            
        else:
            self.xml = None
            self.dict = None
            
class RetrievePoLines():
    def __init__(self, q=None, status=None, limit=None, offset=None, order_by=None, 
                       direction=None, acquisition_method=None, expand=None, library=None, 
                       min_expected_arrival_date=None, max_expected_arrival_date=None, 
                       apikey=None):
                       
        self.base_url = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/acq/po-lines'
        self.url = f"{self.base_url}?status={status}&limit={limit}&apikey={apikey}"
        self.r = http.retrieve_xml(url=self.url, method="get")
        
        # Check for errors in Response object.
        self.errors = errors.Errors(self.r)
        
        # Parse return
        if self.errors.exist == False:
            self.xml = self.r.text
            self.dict = xmltodict.parse(self.xml)
            #self.fund_code = self.dict['po_line']['fund_distributions']['fund_distribution']['fund_code'].get('#text', None)
            
        else:
            self.xml = None
            self.dict = None