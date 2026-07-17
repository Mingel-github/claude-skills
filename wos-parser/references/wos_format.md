# Web of Science 导出格式说明

## 导出设置

在Web of Science中导出时，请选择：
- 格式：**纯文本 (.txt)**
- 记录内容：**全记录与参考文献**

## 支持的格式

### 格式1：标记格式（推荐）

文件以 `FN Clarivate Analytics Web of Science` 开头，每条记录以 `ER` 结束：

```
FN Clarivate Analytics Web of Science
VR 1.0
PT J
AU Smith, John
   Brown, Robert
TI Autonomous GPS Integrity Monitoring Using Pseudorange Residual
SO NAVIGATION, 1988, 35(2), pp.255-274
PY 1988
DI 10.1002/j.2161-4296.1988.tb00955.x
AB The use of GPS for navigation-critical applications...
ER

PT J
AU ...
TI ...
ER
```

### 格式2：纯文本格式（旧版）

每条记录以 `Record X of Y` 开头：

```
Record 1 of 50
Author(s): Smith, J.; Brown, R.
Title: Autonomous GPS Integrity Monitoring Using Pseudorange Residual
Source: NAVIGATION, 1988, 35(2), pp.255-274
Year: 1988
DOI: 10.1002/j.2161-4296.1988.tb00955.x
Abstract: The use of GPS for navigation-critical applications...
```

## 主要字段标签

| 标签 | 全称 | 说明 |
|------|------|------|
| PT | Publication Type | J=期刊, C=会议, B=书籍 |
| AU | Authors | 多作者续行缩进 |
| TI | Title | 论文标题 |
| SO | Source | 期刊/会议全称 |
| PY | Year | 发表年份 |
| AB | Abstract | 摘要（可能跨多行） |
| DI | DOI | 数字对象标识符 |
| DT | Document Type | Article, Proceedings Paper, ... |
| BP/EP | Begin/End Page | 起止页码 |
| UT | Unique ID | WoS唯一标识号 |
| ER | End of Record | 记录结束标记 |

## 注意事项

1. 多行字段的续行以空格开头（如摘要、作者列表）
2. 部分记录可能缺少某些字段（如DOI）
3. 文件编码为 UTF-8（可能含BOM）
4. 中英文混合的WoS版本均可处理

## 示例

见 `assets/sample_wos.txt`
