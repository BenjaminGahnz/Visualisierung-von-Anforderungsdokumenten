from xml.etree.ElementTree import Element
from .. import TReqz


class reqif_relation_group(TReqz.reqif_identifiable):

    def __init__(self, content: Element = None, id_dict=None):
        self.source_specification: TReqz.reqif_object = None  # local_ref, required
        self.target_specification: TReqz.reqif_object = None  # local_ref, required
        self.spec_relations: list = list()  # local_ref, optional
        self.type: TReqz.reqif_relation_group_type = None  # local_ref, required
        super(reqif_relation_group, self).__init__(content, id_dict)
        self.name = "RELATION-GROUP"

    def decode(self, content: Element, id_dict: TReqz.reqif_id_dict = None):
        super().decode(content, id_dict)
        namespace = TReqz.xml_utils.get_tag_namespace(content.tag)

        self.source_specification = TReqz.reqif_utils.get_local_ref_from_element_text(
            content, id_dict, "./{0}SOURCE-SPECIFICATION/{0}SPECIFICATION-REF".format(namespace))
        self.target_specification = TReqz.reqif_utils.get_local_ref_from_element_text(
            content, id_dict, "./{0}TARGET-SPECIFICATION/{0}SPECIFICATION-REF".format(namespace))
        self.type = TReqz.reqif_utils.get_local_ref_from_element_text(
            content, id_dict, "./{0}TYPE/{0}RELATION-GROUP-TYPE-REF".format(namespace))
        self.spec_relations = TReqz.reqif_utils.generate_local_ref_list_from_elements_text(
            content, id_dict, "./{0}SPEC-RELATIONS".format(namespace))

    def encode(self):
        elem = super().encode()
        elem.tag = self.name

        if self.type != None:
            typeElement = TReqz.xml_utils.addRequiredSubElement(elem, "TYPE")
            TReqz.xml_utils.addRequiredSubElement(
                typeElement, "RELATION-GROUP-TYPE-REF", self.type.identifier)

        if self.source_specification != None:
            sourceElement = TReqz.xml_utils.addRequiredSubElement(
                elem, "SOURCE-SPECIFICATION")
            TReqz.xml_utils.addRequiredSubElement(
                sourceElement, "SPECIFICATION-REF", self.source_specification.identifier)

        if self.target_specification != None:
            targetElement = TReqz.xml_utils.addRequiredSubElement(
                elem, "TARGET-SPECIFICATION")
            TReqz.xml_utils.addRequiredSubElement(
                targetElement, "SPECIFICATION-REF", self.target_specification.identifier)

        if self.spec_relations != None and len(self.spec_relations) > 0:
            attsElement = TReqz.xml_utils.addRequiredSubElement(
                elem, "SPEC-RELATIONS")
            for spec in self.spec_relations:
                TReqz.xml_utils.addRequiredSubElement(
                    attsElement, "SPEC-RELATION-REF", spec.identifier)

        return elem
