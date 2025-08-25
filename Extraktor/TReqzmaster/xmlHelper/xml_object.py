from xml.etree.ElementTree import Element
import re
from .. import xmlHelper


class xml_object:
    """ a basic xml-object (abstract)
    """

    def __init__(self, content: Element = None):
        self.name: str = "no name"

    def fill(self, **kwargs):
        """[summary]
        """

        for key, value in kwargs.items():
            setattr(self, key, value)

    def get(self, attributeName: str, default=None):
        """[summary]
        
        Arguments:
            attributeName {str} -- [description]
        
        Keyword Arguments:
            default {[type]} -- [description] (default: {None})

        Returns:
            {bool} -- whether the tag name is the expected (true = yes, false = no)
        """

        return getattr(self, attributeName, default)

    def decode(self, content: Element):
        """[summary]
        
        Arguments:
            content {Element} -- [description]
        """

        raise NotImplementedError

    def encode(self):
        """[summary]
        
        Returns:
            [type] -- [description]
        """
    
        return xmlHelper.xml_utils.createSubElement(None)
