package org.getaviz.generator.jqa;

import org.apache.commons.lang3.StringUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.commons.text.StringEscapeUtils;
import org.getaviz.generator.ProgrammingLanguage;
import org.getaviz.generator.SettingsConfiguration;
import org.getaviz.generator.Step;
import org.getaviz.generator.database.DatabaseConnector;
import org.getaviz.generator.database.Labels;
import org.neo4j.driver.Value;
import org.neo4j.driver.Result;
import org.neo4j.driver.Record;
import org.neo4j.driver.types.Node;


import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Arrays;


public class JQA2JSON implements Step {
	private SettingsConfiguration config;
	private Log log = LogFactory.getLog(this.getClass());
	private DatabaseConnector connector = DatabaseConnector.getInstance();
	private List<ProgrammingLanguage> languages;

	public JQA2JSON(SettingsConfiguration config, List<ProgrammingLanguage> languages) {
		this.config = config;
		this.languages = languages;
	}

	public void run() {
		log.info("JQA2JSON has started.");
		ArrayList<Node> elements = new ArrayList<>();
		/*connector.executeRead("MATCH (n)<-[:VISUALIZES]-() RETURN n ORDER BY n.hash").forEachRemaining(result -> {
			elements.add(result.get("n").asNode());
		});*/

		//* Hierdran könnte es liegen das der Packageexplorer so durcheinander ist
		List<Record> resultsVisualizedBy = connector.executeRead("MATCH (n)<-[:VISUALIZES]-() RETURN n ORDER BY n.getavizOrder");
		resultsVisualizedBy.forEach(result -> {
			elements.add(result.get("n").asNode());
		});
		Writer fw = null;
		try {
			String path = config.getOutputPath() + "metaData.json";
			fw = new FileWriter(path);
			fw.write(toJSON(elements));
		} catch (IOException e) {
			log.error(e);
		} finally {
			if (fw != null)
				try {
					fw.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
		}
		log.info("JQA2JSON has finished.");
	}

	@Override
	public boolean checkRequirements() {
		return languages.contains(ProgrammingLanguage.JAVA);
	}

// ToDo Anpassen: Chapter fehlt      			
	private String toJSON(List<Node> list) {
		StringBuilder builder = new StringBuilder();
		boolean hasElements = false;
		for (final Node el : list) {
			if (!hasElements) {
				hasElements = true;
				builder.append("[{");
			} else {
				builder.append("\n},{");
			}
			if (el.hasLabel(Labels.Specification.name()) || el.hasLabel(Labels.Section.name())) {
				builder.append(toMetaDataDistrict(el));
				builder.append("\n");
			} else { {
				builder.append(toMetaDataRequirement(el));
				builder.append("\n");
			}}

 /*Ab hier glaube ich unnötig
			if ((el.hasLabel(Labels.Type.name()) && el.hasLabel(Labels.Annotation.name()))) {
				builder.append(toMetaDataAnnotation(el));
				builder.append("\n");
			}
			if ((el.hasLabel(Labels.Type.name()) && el.hasLabel(Labels.Enum.name()))) {
				builder.append(toMetaDataEnum(el));
				builder.append("\n");
			}
			if (el.hasLabel(Labels.Method.name())) {
				builder.append(toMetaDataMethod(el));
				builder.append("\n");
			}
			if ((el.hasLabel(Labels.Field.name()) && (!el.hasLabel(Labels.Enum.name())))) {
				builder.append(toMetaDataAttribute(el));
			}
			if ((el.hasLabel(Labels.Field.name()) && el.hasLabel(Labels.Enum.name()))) {
				builder.append(toMetaDataEnumValue(el));
				builder.append("\n");
			}
*/
		}
		if (hasElements) {
			builder.append("}]");
		}
		return builder.toString();
	}

	private String toMetaDataDistrict(Node district) {
		log.info("District has been called ");
		List<Record> parentHash = connector
			.executeRead("MATCH (parent)-[:IS_PARENT_OF]->(district) WHERE ID(district) = " + district.id()
			+ " RETURN  parent");
		String belongsTo = "root"; 
		if (!parentHash.isEmpty()) {
			belongsTo = parentHash.get(0).get("parent").asNode().get("hash").asString(); 
		}

		log.info("Processing district with ID: " + district.id());
        log.info("getavizOrder value: " + district.get("getavizOrder"));

		return "\"id\":            \"" + district.get("hash").asString() + "\"," +
			"\n" +
			"\"qualifiedName\": \"" + district.get("fqn").asString() + "\"," +
			"\n" +
			"\"name\":          \"" + district.get("name").asString() + "\"," +
			"\n" +
			"\"type\":          \"FAMIX.Namespace\"," + 
			"\n" +
			"\"subClassOf\":    \"" + getInboundLinkDistrict(district) + "\"," + //! Nur die Links der Sections anzeigen
			"\n" +																//! Oder die Links der auf den Platten liegenden Anforderungen
			"\"superClassOf\":  \"" + getOutboundLinkDistrict(district) + "\"," +
			"\n" +
			"\"belongsTo\":     \"" + belongsTo + "\"," +
			"\n" +
			"\"nodeID\":     \"" + district.get("getavizOrder") + "\"" +
			"\n";
	}

	private String toMetaDataRequirement(Node requirement) { //? Gibt es vorraussetzungen was für ein Label das belongsTo element haben muss ??
		String belongsTo = "Wenn du das siehts ist was falsch"; //Initialisierung entfernen
		List<Record> parent = connector
				.executeRead("MATCH (parent)-[:IS_PARENT_OF]->(requirement) WHERE ID(requirement) = " + requirement.id() + " RETURN parent");
		if (!parent.isEmpty()) {
			belongsTo = parent.get(0).get("parent").asNode().get("hash").asString();
		} 
		
//! Entweder Parent= Chapter oder Parent= District 
//! Ooder Paren= ElternElement, Parent= Chapter und dann erst Parent= District

		return "\"id\":            \"" + requirement.get("hash").asString() + "\"," +
				"\n" +
				"\"qualifiedName\": \"" + requirement.get("fqn").asString() + "\"," +
				"\n" +
				"\"name\":          \"" + requirement.get("name").asString() + "\"," +
				"\n" +
				"\"type\":          \"FAMIX.Class\"," +
				"\n" +
				"\"modifiers\":     \"" +   "\"," + 	//!"getModifiers(requirement)" - wurde gelöscht	//getModifiers könnte für Farben benutzt werden
				"\n" + //* Werden für Beziehungen verwendet glaube ich
				"\"subClassOf\":    \"" + getInboundLink(requirement) + "\"," +
				"\n" +
				"\"superClassOf\":  \"" + getOutboundLink(requirement) + "\"," +
				"\n" +
				"\"belongsTo\":     \"" + belongsTo + "\"," +
				"\n" +
				"\"nodeID\":     \"" + requirement.get("getavizOrder") + "\"" +
				"\n";
				
	}

//? Wird das gebraucht um bspw. Beziehungen zwischen Anforderungen darzustellen ?
	/*		 
	private String toMetaDataAttribute(Node attribute) {
		String belongsTo = "";
		String declaredType = "";
		Result parent = connector
				.executeRead("MATCH (parent)-[:CONTAINS|DECLARES]->(attribute) WHERE ID(attribute) = " + attribute.id()
						+ " RETURN parent.hash");
		if (parent.hasNext()) {
			belongsTo = parent.single().get("parent.hash").asString();
		}
		Node type = connector
				.executeRead("MATCH (attribute)-[:OF_TYPE]->(t) WHERE ID(attribute) = " + attribute.id() + " RETURN t")
				.next().get("t").asNode();
		if (type != null) {
			declaredType = type.get("name").asString();
		}
		return "\"id\":            \"" + attribute.get("hash").asString() + "\"," +
				"\n" +
				"\"qualifiedName\": \"" + attribute.get("fqn").asString() + "\"," +
				"\n" +
				"\"name\":          \"" + attribute.get("name").asString() + "\"," +
				"\n" +
				"\"type\":          \"FAMIX.Attribute\"," +
				"\n" +
				"\"modifiers\":     \"" + getModifiers(attribute) + "\"," +
				"\n" +
				"\"declaredType\":  \"" + declaredType + "\"," +
				"\n" +
				"\"accessedBy\":\t \"" + getAccessedBy(attribute) + "\"," +
				"\n" +
				"\"belongsTo\":     \"" + belongsTo + "\"" +
				"\n";
	}
*/

	private String getInboundLink(Node element) {
		ArrayList<String> tmp = new ArrayList<>();
		List <Record> inboundLinkResult = connector.executeRead("MATCH (sub:Requirement)-[:LINKS_TO]->(element) WHERE ID(element) = " + element.id() + " RETURN sub");
		for (Record result : inboundLinkResult) {
			Node node = result.get("sub").asNode();
			if(node.containsKey("hash")) {
				tmp.add(node.get("hash").asString());
			}
		};
		Collections.sort(tmp);
		return removeBrackets(tmp);
	}

	private String getOutboundLink(Node element) {
		ArrayList<String> tmp = new ArrayList<>();
		List <Record> outboundLinkResult = connector.executeRead("MATCH (req)-[:LINKS_TO]->(node) WHERE ID(req) = " + element.id() + " RETURN node");
		for (Record result : outboundLinkResult) {
		Node node = result.get("node").asNode();
			if(node.containsKey("hash")) {
				tmp.add(node.get("hash").asString());
			}
		};
		Collections.sort(tmp);
		return removeBrackets(tmp);
	}

	private String getInboundLinkDistrict(Node element) {
		ArrayList<String> tmp = new ArrayList<>();
		List <Record> inboundLinkResult = connector.executeRead("MATCH (district)-[:VISUALISES]->(element)<-[:LINKS_TO]-(node) WHERE ID(district) = " + element.id() + " RETURN node");
		for (Record result : inboundLinkResult) {
			Node node = result.get("node").asNode();
			if(node.containsKey("hash")) {
				tmp.add(node.get("hash").asString());
			}
		};

		List <Record> childsInboundLinkResults = connector.executeRead(
            "MATCH (district:Section)-[:IS_PARENT_OF*]->(child) " +
			"MATCH (child)-[:VISUALIZES]-(element)<-[:LINKS_TO*]-(source) " +
            "WHERE ID(district) = " + element.id() + " " +
            "RETURN collect(source.hash) AS hashes"
        );
		if (!childsInboundLinkResults.isEmpty()) {
            Record record = childsInboundLinkResults.get(0);
            List<String> hashes = record.get("hashes").asList(Value::asString);
            for (String hash : hashes) {
                tmp.add(hash);
            }
        }
		Collections.sort(tmp);
		return removeBrackets(tmp);
	}

	private String getOutboundLinkDistrict(Node element) {
		ArrayList<String> tmp = new ArrayList<>();
		List <Record> outboundLinkResult = connector.executeRead("MATCH (district)-[:VISUALISES]->(element)-[:LINKS_TO]->(node) WHERE ID(district) = " + element.id() + " RETURN node");
		for (Record result : outboundLinkResult) {
			Node node = result.get("node").asNode();
			if(node.containsKey("hash")) {
				tmp.add(node.get("hash").asString());
			}
		};

		List <Record> childsOutboundLinkResults = connector.executeRead(
            "MATCH (district)-[:IS_PARENT_OF*]->(child) " +
			"MATCH (child)-[:VISUALIZES]-(element)-[:LINKS_TO*]->(target) " +
            "WHERE ID(district) = " + element.id() + " " +
            "RETURN collect(target.hash) AS hashes"
        );
		if (!childsOutboundLinkResults.isEmpty()) {
            Record record = childsOutboundLinkResults.get(0);
            List<String> hashes = record.get("hashes").asList(Value::asString);
            for (String hash : hashes) {
                tmp.add(hash);
            }
        }
		Collections.sort(tmp);
		return removeBrackets(tmp);
	}
	// Könnte man benutzen um Anforderungen mit bestimmten Attributen eine Farbe zu geben, 
	//*ne das ist für was anderes
/* 
	private String getModifiers(Node element) {
		ArrayList<String> tmp = new ArrayList<>();
		if (element.containsKey("visibility")) {
			tmp.add(element.get("visibility").asString());
		}
		if (element.containsKey("final")) {
			if (element.get("final").asBoolean()) {
				tmp.add("final");
			}
		}
		if (element.containsKey("abstract")) {
			if (element.get("abstract").asBoolean()) {
				tmp.add("abstract");
			}
		}
		if (element.containsKey("static")) {
			tmp.add("static");
		}
		Collections.sort(tmp);
		return removeBrackets(tmp);
	}
*/
	private String removeBrackets(List<String> list) {
		return removeBrackets(list.toString());
	}

	private String removeBrackets(String string) {
		return StringUtils.remove(StringUtils.remove(string, "["), "]");
	}
}


