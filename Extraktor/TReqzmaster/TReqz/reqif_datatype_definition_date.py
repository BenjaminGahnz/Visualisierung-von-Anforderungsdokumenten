from .. import TReqz
from xml.etree.ElementTree import Element


class reqif_datatype_definition_date(TReqz.reqif_datatype_definition):

    def __init__(self, content: Element = None, id_dict=None):
        super(reqif_datatype_definition_date, self).__init__(content, id_dict)
        self.name = "DATATYPE-DEFINITION-DATE"

    def encode(self):
        elem = super().encode()
        elem.tag = self.name
        return elem
