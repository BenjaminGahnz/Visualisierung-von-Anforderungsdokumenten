
class reqif_config:

    REQIF_NAMESPACE = "http://www.omg.org/spec/ReqIF/20110401/reqif.xsd"

    ATTRIBUTE_DEFINITION_TO_VALUE: dict = {"reqif_attribute_definition_boolean": "reqif_attribute_value_boolean",
                                             "reqif_attribute_definition_date": "reqif_attribute_value_date",
                                             "reqif_attribute_definition_enumeration": "reqif_attribute_value_enumeration",
                                             "reqif_attribute_definition_integer": "reqif_attribute_value_integer",
                                             "reqif_attribute_definition_real": "reqif_attribute_value_real",
                                             "reqif_attribute_definition_string": "reqif_attribute_value_string",
                                             "reqif_attribute_definition_xhtml": "reqif_attribute_value_xhtml"}

    ATTRIBUTE_VALUE_TO_DEFINITION = dict(
        map(reversed, ATTRIBUTE_DEFINITION_TO_VALUE.items()))

    ATTRIBUTE_DEFINITION_TAG_TO_CLASS = {"ATTRIBUTE-DEFINITION-BOOLEAN": "reqif_attribute_definition_boolean",
                                         "ATTRIBUTE-DEFINITION-DATE": "reqif_attribute_definition_date",
                                         "ATTRIBUTE-DEFINITION-INTEGER": "reqif_attribute_definition_integer",
                                         "ATTRIBUTE-DEFINITION-ENUMERATION": "reqif_attribute_definition_enumeration",
                                         "ATTRIBUTE-DEFINITION-REAL": "reqif_attribute_definition_real",
                                         "ATTRIBUTE-DEFINITION-STRING": "reqif_attribute_definition_string",
                                         "ATTRIBUTE-DEFINITION-XHTML": "reqif_attribute_definition_xhtml"}

    DATATYPE_DEFINITION_TAG_TO_CLASS = {"DATATYPE-DEFINITION-BOOLEAN": "reqif_datatype_definition_boolean",
                                        "DATATYPE-DEFINITION-DATE": "reqif_datatype_definition_date",
                                        "DATATYPE-DEFINITION-ENUMERATION": "reqif_datatype_definition_enumeration",
                                        "DATATYPE-DEFINITION-INTEGER": "reqif_datatype_definition_integer",
                                        "DATATYPE-DEFINITION-REAL": "reqif_datatype_definition_real",
                                        "DATATYPE-DEFINITION-STRING": "reqif_datatype_definition_string",
                                        "DATATYPE-DEFINITION-XHTML": "reqif_datatype_definition_xhtml"}

    ATTRIBUTE_VALUE_TAG_TO_CLASS = {"ATTRIBUTE-VALUE-BOOLEAN": "reqif_attribute_value_boolean",
                                    "ATTRIBUTE-VALUE-DATE": "reqif_attribute_value_date",
                                    "ATTRIBUTE-VALUE-ENUMERATION": "reqif_attribute_value_enumeration",
                                    "ATTRIBUTE-VALUE-INTEGER": "reqif_attribute_value_integer",
                                    "ATTRIBUTE-VALUE-REAL": "reqif_attribute_value_real",
                                    "ATTRIBUTE-VALUE-STRING": "reqif_attribute_value_string",
                                    "ATTRIBUTE-VALUE-XHTML": "reqif_attribute_value_xhtml"}

    SPEC_TYPES_TAG_TO_CLASS = {"RELATION-GROUP-TYPE": "reqif_relation_group_type",
                               "SPECIFICATION-TYPE": "reqif_specification_type",
                               "SPEC-RELATION-TYPE": "reqif_spec_relation_type",
                               "SPEC-OBJECT-TYPE": "reqif_spec_object_type"}

    SPEC_HIERARCHY_TAG_TO_CLASS = {"SPEC-HIERARCHY": "reqif_spec_hierarchy"}

    SPEC_OBJECTS_TAG_TO_CLASS = {"SPEC-OBJECT": "reqif_spec_object"}

    SPEC_RELATIONS_TAG_TO_CLASS = {"SPEC-RELATION": "reqif_spec_relation"}

    SPECIFICATIONS_TAG_TO_CLASS = {"SPECIFICATION": "reqif_specification"}

    SPEC_RELATION_GROUPS_TAG_TO_CLASS = {"RELATION-GROUP": "reqif_relation_group"}
