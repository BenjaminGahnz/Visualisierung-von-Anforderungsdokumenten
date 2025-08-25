from xml.etree.ElementTree import Element
from .. import TReqz


class reqif_specification_type(TReqz.reqif_identifiable):

    def __init__(self, content: Element = None, id_dict=None):
        self.spec_attributes: list = list()  # reqif_attribute_definition, optional
        super(reqif_specification_type, self).__init__(content, id_dict)
        self.name = "SPECIFICATION-TYPE"

    def decode(self, content: Element, id_dict: TReqz.reqif_id_dict = None):
        super().decode(content, id_dict)
        namespace = TReqz.xml_utils.get_tag_namespace(content.tag)

        self.spec_attributes = TReqz.reqif_utils.generate_object_list_by_element_class(
            content, id_dict, "./{0}SPEC-ATTRIBUTES".format(namespace), TReqz.reqif_config.ATTRIBUTE_DEFINITION_TAG_TO_CLASS)

    def encode(self):
        elem = super().encode()
        elem.tag = self.name

        if len(self.spec_attributes) > 0:
            specattributesElement = TReqz.xml_utils.addRequiredSubElement(
                elem, "SPEC-ATTRIBUTES")
            for spec in self.spec_attributes:
                TReqz.xml_utils.addEncodedSubElement(
                    specattributesElement, spec)

        return elem
