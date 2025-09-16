import os
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from contextlib import asynccontextmanager

# 定义模型结构，需要与训练时的结构一致
class SimpleTransformer(nn.Module):
    """
    简化版的Transformer模型，适用于CPU训练
    """
    def __init__(self, vocab_size, d_model=256, nhead=4, num_layers=4):
        super(SimpleTransformer, self).__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        encoder_layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.fc_out = nn.Linear(d_model, vocab_size)
        
    def forward(self, x):
        # 创建一个简单的注意力掩码，防止模型看到未来的token
        mask = torch.triu(torch.ones(x.size(1), x.size(1)) * float('-inf'), diagonal=1)
        
        x = self.embedding(x)
        x = self.transformer_encoder(x, mask=mask)
        x = self.fc_out(x)
        return x

# 定义请求和响应模型
class GenerationRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 50
    temperature: float = 0.7

class GenerationResponse(BaseModel):
    generated_text: str

# 全局变量
model = None
vocab = None
id_to_word = None

# 使用新的生命周期管理方式
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时加载模型
    global model, vocab, id_to_word
    
    # 加载配置
    config_path = "d:/aa/欧鹏杯/基于DeepSeek自建模型/my_model/output/final/config.json"
    model_path = "d:/aa/欧鹏杯/基于DeepSeek自建模型/my_model/output/final/model.pt"
    vocab_path = "d:/aa/欧鹏杯/基于DeepSeek自建模型/my_model/data/vocab.json"
    
    # 检查文件是否存在
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"模型文件不存在: {model_path}")
    if not os.path.exists(vocab_path):
        raise FileNotFoundError(f"词汇表文件不存在: {vocab_path}")
    
    # 加载配置
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    # 加载词汇表
    with open(vocab_path, 'r', encoding='utf-8') as f:
        vocab = json.load(f)
    
    # 创建id到词的映射
    id_to_word = {int(v): k for k, v in vocab.items()}
    
    # 创建模型
    model = SimpleTransformer(
        vocab_size=config["vocab_size"],
        d_model=config["dim"],
        nhead=config["n_heads"],
        num_layers=config["n_layers"]
    )
    
    # 加载模型权重
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    
    print(f"模型已加载，词汇表大小: {config['vocab_size']}")
    
    yield
    
    # 关闭时清理资源
    print("正在关闭API服务器...")

# 创建FastAPI应用
app = FastAPI(
    title="CPU版自定义大模型API", 
    description="基于简化版Transformer的CPU版自定义大模型API服务",
    lifespan=lifespan
)

def generate_text(model, prompt_tokens, max_new_tokens=50, temperature=0.7):
    """
    生成文本
    
    Args:
        model: 模型
        prompt_tokens: 提示词的token ID列表
        max_new_tokens: 最大生成的新token数量
        temperature: 生成文本的随机性，值越大随机性越高
        
    Returns:
        生成的token ID列表
    """
    input_ids = torch.tensor([prompt_tokens], dtype=torch.long)
    
    with torch.no_grad():
        for _ in range(max_new_tokens):
            # 获取模型输出
            outputs = model(input_ids)
            
            # 获取下一个token的预测
            next_token_logits = outputs[:, -1, :] / temperature
            
            # 应用softmax获取概率
            probs = F.softmax(next_token_logits, dim=-1)
            
            # 采样下一个token
            next_token = torch.multinomial(probs, num_samples=1)
            
            # 将新token添加到输入序列
            input_ids = torch.cat([input_ids, next_token], dim=1)
    
    return input_ids[0].tolist()

def tokenize_text(text, vocab):
    """
    将文本转换为token ID
    
    Args:
        text: 输入文本
        vocab: 词汇表
        
    Returns:
        token ID列表
    """
    # 使用与训练时相同的分词方法
    import re
    words = re.findall(r'\w+|[^\w\s]', text)
    tokens = []
    
    for word in words:
        if word in vocab:
            tokens.append(vocab[word])
        else:
            # 对于未知词，可以使用特殊token或者跳过
            tokens.append(1)  # 假设1是未知词的token
    
    return tokens

def detokenize_text(tokens, id_to_word):
    """
    将token ID转换为文本
    
    Args:
        tokens: token ID列表
        id_to_word: ID到词的映射
        
    Returns:
        文本
    """
    words = []
    
    for token in tokens:
        if token in id_to_word:
            words.append(id_to_word[token])
        else:
            words.append("<unk>")
    
    return " ".join(words)

@app.post("/generate", response_model=GenerationResponse)
async def generate_endpoint(request: GenerationRequest) -> Dict[str, Any]:
    """
    生成文本
    
    Args:
        request: 生成请求
        
    Returns:
        生成的文本
    """
    global model, vocab, id_to_word
    
    if model is None or vocab is None or id_to_word is None:
        raise HTTPException(status_code=500, detail="模型未加载")
    
    # 将输入文本转换为token ID
    prompt_tokens = tokenize_text(request.prompt, vocab)
    
    # 生成文本
    output_tokens = generate_text(
        model=model,
        prompt_tokens=prompt_tokens,
        max_new_tokens=request.max_new_tokens,
        temperature=request.temperature
    )
    
    # 将token ID转换为文本
    generated_text = detokenize_text(output_tokens, id_to_word)
    
    return {"generated_text": generated_text}

@app.get("/health")
async def health_check():
    """
    健康检查
    
    Returns:
        健康状态
    """
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/generate", response_model=GenerationResponse)
async def generate_endpoint(request: GenerationRequest) -> Dict[str, Any]:
    """
    生成文本
    
    Args:
        request: 生成请求
        
    Returns:
        生成的文本
    """
    global model, vocab, id_to_word
    
    if model is None or vocab is None or id_to_word is None:
        raise HTTPException(status_code=500, detail="模型未加载")
    
    # 将输入文本转换为token ID
    prompt_tokens = tokenize_text(request.prompt, vocab)
    
    # 生成文本
    output_tokens = generate_text(
        model=model,
        prompt_tokens=prompt_tokens,
        max_new_tokens=request.max_new_tokens,
        temperature=request.temperature
    )
    
    # 将token ID转换为文本
    generated_text = detokenize_text(output_tokens, id_to_word)
    
    return {"generated_text": generated_text}


class ChatMessage(BaseModel):
    role: str  # "system", "user", "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    max_new_tokens: int = 50
    temperature: float = 0.7

class ChatResponse(BaseModel):
    message: ChatMessage

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> Dict[str, Any]:
    """
    聊天接口
    
    Args:
        request: 聊天请求
        
    Returns:
        助手的回复
    """
    global model, vocab, id_to_word
    
    if model is None or vocab is None or id_to_word is None:
        raise HTTPException(status_code=500, detail="模型未加载")
    
    # 简单处理：将所有消息连接起来作为提示
    prompt = " ".join([msg.content for msg in request.messages])
    
    # 将输入文本转换为token ID
    prompt_tokens = tokenize_text(prompt, vocab)
    
    # 生成文本
    output_tokens = generate_text(
        model=model,
        prompt_tokens=prompt_tokens,
        max_new_tokens=request.max_new_tokens,
        temperature=request.temperature
    )
    
    # 将token ID转换为文本
    generated_text = detokenize_text(output_tokens, id_to_word)
    
    return {"message": {"role": "assistant", "content": generated_text}}

@app.get("/")
async def root():
    """
    根路径，返回简单的欢迎信息
    """
    return {"message": "欢迎使用CPU版自定义大模型API"}


def main():
    """
    启动API服务
    """
    print("正在启动API服务器...")
    # Use the app directly instead of the string reference
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

if __name__ == "__main__":
    main()