package org.getaviz.generator.city;

import org.getaviz.generator.SettingsConfiguration;
import org.getaviz.generator.city.m2m.BuildingSegmentComparator;
import org.getaviz.generator.database.DatabaseConnector;
import org.getaviz.generator.database.Labels;
import org.neo4j.driver.Result;
import org.neo4j.driver.types.Node;
import org.neo4j.driver.Record;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class CityUtils {

	private static SettingsConfiguration config = SettingsConfiguration.getInstance();
	private static DatabaseConnector connector = DatabaseConnector.getInstance();

	public static String setBuildingSegmentColor(Node relatedEntity) {
		String color;
		String visibility = relatedEntity.get("visibility").asString("");
		switch (config.getScheme()) {
			case VISIBILITY:
				switch (visibility) {
					case "public":
						color = config.getCityColor("dark_green");
						break;
					case "protected":
						color = config.getCityColor("yellow");
						break;
					case "private":
						color = config.getCityColor("red");
						break;
					default:
						// Package visibility or default
						color = config.getCityColor("blue");
						break;
				}
				break;
			case TYPES:
				if(relatedEntity.hasLabel(Labels.Field.name())) {
					color = setAttributeColor(relatedEntity.id());
				} else if(relatedEntity.hasLabel(Labels.Method.name())) {
					color = setMethodColor(relatedEntity);
				} else {
					color =  config.getCityColor("blue");
				}
				break;
			default:
				color = config.getCityColor("blue");
		}

		return color;
	}	

	private static String setAttributeColor(long relatedEntity) {
		String color;
		List<Record> primitivRecord  = connector.executeRead("MATCH (n)-[OF_TYPE]->(t:Primitive) WHERE ID(n) = " + relatedEntity + " RETURN t");
		if(primitivRecord.size() > 0) {
			color = config.getCityColor("pink");
		} else { // complex type
			color = config.getCityColor("aqua");
		}
		return color;
	}
	

	private static String setMethodColor(Node relatedEntity) {
		String color;
		boolean isStatic = relatedEntity.get("static").asBoolean(false);
		boolean isAbstract = relatedEntity.get("abstract").asBoolean(false);
	
		if (relatedEntity.hasLabel(Labels.Constructor.name())) {
			color = config.getCityColor("red");
		} else if (relatedEntity.hasLabel(Labels.Getter.name())) {
			color = config.getCityColor("light_green");
		} else if (relatedEntity.hasLabel(Labels.Setter.name())) {
			color = config.getCityColor("dark_green");
		} else if (isStatic) {
			color = config.getCityColor("yellow");
		} else if (isAbstract) {
			color = config.getCityColor("orange");
		} else {
			// Default
			color = config.getCityColor("violet");
		}
		return color;
	}

	/**
	 * Sorting the BuildingSegments with help of
	 * {@link BuildingSegmentComparator} based on sorting settings
	 * 
	 * @param segments BuildingSegments which are to be sorted.
	 *
	 */
	
	public static void sortBuildingSegments(final List<Node> segments) {
		final List<BuildingSegmentComparator> sortedList = new ArrayList<>(segments.size());
		for (Node segment : segments)
			sortedList.add(new BuildingSegmentComparator(segment));
		Collections.sort(sortedList);
		segments.clear();
		for (BuildingSegmentComparator bsc : sortedList)
			segments.add(bsc.getSegment());
	}
	
	public static List<Node> getChildren(Long parent) {
		ArrayList<Node> children = new ArrayList<>();
		List<Record> childs = connector.executeRead("MATCH (n)-[:IS_PARENT_OF]->(child) WHERE ID(n) = " + parent + " RETURN child");
		for (Record child : childs) {
			children.add(child.get("child").asNode());
		}
		return children;
	}

	 //! Ich hab doch keine Methoden ode Fields wofür ist das ??
	public static List<Node> getMethods(Long building) {
		ArrayList<Node> methods = new ArrayList<>();
		List<Record> bsResult = connector.executeRead("MATCH (n)-[:CONTAINS]->(bs:BuildingSegment)-[:VISUALIZES]->(m:Method) WHERE ID(n) = " + building + " RETURN bs");
		for (Record record : bsResult) {
			methods.add(record.get("bs").asNode());
		}
		return methods;
	}
	
	public static List<Node> getData(Long building) {
		ArrayList<Node> data = new ArrayList<>();
		List<Record> dataResult = connector.executeRead("MATCH (n)-[:CONTAINS]->(bs:BuildingSegment)-[:VISUALIZES]->(f:Field) WHERE ID(n) = " + building + " RETURN bs");
		for (Record record : dataResult) {
			data.add(record.get("bs").asNode());
		}
		return data;
	}
}