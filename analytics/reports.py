#!/usr/bin/python3
from alma import http
from alma import errors
from lxml import objectify
import xmltodict
import sys


class RetrieveAnalyticsReport():
    def __init__(self, path="", filter="", limit="25", col_names="true",
                 token="", apikey=""):
        self.RetrieveAnalyticsReport = RetrieveAnalyticsReport

        self.base_url = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/analytics/reports'
        self.url = f"{self.base_url}?apikey={apikey}&path={path}&filter={filter}&limit={limit}&col_names={col_names}"
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

            self.ResumptionToken = self.dict['report']['QueryResult']['ResumptionToken']

            # Headings and column names
            self.columnHeadings = []
            self.columnNames = []
            self.columnIndexes = {}

            columns_dict = self.dict['report']['QueryResult']['ResultXml']['rowset']['xsd:schema']['xsd:complexType']['xsd:sequence']['xsd:element']

            for column_dict in columns_dict:
                column_index = column_dict['@name']
                column_header = column_dict['@saw-sql:columnHeading']

                self.columnNames.append(column_dict['@name'])
                self.columnHeadings.append(column_dict['@saw-sql:columnHeading'])

                self.columnIndexes[column_header] = {}
                self.columnIndexes[column_header]['row'] = column_index.replace('Column', '')

            self.headers = self.columnHeadings

        # Set rows
        self.rowset = []
        self.get_rows(self.dict)

        # Send resumption token until finished
        while self.is_finished(self.dict) is False:
            print("Making another pass...")
            self.base_url = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/analytics/reports'
            self.url = f"{self.base_url}?apikey={apikey}&path={path}&filter={filter}&limit={limit}&col_names={col_names}&token={self.ResumptionToken}"
            self.r = http.retrieve_xml(url=self.url, method="get")
            self.xml = self.r.text
            self.dict = xmltodict.parse(self.xml, dict_constructor=dict)
            self.get_rows(self.dict)

        # Get record count
        try:
            self.totalRows = len(self.rowset)
        except:
            self.totalRows = ""

    # methods #################################################################
    def is_finished(self, xml_dict):
        self.IsFinished = xml_dict['report']['QueryResult']['IsFinished']
        if self.IsFinished == "true":
            self.IsFinished = True
        if self.IsFinished == "false":
            self.IsFinished = False

        return self.IsFinished

    def get_rows(self, xml_dict):
        try:
            for row in xml_dict['report']['QueryResult']['ResultXml']['rowset']['Row']:
                row_list = []
                for column in self.columnNames:
                    value = row.get(column, "")
                    row_list.append(value)
                self.rowset.append(row_list)
        except:
            row = xml_dict['report']['QueryResult']['ResultXml']['rowset']['Row']
            row_list = []
            for column in self.columnNames:
                value = row.get(column, "")
                row_list.append(value)
            self.rowset.append(row_list)

    def get_col_index(self, column_name):
        return str(self.columnIndexes[column_name]['row'])
