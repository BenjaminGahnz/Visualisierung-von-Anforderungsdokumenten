from .. import TReqz
from xml.etree.ElementTree import Element


class reqif_datatype_definition_real(TReqz.reqif_datatype_definition):

    def __init__(self, content: Element = None, id_dict=None):
        self.accuracy: int = None  # attribute, required
        self.max: float = None  # attribute, required
        self.min: float = None  # attribute, required
        super(reqif_datatype_definition_real, self).__init__(content, id_dict)
        self.name = "DATATYPE-DEFINITION-REAL"

    def decode(self, content: Element, id_dict: TReqz.reqif_id_dict = None):
        super().decode(content, id_dict)
        self.accuracy = TReqz.reqif_utils.unescapeAttribute(content.get("ACCURACY"))
        self.max = TReqz.reqif_utils.unescapeAttribute(content.get("MAX"))
        self.min = TReqz.reqif_utils.unescapeAttribute(content.get("MIN"))

    def encode(self):
        elem = super().encode()
        elem.tag = self.name
        TReqz.xml_utils.setElementAttribute(elem, "ACCURACY", TReqz.reqif_utils.escapeAttribute(self.accuracy))
        TReqz.xml_utils.setElementAttribute(elem, "MAX", TReqz.reqif_utils.escapeAttribute(self.max))
        TReqz.xml_utils.setElementAttribute(elem, "MIN", TReqz.reqif_utils.escapeAttribute(self.min))
        return elem
