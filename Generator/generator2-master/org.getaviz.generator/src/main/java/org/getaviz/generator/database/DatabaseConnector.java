package org.getaviz.generator.database;

import org.neo4j.driver.AuthTokens;
import org.neo4j.driver.Driver;
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.Session;
import org.neo4j.driver.Transaction;
import org.neo4j.driver.TransactionWork;
import org.neo4j.driver.Result;
import org.neo4j.driver.Record;
import org.neo4j.driver.types.Node;

import java.util.List;
import java.util.Collections;
import java.util.ArrayList;

public class DatabaseConnector implements AutoCloseable {
    private static String URL = "bolt://localhost:7687"; //! Anpassen
    private static String USERNAME = "neo4j";   //! Anpassen
    private static String PASSWORD = "Benni1998";//! Anpassen 
    private final Driver driver;
    private static DatabaseConnector instance = null;

    
    public DatabaseConnector(String url, String username, String password) {
        this.driver = GraphDatabase.driver(url, AuthTokens.basic(username, password));
    }

    
    private DatabaseConnector() {
        this(URL, USERNAME, PASSWORD);
    }

    public static String getDatabaseURL() {
        return URL;
    }

    public static synchronized DatabaseConnector getInstance() {
        if (instance == null) {
            instance = new DatabaseConnector();
        }
        return instance;
    }

    public static synchronized DatabaseConnector getInstance(String url, String username, String password) {
        if (instance == null) {
            instance = new DatabaseConnector(url, username, password);
        }
        return instance;
    }

    public void executeWrite(String... statements) {
        try (Session session = driver.session()) {
            session.executeWrite(tx -> {
                for (String statement : statements) {
                    tx.run(statement);
                }
                return null;
            });
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
//! Anpassen, das funktioniert so nicht
    public Node addNode(String statement, String parameterName) {
        try (Session session = driver.session()) {
            return session.writeTransaction(tx -> {
                Result result = tx.run(statement + " RETURN " + parameterName);
                return result.single().get(parameterName).asNode();
            });
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

   /*  public List<Record>  executeRead(String statement) {
        try (Session session = driver.session()) {
            Result result = session.executeRead(tx -> tx.run(statement));
            List <Record> records = result.list();
            return records;//return records; // Consume the Result object and return a List<Record>
    } catch (Exception e) {
        e.printStackTrace();
        return Collections.emptyList(); // Return an empty list in case of an error
    }
    }*/

    public List<Record> executeRead(String statement) {
        try (Session session = driver.session()) {
            return session.readTransaction(tx -> {
                Result result = tx.run(statement);
                List<Record> records = result.list();
                return records;
            });
        } catch (Exception e) {
            e.printStackTrace();
            return Collections.emptyList();
        }
    }
    
//! node.id(); ist veraltet sollte ersetzt werden
    public Node getVisualizedEntity(Long id) {
        List<Record> result = executeRead("MATCH (n)-[:VISUALIZES]->(e) WHERE ID(n) = " + id + " RETURN e");
        if (!result.isEmpty()) {
            return result.get(0).get("e").asNode();
            
        }
        return null;
    }
    
    //! Same wie oben
    public Node getPosition(Long id) {
        List<Record> result = executeRead("MATCH (n)-[:HAS]->(p:Position) WHERE ID(n) = " + id + " RETURN p");
        if (!result.isEmpty()) {
            return result.get(0).get("p").asNode();
        }
        return null;
    }

    @Override
    public void close() {
        driver.close();
    }
}
