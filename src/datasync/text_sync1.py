import pandas as pd
import json

# 读取JSONL文件
from datasync.uitils import Neo4jWriter

data = []
with open('F:\\PycharmProjects\\smart_medical\\data\\knowledge_graph\\medical_kg.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data.append(json.loads(line))

# 创建主表数据
main_data = []
# 创建关联表数据
acompany_data = []
symptom_data = []
department_data = []
drug_data = []
check_data = []
treat_data = []

# 处理每条记录
for idx, record in enumerate(data):
    # 主表数据
    main_entry = {
        'id': idx,
        'name': record['name'],
        'desc': record['desc'],
        'cause': record['cause'],
        'way': record['way'],
        'prevent': record['prevent'],
        'people': record['people'],
        'duration': record['duration']
    }
    main_data.append(main_entry)

    # 处理伴随症状 (acompany)
    for item in record.get('acompany', []):
        acompany_data.append({
            'disease_id': idx,
            'disease_name': record['name'],
            'acompany': item
        })

    # 处理症状 (symptom)
    for item in record.get('symptom', []):
        symptom_data.append({
            'disease_id': idx,
            'disease_name': record['name'],
            'symptom': item
        })

    # 处理科室 (department)
    for item in record.get('department', []):
        department_data.append({
            'disease_id': idx,
            'disease_name': record['name'],
            'department': item
        })

    # 处理药物 (drug)
    for item in record.get('drug', []):
        drug_data.append({
            'disease_id': idx,
            'disease_name': record['name'],
            'drug': item
        })

    # 处理检查项目 (check)
    for item in record.get('check', []):
        check_data.append({
            'disease_id': idx,
            'disease_name': record['name'],
            'check_item': item
        })

    # 处理治疗方法 (treat)
    for item in record.get('treat', []):
        treat_data.append({
            'disease_id': idx,
            'disease_name': record['name'],
            'treatment': item
        })

# 创建DataFrame
main_df = pd.DataFrame(main_data)
acompany_df = pd.DataFrame(acompany_data)
symptom_df = pd.DataFrame(symptom_data)
department_df = pd.DataFrame(department_data)
drug_df = pd.DataFrame(drug_data)
check_df = pd.DataFrame(check_data)
treat_df = pd.DataFrame(treat_data)

# # 显示各表结构
# print("主表 (main_df):"+main_df.columns)
# writer = Neo4jWriter()
#
# print("-----写入疾病-----")
# #取出主表中id和name,desc列，将他们组装成一个字典list,如果name为空则去掉这一行
# main_df_isNotNull = main_df[main_df['name'].notnull()]
# main_df_processed = main_df_isNotNull[['id', 'name', 'desc']].to_dict(orient='records')
# writer.write_disease_nodes('Disease', main_df_processed)
#
# print("-----写入诱因-----")
# #取出主表中id和cause列，将cause换成name将他们组装成一个字典list,如果name为空则去掉这一行
# cause_df = main_df[main_df['cause'].notnull()]
# cause_df_processed = cause_df[['id', 'cause']].rename(columns={'cause': 'name'}).to_dict(orient='records')
# writer.write_nodes('Cause', cause_df_processed)
# writer.write_disease_relations('CAUSE','Cause','Disease',cause_df_processed)
#
#
# print("-----写入传播途径-----")
# #取出主表中id和way列，将way换成name将他们组装成一个字典list,如果name为空则去掉这一行
# way_df = main_df[main_df['way'].notnull()]
# way_df_processed = way_df[['id', 'way']].rename(columns={'way': 'name'}).to_dict(orient='records')
# writer.write_nodes('Way', way_df_processed)
# writer.write_disease_relations('TRANSMIT','Disease','Way',cause_df_processed)
#
# print("-----写入治疗周期-----")
# #取出主表中id和duration列，将pduration换成name将他们组装成一个字典list,如果name为空则去掉这一行
# duration_df = main_df[main_df['duration'].notnull()]
# duration_df_processed = duration_df[['id', 'duration']].rename(columns={'duration': 'name'}).to_dict(orient='records')
# writer.write_nodes('Duration', duration_df_processed)
# writer.write_disease_relations('DURATION','Disease','Duration',duration_df_processed)
#
# print("-----写入预防措施-----")
# #取出主表中id和prevent列，将prevent换成name将他们组装成一个字典list,如果name为空则去掉这一行
# prevent_df = main_df[main_df['prevent'].notnull()]
# prevent_df_processed = prevent_df[['id', 'prevent']].rename(columns={'prevent': 'name'}).to_dict(orient='records')
# writer.write_nodes('Prevent', prevent_df_processed)
# writer.write_disease_relations('PREVENT','Prevent','Disease',prevent_df_processed)
#
# print("-----写入人群-----")
# #取出主表中id和people列，将people换成name将他们组装成一个字典list,如果name为空则去掉这一行
# people_df = main_df[main_df['people'].notnull()]
# people_df_processed = people_df[['id', 'people']].rename(columns={'people': 'name'}).to_dict(orient='records')
# writer.write_nodes('People', people_df_processed)
# writer.write_disease_relations('PEOPLE','Disease','People',people_df_processed)

















# print(f"主表行数: {len(main_df)}")
#
print("\n伴随症状表 (acompany_df):")
print(acompany_df.head())
print(f"伴随症状表行数: {len(acompany_df)}")
#
# print("\n症状表 (symptom_df):")
# print(symptom_df.head())
# print(f"症状表行数: {len(symptom_df)}")
#
# print("\n科室表 (department_df):")
# print(department_df.head())
# print(f"科室表行数: {len(department_df)}")
#
# print("\n药物表 (drug_df):")
# print(drug_df.head())
# print(f"药物表行数: {len(drug_df)}")
#
# print("\n检查项目表 (check_df):")
# print(check_df.head())
# print(f"检查项目表行数: {len(check_df)}")
#
# print("\n治疗方法表 (treat_df):")
# print(treat_df.head())
# print(f"治疗方法表行数: {len(treat_df)}")