from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET

class xml_parser(object):
    """ this class represents a parser interface
    """

    def __init__(self):
        pass

    def parseFile(self, contentFile: str)->Element:
        file = open(contentFile, "r")
        res = self.parse(file.read())
        file.close()
        return res

    def parse(self, content: str)->Element:
        root:Element = ET.fromstring(content)
        return root

    def dump(self, content, pettyprint=True)->None:
        raise NotImplementedError

    def dumpToFile(self, content, fileName: str, pettyprint=True)->None:
        raise NotImplementedError
