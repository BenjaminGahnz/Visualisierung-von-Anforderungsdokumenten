from .. import TReqz
from xml.etree.ElementTree import Element


class reqif_enum_value(TReqz.reqif_identifiable):

    def __init__(self, content: Element = None, id_dict=None):
        self.embedded_value: TReqz.reqif_embeded_value = None  # element, required
        super(reqif_enum_value, self).__init__(content, id_dict)
        self.name = "ENUM-VALUE"

    def decode(self, content: Element, id_dict: TReqz.reqif_id_dict = None):
        super().decode(content, id_dict)
        namespace = TReqz.xml_utils.get_tag_namespace(content.tag)

        elem = content.find(
            "./{0}PROPERTIES/{0}EMBEDDED-VALUE".format(namespace))
        if elem != None:
            self.embedded_value = TReqz.reqif_embeded_value(elem, id_dict)

    def encode(self):
        elem = super().encode()
        elem.tag = self.name

        if self.embedded_value != None:
            valueElement = TReqz.xml_utils.addRequiredSubElement(
                elem, "PROPERTIES")
            TReqz.xml_utils.addEncodedSubElement(
                valueElement, self.embedded_value)
        return elem
