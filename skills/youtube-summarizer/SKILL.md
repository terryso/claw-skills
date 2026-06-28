---
name: youtube-summarizer
slug: youtube-summarizer-user-9e3b7930
displayName: YouTube Summarizer
version: 1.0.0
summary: 下载 YouTube 字幕并生成结构化总结（核心观点/金句/亮点），默认中文输出，支持多语言
license: MIT
description: Download YouTube video transcripts and generate structured summaries with key viewpoints, notable quotes, and topic analysis. Use when the user shares a YouTube URL and asks to summarize the video, extract transcripts, or get content insights. Supports any YouTube URL format (watch, youtu.be, shorts, embed, live).
allowed-tools: Bash(python3:*), Bash(pip3:*), Bash(yt-dlp:*)
---

# YouTube Summarizer

Download YouTube video transcripts/subtitles and generate structured content summaries with key viewpoints, notable quotes, and topic analysis.

## Setup

Install dependencies (skip if already installed):

```bash
pip3 install youtube-transcript-api -q
# yt-dlp is needed for video metadata (title, channel, duration)
# Install if not present: brew install yt-dlp  OR  pip3 install yt-dlp
```

## Workflow

### Step 1: Fetch Transcript

`SKILL_DIR` is the directory containing this SKILL.md file.

```bash
# JSON output with metadata
python3 SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# Plain text with timestamps (recommended for summarization)
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only --timestamps

# Specific language with fallback chain
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language en,zh --text-only --timestamps
```

The script accepts any standard YouTube URL format: `watch?v=`, `youtu.be/`, `shorts/`, `embed/`, `live/`, or a raw 11-character video ID.

### Step 2: Fetch Video Metadata

Get title, channel, duration, and upload date for context:

```bash
yt-dlp --skip-download --print "%(title)s|%(channel)s|%(duration_string)s|%(upload_date)s" "URL"
```

### Step 3: Read Full Transcript

For long videos (>30 min), the transcript output may be large. Read in sections:

```bash
# First half
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only --timestamps | head -500
# Second half
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only --timestamps | tail -400
```

### Step 4: Generate Summary

Analyze the transcript and produce a structured summary. **ALL content must be in the chosen language — including section labels, table headers, and metadata fields.** Only the template structure (emojis, table format, blockquote format) stays fixed. The actual words are all localized.

Template structure (translate every label into the output language):

```
## [localized: "视频总结" / "Video Summary"]

**[localized label]:** (title)
**[localized label]:** (channel)
**[localized label]:** (guest, if identifiable)
**[localized label]:** (duration) | **[localized label]:** (date)

---

### [localized: one-line summary]
(1-2 sentence overview)

---

### [localized: "核心观点" / "Key Viewpoints"]

| [localized: 话题] | [localized: 观点] |
|-------|-----------|
| ... | ... |

---

### [localized: "金句" / "Notable Quotes"]
> "Original language quote" — Speaker

---

### [localized: "其他亮点" / "Other Highlights"]
- ...

---

### [localized: "注意/偏见" / "Notes / Bias"]
- ...
```

### Output Language

The summary language is determined by this priority:

1. **User explicitly specifies** (e.g. "用中文总结", "summarize in Japanese", "用英语总结") → use that language
2. **User does not specify** → **default to 中文 (Chinese)** for ALL content
3. **Quotes** → always keep in the original spoken language (do not translate quotes)
4. **Section labels, table headers, metadata fields** → translate into the output language (中文 by default)
5. **Only structural format** (tables, blockquotes, bold) stays fixed — no emojis

## Error Handling

| Error | Solution |
|-------|----------|
| `youtube-transcript-api not installed` | Run `pip3 install youtube-transcript-api` |
| `Transcripts are disabled` | Tell user subtitles are disabled for this video |
| `No transcript found` | Retry without `--language` flag, then note actual language |
| Empty output | Video may not have auto-generated subtitles; inform user |
| `yt-dlp: command not found` | Install with `pip3 install yt-dlp` or `brew install yt-dlp` |

## Reference Example

See `references/example-output.md` for a real summary (GLM-5.2 interview video, Chinese output). Use it as the quality bar for structure, conciseness, and depth.

## Tips

- **Speaker identification:** For interview/podcast videos, identify speakers from the intro and label viewpoints accordingly
- **Sponsor segments:** Skip ad reads (common in tech videos) — note them in ⚠️ section
- **Long videos (>1hr):** Process in chunks; the script outputs ~500-800 lines for a typical 1.5hr video
- **Non-English videos:** The transcript will be in the video's language; summarize in the output language per the rules above (default 中文)
