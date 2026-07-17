#!/usr/bin/env python3
"""
extract_pdf.py — 本地PDF提取（免费）
基于 pdfProcess_v4.py 精简，仅保留：解锁、两栏提取、分离参考文献
"""

import re
import os
import sys
from pathlib import Path
import pandas as pd

# ==================== 依赖检查 ====================
try:
    import fitz
except ImportError:
    print("\n  Missing package 'fitz'. Please run: pip install pymupdf\n")
    sys.exit(1)

try:
    import pikepdf
except ImportError:
    print("\n  Missing package 'pikepdf'. Please run: pip install pikepdf\n")
    sys.exit(1)

fitz.TOOLS.mupdf_display_errors(False)

# ==================== 常量 ====================
REF_MARKERS = re.compile(
    r'^(references|bibliography|参\s*考\s*文\s*献|文\s*献|works cited)',
    re.IGNORECASE | re.MULTILINE
)


# ==================== 解锁PDF ====================
def unlock_pdf(pdf_path: Path) -> bool:
    """解锁加密PDF（原地修改）"""
    try:
        with pikepdf.Pdf.open(pdf_path) as pdf:
            if pdf.is_encrypted:
                temp = pdf_path.parent / f"__temp_{pdf_path.name}"
                pdf.save(temp)
                os.remove(pdf_path)
                os.rename(temp, pdf_path)
                return True
        return False
    except pikepdf.PasswordError:
        print(f"  ⚠️ 密码保护: {pdf_path.name}")
        return False
    except Exception as e:
        print(f"  ✗ 解锁失败: {pdf_path.name} — {e}")
        return False


# ==================== 两栏提取 ====================
def extract_page_text_smart(page) -> str:
    """两栏感知的页面文本提取"""
    blocks = page.get_text("blocks")
    text_blocks = [(b[0], b[1], b[2], b[3], b[4]) for b in blocks if b[6] == 0 and b[4].strip()]

    if not text_blocks:
        return page.get_text("text")

    pw = page.rect.width
    left = [b for b in text_blocks if b[2] < pw * 0.38]
    right = [b for b in text_blocks if b[0] > pw * 0.62]

    if left and right:
        left.sort(key=lambda b: b[1])
        right.sort(key=lambda b: b[1])
        return '\n'.join(b[4] for b in left + right)

    text_blocks.sort(key=lambda b: (round(b[1] / 5) * 5, b[0]))
    return '\n'.join(b[4] for b in text_blocks)


def extract_full_text(pdf_path: Path) -> str:
    """提取PDF全文"""
    doc = fitz.open(pdf_path)
    text = '\n'.join(extract_page_text_smart(p) for p in doc)
    doc.close()
    return text


# ==================== 分离参考文献 ====================
def split_body_and_refs(full_text: str) -> tuple:
    """分离正文和参考文献"""
    m = REF_MARKERS.search(full_text)
    if not m:
        return full_text, ""
    return full_text[:m.start()].strip(), full_text[m.start():].strip()


# ==================== 主处理 ====================
def extract_all_pdfs(priority_csv: Path, pdf_dir: Path, output_dir: Path) -> dict:
    """
    对所有PDF执行本地提取
    输出: {seq_id}.raw.txt (全部) 和 {seq_id}.txt (中低优先级直接复制)
    """
    df = pd.read_csv(priority_csv)
    raw_dir = Path(output_dir) / 'raw'
    fixed_dir = Path(output_dir) / 'fixed'
    raw_dir.mkdir(parents=True, exist_ok=True)
    fixed_dir.mkdir(parents=True, exist_ok=True)

    stats = {'total': len(df), 'extracted': 0, 'unlocked': 0, 'failed': 0}

    print(f"处理 {len(df)} 篇PDF...")

    for _, row in df.iterrows():
        seq_id = row['seq_id']
        pdf_path = pdf_dir / f"{seq_id}.pdf"

        if not pdf_path.exists():
            print(f"  ⚠️ PDF不存在: {seq_id}")
            stats['failed'] += 1
            continue

        # 解锁
        if unlock_pdf(pdf_path):
            stats['unlocked'] += 1

        # 提取全文
        try:
            full_text = extract_full_text(pdf_path)
            body, refs = split_body_and_refs(full_text)

            # 保存原始提取（全部）
            raw_path = raw_dir / f"{seq_id}.raw.txt"
            raw_path.write_text(body, encoding='utf-8')

            # 根据批次决定是否复制到fixed
            batch = row.get('batch', '低优先级')
            if batch in ['高优先级']:
                # 高优先级：暂存raw，后续由fix_formulas.py处理
                # 但先放一个raw版本到fixed，后续会被覆盖
                fixed_path = fixed_dir / f"{seq_id}.txt"
                fixed_path.write_text(body, encoding='utf-8')
            else:
                # 中低优先级：直接复制raw到fixed
                fixed_path = fixed_dir / f"{seq_id}.txt"
                fixed_path.write_text(body, encoding='utf-8')

            stats['extracted'] += 1
            print(f"  ✓ {seq_id} ({batch})")

        except Exception as e:
            stats['failed'] += 1
            print(f"  ✗ {seq_id} — {e}")

    print(f"\n完成: 提取 {stats['extracted']} 篇, 解锁 {stats['unlocked']} 篇, 失败 {stats['failed']} 篇")
    return stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='本地PDF提取')
    parser.add_argument('--priority', required=True, help='priority_list.csv路径')
    parser.add_argument('--pdf-dir', required=True, help='PDF目录')
    parser.add_argument('--output', required=True, help='输出目录')
    args = parser.parse_args()

    extract_all_pdfs(
        Path(args.priority),
        Path(args.pdf_dir),
        Path(args.output)
    )