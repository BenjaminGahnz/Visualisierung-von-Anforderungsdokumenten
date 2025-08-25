from xml.etree.ElementTree import Element
from .. import TReqz


class reqif_attribute_definition_real(TReqz.reqif_attribute_definition):

    def __init__(self, content: Element = None, id_dict=None):
        super(reqif_attribute_definition_real, self).__init__(content, id_dict)
        self.name = "ATTRIBUTE-DEFINITION-REAL"

    def decode(self, content: Element, id_dict: TReqz.reqif_id_dict = None):
        super().decode(content, id_dict)
        namespace = TReqz.xml_utils.get_tag_namespace(content.tag)

        self.default_value = TReqz.reqif_utils.generate_object_by_element_class(
            content, id_dict, "./{0}DEFAULT-VALUE/{0}ATTRIBUTE-VALUE-REAL".format(namespace), "reqif_attribute_value_real")

        self.type = TReqz.reqif_utils.get_local_ref_from_element_text(
            content, id_dict, "./{0}TYPE/{0}DATATYPE-DEFINITION-REAL-REF".format(namespace))

    def encode(self):
        elem = super().encode()
        elem.tag = self.name
        if self.default_value != None:
            defaultElement = TReqz.xml_utils.addRequiredSubElement(
                elem, "DEFAULT-VALUE")
            TReqz.xml_utils.addEncodedSubElement(
                defaultElement, self.default_value)

        if self.type != None:
            typeElement = TReqz.xml_utils.addRequiredSubElement(elem, "TYPE")
            TReqz.xml_utils.addRequiredSubElement(
                typeElement, "DATATYPE-DEFINITION-REAL-REF", self.type.identifier)
        return elem
