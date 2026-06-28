---
name: youtube-summarizer
description: Download YouTube video transcripts and generate structured summaries with key viewpoints. Use when the user shares a YouTube URL and asks to summarize the video, extract transcripts, or get content insights. Supports any YouTube URL format (watch, youtu.be, shorts, embed, live).
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

Analyze the transcript and produce a structured summary in the user's language. Default output format:

```
## 📺 Video Summary

**Title:** (from metadata)
**Channel:** (from metadata)
**Guest/Speaker:** (if identifiable from intro)
**Duration:** (from metadata) | **Published:** (from metadata)

---

### One-Line Summary
(1-2 sentence overview of what the video is about)

---

### 🎯 Key Viewpoints

| Topic | Viewpoint |
|-------|-----------|
| (topic 1) | (who said what) |
| (topic 2) | (who said what) |
| ... | ... |

---

### 🔥 Notable Quotes
> "Quote 1" — Speaker
> "Quote 2" — Speaker

---

### 📌 Other Highlights
- Bullet points for interesting anecdotes, data, demos, or stories

---

### ⚠️ Notes / Bias
- Mention any obvious biases, sponsor segments, or unverified claims
```

### Output Language

- Match the user's message language for the summary
- Keep original language for quotes and transcript
- If user writes in Chinese → output summary in Chinese
- If user writes in English → output summary in English

## Error Handling

| Error | Solution |
|-------|----------|
| `youtube-transcript-api not installed` | Run `pip3 install youtube-transcript-api` |
| `Transcripts are disabled` | Tell user subtitles are disabled for this video |
| `No transcript found` | Retry without `--language` flag, then note actual language |
| Empty output | Video may not have auto-generated subtitles; inform user |
| `yt-dlp: command not found` | Install with `pip3 install yt-dlp` or `brew install yt-dlp` |

## Tips

- **Speaker identification:** For interview/podcast videos, identify speakers from the intro and label viewpoints accordingly
- **Sponsor segments:** Skip ad reads (common in tech videos) — note them in ⚠️ section
- **Long videos (>1hr):** Process in chunks; the script outputs ~500-800 lines for a typical 1.5hr video
- **Non-English videos:** The transcript will be in the video's language; summarize/translate per user request
