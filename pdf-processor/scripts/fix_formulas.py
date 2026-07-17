#!/usr/bin/env python3
"""
fix_formulas.py — AI公式修复（仅高优先级，可选独立脚本）

注意：在 Claude Code 中使用 /skill pdf-processor 时，公式修复由 Claude 直接完成。
本脚本仅在需要独立运行时使用，此时需要设置 DEEPSEEK_API_KEY 环境变量。
"""

import os
import time
import requests
from pathlib import Path
import pandas as pd

# ==================== 配置 ====================
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"


def load_fix_prompt():
    """读取修复Prompt模板"""
    ref_path = Path(__file__).parent.parent / 'references' / 'fix_prompt.md'
    if ref_path.exists():
        with open(ref_path, 'r', encoding='utf-8') as f:
            return f.read()
    return """你是学术论文公式修复专家。将提取的文本中的数学公式转为LaTeX格式。

要求：
1. 识别所有数学表达式、公式、符号
2. 行内公式用 $...$ 包裹
3. 独立公式用 $$...$$ 包裹
4. 希腊字母：σ→\\sigma, μ→\\mu, α→\\alpha, β→\\beta, γ→\\gamma, δ→\\delta, ε→\\epsilon, θ→\\theta, λ→\\lambda, π→\\pi, Σ→\\Sigma, Δ→\\Delta, Ω→\\Omega
5. 上下标：x^2→x^{2}, x_i→x_{i}, x_{ij}→x_{ij}
6. 分数：a/b→\\frac{a}{b}
7. 根号：√→\\sqrt{}
8. 求和：∑→\\sum, 积分：∫→∫
9. 保持所有文本内容不变，只改公式部分
10. 输出完整文本，不要只输出公式部分"""


def fix_formulas_in_text(raw_text: str, api_key: str = None) -> str:
    """调用AI修复单篇论文的公式"""
    key = api_key or DEEPSEEK_API_KEY
    if not key:
        raise ValueError(
            "请设置 DEEPSEEK_API_KEY 环境变量，"
            "或在 Claude Code 中直接使用 /skill pdf-processor（无需 API Key）"
        )

    if len(raw_text) > 30000:
        raw_text = raw_text[:30000] + "\n\n[... 内容截断 ...]"

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": load_fix_prompt()},
            {"role": "user", "content": f"请将以下文本中的公式转为LaTeX格式：\n\n{raw_text}"}
        ],
        "temperature": 0.1,
        "max_tokens": 8192
    }

    try:
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"API调用失败: {e}")


def fix_high_priority_pdfs(
        priority_csv: Path,
        raw_dir: Path,
        fixed_dir: Path,
        api_key: str = None,
        max_papers: int = 0
) -> dict:
    """处理高优先级论文的公式修复"""
    df = pd.read_csv(priority_csv)
    high_priority = df[df['batch'] == '高优先级']

    if max_papers > 0:
        high_priority = high_priority.head(max_papers)

    stats = {
        'total': len(high_priority),
        'fixed': 0,
        'failed': 0,
        'skipped': 0
    }

    print(f"修复 {len(high_priority)} 篇高优先级论文...")

    for _, row in high_priority.iterrows():
        seq_id = row['seq_id']
        raw_path = raw_dir / f"{seq_id}.raw.txt"

        if not raw_path.exists():
            print(f"  ⚠️ 原始文件不存在: {seq_id}")
            stats['skipped'] += 1
            continue

        try:
            raw_text = raw_path.read_text(encoding='utf-8')
            fixed_text = fix_formulas_in_text(raw_text, api_key)
            fixed_path = fixed_dir / f"{seq_id}.txt"
            fixed_path.write_text(fixed_text, encoding='utf-8')
            stats['fixed'] += 1
            print(f"  ✓ {seq_id}")
        except Exception as e:
            stats['failed'] += 1
            print(f"  ✗ {seq_id} — {e}")

        time.sleep(2)

    print(f"\n完成: 修复 {stats['fixed']} 篇, 失败 {stats['failed']} 篇, 跳过 {stats['skipped']} 篇")
    return stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='AI公式修复（高优先级）— 独立运行需 DEEPSEEK_API_KEY'
    )
    parser.add_argument('--priority', required=True, help='priority_list.csv路径')
    parser.add_argument('--raw-dir', required=True, help='raw目录')
    parser.add_argument('--fixed-dir', required=True, help='fixed目录')
    parser.add_argument('--max', type=int, default=0, help='最多处理数量')
    parser.add_argument('--api-key', type=str, help='DeepSeek API Key')
    args = parser.parse_args()

    fix_high_priority_pdfs(
        Path(args.priority),
        Path(args.raw_dir),
        Path(args.fixed_dir),
        args.api_key,
        args.max
    )
