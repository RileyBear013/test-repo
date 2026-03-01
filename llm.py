#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LLM 文本分类示例
使用 LLM API 进行文本分类
"""

import os
import requests
import json

# LLM API 配置
LLM_API_KEY = os.getenv("LLM_API_KEY", "sk-haunoctozgqegmoqrrueywvfikahrjlicbsknnqgnnyeffvj")
LLM_API_URL = "https://api.hauno.com/v1/chat/completions"  # 示例 URL，请根据实际 API 调整


def classify_text(text: str, categories: list[str]) -> dict:
    """
    使用 LLM 对文本进行分类
    
    Args:
        text: 要分类的文本
        categories: 分类类别列表，如 ["新闻", "娱乐", "科技", "体育"]
    
    Returns:
        包含分类结果的字典
    """
    categories_str = "、".join(categories)
    prompt = f"""请将以下文本分类到以下类别之一：{categories_str}

文本：{text}

请只返回分类结果，不要解释。"""
    
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-3.5-turbo",  # 根据实际可用模型调整
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,  # 降低温度以获得更稳定的分类
        "max_tokens": 50
    }
    
    try:
        response = requests.post(LLM_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        category = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        
        return {
            "text": text,
            "category": category,
            "categories": categories,
            "success": True
        }
    except Exception as e:
        return {
            "text": text,
            "category": None,
            "categories": categories,
            "success": False,
            "error": str(e)
        }


def main():
    """主函数 - 示例用法"""
    # 示例文本
    sample_texts = [
        "苹果公司发布了新一代 iPhone",
        "今天下午会有一场足球比赛",
        "这部电影太好看了，强烈推荐！"
    ]
    
    # 定义分类类别
    categories = ["科技", "体育", "娱乐"]
    
    print("=== LLM 文本分类示例 ===\\n")
    
    for text in sample_texts:
        result = classify_text(text, categories)
        
        if result["success"]:
            print(f"文本：{result['text']}")
            print(f"分类：{result['category']}")
            print(f"可用类别：{', '.join(result['categories'])}")
            print()
        else:
            print(f"错误：{result['error']}")


if __name__ == "__main__":
    main()
