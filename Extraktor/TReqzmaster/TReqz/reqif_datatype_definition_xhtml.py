from .. import TReqz
from xml.etree.ElementTree import Element


class reqif_datatype_definition_xhtml(TReqz.reqif_datatype_definition):

    def __init__(self, content: Element = None, id_dict=None):
        super(reqif_datatype_definition_xhtml, self).__init__(content, id_dict)
        self.name = "DATATYPE-DEFINITION-XHTML"

    def decode(self, content: Element, id_dict: TReqz.reqif_id_dict = None):
        super().decode(content, id_dict)

    def encode(self):
        elem = super().encode()
        elem.tag = self.name
        return elem
