from xml.etree.ElementTree import Element
from .. import TReqz


class reqif_specification(TReqz.reqif_identifiable):

    def __init__(self, content: Element = None, id_dict=None):
        self.values: list = list()  # reqif_attribute_value
        self.children: list = list()  # reqif_spec_hierarchy
        self.type: TReqz.reqif_specification_type = None  # localRef, required
        super(reqif_specification, self).__init__(content, id_dict)
        self.name = "SPECIFICATION"

    def decode(self, content: Element, id_dict: TReqz.reqif_id_dict = None):
        super().decode(content, id_dict)
        namespace = TReqz.xml_utils.get_tag_namespace(content.tag)

        self.values = TReqz.reqif_utils.generate_object_list_by_element_class(
            content, id_dict, "./{0}VALUES".format(namespace), TReqz.reqif_config.ATTRIBUTE_VALUE_TAG_TO_CLASS)

        self.children = TReqz.reqif_utils.generate_object_list_by_element_class(
            content, id_dict, "./{0}CHILDREN".format(namespace), TReqz.reqif_config.SPEC_HIERARCHY_TAG_TO_CLASS)

        self.type = TReqz.reqif_utils.get_local_ref_from_element_text(
            content, id_dict, "./{0}TYPE/{0}SPECIFICATION-TYPE-REF".format(namespace))

    def encode(self):
        elem = super().encode()
        elem.tag = self.name

        if self.values!= None and len(self.values) > 0:
            valuesElement = TReqz.xml_utils.addRequiredSubElement(
                elem, "VALUES")
            for value in self.values:
                TReqz.xml_utils.addEncodedSubElement(valuesElement, value)

        if self.children != None and len(self.children) > 0:
            childrenElement = TReqz.xml_utils.addRequiredSubElement(
                elem, "CHILDREN")
            for child in self.children:
                TReqz.xml_utils.addEncodedSubElement(childrenElement, child)

        if self.type != None:
            typeElement = TReqz.xml_utils.addRequiredSubElement(elem, "TYPE")
            TReqz.xml_utils.addRequiredSubElement(
                typeElement, "SPECIFICATION-TYPE-REF", self.type.identifier)

        return elem
