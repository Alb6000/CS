import xml.etree.cElementTree as ET


def composeNode(tagname, content):
    return "<" + tagname + "><![CDATA[" + content + "]]></" + tagname + ">"

def getLocation(addressLocality, addressRegion):
    if len(addressLocality) > 0:
        if len(addressRegion) > 0:
            location = addressLocality + ", " + addressRegion
        else:
            location = addressLocality
    else:
        location = addressRegion

    return location

def getRate(rate):
    outrate = rate
    if outrate.find('Unspecified')>-1:
        outrate = '£Contractor Rate'
    elif outrate=='':
        outrate = '£Contractor Rate'

    return outrate




class Job:
    'Common base class for all employees'
    empCount = 0

    def __init__(self, URL, template):
        self.URL = URL
        self.template = template
        self.salary = 'Not Specified'
        self.type = 'Not specified'
        self.datepublished = 'Not specified'
        self.location = 'Not specified'
        self.title = 'Not specified'
        self.description = 'Not specified'
        self.company = 'Not specified'

        self.addressLocality=''
        self.addressRegion=''

    def expired(self):
        self.salary = 'Expired'
        self.type = 'Expired'
        self.datepublished = 'Expired'
        self.location = 'Expired'
        self.title = 'Expired'
        self.description = 'Expired'
        self.company = 'Expired'
        self.CSDesc = 'Expired'

    def setCSDesc(self):
        self.CSDesc = self.title + " at " + self.company +", " + getLocation(self.addressLocality,  self.addressRegion)  +", " + getRate(self.salary)

    def createXML(self):

        xml = "<job>" + \
              composeNode("CSDesc", self.CSDesc) + \
              composeNode("company",self.company) + \
              composeNode("url", self.URL) + \
              composeNode("title", self.title) + \
              composeNode("dateposted", self.datepublished) + \
              composeNode("location", self.location) + \
              composeNode("type", self.type) + \
              composeNode("salary", self.salary) + \
              composeNode("description", self.description) + \
              "</job>"
        return xml
