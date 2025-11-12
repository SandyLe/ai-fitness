import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig

# 模型路径
MODEL_PATH = "d:\\aa\\2025设计大赛\\自建模型\\基于DeepSeek自建模型\\my_model\\output\\final"
CONFIG_PATH = "d:\\aa\\2025设计大赛\\自建模型\\基于DeepSeek自建模型\\my_model\\configs\\my_model_cpu.json"

# 加载自定义配置
with open(CONFIG_PATH, "r") as f:
    custom_config = json.load(f)

# 创建完整的配置
config = {
    "model_type": "gpt2",
    "vocab_size": 50257,
    "n_ctx": 1024,
    "n_embd": custom_config["dim"],
    "n_head": custom_config["n_heads"],
    "n_layer": custom_config["n_layers"],
    "bos_token_id": 50256,
    "eos_token_id": 50256,
    "pad_token_id": 50256
}

# 保存配置到模型目录
config_path = os.path.join(MODEL_PATH, "config.json")
with open(config_path, "w") as f:
    json.dump(config, f)

# 加载配置
config = AutoConfig.from_pretrained(MODEL_PATH)

# 创建tokenizer文件
tokenizer_path = os.path.join(MODEL_PATH, "tokenizer.json")
if not os.path.exists(tokenizer_path):
    # 使用训练数据创建新的tokenizer
    from tokenizers import ByteLevelBPETokenizer
    tokenizer = ByteLevelBPETokenizer()
    
    # 使用训练数据训练tokenizer
    tokenizer.train(
        files=["d:\\aa\\2025设计大赛\\自建模型\\基于DeepSeek自建模型\\my_model\\data\\raw_data.txt"],
        vocab_size=50257,
        min_frequency=2,
        special_tokens=["<s>", "</s>", "<pad>", "<unk>"]
    )
    
    # 保存tokenizer
    tokenizer.save(tokenizer_path)

# 加载tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# 直接从模型文件加载
model_file = "d:\\aa\\2025设计大赛\\自建模型\\基于DeepSeek自建模型\\my_model\\output\\model.pt"
if os.path.exists(model_file):
    # 使用torch.load直接加载模型
    model_state = torch.load(model_file, map_location=torch.device('cpu'))
    
    # 创建模型实例
    model = AutoModelForCausalLM.from_config(config)
    
    # 加载状态字典
    model.load_state_dict(model_state)
    print(f"已从 {model_file} 加载模型")
else:
    # 尝试从其他位置加载
    alternative_paths = [
        "d:\\aa\\2025设计大赛\\自建模型\\基于DeepSeek自建模型\\my_model\\output\\checkpoint-final\\model.pt",
        "d:\\aa\\2025设计大赛\\自建模型\\基于DeepSeek自建模型\\my_model\\output\\checkpoint-best\\model.pt",
        "d:\\aa\\2025设计大赛\\自建模型\\基于DeepSeek自建模型\\my_model\\model.pt"
    ]
    
    model_loaded = False
    for path in alternative_paths:
        if os.path.exists(path):
            model_state = torch.load(path, map_location=torch.device('cpu'))
            model = AutoModelForCausalLM.from_config(config)
            model.load_state_dict(model_state)
            print(f"已从 {path} 加载模型")
            model_loaded = True
            break
    
    if not model_loaded:
        raise FileNotFoundError(f"未找到模型文件。请确保模型文件存在于以下路径之一: {model_file}, {', '.join(alternative_paths)}")

def generate_response(prompt, max_length=100, temperature=0.7):
    # 编码输入
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # 生成响应
    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            max_length=max_length,
            temperature=temperature,
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # 解码输出
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def main():
    print("正在初始化模型...")
    print("模型路径:", MODEL_PATH)
    print("配置路径:", CONFIG_PATH)
    
    try:
        print("欢迎使用康训助手终端API！输入'退出'来结束对话。")
        
        while True:
            # 获取用户输入
            user_input = input("\n你：")
            
            # 退出条件
            if user_input.lower() in ["退出", "exit", "quit"]:
                print("助手：再见！祝你康训顺利！")
                break
                
            print("正在生成响应...")
            # 生成响应
            response = generate_response(user_input)
            
            # 显示助手回复
            print(f"助手：{response}")
            print("响应生成完成，等待下一次输入...")
            
    except Exception as e:
        print(f"发生错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()