from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
from .. import TReqz
import re


class reqif_attribute_value_xhtml(TReqz.reqif_attribute_value):

    def __init__(self, content: Element = None, id_dict=None):
        self.definition: TReqz.reqif_attribute_definition_xhtml = None  # localRef, required
        self.the_original_value: str = None  # element, optional
        self.is_simplified: str = None  # attribute, optional
        super(reqif_attribute_value_xhtml, self).__init__(content, id_dict)
        self.name = "ATTRIBUTE-VALUE-XHTML"

    def decode(self, content: Element, id_dict: TReqz.reqif_id_dict = None):
        super().decode(content, id_dict)
        namespace = TReqz.xml_utils.get_tag_namespace(content.tag)
        elem = TReqz.xml_utils.get_element(
            content, "./{0}THE-VALUE".format(namespace))

        # check whether there are more than one subelement
        children=None
        if elem != None:
            children = list(elem) # .getchildren() removed
        if children != None and len(children)==0:
            elem=None
        elif children != None and len(children)==1:
            elem = elem[0]
        else:
            # more than one (not allowed but possible) or empty value
            if children != None:
                elem = Element('div')
            else:
                elem = None

        self.the_value = TReqz.xml_utils.decodeXhtml(elem)

        elem = TReqz.xml_utils.get_element(
            content, "./{0}THE-ORIGINAL-VALUE".format(namespace))
        if elem != None:
            self.the_original_value = ET.tostring(
                elem, encoding='utf-8', method='text')
        self.is_simplified = TReqz.reqif_utils.unescapeAttribute(content.get("IS-SIMPLIFIED"))
        self.definition = TReqz.reqif_utils.get_local_ref_from_element_text(
            content, id_dict, "./{0}DEFINITION/{0}ATTRIBUTE-DEFINITION-XHTML-REF".format(namespace))

    def encode(self):
        elem = super().encode()
        elem.tag = self.name
        TReqz.xml_utils.setElementAttribute(
            elem, "IS-SIMPLIFIED", TReqz.reqif_utils.escapeAttribute(self.is_simplified))

        TReqz.xml_utils.addOptionalSubElement(
            elem, "THE-ORIGINAL-VALUE", self.the_original_value)

        value = self.the_value
        encodedXhtml = TReqz.xml_utils.encodeXhtml(value)

        thevalueElement = TReqz.xml_utils.addRequiredSubElement(
            elem, "THE-VALUE")
        thevalueElement.append(encodedXhtml)

        if self.definition != None:
            definitionElement = TReqz.xml_utils.addRequiredSubElement(
                elem, "DEFINITION")
            TReqz.xml_utils.addRequiredSubElement(
                definitionElement, "ATTRIBUTE-DEFINITION-XHTML-REF", self.definition.identifier)
        return elem
