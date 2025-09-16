import json

# 检查处理后的数据
with open("d:/aa/2025设计大赛/自建模型/基于DeepSeek自建模型/my_model/data/processed_data.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        print("输入ID:", data["input_ids"])
        print("注意力掩码:", data["attention_mask"])
        print("-" * 50)

# 检查词汇表
with open("d:/aa/2025设计大赛/自建模型/基于DeepSeek自建模型/my_model/data/vocab.json", "r", encoding="utf-8") as f:
    vocab = json.load(f)
    print("\n词汇表大小:", len(vocab))
    print("词汇表示例:", dict(list(vocab.items())[:5]))