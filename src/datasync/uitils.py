# 写入Neo4j的工具类
from neo4j import GraphDatabase
from configuration.config import *


class Neo4jWriter:
    def __init__(self):
        self.driver = GraphDatabase.driver(**NEO4J_CONFIG)

    # 写入节点（批量，固定标签）
    def write_disease_nodes(self, label: str, properties: list[dict]):
        cypher = f"""
            UNWIND $batch AS item
            MERGE (:{label} {{id: item.id, name: item.name, desc: item.desc}})
        """
        self.driver.execute_query(cypher, batch=properties)

        # 写入节点（批量，固定标签）

    def write_nodes(self, label: str, properties: list[dict]):
        cypher = f"""
               UNWIND $batch AS item
               MERGE (:{label} {{id: item.id, name: item.name}})
           """
        self.driver.execute_query(cypher, batch=properties)

    # 写入关系
    def write_relations(self, type: str, start_label, end_label, relations: list[dict]):
        cypher = f"""
                    UNWIND $batch AS item
                    MATCH (start:{start_label} {{id: item.start_id}}), (end:{end_label} {{id: item.end_id}})
                    MERGE (start)-[:{type}]->(end)
                """
        self.driver.execute_query(cypher, batch=relations)

    # 写入关系
    def write_disease_relations(self, type: str, start_label, end_label, relations: list[dict]):
        cypher = f"""
                    UNWIND $batch AS item
                    MATCH (start:{start_label} {{id: item.id}}), (end:{end_label} {{id: item.id}})
                    MERGE (start)-[:{type}]->(end)
                """
        self.driver.execute_query(cypher, batch=relations)


    def drop_constraint(self):
        """删除所有约束"""
        driver = self.driver
        records = driver.execute_query("show constraints").records
        for record in records:
            driver.execute_query(f"drop constraint {record['name']} if exists")

    def drop_index_without_constraint(self):
        """删除所有没有约束的索引"""
        driver = self.driver
        records = driver.execute_query("show index").records
        for record in records:
            if not record["owningConstraint"]:
                driver.execute_query(f"drop index {record['name']} if exists")

    def drop_nodes(self):
        """ 删除所有的节点"""
        driver = self.driver
        cypher = "MATCH (n) DETACH DELETE n;"
        driver.execute_query(cypher)





if __name__ == '__main__':
    writer = Neo4jWriter()
    writer.drop_constraint()
    writer.drop_index_without_constraint()
    writer.drop_nodes()




