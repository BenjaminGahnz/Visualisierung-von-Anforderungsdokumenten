import json
import TReqzmaster


def reqifToJson(reqifFile:str)->str:
    result = {
        "documents": []
            }
    
    reqif = TReqzmaster.TReqz.reqif(reqifFile)
    documentIds = reqif.getAllDocumentIds()
    
    for documentId in documentIds:
        
        document = reqif.getObject(documentId)
        document_long_name = document.long_name if document.long_name else "Unnamed Document"
        
        
        # Columns
        #typeId = reqif.getDocumentSpecObjectTypeId(documentId)
        #columns = reqif.getAllAttributeTypeLongNames(typeId)
        
        # Anforderungen
        allRequirements = reqif.getAllDocumentRequirementIds(documentId)
        reqData = list()
        for requirement in allRequirements:
            reqData.append({
                            "id":requirement,
                            "content":reqif.getRequirementValues(requirement, convertEnums = True)})
        
        result["documents"].append({
            "id": documentId,
            "longName": document_long_name,
            #"columns": columns,
            "requirements": reqData
        })
        
    return json.dumps(result, indent=4)
    
    
