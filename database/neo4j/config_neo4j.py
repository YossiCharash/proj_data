from neo4j import GraphDatabase

neo4j_driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("admin", "1234")
)
