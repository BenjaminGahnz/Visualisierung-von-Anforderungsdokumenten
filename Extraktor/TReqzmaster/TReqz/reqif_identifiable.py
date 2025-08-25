import xml.etree.cElementTree as ET
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
from .. import TReqz


class reqif_identifiable(TReqz.reqif_object):

    def __init__(self, content: Element = None, id_dict=None):
        self.desc: str = None  # attribute, optional
        self.identifier: str = None  # attribute, required
        self.last_change: str = None  # attribute, required
        self.long_name: str = None  # attribute, optional
        self.alternative_id: str = None  # element, optional
        super(reqif_identifiable, self).__init__(content, id_dict)

    def create(self, id_dict=None):
        self.identifier = TReqz.reqif_utils.generateNextLocalId(id_dict)
        if self.identifier != None and id_dict != None:
            id_dict.add(self)
        else:
            # problem
            pass
        return self.identifier

    def decode(self, content: Element, id_dict=None):  # :TReqz.reqif_id_dict.reqif_id_dict
        super().decode(content, id_dict)
        namespace = TReqz.xml_utils.get_tag_namespace(content.tag)

        self.desc = TReqz.reqif_utils.unescapeAttribute(content.get("DESC"))
        self.identifier = TReqz.reqif_utils.unescapeAttribute(content.get("IDENTIFIER"))
        if self.identifier != None and id_dict != None:
            id_dict.add(self)
        self.last_change = TReqz.reqif_utils.unescapeAttribute(content.get("LAST-CHANGE"))
        self.long_name = TReqz.reqif_utils.unescapeAttribute(content.get("LONG-NAME"))

        alternativeidElement = TReqz.xml_utils.get_element(
            content, "./{0}ALTERNATIVE-ID/{0}ALTERNATIVE-ID".format(namespace))
        if alternativeidElement != None:
            self.alternative_id = TReqz.reqif_utils.unescapeAttribute(alternativeidElement.get("IDENTIFIER"))

    def encode(self):
        elem = super().encode()
        TReqz.xml_utils.setElementAttribute(elem, "DESC", TReqz.reqif_utils.escapeAttribute(self.desc))
        TReqz.xml_utils.setElementAttribute(
            elem, "IDENTIFIER", TReqz.reqif_utils.escapeAttribute(self.identifier))
        TReqz.xml_utils.setElementAttribute(
            elem, "LAST-CHANGE", TReqz.reqif_utils.escapeAttribute(self.last_change))
        TReqz.xml_utils.setElementAttribute(
            elem, "LONG-NAME", TReqz.reqif_utils.escapeAttribute(self.long_name))

        if self.alternative_id != None:
            alternativeidElement = TReqz.xml_utils.addRequiredSubElement(
                elem, "ALTERNATIVE-ID")
            alternativeidElementWithAttribute = TReqz.xml_utils.addRequiredSubElement(
                alternativeidElement, "ALTERNATIVE-ID")
            TReqz.xml_utils.setElementAttribute(
                alternativeidElementWithAttribute, "IDENTIFIER", TReqz.reqif_utils.escapeAttribute(self.alternative_id))

        return elem
