# Claw Skills

Collection of AI agent skills for Claude Code, OpenClaw, and other skill-compatible agents.

[中文文档](README_CN.md)

## Installation

### Option 1: Claude Code Plugin Marketplace (Recommended)

```bash
/plugin marketplace add terryso/claw-skills
/plugin install claw-skills
```

### Option 2: npx skills

```bash
npx skills add terryso/claw-skills
```

### Option 3: Git Submodule

```bash
git submodule add https://github.com/terryso/claw-skills.git .agents/claw-skills
```

### Option 4: Clone & Copy

```bash
git clone https://github.com/terryso/claw-skills.git
cp -r claw-skills/skills/* ~/.claude/skills/
```

## Available Skills

### peekaboo-cli

macOS UI automation CLI tool for screen capture, window control, element clicking, text input, and more.

**Features:**
- Capture screenshots with element annotations
- Click, type, and interact with UI elements
- Manage windows and applications
- Navigate menus and control the dock
- Support for hotkeys and gestures

**Usage:**
```bash
# In Claude Code with skill installed:
"Take a screenshot of the current window"
"Click the Submit button in Safari"
"Open Notes and create a new note"
```

---

### polyv-live-cli

Polyv live streaming service management tool with channel management, streaming operations, product management, coupons, and more.

**Features:**
- Channel management (频道管理)
- Streaming operations (推流操作)
- Product management (商品管理)
- Coupons and lottery (优惠券、抽奖)
- Playback and statistics (回放、统计)

**Usage:**
```bash
# In Claude Code with skill installed:
"List all Polyv channels"
"Create a new live channel"
"Get streaming URL for channel 123456"
```

---

### youtube-summarizer

Download YouTube video transcripts and generate structured summaries with key viewpoints, notable quotes, and topic analysis.

**Features:**
- Download subtitles/transcripts from any YouTube URL
- Extract video metadata (title, channel, duration, upload date)
- Generate structured summaries (key viewpoints, quotes, highlights)
- Multi-language support (auto-detect or specify language)
- Works with watch, youtu.be, shorts, embed, and live URLs

**Usage:**
```bash
# In Claude Code with skill installed:
"Summarize this video: https://youtube.com/watch?v=VIDEO_ID"
"Download the transcript from https://youtu.be/VIDEO_ID"
"总结这个视频: https://youtube.com/watch?v=VIDEO_ID"
```

---

### akshare-stock

基于 AkShare 的 A股量化数据分析工具，获取实时行情、历史K线、财务数据、资金流向、龙虎榜、融资融券等数据。

**功能特性：**
- 实时行情查询（全市场/指定板块）
- 历史K线数据（日/周/月，支持前复权）
- 财务报表与主要财务指标
- 行业板块与概念板块分析
- 资金流向、龙虎榜、新股IPO、融资融券数据
- 备选 Baostock 轻量方案

**使用示例：**
```bash
# 安装技能后，在 Claude Code 中：
"查一下贵州茅台最近一个月的K线数据"
"帮我分析半导体板块今天的资金流向"
"查询最新的龙虎榜数据"
```

---

### youtube-subtitle-burner

Download YouTube videos to local, extract word-level subtitle timings, translate to Chinese, and burn subtitles into the video frame by frame with PIL.

**Features:**
- Download YouTube video (best quality, H.264 transcode)
- Extract accurate word-level timings from json3 format (not VTT, avoids subtitle desync)
- LLM translation from English to Chinese
- PIL frame-by-frame subtitle rendering (yellow background, black text, rounded box)
- 2x supersample antialiasing (smooth text edges, no jaggedness)
- Streaming pipe processing (no temp files, avoids disk overflow)
- Supports landscape and portrait videos

**Subtitle Parameters:**
- Font: STHeiti Medium
- Landscape 56px / Portrait 58px
- Black text, yellow semi-transparent background (255,220,0,180)
- Bottom center, max 15 chars per line

**Usage:**
```bash
# In Claude Code or OpenClaw:
"Download this YouTube video and add Chinese subtitles: https://youtube.com/watch?v=VIDEO_ID"
```

---

### explainer-video

Turn an article or post into a 60-second code-rendered explainer video: a single self-contained HTML timeline rendered frame-by-frame with headless Chromium and assembled with ffmpeg.

**Features:**
- Deterministic rendering: every frame is a pure function of time (`seekTo`/`seek`), no wall-clock playback
- Spring physics with slight overshoot; seam grammar (vector-matched cuts, cross-dissolves banned, oversized cursor, waterfall text entry)
- Beat-grid analysis (numpy): cuts on downbeats, hits on beats, zero dead time
- 60fps + real motion blur (subframe capture + ffmpeg tmix)
- Chinese TTS narration, CC music bed with ducking, beat-synced UI sound effects
- Loudness-normalized to -14 LUFS; SRT sidecar (subtitles never burned in)
- 16:9 (1280x720) and 9:16 (720x1280) layouts

**Usage:**
```bash
# In Claude Code or OpenClaw:
"Turn this blog post into a 60-second explainer video: https://example.com/post"
```

---

## Why Skills over MCP Server?

| Feature | Skill | MCP Server |
|---------|-------|------------|
| Setup complexity | Simple (copy files) | Moderate (config) |
| **Tools limit** | **No limit** | **IDE has tools quota** |
| Tool access | CLI commands (unlimited) | Structured tools (limited) |
| Flexibility | Full CLI power | Constrained by tool schema |

**Key advantage:** MCP servers are limited by the IDE's maximum number of tools. Skills have no such limitation - they provide comprehensive documentation for unlimited CLI commands while consuming zero tool slots.

For example, `peekaboo-cli` has 35+ commands. If each command were an MCP tool, it would consume significant quota. As a skill, it costs nothing.

---

## Directory Structure

```
claw-skills/
├── README.md
├── README_CN.md
├── LICENSE
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
└── skills/
    ├── peekaboo-cli/
    │   ├── SKILL.md
    │   └── references/
    ├── polyv-live-cli/
    │   ├── SKILL.md
    │   └── references/
    ├── youtube-summarizer/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── fetch_transcript.py
    └── youtube-subtitle-burner/
        ├── SKILL.md
        └── scripts/
            ├── parse_json3_subs.py
            ├── translate_subs.py
            └── burn_subtitles.py
    └── explainer-video/
        ├── SKILL.md
        ├── bin/
        │   ├── beat_grid.py
        │   └── render_frames.py
        └── references/
            ├── render-pipeline.md
            ├── beat-grid.md
            ├── audio-mix.md
            ├── seam-grammar.md
            └── qa-checklist.md
```

## Contributing

Issues and Pull Requests welcome to add new skills.

## License

MIT
