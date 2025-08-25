package org.getaviz.generator.jqa;

import org.apache.commons.codec.digest.DigestUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.getaviz.generator.ProgrammingLanguage;
import org.getaviz.generator.Step;
import org.getaviz.generator.database.DatabaseConnector;
import org.neo4j.driver.Result;
import org.neo4j.driver.Record;
import org.neo4j.driver.Value;
import org.neo4j.driver.types.Node;

import java.util.List;

// ToDo: Chapter müssen unbedingt ergänzt werden!

// Hier werden name und fqn für die Spezifikationen(=Packages) und Anforderungen(=Class) ergänzt

public class JavaEnhancement implements Step {
	private Log log = LogFactory.getLog(this.getClass());
	private DatabaseConnector connector = DatabaseConnector.getInstance();
	private boolean skipScan;
	private List<ProgrammingLanguage> languages;

// Muss true sein! 
	public JavaEnhancement(boolean skipScan, List<ProgrammingLanguage> languages) {
		this.skipScan = skipScan; // ToDo brauch ich das ?
		this.languages = languages;
		
	}
// TODO: Anpassen, brauch ich das ?
	public boolean checkRequirements() {
		if(!languages.contains(ProgrammingLanguage.JAVA)) return false;
		return true;
	}

	public void run() {
		log.info("Starting database enhancement check.");
		if(checkRequirements()) {
			log.info("Database enhancement started.");
			addHashes();
			log.info("Database enhancement finished");
		} else {
			log.info("Database enhancement requirements not met.");
		}
	}

	private void addHashes() {
		log.info("Collecting all specifications.");
		//connector.executeRead(collectAllSpecifications());
		List<Record> recordsSpecs = connector.executeRead(collectAllSpecifications());
        log.info("Processing all Specifications.");
        recordsSpecs.forEach(this::enhanceSpecification);
		
		log.info("Collecting all Sections.");
		List <Record> recordsSects  = connector.executeRead(collectAllSectios());
		recordsSects.forEach(this::enhanceSection); // Process each record

		//? Warum war das da zwei mal?
		/*log.info("Collecting all Sections");
		List <Record> recordsSects  = preorderTraversal();
		//log.info("Processing all Sections V2.");
    	recordsSects.forEach(this::enhanceSection); // Process each record*/
		
		log.info("Collecting all Requirements.");
		List<Record> recordsReqs = connector.executeRead(collectAllRequirements());
		recordsReqs.forEach(this::enhanceRequirement); // Process each record	
	}
	
	//!Testweise Hash mit ID ersetzen
	//ToDOTesten !!!!!!!!!
	/* 
	private String createHash(String fqn) { 
		return "ID_" + DigestUtils.sha1Hex(fqn);
	}
	*/



	private String collectAllSpecifications() {
		return "MATCH (n:Specification) RETURN n"; // ToDo: Chapter ebenfalls
	}

	private String collectAllSectios(){
		return "MATCH (root:Specification) " +
                "CALL {" +
                "  WITH root" +
                "  MATCH (root)-[:IS_PARENT_OF*]->(child:Section)" +
                "  RETURN child" +
                "} " +
                "WITH root, collect(child) AS childs " +
                "UNWIND childs AS Section " +
                "RETURN Section " +
                "ORDER BY Section.depth ";
	}
	
	/*private String collectAllSections(){
		return "MATCH (n:Section) RETURN n";
	}*/

	private String collectAllRequirements() {
    return "MATCH (n:Requirement) WHERE NOT 'Section' IN labels(n) RETURN n";
	}



//! Woher weiss ich das die Reihenfolge beachtet wird, damit jedes Eltern- Requirement ein FQN hat?
//? So gelöst das FQN immer REQIF.SECTION.Name 


//ToDo: 	gut wäre es auch beim Sammeln der Requirements von der Wurzel aus durchzu iterieren, 
//ToDO: 	um sicherzustellen das das Eltern-Requirement bereits über ein FQN verfügt.*/

	private void enhanceSpecification(Record record) {
		try {
			Node node = record.get("n").asNode();
			String fqn = "";
			String name = "";
			String ID =  node.get("ID").asString();
			String hash = ID;

			if (node.containsKey("LongName")) {
				Value nameValue = node.get("LongName"); //? Richtig geschrieben ??
				
				if (!nameValue.isNull()) {
					name = nameValue.asString();
				} else {
					name = String.valueOf(node.id());
				}
			}
			if (name.isEmpty()) {
				name = String.valueOf(node.id());
			}

			fqn =  "ReqIF." + name;

//! Zum Testen Hash mit id ersetzt !!!!!!!!!!
/* 
			connector.executeWrite(
				"MATCH (n) WHERE ID(n) = " + node.id() + 
				" SET n.name = '" + name + "', n.fqn = '" + fqn + "', n.hash = '" + createHash(fqn) + "'");
			}
*/

			connector.executeWrite(
				"MATCH (n) WHERE ID(n) = " + node.id() + 
				" SET n.name = '" + name + "', n.fqn = '" + fqn + "', n.hash = '" + hash + "'");
			}

		 catch (Exception e) {
			log.error("Error enhancing node", e);
		}			
	}

	private void enhanceSection(Record record) {
		try {
			Node node = record.get("Section").asNode();
			String fqn = "";
			String name = "";
			String hash = node.get("ID").asString();

			if (node.containsKey("ReqIF.ChapterName")) {
				Value nameValue = node.get("ReqIF.ChapterName");
				if (!nameValue.isNull()) {
					name = nameValue.asString();
				} else {
					name = node.get("ReqIF.ForeignID").asString();}
			}
			else {
				name = node.get("ReqIF.ForeignID").asString();
	//? Kann eigentlich weg, weil vereinbart wurde, das ForeignID immer gesetzt ist!
				if (name.isEmpty()) {
					name = String.valueOf(node.id());
				}
			}

			List<Record> containerRecords = connector.executeRead(
				"MATCH (n)<-[:IS_PARENT_OF*]-(container:Specification) " +
				"WHERE ID(n) = " + node.id() + " " +
				"RETURN container"
			);

			Node container = null;
				container = containerRecords.get(0).get("container").asNode();
				String containerFqn = container.get("fqn").asString();
				fqn = containerFqn + "." + name;
//! Auch Hash ersetzt
/* 
			connector.executeWrite(
				"MATCH (n) WHERE ID(n) = " + node.id() + 
				" SET n.name = '" + name + "', n.fqn = '" + fqn + "', n.hash = '" + createHash(fqn) + "'");
*/

			connector.executeWrite(
				"MATCH (n) WHERE ID(n) = " + node.id() + 
				" SET n.name = '" + name + "', n.fqn = '" + fqn + "', n.hash = '" + hash + "'");
			
		 
		} catch (Exception e) {
			log.error("Error enhancing node", e);
		}
	}

	private void enhanceRequirement(Record record) {
			try {
				Node node = record.get("n").asNode();
				String hash = node.get("ID").asString();
				String fqn = "";
				String name = "";
		
				if (node.containsKey("ReqIF.ChapterName")) {
					Value nameValue = node.get("ReqIF.ChapterName");
					if (!nameValue.isNull()) {
						name = nameValue.asString();
					}else {
						name = node.get("ReqIF.ForeignID").asString();}
				}
				else {
					name = node.get("ReqIF.ForeignID").asString();
		//? Kann eigentlich weg, weil vereinbart wurde, das ForeignID immer gesetzt ist!
					if (name.isEmpty()) {
						name = String.valueOf(node.id());
					}
				}

				List<Record> containerRecords = connector.executeRead(
						"MATCH (n)<-[:IS_PARENT_OF*]-(container:Section) " +
						"WHERE ID(n) = " + node.id() + " " +
						"RETURN container " +
						"LIMIT 1"
					);

				if (containerRecords.isEmpty()){
					containerRecords = connector.executeRead(
						"MATCH (n)<-[:IS_PARENT_OF]-(container:Specification) " +
						"WHERE ID(n) = " + node.id() + " " +
						"RETURN container"	);
				}
				Node container = null;
				container = containerRecords.get(0).get("container").asNode();
				String containerFqn = container.get("fqn").asString();
				fqn = containerFqn + "." + name;

//! Auch Hash ersetzt
/* 
			connector.executeWrite(
				"MATCH (n) WHERE ID(n) = " + node.id() + 
				" SET n.name = '" + name + "', n.fqn = '" + fqn + "', n.hash = '" + createHash(fqn) + "'");
*/

				connector.executeWrite(
					"MATCH (n) WHERE ID(n) = " + node.id() + 
					" SET n.name = '" + name + "', n.fqn = '" + fqn + "', n.hash = '" + hash + "'");
				
				} 
			catch (Exception e) {
			log.error("Error enhancing node", e);
			}
	
	}


}

	
/* 	private void enhanceNode(Record record) {
	try {
		Node node = record.get("n").asNode();
		String fqn = "";
		String name = "";

		if (node.containsKey("ReqIF.ChapterName")) {
			Value nameValue = node.get("ReqIF.ChapterName");
			if (!nameValue.isNull()) {
				name = nameValue.asString();
			}
		}
		else {
			name = node.get("ReqIF.ForeignID").asString();
//? Kann eigentlich weg, weil vereinbart wurde, das ForeignID immer gesetzt ist!
			if (name.isEmpty()) {
				name = String.valueOf(node.id());
			}
		}


		if (node.hasLabel("Requirement")) {	

			List<Record> containerRecords = connector.executeRead(
				"MATCH (n)<-[:IS_PARENT_OF*]-(container:Section) " +
				"WHERE ID(n) = " + node.id() + " " +
				"RETURN container " +
				"LIMIT 1"
			);
//? Kurz ausgeklammert um zu kucken ob containerRecords vlt überschrieben wird
//ToDo: wieder ausklammer!!
			if (containerRecords.isEmpty()){
				containerRecords = connector.executeRead(
					"MATCH (n)<-[:IS_PARENT_OF]-(container:Specification) " +
					"WHERE ID(n) = " + node.id() + " " +
					"RETURN container"	);
			}
			Node container = null;
			container = containerRecords.get(0).get("container").asNode();
			String containerFqn = container.get("fqn").asString();
			fqn = containerFqn + "." + name;
		} 
		if (node.hasLabel("Section")) {	

			List<Record> containerRecords = connector.executeRead(
				"MATCH (n)<-[:IS_PARENT_OF*]-(container:Specification) " +
				"WHERE ID(n) = " + node.id() + " " +
				"RETURN container"
			);
			Node container = null;
				container = containerRecords.get(0).get("container").asNode();
				String containerFqn = container.get("fqn").asString();
				fqn = containerFqn + "." + name;
		} 
		if (node.hasLabel("Specification")) {
			if (node.containsKey("LongName")) {
				Value nameValue = node.get("LongName"); //? Richtig geschrieben ??
				if (!nameValue.isNull()) {
					name = nameValue.asString();
				}
			}
			if (name.isEmpty()) {
				name = String.valueOf(node.id());
			}

			fqn =  "ReqIF." + name;
			}

			//?Könnte man das das nicht auch in eine Cypher Query setzen ? 
		connector.executeWrite(
			"MATCH (n) WHERE ID(n) = " + node.id() + " SET n.name = '" + name + "', n.fqn = '" + fqn + "'");
			//Könnte man den Hash nicht durch die ID ersetzen ?
		connector.executeWrite(
			"MATCH (n) WHERE ID(n) = " + node.id() + " SET n.hash = '" + createHash(fqn) + "'");
		
		} catch (Exception e) {
			log.error("Error enhancing node", e);
		}
	
	}*/


