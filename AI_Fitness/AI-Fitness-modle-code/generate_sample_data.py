import json

# 创建一些示例对话数据
sample_conversations = [
    "人工智能是研究、开发用于模拟、延伸和扩展人的智能的理论、方法、技术及应用系统的一门新的技术科学。",
    "深度学习是机器学习的分支，是一种以人工神经网络为架构，对数据进行表征学习的算法。",
    "计算机视觉是人工智能的重要分支，主要研究如何使计算机理解和处理图像及视频。",
    "自然语言处理技术让计算机能够理解、解释和生成人类语言，是人工智能的核心技术之一。",
    "机器学习通过算法让计算机从数据中学习，不断提高自身的性能和准确度。"
]

# 确保数据目录存在
import os
data_dir = "d:/aa/2025设计大赛/自建模型/基于DeepSeek自建模型/my_model/data"
os.makedirs(data_dir, exist_ok=True)

# 将数据保存到文件
with open(os.path.join(data_dir, "raw_data.txt"), "w", encoding="utf-8") as f:
    for conversation in sample_conversations:
        f.write(conversation + "\n")

print("示例数据已生成并保存到 data/raw_data.txt")