import xml.etree.cElementTree as ET
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
import re
from .. import TReqz


class reqif_id_dict(object):

    def __init__(self):
        self.identifiers = dict()  # reqif_identifiable

    def getLen(self)->int:
        """ returns the dict size

        Returns:
            {int} -- the size
        """

        return len(self.identifiers)

    def add(self, newElem: TReqz.reqif_identifiable):
        """ adds an element to the dict

        Arguments:
            newElem {TReqz.reqif_identifiable} -- the new element
        """

        self.identifiers[newElem.identifier] = newElem

    def get(self, name: str):
        """ returns an element by its identifier

        Arguments:
            name {str} -- the identifier

        Returns:
            {reqif_} -- the element
        """

        return self.identifiers.get(name)

    def getIdentifierByObject(self, elem: TReqz.reqif_identifiable):
        """ returns an elements identifier

        Arguments:
            elem {TReqz.reqif_identifiable} -- the element

        Returns:
            {str} -- the identifier
        """

        return elem.identifier

    def remove(self, name: str):
        """ removes an element by its identifier

        Arguments:
            name {str} -- the identifier

        Returns:
            {reqif_} -- the removed object
        """

        if self.identifiers.get(name) == None:
            return None

        return self.identifiers.pop(name)
