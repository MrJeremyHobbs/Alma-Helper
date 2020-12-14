import xmltodict
from lxml import objectify

class Errors():
    def __init__(self, r):
    
        self.Errors = Errors
        
        # Convert Reponse object to XML plain text and bytes.
        self.xml = r.text
        self.xml_bytes = bytes(self.xml, encoding="utf-8")    
        
        # Check for invalid API key.
        if self.xml == "Invalid API Key":
            self.exist = True
            self.message = self.xml
        else:
            self.exist = False
        
        # Create XML object.
        if self.exist == False:
            self.object = objectify.fromstring(self.xml_bytes)
            
            # Check for error messages in the XML object.
            if hasattr(self.object, "errorsExist") == True:
                self.exist = True
                self.message = self.object.errorList.error.errorMessage
            else:
                self.exist = False