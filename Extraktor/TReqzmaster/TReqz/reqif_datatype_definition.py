from .. import TReqz
from xml.etree.ElementTree import Element


class reqif_datatype_definition(TReqz.reqif_identifiable):
    def __init__(self, content: Element = None, id_dict=None):
        super(reqif_datatype_definition,
              self).__init__(content, id_dict)
        self.name = "DATATYPE-DEFINITION"
