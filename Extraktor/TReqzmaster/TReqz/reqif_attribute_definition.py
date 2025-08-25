from xml.etree.ElementTree import Element
from .. import TReqz


class reqif_attribute_definition(TReqz.reqif_identifiable):

    def __init__(self, content: Element = None, id_dict=None):
        self.default_value: TReqz.reqif_attribute_value = None  # element, optional
        self.type: TReqz.reqif_datatype_definition = None  # local_ref, required
        self.is_editable: str = None  # attribute, optional
        super(reqif_attribute_definition, self).__init__(content, id_dict)
        self.name:str = "ATTRIBUTE-DEFINITION"

    def decode(self, content: Element, id_dict: TReqz.reqif_id_dict = None):
        super().decode(content, id_dict)

        self.is_editable = TReqz.reqif_utils.unescapeAttribute(content.get("IS-EDITABLE"))

    def encode(self):
        elem = super().encode()
        elem.tag = self.name
        TReqz.xml_utils.setElementAttribute(
            elem, "IS-EDITABLE", TReqz.reqif_utils.escapeAttribute(self.is_editable))
        return elem
