---
name: youtube-summarizer
slug: youtube-summarizer-cn
displayName: YouTube 视频总结器
version: 1.1.0
summary: 下载 YouTube 字幕并生成结构化总结（核心观点/金句/亮点），默认中文输出，支持多语言
license: MIT
description: 下载 YouTube 视频字幕并生成结构化总结。当用户分享 YouTube 链接并要求总结视频、提取字幕或获取内容洞察时使用。支持所有 YouTube URL 格式（watch、youtu.be、shorts、embed、live）。
allowed-tools: Bash(python3:*), Bash(pip3:*), Bash(yt-dlp:*)
---

# YouTube 视频总结器

下载 YouTube 视频字幕，生成包含核心观点、金句摘录和亮点分析的结构化总结。

## 环境准备

安装依赖（已安装可跳过）：

```bash
pip3 install youtube-transcript-api -q
# yt-dlp 用于获取视频元数据（标题、频道、时长）
# 未安装可执行: brew install yt-dlp  或  pip3 install yt-dlp
```

## 工作流程

### 第一步：获取字幕

`SKILL_DIR` 为本 SKILL.md 所在目录。

```bash
# JSON 格式输出（含元数据）
python3 SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# 纯文本 + 时间戳（推荐用于总结）
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only --timestamps

# 指定语言（含回退链）
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language en,zh --text-only --timestamps
```

脚本支持所有标准 YouTube URL 格式：`watch?v=`、`youtu.be/`、`shorts/`、`embed/`、`live/`，或直接传入 11 位视频 ID。

### 第二步：获取视频元数据

获取标题、频道、时长和发布日期：

```bash
yt-dlp --skip-download --print "%(title)s|%(channel)s|%(duration_string)s|%(upload_date)s" "URL"
```

### 第三步：读取完整字幕

长视频（>30 分钟）的字幕输出可能较大，建议分段读取：

```bash
# 前半部分
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only --timestamps | head -500
# 后半部分
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only --timestamps | tail -400
```

### 第四步：生成总结

分析字幕内容，生成结构化总结。**所有内容（包括章节标题、表头、元数据字段）都必须使用指定语言。** 只有模板结构（表格、引用块、加粗）保持固定。

模板结构（将每个标签翻译为输出语言）：

```
## [本地化: "视频总结" / "Video Summary"]

**[本地化标签]:** (标题)
**[本地化标签]:** (频道)
**[本地化标签]:** (嘉宾，如可识别)
**[本地化标签]:** (时长) | **[本地化标签]:** (日期)

---

### [本地化: 一句话概括]
(1-2 句概述)

---

### [本地化: "核心观点" / "Key Viewpoints"]

| [本地化: 话题] | [本地化: 观点] |
|-------|-----------|
| ... | ... |

---

### [本地化: "金句" / "Notable Quotes"]
> "原文引用" — 发言者

---

### [本地化: "其他亮点" / "Other Highlights"]
- ...

---

### [本地化: "注意/偏见" / "Notes / Bias"]
- ...
```

### 输出语言规则

输出语言按以下优先级确定：

1. **用户明确指定**（如"用中文总结"、"summarize in Japanese"、"用英语总结"）→ 使用该语言
2. **用户未指定** → **默认中文**，所有内容都用中文
3. **金句引用** → 始终保留原文语言（不翻译引用）
4. **章节标题、表头、元数据字段** → 翻译为输出语言（默认中文）
5. **仅结构格式**（表格、引用块、加粗）跨语言固定 — 不使用 emoji

## 错误处理

| 错误 | 解决方案 |
|------|----------|
| `youtube-transcript-api not installed` | 执行 `pip3 install youtube-transcript-api` |
| `Transcripts are disabled` | 告知用户该视频已禁用字幕 |
| `No transcript found` | 去掉 `--language` 参数重试，并告知实际语言 |
| 输出为空 | 视频可能没有自动生成的字幕，告知用户 |
| `yt-dlp: command not found` | 执行 `pip3 install yt-dlp` 或 `brew install yt-dlp` |

## 使用技巧

- **发言者识别：** 访谈/播客类视频，从开场白识别发言者，并在观点中标注
- **广告段落：** 跳过口播广告（科技视频常见）— 在注意/偏见部分标注
- **长视频（>1小时）：** 分段处理；1.5 小时视频通常输出 500-800 行字幕
- **非中文视频：** 字幕为视频原始语言；按上述语言规则用输出语言（默认中文）总结
