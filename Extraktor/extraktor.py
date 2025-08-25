from neo4j import GraphDatabase
import TReqzmaster
from reqif2json import reqifToJson

#!Es fehlt check ob es Informationen in dem Document gibt 
#! Allgemein fehlen Typen

#! Vereinbarungen Implementors Guide einpflegen 

#! Beispiel Dateien Bereitstellen 
#! Wie Docker Container zusammen führen
#! getavizOrder zu NodeID ändern



# Reqif FDateio Pfad
reqif_file = r"C:\Users\Benja\reqif\TEST2\TEST.reqif"
json_output_file_path = r"C:\Users\Benja\VS_Code\py2neo4j\requirements.json"


# Neo4j Connection
uri = "bolt://localhost:7687"  # Hier uri der neo4j db eintragen
auth = ("neo4j", "Benni1998")  #  name + pw

order = 0

def get_order():
    global order
    node_order = order
    order += 1
    return node_order
    

# recursively iterates overrequirements and adds nodes + relationships
def iterate_requirements(requirements, parent_id=None):
    for requirement_id, children in requirements.items():
        # Get the values for the requirement
        values = reqif.getRequirementValues(requirement_id, convertEnums=True)
        values['getavizOrder'] = get_order()
        
        # Create a node for the requirement
        if values.get("Type") == ['Section'] or values.get("ReqIF-WF.Type") == ['Chapter']: #sonderregelung für meine Bsp. Datei
            session.run("""
                MATCH (parent {ID: $parent_id})
                CREATE (requirement:Section {ID: $requirement_id})
                SET requirement += $values
                MERGE (parent)-[:IS_PARENT_OF]->(requirement)     
                """, parent_id=parent_id, requirement_id=requirement_id, values=values)
            iterate_requirements(children, requirement_id)
        elif values.get("Type") == ['Requirement']:
            session.run("""
                MATCH (parent {ID: $parent_id})
                CREATE (requirement:Requirement {ID: $requirement_id})
                SET requirement += $values
                MERGE (parent)-[:IS_PARENT_OF]->(requirement)     
                """, parent_id=parent_id, requirement_id=requirement_id, values=values)
            iterate_requirements(children, requirement_id)
        else:   iterate_requirements(children, parent_id) #! Das ist neu fall type Information 
        
        

with GraphDatabase.driver(uri, auth=auth) as driver:    
    driver.verify_connectivity()    
    with driver.session() as session:
        
        reqif = TReqzmaster.TReqz.reqif(reqif_file)
        document_ids = reqif.getAllDocumentIds()
        hierarchical_requirements = {}
        for document_id in document_ids:
            hierarchical_requirements[document_id] = reqif.getDocumentHierarchicalRequirementIds(document_id)

     
        session.run("""
            MATCH (n) DETACH DELETE n
            """)

        for document_id, requirements in hierarchical_requirements.items():
            document_long_name = reqif.getObject(document_id).long_name if reqif.getObject(document_id).long_name else "Unnamed Document"
            session.run("""
            CREATE (spec:Specification {ID: $ID, LongName: $LongName, getavizOrder: $order})
            """, ID=document_id, LongName=document_long_name, order=get_order())
            
            iterate_requirements(requirements, document_id)
            
                # Links 
        links = reqif.getObjects(reqif.getLinkIds())
        for link in links:
            sourceId = None if link.source == None else link.source.identifier
            targetId = None if link.target == None else link.target.identifier
            session.run("""
                        MATCH (source {ID: $source})
                        MATCH (target {ID: $target})
                        MERGE (source)-[:LINKS_TO]->(target)
                        """, source=sourceId, target=targetId)
            
        session.run("""
                    MATCH (s:Section)
                    WHERE NOT (s)-[:IS_PARENT_OF]->()
                    DETACH DELETE s 
                    """)
             
json_result = reqifToJson(reqif_file)  
with open(json_output_file_path, "w") as file:
    file.write(json_result)   
            

            
            



