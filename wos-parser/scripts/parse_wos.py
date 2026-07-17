#!/usr/bin/env python3
"""
parse_wos.py — 解析Web of Science导出文件（标记格式）

支持两种WoS导出格式：
  - 标记格式: FN/VR/PT/AU/TI/AB/PY/ER（WoS标准导出格式）
  - 纯文本格式: Record X of Y + Author(s):/Title:/...（旧格式）

输出: papers_metadata.csv（含wos_id + seq_id双序号）
"""

import re
import csv
import json
from pathlib import Path


def _natural_sort_key(path: Path) -> list:
    """按文件名中的数字自然排序：file2 < file10 而非 file10 < file2"""
    import re as _re
    text = path.stem
    parts = _re.split(r'(\d+)', text)
    return [int(p) if p.isdigit() else p.lower() for p in parts]


def detect_format(content: str) -> str:
    """检测WoS文件格式"""
    if content.startswith('FN Clarivate') or content.startswith('﻿FN'):
        return 'tagged'
    if 'Record 1 of' in content:
        return 'plaintext'
    return 'unknown'


def parse_tagged_format(content: str) -> list[dict]:
    """解析标记格式（FN/VR/PT/AU/.../ER）"""

    # 移除BOM
    content = content.lstrip('﻿')

    # 按 ER 分割记录（ER 出现在行首）
    raw_records = re.split(r'(?<=^ER\n)', content, flags=re.MULTILINE)
    records = []

    for raw in raw_records:
        if not raw.strip():
            continue
        record = _parse_tagged_record(raw)
        if record.get('title') or record.get('abstract'):
            records.append(record)

    return records


def _parse_tagged_record(text: str) -> dict:
    """解析单条标记格式记录"""

    lines = text.split('\n')
    fields = {}
    current_tag = None
    tag_pattern = re.compile(r'^([A-Z0-9]{2})\s*(.*)')

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped == 'ER':
            break

        # 续行：以空格/tab开头
        if line.startswith((' ', '\t')) and current_tag:
            sep = ' ; ' if current_tag == 'AU' else ' '
            fields[current_tag] += sep + stripped

        # 新标签行：行首两字符（大写字母或数字）
        elif not line.startswith((' ', '\t')):
            m = tag_pattern.match(stripped)
            if m:
                current_tag = m.group(1)
                value = m.group(2)
                if current_tag in fields:
                    fields[current_tag] += ' ; ' + value
                else:
                    fields[current_tag] = value
            # 无法识别的行忽略（可能是格式错误）

    # 提取目标字段
    title = fields.get('TI', '')
    authors = fields.get('AU', '')
    source = fields.get('SO', '')
    year = fields.get('PY', '')
    abstract = fields.get('AB', '')
    doi = fields.get('DI', '')
    doc_type = fields.get('DT', '')
    pub_type = fields.get('PT', '')
    wos_ut = fields.get('UT', '')

    # 新增字段
    author_address = fields.get('C1', '')       # 作者机构地址
    funding = fields.get('FU', '')              # 基金资助
    times_cited = fields.get('TC', '')          # 被引次数
    issn = fields.get('SN', '')                 # ISSN
    isbn = fields.get('BN', '')                 # ISBN
    researcher_id = fields.get('RI', '')        # ResearcherID
    author_ids = fields.get('AI', '')            # 作者标识符
    pubmed_id = fields.get('PM', '')            # PubMed ID
    conference_title = fields.get('CT', '')     # 会议全称
    sponsors = fields.get('SP', '')             # 主办方
    conference_city = fields.get('CL', '')      # 会议城市
    usage_u1 = fields.get('U1', '')             # 使用计数(最近180天)
    usage_u2 = fields.get('U2', '')             # 使用计数(2013至今)
    z9 = fields.get('Z9', '')                   # 总被引次数(核心合集)

    record = {
        'title': title,
        'author': authors,
        'source': source,
        'journal': source.split(',')[0].strip() if source else '',
        'year': year,
        'doi': doi,
        'abstract': abstract,
        'doc_type': doc_type,
        'pub_type': pub_type,
        'wos_ut': wos_ut,
        'author_address': author_address,
        'funding': funding,
        'times_cited': times_cited,
        'issn': issn,
        'isbn': isbn,
        'researcher_id': researcher_id,
        'author_ids': author_ids,
        'pubmed_id': pubmed_id,
        'conference_title': conference_title,
        'sponsors': sponsors,
        'conference_city': conference_city,
        'usage_u1': usage_u1,
        'usage_u2': usage_u2,
        'z9': z9,
    }
    return record


def parse_plaintext_format(content: str) -> list[dict]:
    """解析纯文本格式（Record X of Y ...）"""
    RECORD_SPLIT = re.compile(r'Record \d+ of \d+')

    FIELD_PATTERNS = {
        'author': re.compile(
            r'^(?:Author\(s\)|Authors|AU|作者)\s*[:：]\s*(.+?)(?=\n(?:[A-Z]|$))',
            re.DOTALL | re.IGNORECASE,
        ),
        'title': re.compile(
            r'^(?:Title|TI|标题)\s*[:：]\s*(.+?)(?=\n(?:[A-Z]|$))',
            re.DOTALL | re.IGNORECASE,
        ),
        'source': re.compile(
            r'^(?:Source|SO|来源)\s*[:：]\s*(.+?)(?=\n(?:[A-Z]|$))',
            re.DOTALL | re.IGNORECASE,
        ),
        'year': re.compile(r'^(?:Year|PY|年份)\s*[:：]\s*(\d{4})', re.IGNORECASE),
        'doi': re.compile(
            r'^(?:DOI|doi|DI)\s*[:：]\s*(10\.\d{4,9}/[^\s,;"\'<>\[\]{}]+)',
            re.IGNORECASE,
        ),
        'abstract': re.compile(
            r'^(?:Abstract|AB|摘要)\s*[:：]\s*(.+?)(?=\n(?:[A-Z]|$))',
            re.DOTALL | re.IGNORECASE,
        ),
        'author_address': re.compile(
            r'^(?:Addresses|C1|Author\s+Address|Reprint\s+Address)\s*[:：]\s*(.+?)(?=\n(?:[A-Z]|$))',
            re.DOTALL | re.IGNORECASE,
        ),
        'funding': re.compile(
            r'^(?:Funding|FU|Funding\s+Agency|基金)\s*[:：]\s*(.+?)(?=\n(?:[A-Z]|$))',
            re.DOTALL | re.IGNORECASE,
        ),
        'times_cited': re.compile(
            r'^(?:Times\s+Cited|TC|被引)\s*[:：]\s*(\d+)', re.IGNORECASE,
        ),
        'issn': re.compile(r'^(?:ISSN|SN)\s*[:：]\s*([\d\-X]+)', re.IGNORECASE),
        'isbn': re.compile(r'^(?:ISBN|BN)\s*[:：]\s*([\d\-X]+)', re.IGNORECASE),
        'researcher_id': re.compile(
            r'^(?:Researcher\s*ID|RI)\s*[:：]\s*(.+?)(?=\n(?:[A-Z]|$))',
            re.IGNORECASE,
        ),
        'author_ids': re.compile(
            r'^(?:Author\s+Identifiers|AI|ORCID)\s*[:：]\s*(.+?)(?=\n(?:[A-Z]|$))',
            re.IGNORECASE,
        ),
        'pubmed_id': re.compile(r'^(?:PubMed\s+ID|PM)\s*[:：]\s*(\d+)', re.IGNORECASE),
        'doc_type': re.compile(
            r'^(?:Document\s+Type|DT|文献类型)\s*[:：]\s*(.+?)(?=\n(?:[A-Z]|$))',
            re.IGNORECASE,
        ),
        'pub_type': re.compile(
            r'^(?:Publication\s+Type|PT)\s*[:：]\s*(.+?)(?=\n(?:[A-Z]|$))',
            re.IGNORECASE,
        ),
        'wos_ut': re.compile(r'^(?:UT|WoS\s+Unique\s+ID|入藏号)\s*[:：]\s*(.+)', re.IGNORECASE),
        'conference_title': re.compile(
            r'^(?:Conference\s+Title|CT|会议)\s*[:：]\s*(.+?)(?=\n(?:[A-Z]|$))',
            re.IGNORECASE,
        ),
        'sponsors': re.compile(
            r'^(?:Sponsors|SP|主办)\s*[:：]\s*(.+?)(?=\n(?:[A-Z]|$))',
            re.IGNORECASE,
        ),
        'conference_city': re.compile(
            r'^(?:Conference\s+City|CL|会议城市)\s*[:：]\s*(.+?)(?=\n(?:[A-Z]|$))',
            re.IGNORECASE,
        ),
        'usage_u1': re.compile(
            r'^(?:Usage\s+Count.*180|U1)\s*[:：]\s*(\d+)', re.IGNORECASE,
        ),
        'usage_u2': re.compile(
            r'^(?:Usage\s+Count.*2013|U2)\s*[:：]\s*(\d+)', re.IGNORECASE,
        ),
        'z9': re.compile(
            r'^(?:Total\s+Times\s+Cited|Z9|被引频次)\s*[:：]\s*(\d+)', re.IGNORECASE,
        ),
    }

    matches = list(RECORD_SPLIT.finditer(content))
    if not matches:
        raise ValueError("未找到WoS记录，请确认文件格式")

    records = []

    for i, match in enumerate(matches, 1):
        start = match.start()
        end = matches[i].start() if i < len(matches) else len(content)
        record_text = content[start:end]

        record = {'wos_id': i, 'seq_id': i}
        for key in FIELD_PATTERNS:
            record[key] = ''

        for field, pattern in FIELD_PATTERNS.items():
            m = pattern.search(record_text)
            if m:
                value = re.sub(r'\s+', ' ', m.group(1)).strip()
                record[field] = value

        source = record.get('source', '')
        record['journal'] = source.split(',')[0].strip() if source else ''

        records.append(record)

    return records


def parse_wos_file(wos_file: Path, output_dir: Path, start_id: int = 1) -> dict:
    """解析单个WoS导出文件，自动检测格式。
    start_id: 起始 wos_id（用于多文件合并时连续编号）"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(wos_file, 'r', encoding='utf-8') as f:
        content = f.read()

    fmt = detect_format(content)

    if fmt == 'tagged':
        records = parse_tagged_format(content)
    elif fmt == 'plaintext':
        records = parse_plaintext_format(content)
    else:
        raise ValueError(
            "无法识别WoS文件格式。支持的格式：\n"
            "  1. 标记格式（FN Clarivate Analytics Web of Science ...）\n"
            "  2. 纯文本格式（Record X of Y ...）"
        )

    print(f"  文件: {wos_file.name}")
    print(f"  格式: {fmt}, 记录数: {len(records)}, 起始ID: {start_id}")

    # 分配双序号
    for i, r in enumerate(records):
        r['wos_id'] = start_id + i
        r['seq_id'] = start_id + i

    return {
        'records': records,
        'format': fmt,
        'count': len(records),
        'file': str(wos_file.name),
    }


FIELD_NAMES = [
    'wos_id', 'seq_id', 'author', 'title', 'journal', 'source',
    'year', 'doi', 'abstract', 'doc_type', 'pub_type', 'wos_ut',
    'author_address', 'funding', 'times_cited', 'issn', 'isbn',
    'researcher_id', 'author_ids', 'pubmed_id',
    'conference_title', 'sponsors', 'conference_city',
    'usage_u1', 'usage_u2', 'z9',
]


def save_results(records: list[dict], output_dir: Path) -> dict:
    """保存CSV和统计JSON"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    stats = {
        'total': len(records),
        'has_abstract': sum(1 for r in records if r.get('abstract')),
        'has_doi': sum(1 for r in records if r.get('doi')),
        'has_title': sum(1 for r in records if r.get('title')),
        'has_author': sum(1 for r in records if r.get('author')),
        'has_funding': sum(1 for r in records if r.get('funding')),
        'has_address': sum(1 for r in records if r.get('author_address')),
    }

    output_path = output_dir / 'papers_metadata.csv'
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES, extrasaction='ignore')
        writer.writeheader()
        for r in records:
            row = {k: r.get(k, '') for k in FIELD_NAMES}
            writer.writerow(row)

    print(f"CSV已保存: {output_path}")

    stats_path = output_dir / 'parse_stats.json'
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    return stats


def parse_multiple_files(wos_files: list[Path], output_dir: Path) -> dict:
    """解析多个WoS文件，合并为一个CSV，连续编号"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    all_records = []
    next_id = 1
    file_results = []

    for fpath in wos_files:
        result = parse_wos_file(fpath, output_dir, start_id=next_id)
        all_records.extend(result['records'])
        next_id += result['count']
        file_results.append(result)

    total = len(all_records)

    # 统计
    stats = {
        'total': total,
        'has_abstract': sum(1 for r in all_records if r.get('abstract')),
        'has_doi': sum(1 for r in all_records if r.get('doi')),
        'has_title': sum(1 for r in all_records if r.get('title')),
        'has_author': sum(1 for r in all_records if r.get('author')),
        'has_funding': sum(1 for r in all_records if r.get('funding')),
        'has_address': sum(1 for r in all_records if r.get('author_address')),
        'files_processed': len(wos_files),
        'file_details': file_results,
    }

    # 保存合并CSV
    output_path = output_dir / 'papers_metadata.csv'
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES, extrasaction='ignore')
        writer.writeheader()
        for r in all_records:
            row = {k: r.get(k, '') for k in FIELD_NAMES}
            writer.writerow(row)

    print(f"\n合并完成: {total} 条记录 → {output_path}")

    # 保存统计JSON
    stats_path = output_dir / 'parse_stats.json'
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    return stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='解析Web of Science导出文件')
    parser.add_argument('--input', action='append', required=True,
                        help='WoS导出文件路径（可多次指定，如 --input f1.txt --input f2.txt）')
    parser.add_argument('--output', required=True, help='输出目录')
    parser.add_argument('--start-id', type=int, default=1,
                        help='起始 wos_id（默认1；多文件时自动连续编号，忽略此参数）')
    args = parser.parse_args()

    wos_files = sorted([Path(f) for f in args.input], key=_natural_sort_key)

    if len(wos_files) == 1:
        result = parse_wos_file(wos_files[0], Path(args.output), start_id=args.start_id)
        stats = save_results(result['records'], Path(args.output))
    else:
        print(f"处理 {len(wos_files)} 个文件...")
        stats = parse_multiple_files(wos_files, Path(args.output))

    print(f"\n统计:")
    print(f"  总记录: {stats['total']}")
    print(f"  有标题: {stats['has_title']}")
    print(f"  有作者: {stats['has_author']}")
    print(f"  有摘要: {stats['has_abstract']}")
    print(f"  有DOI: {stats['has_doi']}")
    print(f"  有基金: {stats.get('has_funding', 0)}")
    print(f"  有地址: {stats.get('has_address', 0)}")
