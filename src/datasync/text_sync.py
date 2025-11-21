import json
from configuration.config import medica_kd_path
from datasync.uitils import Neo4jWriter  # 注意模块名拼写修正


class TextSynchronizer:
    def __init__(self):
        self.writer = Neo4jWriter()

    def process_jsonl_file(self, file_path):
        """
        处理jsonl文件，对每个元素进行判断和处理
        """
        diseases = []
        departments = []
        symptoms = []
        causes = []
        drugs = []
        ways = []
        prevents = []
        checks = []
        treats = []
        peoples = []
        durations = []
        foods = []

        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 0):
                try:
                    data = json.loads(line.strip())
                    disease, department, symptom, cause, drug, way, prevent, check, treat, people, duration, food = \
                        self._process_single_element(data, line_num)

                    diseases.append(disease)
                    departments.append(department)
                    symptoms.append(symptom)
                    causes.append(cause)
                    drugs.append(drug)
                    ways.append(way)
                    prevents.append(prevent)
                    checks.append(check)
                    treats.append(treat)
                    peoples.append(people)
                    durations.append(duration)
                    foods.append(food)
                except json.JSONDecodeError as e:
                    print(f"第{line_num}行JSON解析错误: {e}")
                except Exception as e:
                    print(f"第{line_num}行处理错误: {e}")

        # 批量写入 Neo4j
        self.writer.write_nodes('Disease', diseases)
        self.writer.write_nodes('Department', departments)
        self.writer.write_nodes('Symptom', symptoms)
        self.writer.write_nodes('Cause', causes)
        self.writer.write_nodes('Drug', drugs)
        self.writer.write_nodes('Way', ways)
        self.writer.write_nodes('Prevent', prevents)
        self.writer.write_nodes('Check', checks)
        self.writer.write_nodes('Treat', treats)
        self.writer.write_nodes('Food', foods)
        self.writer.write_nodes('People', peoples)
        self.writer.write_nodes('Duration', durations)

    def _safe_join(self, items):
        """安全地将列表转换为逗号连接的字符串"""
        if not isinstance(items, list):
            return ''
        return ','.join(str(item) for item in items)

    def _process_single_element(self, data, line_num):
        """
        处理单个元素，进行各种判断
        """
        disease = {
            'name': data.get('name', ''),
            'desc': data.get('desc', ''),
            'id': line_num
        }

        symptom = {
            'name': data.get('symptom', ''),
            'id': line_num
        }
        cause = {
            'name': data.get('cause', ''),
            'id': line_num
        }


        way = {
            'name': data.get('way', ''),
            'id': line_num
        }
        prevent = {
            'name': data.get('prevent', ''),
            'id': line_num
        }

        people = {
            'name': data.get('people', ''),
            'id': line_num
        }
        duration = {
            'name': data.get('duration', ''),
            'id': line_num
        }

        return disease, symptom, cause,  way, prevent,   people, duration

    #处理ACOMPANY伴随疾病
    def process_ACOMPANY(self,file_path):
        acompanys = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 0):
                try:
                    data = json.loads(line.strip())



                except json.JSONDecodeError as e:
                    print(f"第{line_num}行JSON解析错误: {e}")
                except Exception as e:
                    print(f"第{line_num}行处理错误: {e}")



if __name__ == "__main__":
    file_path = str(medica_kd_path / 'medical_kg.jsonl')
    print("开始处理文件...")
    text_sync = TextSynchronizer()
    text_sync.process_jsonl_file(file_path)
