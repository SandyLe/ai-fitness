import os
import json
import argparse
from typing import Dict, Any

import torch
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.nn.functional as F

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

class TextDataset(Dataset):
    """文本数据集"""
    
    def __init__(self, data_path: str, max_length: int = 512):
        """
        初始化数据集
        
        Args:
            data_path: 数据文件路径
            max_length: 最大序列长度
        """
        self.data = []
        with open(data_path, 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line)
                if len(item['input_ids']) <= max_length:
                    self.data.append(item)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        item = self.data[idx]
        return {
            'input_ids': torch.tensor(item['input_ids'], dtype=torch.long),
            'attention_mask': torch.tensor(item['attention_mask'], dtype=torch.long)
        }

def collate_fn(batch):
    """
    数据批处理函数
    
    Args:
        batch: 数据批次
        
    Returns:
        处理后的批次数据
    """
    max_length = max(len(item['input_ids']) for item in batch)
    
    input_ids = []
    attention_mask = []
    
    for item in batch:
        ids = item['input_ids']
        mask = item['attention_mask']
        
        # 填充到最大长度
        padding_length = max_length - len(ids)
        input_ids.append(torch.cat([ids, torch.zeros(padding_length, dtype=torch.long)]))
        attention_mask.append(torch.cat([mask, torch.zeros(padding_length, dtype=torch.long)]))
    
    return {
        'input_ids': torch.stack(input_ids),
        'attention_mask': torch.stack(attention_mask)
    }

def load_config(config_path: str) -> Dict:
    """
    加载模型配置
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置字典
    """
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config

def train(args: Dict[str, Any]):
    """
    训练模型
    
    Args:
        args: 训练参数
    """
    # 设置随机种子
    torch.manual_seed(args['seed'])
    
    # 设置为CPU模式
    device = "cpu"
    
    # 加载词汇表
    vocab_path = os.path.join(os.path.dirname(args['train_data']), "vocab.json")
    if os.path.exists(vocab_path):
        with open(vocab_path, 'r', encoding='utf-8') as f:
            vocab = json.load(f)
        vocab_size = len(vocab) + 1  # +1 for padding token
    else:
        # 如果没有词汇表，则从训练数据中估计
        print("未找到词汇表，将从训练数据中估计词汇量...")
        with open(args['train_data'], 'r', encoding='utf-8') as f:
            max_id = 0
            for line in f:
                item = json.loads(line)
                max_id = max(max_id, max(item['input_ids']))
        vocab_size = max_id + 1
    
    print(f"词汇表大小: {vocab_size}")
    
    # 加载配置
    config = load_config(args['config'])
    
    # 创建模型
    model = SimpleTransformer(
        vocab_size=vocab_size,
        d_model=config.get('dim', 256),
        nhead=config.get('n_heads', 4),
        num_layers=config.get('n_layers', 4)
    )
    model = model.to(device)
    
    # 加载数据集
    train_dataset = TextDataset(args['train_data'], max_length=args['max_length'])
    train_loader = DataLoader(
        train_dataset,
        batch_size=args['batch_size'],
        shuffle=True,
        collate_fn=collate_fn,
        num_workers=0  # 在Windows上使用多进程可能会有问题
    )
    
    # 定义优化器
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=args['learning_rate'],
        weight_decay=args['weight_decay']
    )
    
    # 训练循环
    model.train()
    for epoch in range(args['num_epochs']):
        total_loss = 0
        for batch_idx, batch in enumerate(train_loader):
            # 将数据移动到设备
            input_ids = batch['input_ids'].to(device)
            
            # 创建目标（将输入向右移动一位）
            target = input_ids[:, 1:].contiguous()
            input_ids = input_ids[:, :-1].contiguous()
            
            # 前向传播
            outputs = model(input_ids)
            
            # 计算损失
            loss = F.cross_entropy(outputs.view(-1, outputs.size(-1)), target.view(-1))
            
            # 反向传播
            loss.backward()
            
            # 梯度裁剪
            torch.nn.utils.clip_grad_norm_(model.parameters(), args['max_grad_norm'])
            
            # 更新参数
            optimizer.step()
            optimizer.zero_grad()
            
            total_loss += loss.item()
            
            # 打印批次信息
            if (batch_idx + 1) % args['log_every'] == 0:
                print(f"Epoch {epoch+1}/{args['num_epochs']}, Batch {batch_idx+1}/{len(train_loader)}, Loss: {loss.item():.4f}")
        
        # 打印训练信息
        avg_loss = total_loss / len(train_loader)
        print(f"Epoch {epoch+1}/{args['num_epochs']}, Average Loss: {avg_loss:.4f}")
        
        # 保存模型
        if (epoch + 1) % args['save_every'] == 0:
            save_dir = os.path.join(args['output_dir'], f"checkpoint-{epoch+1}")
            os.makedirs(save_dir, exist_ok=True)
            
            # 保存模型权重
            torch.save(model.state_dict(), os.path.join(save_dir, "model.pt"))
            
            # 保存配置
            with open(os.path.join(save_dir, "config.json"), 'w') as f:
                json.dump({
                    "vocab_size": vocab_size,
                    "dim": config.get('dim', 256),
                    "n_heads": config.get('n_heads', 4),
                    "n_layers": config.get('n_layers', 4)
                }, f, indent=2)
    
    # 保存最终模型
    save_dir = os.path.join(args['output_dir'], "final")
    os.makedirs(save_dir, exist_ok=True)
    
    # 保存模型权重
    torch.save(model.state_dict(), os.path.join(save_dir, "model.pt"))
    
    # 保存配置
    with open(os.path.join(save_dir, "config.json"), 'w') as f:
        json.dump({
            "vocab_size": vocab_size,
            "dim": config.get('dim', 256),
            "n_heads": config.get('n_heads', 4),
            "n_layers": config.get('n_layers', 4)
        }, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="在CPU上训练简化版语言模型")
    parser.add_argument("--config", type=str, required=True, help="模型配置文件路径")
    parser.add_argument("--train_data", type=str, required=True, help="训练数据路径")
    parser.add_argument("--output_dir", type=str, required=True, help="输出目录")
    parser.add_argument("--batch_size", type=int, default=1, help="批次大小")
    parser.add_argument("--max_length", type=int, default=512, help="最大序列长度")
    parser.add_argument("--num_epochs", type=int, default=1, help="训练轮数")
    parser.add_argument("--learning_rate", type=float, default=5e-5, help="学习率")
    parser.add_argument("--weight_decay", type=float, default=0.01, help="权重衰减")
    parser.add_argument("--max_grad_norm", type=float, default=1.0, help="最大梯度范数")
    parser.add_argument("--save_every", type=int, default=1, help="每多少轮保存一次模型")
    parser.add_argument("--log_every", type=int, default=10, help="每多少批次记录一次日志")
    parser.add_argument("--seed", type=int, default=42, help="随机种子")
    
    args = parser.parse_args()
    
    # 将参数转换为字典
    train_args = vars(args)
    
    # 训练模型
    train(train_args)

if __name__ == "__main__":
    main()