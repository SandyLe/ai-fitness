import json
import os
from typing import List, Dict
import re

def load_raw_data(data_path: str) -> List[Dict]:
    """
    加载原始数据
    
    Args:
        data_path: 数据文件路径
        
    Returns:
        数据列表
    """
    data = []
    with open(data_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                # 如果不是JSON格式，假设是纯文本
                data.append({"text": line.strip()})
    return data

def clean_data(data: List[Dict]) -> List[Dict]:
    """
    清洗数据
    
    Args:
        data: 原始数据列表
        
    Returns:
        清洗后的数据列表
    """
    cleaned_data = []
    for item in data:
        # 根据您的需求进行数据清洗
        if 'text' in item and len(item['text'].strip()) > 0:
            cleaned_data.append({
                'text': item['text'].strip()
            })
    return cleaned_data

def simple_tokenize(text: str) -> List[int]:
    """
    简单的分词函数，将文本分割成字符
    
    Args:
        text: 输入文本
        
    Returns:
        token ID列表
    """
    # 创建一个简单的字符到ID的映射
    chars = list(set(text))
    char_to_id = {char: i + 1 for i, char in enumerate(chars)}  # 0 保留给padding
    
    # 将文本转换为token ID
    return [char_to_id[char] for char in text]

def tokenize_data(data: List[Dict], max_length: int = 1024) -> List[Dict]:
    """
    对数据进行简单分词
    
    Args:
        data: 清洗后的数据列表
        max_length: 最大序列长度
        
    Returns:
        分词后的数据列表
    """
    tokenized_data = []
    
    # 对所有文本进行分词
    all_text = " ".join([item['text'] for item in data])
    
    # 创建一个简单的词汇表（这里使用空格分割的单词）
    words = re.findall(r'\w+|[^\w\s]', all_text)
    vocab = list(set(words))
    word_to_id = {word: i + 1 for i, word in enumerate(vocab)}  # 0 保留给padding
    
    for item in data:
        text = item['text']
        words = re.findall(r'\w+|[^\w\s]', text)
        
        # 将单词转换为ID
        tokens = [word_to_id.get(word, 0) for word in words]
        
        # 截断到最大长度
        if len(tokens) > max_length:
            tokens = tokens[:max_length]
        
        tokenized_data.append({
            'input_ids': tokens,
            'attention_mask': [1] * len(tokens)
        })
    
    # 保存词汇表，以便后续使用
    vocab_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                             "my_model", "data", "vocab.json")
    with open(vocab_path, 'w', encoding='utf-8') as f:
        json.dump(word_to_id, f, ensure_ascii=False, indent=2)
    
    return tokenized_data

def save_processed_data(data: List[Dict], output_path: str) -> None:
    """
    保存处理后的数据
    
    Args:
        data: 处理后的数据列表
        output_path: 输出路径
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

def main():
    # 配置参数
    raw_data_path = "d:/aa/2025设计大赛/自建模型/基于DeepSeek自建模型/my_model/data/raw_data.txt"
    processed_data_path = "d:/aa/2025设计大赛/自建模型/基于DeepSeek自建模型/my_model/data/processed_data.jsonl"
    max_length = 1024  # 减小序列长度，适合CPU处理
    
    # 创建数据目录
    os.makedirs("d:/aa/2025设计大赛/自建模型/基于DeepSeek自建模型/my_model/data", exist_ok=True)
    
    # 如果原始数据不存在，创建一个示例文件
    if not os.path.exists(raw_data_path):
        with open(raw_data_path, 'w', encoding='utf-8') as f:
            f.write("这是一个示例文本，用于测试数据处理流程。\n")
            f.write("人工智能是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。\n")
            f.write("深度学习是机器学习的分支，是一种以人工神经网络为架构，对数据进行表征学习的算法。\n")
    
    print("开始加载原始数据...")
    # 处理数据
    raw_data = load_raw_data(raw_data_path)
    print(f"原始数据加载完成，共 {len(raw_data)} 条")
    
    print("开始清洗数据...")
    cleaned_data = clean_data(raw_data)
    print(f"数据清洗完成，共 {len(cleaned_data)} 条")
    
    print("开始分词...")
    tokenized_data = tokenize_data(cleaned_data, max_length)
    print(f"分词完成，共 {len(tokenized_data)} 条")
    
    print("保存处理后的数据...")
    save_processed_data(tokenized_data, processed_data_path)
    
    print(f"数据处理完成，共处理 {len(tokenized_data)} 条数据")
    print(f"处理后的数据已保存到: {processed_data_path}")
    print(f"词汇表已保存到: d:/aa/2025设计大赛/自建模型/基于DeepSeek自建模型/my_model/data/vocab.json")

if __name__ == "__main__":
    main()