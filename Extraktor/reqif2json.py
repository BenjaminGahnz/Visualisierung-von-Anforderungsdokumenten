import json
import TReqzmaster


def reqifToJson(reqifFile:str)->str:
    result = []

    reqif = TReqzmaster.TReqz.reqif(reqifFile)
    documentIds = reqif.getAllDocumentIds()
        
    for documentId in documentIds:
        document = {
            "id": documentId,
            "longName": reqif.getDocumentLongName(documentId),
            "requirements": []
        }

        allRequirements = reqif.getAllDocumentRequirementIds(documentId)
        for requirement in allRequirements:
            requirement_values = reqif.getRequirementValues(requirement, convertEnums=True)
            document["requirements"].append({
                "id": requirement,
                "content": requirement_values
            })

        result["documents"].append(document)
    return json.dumps(result, indent=4)
    
    
