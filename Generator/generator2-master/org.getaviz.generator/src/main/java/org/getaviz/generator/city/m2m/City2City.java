package org.getaviz.generator.city.m2m;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.getaviz.generator.ColorGradient;
import org.getaviz.generator.SettingsConfiguration;
import org.getaviz.generator.SettingsConfiguration.BuildingType;
import org.getaviz.generator.SettingsConfiguration.ClassElementsModes;
import org.getaviz.generator.SettingsConfiguration.Original.BuildingMetric;
import org.getaviz.generator.SettingsConfiguration.Panels.SeparatorModes;
import org.getaviz.generator.Step;
import org.getaviz.generator.city.CityUtils;
import org.getaviz.generator.database.DatabaseConnector;
import org.getaviz.generator.database.Labels;
import org.neo4j.driver.Record;
import org.neo4j.driver.Result;
import org.neo4j.driver.types.Node;
//import org.neo4j.driver.v1.types.Path;
import org.neo4j.driver.types.Path;

import java.util.Map;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.stream.Collectors;
import java.util.Locale;
import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;


// ToDo: Wo werden Length und Width von Districts gesetzt ?

public class City2City implements Step {
	private Log log = LogFactory.getLog(this.getClass());
	private List<String> PCKG_colors;
	private List<String> NOS_colors;
	private HashMap<Long, double[]> properties = new HashMap<>();
	private DatabaseConnector connector = DatabaseConnector.getInstance();

	private String packageColorStart;
	private String packageColorEnd;
	private static int colorPairIndex = 0;
	private static final Map<Long, List<String>> districtColors = new HashMap<>();
	private static final List<String[]> predefinedColorPairs = Arrays.asList(
		new String[]{"#ADD8E6", "#4169E1"}, // Light Blue, Royal Blue
		new String[]{"#90EE90", "#008000"}, // Light Green, Green
		new String[]{"#EE82EE", "#8A2BE2"}, // Light Violet, Violet
		new String[]{"#FFB6C1", "#FF69B4"}, // Light Pink, Pink
		new String[]{"#FFA07A", "#FF4500"}, // Light Orange, Orange
		new String[]{"#FFFACD", "#FFD700"}  // Light Yellow, Yellow
		);
	


	private BuildingType buildingType;
	private String buildingTypeAsString;
	private BuildingMetric originalBuildingMetric;
	private String classColorStart;
	private String classColorEnd;
	private String classColor;
	private String floorColor;
	private String chimneyColor;
	private boolean showBuildingBase;

	private double heightMin;
	private double widthMin;

	private ClassElementsModes classElementsMode;
	private double panelHorizontalMargin;
	private int[] panelHeightTresholdNos;
	private double panelHeightUnit;
	private double panelVerticalMargin;
	private SeparatorModes panelSeparatorMode;
	private double panelVerticalGap;
	private double panelSeparatorHeight;

	private SettingsConfiguration.Bricks.Layout brickLayout;
	private double brickSize;
	private double brickHorizontalMargin;
	private double brickHorizontalGap;

	private boolean showAttributesAsCylinders;


	public City2City(SettingsConfiguration config) {
		this.buildingType = config.getBuildingType();
		this.buildingTypeAsString = config.getBuildingTypeAsString();
		this.packageColorStart = config.getPackageColorStart();
		this.packageColorEnd = config.getPackageColorEnd();
		this.originalBuildingMetric = config.getOriginalBuildingMetric();
		this.classColorStart = config.getClassColorStart();
		this.classColorEnd = config.getClassColorEnd();
		this.floorColor = config.getCityFloorColor();
		this.chimneyColor = config.getCityChimneyColor();
		this.heightMin = config.getHeightMin();
		this.widthMin = config.getWidthMin();
		this.classColor = config.getClassColor();
		this.showBuildingBase = config.isShowBuildingBase();
		this.classElementsMode = config.getClassElementsMode();
		this.panelHorizontalMargin = config.getPanelHorizontalMargin();
		this.brickLayout = config.getBrickLayout();
		this.brickSize = config.getBrickSize();
		this.brickHorizontalMargin = config.getBrickHorizontalMargin();
		this.brickHorizontalGap = config.getBrickHorizontalGap();
		this.panelHeightTresholdNos = config.getPanelHeightTresholdNos();
		this.panelHeightUnit = config.getPanelHeightUnit();
		this.panelVerticalMargin = config.getPanelVerticalMargin();
		this.panelSeparatorMode = config.getPanelSeparatorMode();
		this.panelVerticalGap = config.getPanelVerticalGap();
		this.panelSeparatorHeight = config.getPanelSeparatorHeight();
		this.showAttributesAsCylinders = config.isShowAttributesAsCylinders();
	}

	@Override
	public boolean checkRequirements() {
		return true;
	}

	public void run() {
		log.info("City2City started");
		List<Record> modelResult = connector.executeRead("MATCH (n:Model {building_type: '" + buildingTypeAsString + "'}) RETURN n");
		Node model = null;
		if (!modelResult.isEmpty()) {
			model = modelResult.get(0).get("n").asNode();
		}
		// Erzeugt ColorGradient basierend auf Max District Tiefe
/* 		List<Record> districtMaxLevelResult = connector.executeRead(
		"MATCH p=(n:District)-[:CONTAINS*]->(m:District) WHERE NOT (m)-[:CONTAINS]->(:District) RETURN length(p) AS length ORDER BY length(p) DESC LIMIT 1");
		int districtMaxLevel = 1; //Mit 0 funktioniert es nicht
		if (!districtMaxLevelResult.isEmpty()) {
			districtMaxLevel = districtMaxLevelResult.get(0).get("length").asInt() + 1;
		}
		PCKG_colors = ColorGradient.createColorGradient(packageColorStart, packageColorEnd, districtMaxLevel);
*/
		getDistrictsColors();





		// Erzeugt ColorGradient basierend auf Max Number of Statements
		if (originalBuildingMetric == BuildingMetric.NOS) {
			List<Record> NOSMaxResult = connector.executeRead(
			"MATCH (n:Building) RETURN max(n.numberOfStatements) AS nos"
			);
			int NOS_max = 0;
			if (!NOSMaxResult.isEmpty()) {
				NOS_max = NOSMaxResult.get(0).get("nos").asInt();
			}
			NOS_colors = ColorGradient.createColorGradient(classColorStart, classColorEnd, NOS_max + 1);
		}		
//!Test
		//ToDo: Entwurf Fraben anpassen, das die Priorität der Farbe entspricht


		// Get all Districts and then setDistrictAttributes
		/* 
		List<Record> districtPaths = connector.executeRead("MATCH p=(n:Model:City)-[:CONTAINS*]->(m:District) RETURN p");
		for (Record result : districtPaths) {
			setDistrictAttributes(result.get("p").asPath());
		}*/
		List<Record> setDistricts = connector.executeRead(
			String.format("MATCH (m:Model)-[:CONTAINS]->(d:District) WHERE ID(m) = %d RETURN d", model.id())
		);
		for (Record setDistrictsRecord : setDistricts) {
			Long districtId = setDistrictsRecord.get("d").asNode().id();
			List<String> colorGradient = districtColors.get(districtId);
			setDistrictAttributes(districtId, colorGradient, 0);
		}

		// Get all Buildings and then setBuildingAttributes
		List<Record> buildings = connector.executeRead("MATCH (n:Model:City)-[:CONTAINS*]->(b:Building) RETURN b");
		for (Record result : buildings) {
			setBuildingAttributes(result.get("b").asNode());
		}

		// Save the width and length of a District as an array in the DB
		//ToDo I replaced "RETURN d, element.hash as hash ORDER BY element.hash" with "RETURN d" 
		List<Record> districts = connector.executeRead(
			"MATCH (n:Model:City)-[:CONTAINS*]->(d:District)-[:VISUALIZES]->(element) RETURN d");
		for (Record result : districts) {
			Node node = result.get("d").asNode();
			double width = node.get("width").asDouble(0.0);	
			double length = node.get("length").asDouble(0.0);  
			double[] array = {width, length};
			properties.put(node.id(), array);
		}

		// Save the width and length of a Building as an array in the DB
		//ToDo I replaced "RETURN b, element.hash as hash ORDER BY element.hash" with "RETURN b" 
		List<Record> buildingsWithElements = connector.executeRead(
			"MATCH (n:Model:City)-[:CONTAINS*]->(b:Building)-[:VISUALIZES]->(element) " +
			"RETURN b"
		);
		for (Record result : buildingsWithElements) {
			Node node = result.get("b").asNode();
			double width = node.get("width").asDouble(0.0);
			double length = node.get("length").asDouble(0.0);
			double[] array = {width, length};
			properties.put(node.id(), array);
		}
		CityLayout.cityLayout(model.id(), properties);
		log.info("City2City finished");
			}

	// Setzt immer gleiche Höhe und unterschiedliche Farbe für jeden District 
	/* 
	private void setDistrictAttributes(Path districtPath) {
		String color = PCKG_colors.get(districtPath.length() - 1);
		connector.executeWrite(
			String.format(Locale.US,
				"MATCH (n) WHERE ID(n) = %d SET n.height = %.6f, n.color = '%s'", districtPath.end().id(),
				heightMin, color));
	}
	*/
	private void setDistrictAttributes(Long nodeId, List<String> colorGradient, int level) {
		String color = colorGradient.get(level);
		connector.executeWrite(
			String.format(Locale.US,
				"MATCH (n) WHERE ID(n) = %d SET n.height = %.6f, n.color = '%s'", nodeId, heightMin, color));
	
		List<Record> childDistricts = connector.executeRead(
			String.format("MATCH (n)-[:CONTAINS]->(c:District) WHERE ID(n) = %d RETURN c", nodeId));
		for (Record result : childDistricts) {
			setDistrictAttributes(result.get("c").asNode().id(), colorGradient, level + 1);
			}
		}
		

	private void setBuildingAttributes(Node building) {
		int linkCount = building.get("numberOfLinks").asInt(0);
		int propertyCount = building.get("numberOfProperties").asInt(0);
		setBuildingAttributesOriginal(building, linkCount, propertyCount); 		
	}
	
//Hier werden die Eigenschaften der Gebäude gesetzt!!
//dataCounter und Met""hodCounter entfernen und ersetetzen mit Anzahl Attribute ein jeder Anforderung
	private void setBuildingAttributesOriginal(Node building, int linkCount, int propertyCount) {
		
		double width;
		double length;
		double height;
		String color; 
		//ToDo: überlegen ob ich das wieder freischalte
		//if ( propertyCount == 0) {
			width = 3; //widthMin;
			length = 2; //widthMin;
		//} else {
		//	width = widthMin + ( 0.5 * propertyCount) ;
		//	length = widthMin + ( 0.5 * propertyCount);
		//}
		if (linkCount == 0) {
			height = heightMin; 
		} else {
			height = linkCount;
		}
		if (originalBuildingMetric == BuildingMetric.NOS) {
			color = NOS_colors.get(building.get("numberOfStatements").asInt(0));		//ToDo Anpassen, glaube numberOfStatements exisitert in meiner DB nicht
		} else  {
			color = classColor;
		}
		connector.executeWrite(cypherSetBuildingSegmentAttributes(building.id(), width, length, height, color));
	}
	
	//wirtd trotz des Namens auch für original Buildings benutzt 
	private String cypherSetBuildingSegmentAttributes(Long segment, double width, double length, double height,
		String color) {
			/*DecimalFormatSymbols symbols = new DecimalFormatSymbols(Locale.US);
        	DecimalFormat df = new DecimalFormat("#.######", symbols);
			
			String formattedWidth = df.format(width);
			String formattedLength = df.format(length);
			String formattedHeight = df.format(height);
	
			return String.format(
				"MATCH (n) WHERE ID(n) = %d SET n.width = %s, n.length = %s, n.height = %s, n.color = '%s'", 
				segment, formattedWidth, formattedLength, formattedHeight, color
			);*/

		return String.format(
			Locale.US, //notwendig, da in der DB die Zahlen mit . und nicht mit , geschrieben werden
			"MATCH (n) WHERE ID(n) = %d SET n.width = %.6f, n.length = %.6f, n.height = %.6f, n.color = '%s'", segment,
		width, length, height, color);
		}

	private void getDistrictsColors() {
		List<Record> rootDisricts = connector.executeRead("MATCH (n:Model:City)-[:CONTAINS]->(d:District) RETURN d");
        for (Record root : rootDisricts) {
            Node rootNode = root.get("d").asNode();
            List<Record> districtMaxLevelResult = connector.executeRead(
                String.format("MATCH p=(n:District)-[:CONTAINS*]->(m:District) WHERE ID(n)=%d AND NOT (m)-[:CONTAINS]->(:District) RETURN length(p) AS length ORDER BY length(p) DESC LIMIT 1", rootNode.id()));
            int districtMaxLevel = 1; //Mit 0 funktioniert es nicht
            if (!districtMaxLevelResult.isEmpty()) {
                districtMaxLevel = districtMaxLevelResult.get(0).get("length").asInt() + 1;
            }
			String[] colorPair = generateColorPair();
			List<String> colorGradient = ColorGradient.createColorGradient(colorPair[0], colorPair[1], districtMaxLevel);
			districtColors.put(rootNode.id(), colorGradient);
		}
	}

	//*  Returns up to 6 color Pairs and than starts again from the beginning
	private String[] generateColorPair() {
		String[] colorPair = predefinedColorPairs.get(colorPairIndex);
		colorPairIndex = (colorPairIndex + 1) % predefinedColorPairs.size();
		return colorPair;
	}


}

