# API 使用说明（pdf-processor）

## 公式修复

公式修复通过 Claude Code 直接执行，无需外部 API。

Claude 会读取原始 TXT 文件，将数学公式转换为 LaTeX 格式后输出。

## 修复标准

见 `references/fix_prompt.md`

## 备选：独立运行

如需在 Claude Code 之外独立运行公式修复脚本：

```bash
export DEEPSEEK_API_KEY="sk-你的密钥"
python scripts/fix_formulas.py --priority priority_list.csv --raw-dir raw/ --fixed-dir fixed/
```

但通常不需要——直接在 Claude Code 中使用 `/skill pdf-processor` 即可。
