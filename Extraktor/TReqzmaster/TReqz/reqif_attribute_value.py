from xml.etree.ElementTree import Element
from .. import TReqz


class reqif_attribute_value(TReqz.reqif_object):

    def __init__(self, content: Element = None, id_dict=None):
        self.definition: TReqz.reqif_attribute_definition = None  # element, required
        self.the_value: str = None  # attribute, required
        super(reqif_attribute_value, self).__init__(content, id_dict)
        self.name = "ATTRIBUTE-VALUE"

    def getValue(self):
        if self.the_value == None and self.definition != None:
            return self.definition.default_value
        return self.the_value

    def setValue(self, value: str, id_dict: TReqz.reqif_id_dict):
        self.the_value = value

    def isEmpty(self):
        if self.the_value == None:
            return True
        return False 

    def encode(self):
        elem = super().encode()
        return elem
