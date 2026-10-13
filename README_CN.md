# Claw Skills

适用于 Claude Code、OpenClaw 等 AI Agent 的技能集合。

[English](README.md)

## 安装方式

### 方式1: Claude Code 插件市场 (推荐)

```bash
/plugin marketplace add terryso/claw-skills
/plugin install claw-skills
```

### 方式2: npx skills

```bash
npx skills add terryso/claw-skills
```

### 方式3: Git Submodule

```bash
git submodule add https://github.com/terryso/claw-skills.git .agents/claw-skills
```

### 方式4: 克隆并复制

```bash
git clone https://github.com/terryso/claw-skills.git
cp -r claw-skills/skills/* ~/.claude/skills/
```

## 可用技能

### peekaboo-cli

macOS UI 自动化命令行工具，支持屏幕捕获、窗口控制、元素点击、文本输入等功能。

**功能特性：**
- 捕获带元素标注的截图
- 点击、输入、与 UI 元素交互
- 管理窗口和应用程序
- 导航菜单和控制 Dock
- 支持热键和手势

**使用示例：**
```bash
# 安装技能后，在 Claude Code 中：
"截取当前窗口的屏幕截图"
"点击 Safari 中的提交按钮"
"打开备忘录并创建新笔记"
```

---

### polyv-live-cli

保利威直播服务管理工具，支持频道管理、推流操作、商品管理、优惠券等功能。

**功能特性：**
- 频道管理
- 推流操作
- 商品管理
- 优惠券、抽奖
- 回放、统计

**使用示例：**
```bash
# 安装技能后，在 Claude Code 中：
"列出所有保利威频道"
"创建一个新的直播频道"
"获取频道 123456 的推流地址"
```

---

### youtube-summarizer

下载 YouTube 视频字幕并生成结构化总结，包含核心观点、金句摘录和亮点分析。

**功能特性：**
- 从任意 YouTube URL 下载字幕/转录文本
- 提取视频元数据（标题、频道、时长、发布日期）
- 生成结构化总结（核心观点、金句、亮点）
- 多语言支持（自动检测或指定语言）
- 支持 watch、youtu.be、shorts、embed、live 等所有 URL 格式

**使用示例：**
```bash
# 安装技能后，在 Claude Code 中：
"总结这个视频: https://youtube.com/watch?v=VIDEO_ID"
"下载这个视频的字幕: https://youtu.be/VIDEO_ID"
"Summarize this video: https://youtube.com/watch?v=VIDEO_ID"
```

---

### youtube-subtitle-burner

下载 YouTube 视频到本地，提取 word-level 字幕时间轴，翻译为中文，用 PIL 逐帧烧录字幕到视频画面。

**功能特性：**
- 下载 YouTube 视频（最高画质，H.264 转码）
- 从 json3 格式提取精确 word-level 时间轴（不用 VTT，避免字幕延迟）
- LLM 翻译英文字幕为中文
- PIL 逐帧渲染字幕（黄底黑字，圆角背景框）
- 2x 超采样抗锯齿（消除文字边缘锯齿）
- 流式管道处理（不写临时文件，避免磁盘爆满）
- 支持横屏和竖屏视频

**字幕参数：**
- 字体：STHeiti Medium
- 横屏 56px / 竖屏 58px
- 黑色文字，黄色半透明背景 (255,220,0,180)
- 底部居中，每行 ≤15 字

**使用示例：**
```bash
# 在 Claude Code 或 OpenClaw 中：
"下载这个YouTube视频并加上中文字幕: https://youtube.com/watch?v=VIDEO_ID"
```

---

### explainer-video

把文章或帖子变成 60 秒代码渲染讲解视频：单个自包含 HTML 时间轴，用无头 Chromium 逐帧渲染，再用 ffmpeg 合成。

**功能特性：**
- 确定性渲染：每一帧都是时间的纯函数（`seekTo`/`seek`），不依赖墙钟播放
- 弹簧物理（带轻微过冲）；接缝语法（向量匹配硬切、禁用交叉溶解、超大光标、waterfall 文字入场）
- 节拍网格分析（numpy）：切点卡重拍、事件卡节拍、零死时间
- 60fps + 真动态模糊（子帧捕获 + ffmpeg tmix）
- 中文 TTS 旁白、CC 音乐床（旁白下自动闪避）、节拍 UI 音效
- 响度标准化 -14 LUFS；SRT sidecar（长字幕不烧录进画面）
- 支持 16:9（1280x720）与 9:16（720x1280）

**使用示例：**
```bash
# 在 Claude Code 或 OpenClaw 中：
"把这篇博客文章做成 60 秒讲解视频：https://example.com/post"
```

---

## 为什么选择 Skill 而不是 MCP Server？

| 特性 | Skill | MCP Server |
|------|-------|------------|
| 安装复杂度 | 简单（复制文件） | 中等（需要配置） |
| **Tools 限制** | **无限制** | **IDE 有配额限制** |
| 工具访问 | CLI 命令（无限制） | 结构化工具（有限） |
| 灵活性 | 完整 CLI 能力 | 受工具 schema 约束 |

**核心优势：** MCP Server 受限于 IDE 的最大工具数量配额。Skill 没有这个限制 —— 它们为无限数量的 CLI 命令提供全面的文档，同时不占用任何工具槽位。

例如，`peekaboo-cli` 有 35+ 个命令。如果每个命令都作为 MCP 工具，会消耗大量配额。而作为 Skill，它不占用任何配额。

---

## 目录结构

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
    └── polyv-live-cli/
        ├── SKILL.md
        └── references/
    └── youtube-summarizer/
        ├── SKILL.md
        └── scripts/
            └── fetch_transcript.py
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

## 贡献

欢迎提交 Issue 和 Pull Request 来添加新技能。

## 许可证

MIT
