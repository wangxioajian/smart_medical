from dotenv import load_dotenv

load_dotenv()
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_neo4j import Neo4jGraph, Neo4jVector
from neo4j_graphrag.types import SearchType

from configuration.config import *

class IndexUtil:
    def __init__(self):
        self.graph = Neo4jGraph(
            url=NEO4J_CONFIG["uri"],
            username=NEO4J_CONFIG["auth"][0],
            password=NEO4J_CONFIG["auth"][1],
        )
        # 嵌入模型
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=str(BASE_DIR / 'bge-base-zh-v1.5'),
            encode_kwargs={'normalize_embeddings': True}
        )

    # 创建全文索引，传入索引名称，节点标签，属性
    def create_fulltext_index(self, index_name, label, property):
        cypher = f"""
            CREATE FULLTEXT INDEX {index_name} IF NOT EXISTS
            FOR (n:{label}) ON EACH [n.{property}]
        """
        self.graph.query(cypher)

    # 创建向量索引，需要传入生成向量的“源属性”，以及嵌入向量属性
    def create_vector_index(self, index_name, label, source_property, embedding_property):
        # 生成嵌入向量，并添加到节点属性中
        embedding_dim = self._add_embedding(label, source_property, embedding_property)

        cypher = f"""
            CREATE VECTOR INDEX {index_name} IF NOT EXISTS
            FOR (n:{label})
            ON n.{embedding_property}
            OPTIONS {{ indexConfig: {{
             `vector.dimensions`: {embedding_dim},
             `vector.similarity_function`: 'cosine'
            }}
            }}
        """
        self.graph.query(cypher)

    # 内部函数：生成嵌入向量，并添加到节点属性中，返回向量维度
    def _add_embedding(self, label, source_property, embedding_property):
        # 1. 查询所有节点对应的源属性值，作为模型的输入；还需要查出节点id
        cypher = f"""
            MATCH (n:{label})
            RETURN n.{source_property} AS text, id(n) AS id
        """
        results = self.graph.query(cypher)

        # 2. 获取查询结果中的文本内容
        docs = [ result['text'] for result in results ]

        # 3. 调用嵌入模型，得到嵌入向量
        embeddings = self.embedding_model.embed_documents(docs)


        # 4. 将id和嵌入向量组合成字典形式
        batch = []
        for result, embedding in zip(results, embeddings):
            item = {'id': result['id'], 'embedding': embedding}
            batch.append(item)

        # 5. 执行cypher，按id查节点，写入新的嵌入向量属性
        cypher = f"""
            UNWIND $batch AS item
            MATCH (n:{label})
            WHERE id(n) = item.id
            SET n.{embedding_property} = item.embedding
        """
        self.graph.query(cypher, params={"batch": batch})

        return len(embeddings[0])

if __name__ == '__main__':
    index = IndexUtil()

    index.create_fulltext_index("disease_fulltext_index", "Disease", "name")

    index.create_vector_index("disease_vector_index", "Disease", "name", "embedding")



    index.create_fulltext_index('duration_fulltext_index', 'Duration', 'name')
    index.create_vector_index('Duration_vector_index', 'Duration', 'name', 'embedding')

    index.create_fulltext_index('prevent_fulltext_index', 'Prevent', 'name')
    index.create_vector_index('Prevent_vector_index', 'Prevent', 'name', 'embedding')

    index.create_fulltext_index('people_fulltext_index', 'People', 'name')
    index.create_vector_index('People_vector_index', 'People', 'name', 'embedding')



    index.create_fulltext_index('way_fulltext_index', 'Way', 'name')
    index.create_vector_index('way_vector_index', 'Way', 'name', 'embedding')

