from .. import TReqz
from xml.etree.ElementTree import Element


class reqif_embeded_value(TReqz.reqif_object):

    def __init__(self, content: Element = None, id_dict=None):
        self.key: str = None  # attribute, required
        self.other_content: str = None  # attribute, required
        super(reqif_embeded_value, self).__init__(content, id_dict)
        self.name = "EMBEDDED-VALUE"

    def decode(self, content: Element, id_dict: TReqz.reqif_id_dict = None):
        super().decode(content, id_dict)
        self.key = TReqz.reqif_utils.unescapeAttribute(content.get("KEY"))
        self.other_content = TReqz.reqif_utils.unescapeAttribute(content.get("OTHER-CONTENT"))

    def encode(self):
        elem = super().encode()
        elem.tag = self.name
        TReqz.xml_utils.setElementAttribute(elem, "KEY", TReqz.reqif_utils.escapeAttribute(self.key))
        TReqz.xml_utils.setElementAttribute(
            elem, "OTHER-CONTENT", TReqz.reqif_utils.escapeAttribute(self.other_content))
        return elem
