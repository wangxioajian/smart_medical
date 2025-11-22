import torch
from pathlib import Path

# ==================== 项目根目录 ====================
BASE_DIR = Path(__file__).parent.parent.parent

print(str(BASE_DIR))

medica_kd_path = BASE_DIR / 'data' / 'knowledge_graph'


NEO4J_CONFIG = {
    'uri': "neo4j://localhost:7687",
    'auth': ("neo4j", "199wjq688")
}

# ==================== 路径设置 ====================
# 拼写检查原始数据路径
SPELL_CHECK_RAW_DATA_DIR = BASE_DIR / "data/spell_check/raw"
# 拼写检查已处理数据存放路径
SPELL_CHECK_PROCESSED_DATA_DIR = BASE_DIR / "data/spell_check/processed"
# 意图识别原始数据路径
INTENT_CLASSIFY_RAW_DATA_DIR = BASE_DIR / "data/intent_classify/raw"
# 意图识别已处理数据存放路径
INTENT_CLASSIFY_PROCESSED_DATA_DIR = BASE_DIR / "data/intent_classify/processed"
# 模型参数保存路径
FINETUNED_DIR = BASE_DIR / "finetuned"
# TensorBoard 日志保存路径
LOGS_DIR = BASE_DIR / "logs"
# 向量数据库持久化路径
VECTOR_STORE_DIR = BASE_DIR / "data/vectorstore"
# 本地预训练模型路径
PRETRAINED_DIR = BASE_DIR / "pretrained"
UIE_DIR = BASE_DIR / "uie_pytorch"

WEB_STATIC_DIR = BASE_DIR / 'src' / 'web' / 'static'

# 设备
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

API_KEY = 'sk-0bd2ccf8d7ba4157ae7c49f713b4af31'

# 意图信息
INTENT_INFO = {
    "request": [
        "挂号预约",
        "检查预约",
        "住院预约",
        "报告查询/下载",
        "费用支付/退费",
        "转诊/转院申请",
        "病例邮寄",
        "个人信息修改",
        "服务投诉",
        "建议反馈",
        "系统故障反馈",
    ],
    "consult": [
        "疾病对应详情",
        "疾病对应科室",
        "疾病对应症状",
        "疾病对应并发症",
        "疾病对应诱因",
        "疾病对应药物",
        "疾病宜食用",
        "疾病忌食用",
        "疾病对应传播途径",
        "疾病对应预防措施",
        "疾病对应易感人群",
        "疾病对应检查",
        "疾病对应治疗方式",
        "疾病对应治疗周期",
        "症状解读",
        "诱因导致疾病",
        "药物用于疾病",
        "食物益于疾病",
        "食物忌于疾病",
        "人群类别易感疾病",
        "检查项目用于疾病",
    ],
}

# 意图对应要抽取的实体
ENTITY_INFO = {
    "疾病对应详情": ["疾病"],
    "疾病对应科室": ["疾病"],
    "疾病对应症状": ["疾病"],
    "疾病对应并发症": ["疾病"],
    "疾病对应诱因": ["疾病"],
    "疾病对应药物": ["疾病"],
    "疾病宜食用": ["疾病"],
    "疾病忌食用": ["疾病"],
    "疾病对应传播途径": ["疾病"],
    "疾病对应预防措施": ["疾病"],
    "疾病对应易感人群": ["疾病"],
    "疾病对应检查": ["疾病"],
    "疾病对应治疗方式": ["疾病"],
    "疾病对应治疗周期": ["疾病"],
    "症状解读": ["症状"],
    "诱因导致疾病": ["诱因"],
    "药物用于疾病": ["药物"],
    "食物益于疾病": ["食物"],
    "食物忌于疾病": ["食物"],
    "人群类别易感疾病": ["人群类别"],
    "检查项目用于疾病": ["医学检查"],
}
