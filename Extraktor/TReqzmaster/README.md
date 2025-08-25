# TReqz

[![Build Status](https://travis-ci.com/tilluhlig/TReqz.svg?branch=master)](https://travis-ci.com/tilluhlig/TReqz)
[![Coverage Status](https://coveralls.io/repos/github/tilluhlig/TReqz/badge.svg?branch=master)](https://coveralls.io/github/tilluhlig/TReqz?branch=master)

#### How to use it
``` python
import TReqz.reqif
import TReqz.reqif_utils

if __name__ == "__main__":
    reqifFile = "my_reqif.reqif"

    # TReqz - Test
    reqif_object: TReqz.reqif = TReqz.reqif(reqifFile)
```

#### A simple example
``` python
    header = reqif_object.getHeader()
    header.fill(req_if_tool_id="TReqz",
                creation_time=TReqz.reqif_utils.current_timestamp(),
                source_tool_id="Jira")
```

#### Further examples
``` python
    # the example reqif contains a id-field (my_reqif_object_id, string) and
    # a comment field (reqif_comment_field, xhtml)

    allRequirements = reqif_object.getAllRequirementIds()
    specificRequirement = reqif_object.findRequirementsByFieldValue(
        field="my_reqif_object_id", value="CRS-22")
    allRequirementsHierarchical = reqif_object.getHierarchicalRequirementIds()
    requirementValue = reqif_object.getRequirementValue(
        requirementId="_dc3ba2a0-f0cf-4b83-b61a-483d01f208e2",
        attributeTypeId="_b5709b50-04fe-45be-9354-9246f6979a91")
    requirementId = reqif_object.findRequirementIdByLongName("CRS-22")
    requirementValue2 = reqif_object.getRequirementValueByAttributeLongName(
        requirementId, attributeLongName="my_reqif_object_id")
    requirementValue3 = reqif_object.getRequirementValueByLongNames(
        requirementLongName="CRS-22", attributeLongName="my_reqif_object_id")

    reqif_object.setRequirementValueByLongNames(
        requirementLongName="CRS-22", attributeLongName="my_reqif_object_id", value="CRS-55")
    requirementValue4 = reqif_object.getRequirementValueByLongNames(
        requirementLongName="CRS-22", attributeLongName="my_reqif_object_id")

    reqif_object.setRequirementValueByLongNames(
        "CRS-22", "reqif_comment_field", "<div>myNewComment</div>")
    requirementValue5 = reqif_object.getRequirementValueByLongNames(
        "CRS-22", "reqif_comment_field")

    specObjectTypeId = reqif_object.findSpecObjectTypeIdByRequirementId(
        "_dc3ba2a0-f0cf-4b83-b61a-483d01f208e2")
    documentIds = reqif_object.getAllDocumentIds()
    documentId = documentIds[0]

    newRequirementId = reqif_object.addRequirement(
        documentId, specObjectTypeId, long_name="CRS-99")

    newRequirementId2 = reqif_object.addRequirement(
        documentId, specObjectTypeId, parentRequirementId=newRequirementId, long_name="CRS-100")

    requirementValues = reqif_object.getRequirementValuesByLongName("CRS-22")

    reqif_object.setRequirementValueByLongNames(
        requirementLongName="CRS-100",
        attributeLongName="reqif_comment_field",
        value="<div>myNewComment2</div>")

    requirementValue6 = reqif_object.getRequirementValueByLongNames(
        requirementLongName="CRS-100", attributeLongName="reqif_comment_field")
        
    reqif_object.dumpToFile(reqifFile)
```
