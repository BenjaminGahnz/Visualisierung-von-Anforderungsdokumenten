package org.getaviz.generator.city.s2m;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.getaviz.generator.ProgrammingLanguage;
import org.getaviz.generator.SettingsConfiguration;
import org.getaviz.generator.SettingsConfiguration.BuildingType;
import org.getaviz.generator.SettingsConfiguration.ClassElementsModes;
import org.getaviz.generator.SettingsConfiguration.Original.BuildingMetric;
import org.getaviz.generator.Step;
import org.getaviz.generator.database.DatabaseConnector;
import org.getaviz.generator.database.Labels;
import org.neo4j.driver.Record;
import org.neo4j.driver.Result;
import org.neo4j.driver.types.Node;

import java.util.GregorianCalendar;
import java.util.List;

//! Wie stelle ich sicher das Chapters nicht doppelt aufgerufen werden in enchanceNode????

public class JQA2City implements Step {
	private Log log = LogFactory.getLog(this.getClass());
	private DatabaseConnector connector = DatabaseConnector.getInstance();
	private ClassElementsModes classElementsMode;
	private String buildingTypeAsString;
	private BuildingType buildingType;
	private BuildingMetric originalBuildingMetric;
	private List<ProgrammingLanguage> languages;

	public JQA2City(SettingsConfiguration config, List<ProgrammingLanguage> languages) {
		this.classElementsMode = config.getClassElementsMode();
		this.buildingTypeAsString = config.getBuildingTypeAsString();
		this.buildingType = config.getBuildingType();
		this.originalBuildingMetric = config.getOriginalBuildingMetric();
		this.languages = languages;
	}

	@Override
	public boolean checkRequirements() {
		return languages.contains(ProgrammingLanguage.JAVA);
	}

	public void run() {
		log.info("JQA2City started");
		connector.executeWrite("MATCH (n:City) DETACH DELETE n");
		long model = connector.addNode(
				String.format("CREATE (n:Model:City {date: '%s', building_type: '%s'})",
						new GregorianCalendar().getTime().toString(), buildingTypeAsString),"n").id();
		List<Record> SpecResults = connector.executeRead(
			"MATCH (n:Specification) " + // ToDo: drauf achten das Chapter CONTAINS Beziehung zur Specification hat!
			"RETURN n"
		);
		
		for (Record result : SpecResults) {
			long specification = result.get("n").asNode().id();
			nodeToDistrict(specification, model);
		}
		log.info("JQA2City finished");
	}
// ToDo: Sicher Stellen das Requirements nicht von Spezidication UND Chapter aufgerufen wird
//! DAS IST SUPER WICHTIG
	private void nodeToDistrict(Long node , Long parent) {
		long district = connector.addNode(cypherCreateNode(parent,node,Labels.District.name()),"n").id();
		//!ÄNdern
		List<Record> subDistricts = connector.executeRead("MATCH (n)-[:IS_PARENT_OF]->(p:Section) WHERE ID(n) = " + node + " RETURN p");
		List<Record> subRequirements = connector.executeRead("MATCH (n)-[:IS_PARENT_OF]->(t:Requirement) WHERE NOT 'Section' in labels(t) AND ID(n) = " + node + " RETURN t");
		for (Record result : subDistricts) {
			nodeToDistrict(result.get("p").asNode().id(), district);
		}
		for (Record result : subRequirements) {
			requirementToBuilding(result.get("t").asNode().id(), district);
		}
	}

	private void requirementToBuilding(Long requirementId, Long parent) {
		long buildingId = connector.addNode(cypherCreateNode(parent, requirementId, Labels.Building.name()),"n").id();
		setNumberOfLinks(requirementId, buildingId);
		setNumberOfProperties(requirementId, buildingId);

		//* Wichtig weil Requirements können auch weitere Sub Requirements/Districts haben
		List<Record> subDistricts = connector.executeRead("MATCH (n)-[:IS_PARENT_OF]->(p:Section) WHERE ID(n) = " + requirementId + " RETURN p");
		List<Record> subRequirements = connector.executeRead("MATCH (n)-[:IS_PARENT_OF]->(t:Requirement) WHERE NOT 'Section' in labels(t) AND ID(n) = " + requirementId + " RETURN t");
		for (Record result : subDistricts) {
			nodeToDistrict(result.get("p").asNode().id(), buildingId);
		}
		for (Record result : subRequirements) {
			requirementToBuilding(result.get("t").asNode().id(), buildingId);
		}

		// ? Ich glaube das wird nicht gebraucht, sondern nur in der City_Panels Metaphor 
		/*if (originalBuildingMetric == BuildingMetric.NOS) {
			int numberOfAttributes = getNodePropertyCount(building);
				connector.executeWrite("MATCH(n) WHERE ID(n) = " + building + " SET n.numberOfStatements = " +
					numberOfAttributes);
			}*/
		}

	private void setNumberOfProperties(Long requirementId, Long buildingId) {
		// Query to count the properties of the requirement
		String countQuery = "MATCH (n) WHERE ID(n) = " + requirementId + " RETURN size(keys(n)) AS propertyCount";
		List<Record> countResult = connector.executeRead(countQuery);
		int numberOfProperties = 0;
		if (!countResult.isEmpty()) {
    	numberOfProperties = countResult.get(0).get("propertyCount").asInt();
		}
		String setQuery = "MATCH (n) WHERE ID(n) = " + buildingId + " SET n.numberOfProperties = " + numberOfProperties;
		connector.executeWrite(setQuery);
		}
	
	private void setNumberOfLinks(Long requirementId, Long buildingId) {
		
			String countQuery = "MATCH (n)-[:LINKS_TO]->() WHERE ID(n) = " + requirementId + " RETURN count(*) AS linkCount";
			List<Record> countResult = connector.executeRead(countQuery);
			int numberOfLinks = 0;
			if (!countResult.isEmpty()) {
				numberOfLinks = countResult.get(0).get("linkCount").asInt();
			}
			String linksQuery = "MATCH (n) WHERE ID(n) = " + buildingId + " SET n.numberOfLinks = " + numberOfLinks;
			connector.executeWrite(linksQuery);
			}

	private String cypherCreateNode(Long parent, Long visualizedNode, String label) {
		return String.format(
			"MATCH(parent),(s) WHERE ID(parent) = %d AND ID(s) = %d CREATE (parent)-[:CONTAINS]->(n:City:%s)-[:VISUALIZES]->(s)",
			parent, visualizedNode, label);
	}
}
