from xml.etree.ElementTree import Element
from .. import TReqz


class reqif_spec_relation(TReqz.reqif_identifiable):

    def __init__(self, content: Element = None, id_dict=None):
        self.values: list = [] # reqif_attribute_value, optional
        self.source: TReqz.reqif_object = None  # local_ref, required
        self.target: TReqz.reqif_object = None  # local_ref, required
        self.type: TReqz.reqif_spec_relation_type = None  # local_ref, required
        super(reqif_spec_relation, self).__init__(content, id_dict)
        self.name = "SPEC-RELATION"

    def decode(self, content: Element, id_dict: TReqz.reqif_id_dict = None):
        super().decode(content, id_dict)
        namespace = TReqz.xml_utils.get_tag_namespace(content.tag)

        self.values = TReqz.reqif_utils.generate_object_list_by_element_class(
            content, id_dict, "./{0}VALUES".format(namespace), TReqz.reqif_config.ATTRIBUTE_VALUE_TAG_TO_CLASS)

        self.source = TReqz.reqif_utils.get_create_local_ref_from_element_text(
            content, id_dict, "./{0}SOURCE/{0}SPEC-OBJECT-REF".format(namespace))
        self.target = TReqz.reqif_utils.get_create_local_ref_from_element_text(
            content, id_dict, "./{0}TARGET/{0}SPEC-OBJECT-REF".format(namespace))
        self.type = TReqz.reqif_utils.get_local_ref_from_element_text(
            content, id_dict, "./{0}TYPE/{0}SPEC-RELATION-TYPE-REF".format(namespace))

    def encode(self):
        elem = super().encode()
        elem.tag = self.name

        if len(self.values) > 0:
            valuesElement = TReqz.xml_utils.addRequiredSubElement(
                elem, "VALUES")
            for value in self.values:
                TReqz.xml_utils.addEncodedSubElement(valuesElement, value)

        if self.type != None:
            typeElement = TReqz.xml_utils.addRequiredSubElement(elem, "TYPE")
            TReqz.xml_utils.addRequiredSubElement(
                typeElement, "SPEC-RELATION-TYPE-REF", self.type.identifier)

        if self.source != None:
            sourceElement = TReqz.xml_utils.addRequiredSubElement(elem, "SOURCE")
            TReqz.xml_utils.addRequiredSubElement(
                sourceElement, "SPEC-OBJECT-REF", self.source.identifier)

        if self.target != None:
            targetElement = TReqz.xml_utils.addRequiredSubElement(elem, "TARGET")
            TReqz.xml_utils.addRequiredSubElement(
                targetElement, "SPEC-OBJECT-REF", self.target.identifier)

        return elem
