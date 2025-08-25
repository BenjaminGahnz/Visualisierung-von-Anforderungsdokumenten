package org.getaviz.generator.city.m2t;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.getaviz.generator.SettingsConfiguration;
import org.getaviz.generator.SettingsConfiguration.BuildingType;
import org.getaviz.generator.Step;
import org.getaviz.generator.database.DatabaseConnector;
import org.getaviz.generator.database.Labels;
import org.getaviz.generator.output.AFrame;
import org.neo4j.driver.types.Node;
import org.neo4j.driver.Record;


import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

//ToDo!: der HTML Header wird multible male geprintet, das muss unterbunden werden 

//ToDo Unnötige Teile des Programms enfernen!

public class City2AFrame implements Step {
	private DatabaseConnector connector = DatabaseConnector.getInstance();
	private Log log = LogFactory.getLog(this.getClass());
	private BuildingType buildingType;
	private String outputPath;
	private String buildingTypeAsString;
	private boolean showAttributesAsCylinders;
	private double panelSeparatorHeight;
	private String color;
	private boolean showBuildingBase;
	private AFrame outputFormat;
	private SettingsConfiguration.OutputFormat format;


	public City2AFrame(SettingsConfiguration config) {
		this.buildingType = config.getBuildingType();
		this.outputPath = config.getOutputPath();
		this.buildingTypeAsString = config.getBuildingTypeAsString();
		this.showAttributesAsCylinders = config.isShowAttributesAsCylinders();
		this.panelSeparatorHeight = config.getPanelSeparatorHeight();
		this.color = config.getCityColor("black");
		this.showBuildingBase = config.isShowBuildingBase();
		this.outputFormat = new AFrame();
		this.format = config.getOutputFormat();
	}

	public void run() {
		log.info("City2AFrame has started");
		FileWriter fw = null;
		String fileName = "model.html";

		try {
			log.info("Before calling toAFrameModel");
			String modelContent = toAFrameModel();
			log.info("Model content generated");


			fw = new FileWriter(outputPath + fileName, false); //* false = overwrite orginal war true!
			fw.write(outputFormat.head());
			fw.write(modelContent);
			fw.write(outputFormat.tail());
		
		} catch (IOException e) {
			log.error("Could not create file", e);
		} finally {
			
			if (fw != null)
				try {
					fw.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			else {
				log.error("FileWriter is null");
			}	
		}
		log.info("City2AFrame has finished");
	}

	@Override
	public boolean checkRequirements() {
		return format.equals(SettingsConfiguration.OutputFormat.AFrame);
	}

	private String toAFrameModel() {
		log.info("Entering toAFrameModel method");
	
		StringBuilder districts = new StringBuilder();
		StringBuilder buildings = new StringBuilder();
		StringBuilder segments = new StringBuilder();
	
		try{
		log.info("Starting to fetch district records");
	
		List<Record> districtRecords = connector.executeRead(
			"MATCH (n:Model)-[:CONTAINS*]-(d:District)-[:HAS]->(p:Position) RETURN d,p");
	
		log.info("Fetched " + districtRecords.size() + " district records");
	
		for (Record record : districtRecords) {
			districts.append(toDistrict(record.get("d").asNode(), record.get("p").asNode()));
		}
	
		if (buildingType == BuildingType.CITY_ORIGINAL || showBuildingBase) {
			log.info("Building base is shown or City Original");
			List<Record> buildingRecords = connector.executeRead(
					"MATCH (n:Model)-[:CONTAINS*]-(b:Building)-[:HAS]->(p:Position) RETURN b,p");
			/*List<Record> buildingRecords = connector.executeRead(
				"MATCH (n:Model)-[:CONTAINS*]-(b:Building)-[:HAS]->(p:Position) WHERE n.building_type = '"
						+ buildingTypeAsString + "' RETURN b,p");*/
			for (Record record : buildingRecords) {
				buildings.append(toBuilding(record.get("b").asNode(), record.get("p").asNode()));
			}
		}
		log.info("Exiting toAFrameModel method with " + districts.toString() + buildings.toString() + segments.toString());
		} catch (Exception e) {
		log.error("Error in toAFrameModel method", e);
	}
		return districts.toString() + buildings.toString() + segments;
	}
/* 
	private String toDistrict(Node district, Node position) {
		Node entity = connector.getVisualizedEntity(district.id());
		return "<a-box id=\"" + entity.get("hash").asString() + "\"" +
				"\n" +
				"\t position=\"" + position.get("x") + " " + position.get("y") + " " + position.get("z") + "\"" +
				"\n" +
				"\t width=\"" + district.get("width") + "\"" +
				"\n" +
				"\t height=\"" + district.get("height") + "\"" +
				"\n" +
				"\t depth=\"" + district.get("length") + "\"" +
				"\n" +
				"\t color=\"" + district.get("color").asString() + "\">" +
				"\n" +
				"</a-box>" +
				"\n";
	}

	private String toBuilding(Node building, Node position) {
		Node entity = connector.getVisualizedEntity(building.id());
		return "<a-box id=\"" + entity.get("hash").asString() + "\"" +
				"\t\t position=\"" + position.get("x") + " " + position.get("y") + " " + position.get("z") + "\"" +
				"\n" +
				"\t\t width=\"" + building.get("width") + "\"" +
				"\n" +
				"\t\t height=\"" + building.get("height") + "\"" +
				"\n" +
				"\t\t depth=\"" + building.get("length") + "\"" +
				"\n" +
				"\t\t color=\"" + building.get("color").asString() + "\">" +
				"\n" +
				"</a-box>" +
				"\n";
	} */


/* 
private String toDistrict(Node district, Node position) {
	Node entity = connector.getVisualizedEntity(district.id());

	return "<a-box id=\"" + entity.get("hash").asString() + "\"" +
			"\n" +
			"\t position=\"" + position.get("x") + " " + position.get("y") + " " + position.get("z") + "\"" +
			"\n" +
			"\t width=\"" + district.get("width") + "\"" +
			"\n" +
			"\t height=\"" + district.get("height") + "\"" +
			"\n" +
			"\t depth=\"" + district.get("length") + "\"" +
			"\n" +
			"\t color=\"" + district.get("color").asString() + "\"" + ">" +
			"\n" +
			"<a-entity class=\"DistrictLabel\"" +
			"\n" +
			"\t geometry=\"primitive: plane; width: " + district.get("width").asDouble() * 0.75 + "; height: " + district.get("length").asDouble()*0.03 + ";\"" +
			"\n" +
			"\t position=\"" + district.get("width").asDouble() * -0.45 + " " + (district.get("height").asDouble() * 0.5 - 0.001) + " " + (district.get("length").asDouble() * -0.475) + "\"" +
			"\n" +
			"\t rotation=\"-90 0 0\"" +
			"\n" +
			"\t material=\"opacity: 0\"" +
			"\n" +
			"\t text=\"value: " + getDistrictLabelName(entity.get("name").asString()) + "; " +
			"color: black; " +
			"wrap-count: 25; " +
			"position: 0 0.002 0; " +
			"anchor: left;\"" +
			"\n" +
			">" +
			"\n" +
			"</a-entity>" + 
			"\n" +
			"</a-box>";
	}*/

private String getDistrictLabelName (String name){
	if ( name.length() > 25) {
		name= name.substring(0, 21) + "...";
	}
	return name;
}




private String toBuilding(Node building, Node position) {
	Node entity = connector.getVisualizedEntity(building.id());
return "<a-box id=\"" + entity.get("hash").asString() + "\"" +
"\t\t position=\"" + position.get("x") + " " + position.get("y") + " " + position.get("z") + "\"" +
"\n" +
"\t\t width=\"" + building.get("width") + "\"" +
"\n" +
"\t\t height=\"" + building.get("height") + "\"" +
"\n" +
"\t\t depth=\"" + building.get("length") + "\"" +
"\n" +
"\t\t color=\"" + building.get("color").asString() + "\">" +
"\n" +
"<a-text class=\"BuildingLabel\""  + 
"\n" +
"value=\"" + getBuildingLabelName(entity.get("ReqIF.ForeignID").asString())  + "\"" +
"\n" +
"\t position=\"" + "0" + " " + (0.5*building.get("height").asDouble()+0.001) + " " + "0" + "\"" +
"\n" +
"\t rotation=\"-90 0 0 \"" +
"\n" +
"\t anchor=\"center\"" +
"\n" + 
"\t align=\"center\"" +
"\n" +
"\t color=\"white\"" +
"\n" +
"\t width=\"" + building.get("width").asDouble()*0.9 + "\"" +
"\n" +
"\t hight=\"" +  building.get("length").asDouble() *0.8 + "\""  +
"\n" +
"\t wrap-count=\"10 \"" + ">" +
"\n" +
"</a-text>" + 
"\n"  +
"</a-box>" +
"\n";
}

private String getBuildingLabelName (String name){
	if ( name.length() > 10) {
		name= extractNumbers (name);
	}
	return name;
}

public static String extractNumbers(String name) {
	StringBuilder numbers = new StringBuilder();
	for (char c : name.toCharArray()) {
		if (Character.isDigit(c)) {
			numbers.append(c);
		}
	}
	String label = numbers.toString();
	if (label.length() > 10) {
		label = label.substring(0, 6) + "...";
	}
	return label;

}


//? Neues ToDistrict:
/* 

*/		




private String toDistrict(Node district, Node position) {
	Node entity = connector.getVisualizedEntity(district.id());

	return "<a-box id=\"" + entity.get("hash").asString() + "\"" +
			"\n" +
			"\t position=\"" + position.get("x") + " " + position.get("y") + " " + position.get("z") + "\"" +
			"\n" +
			"\t width=\"" + district.get("width") + "\"" +
			"\n" +
			"\t height=\"" + district.get("height") + "\"" +
			"\n" +
			"\t depth=\"" + district.get("length") + "\"" +
			"\n" +
			"\t color=\"" + district.get("color").asString() + "\"" + ">" +
			"\n" +
			"<a-text" + 
			"\n" +
			"value=\"" + getDistrictLabelName(entity.get("name").asString()) + "\"" +
			"\n" +
			"\t position=\"" + district.get("width").asDouble()*-0.45 + " " + (district.get("height").asDouble()*0.5+0.001) + " " + (district.get("length").asDouble()*-0.47 + 1.5) + "\"" +
			"\n" +
			"\t rotation=\"-90 0 0 \"" + 
			"\n" +						 
			"\t anchor=\"left\"" +		 
			"\n" + 
			"\t color=\"black\"" +
			"\n" +
			"\t width=\"" + district.get("width").asDouble() *0.75 + "\"" +
			"\n" +
			"\t wrap-count=\"25\"" + ">" +
			"\n" +
			"</a-text>" + 
			"\n" +
			"</a-box>";


			/*
	private String toDistrict(Node district, Node position) {
			Node entity = connector.getVisualizedEntity(district.id());

			return "<a-box id=\"" + entity.get("hash").asString() + "\"" +
			"\n" +
			"\t position=\"" + position.get("x") + " " + position.get("y") + " " + position.get("z") + "\"" +
			"\n" +
			"\t width=\"" + district.get("width") + "\"" +
			"\n" +
			"\t height=\"" + district.get("height") + "\"" +
			"\n" +
			"\t depth=\"" + district.get("length") + "\"" +
			"\n" +
			"\t color=\"" + district.get("color").asString() + "\"" + ">" +
			"\n" +
			"<a-text" + 
			"\n" +
			"value=\"" + getDistrictLabelName(entity.get("name").asString()) + "\"" +
			"\n" +
			"\t position=\"" + district.get("width").asDouble()* 0.45 + " " + (district.get("height").asDouble()*0.5+0.001) + " " + (district.get("length").asDouble()*0.47 + 1.5) + "\"" +
			"\n" +
			"\t rotation=\"-90 0 0 \"" + 
			"\n" +						 
			"\t anchor=\"left\"" +		 
			"\n" + 
			"\t color=\"black\"" +
			"\n" +
			"\t width=\"" + checkHeightLabel(district.get("width").asDouble(),district.get("height").asDouble()) *0.75 + "\"" +
			"\n" +
			"\t wrap-count=\"25\"" + ">" +
			"\n" +
			"</a-text>" + 
			"\n" +
			"</a-box>";
			
}
private double checkHeightLabel(double width, double height) {
	double heightText = ((width*0.75) / 484.5) * 41;
	double maxwidth = width;

	if (heightText <= height) {
		return width;
	} else {
        return Math.min((heightText / (0.084 * 0.75)), maxwidth) ;
    }
	}
}

		



			 */
			
} }