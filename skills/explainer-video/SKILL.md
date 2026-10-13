---
name: explainer-video
slug: explainer-video
displayName: 代码渲染讲解视频
version: 1.0.0
summary: 把文章/帖子变成 60 秒代码渲染讲解视频：HTML 时间轴 → 无头浏览器逐帧 → ffmpeg 合成，弹簧物理、接缝语法、节拍网格、-14 LUFS 混音
license: MIT
description: Turn an article or post into a 60-second code-rendered explainer video: a single self-contained HTML timeline rendered frame-by-frame with headless Chromium and assembled with ffmpeg. Use when the user wants a blog post, HN story, or any article distilled into a motion-graphics video with narration, beat-synced motion, and broadcast-loudness audio. Covers 16:9 and 9:16. Not for AI-diffusion video generation or photorealistic footage.
---

# Explainer Video

## Purpose
Produce a ~60s code-rendered explainer video from a source article: HTML animation → deterministic frame capture → ffmpeg assembly → narrated, beat-synced, loudness-normalized MP4.

## Workflow
1. **Distill the source.** Read the article, extract 5-7 beats that fit ~60s. Write one narration line per beat (Chinese unless asked otherwise). Keep on-screen text to keywords only — narration carries the story.
2. **Set the art direction.** Pick a visual language deliberately distinct from previous episodes (background, accent color, typography pairing, recurring motif). Record it; never repeat the last episode's look.
3. **Author one self-contained HTML file.** All motion computed in a pure function of time exposed on window (`seekTo`/`seek`/`render` + others — see `bin/render_frames.py` candidate list). No CSS transitions, no timers, no state between frames. Follow `references/seam-grammar.md` for motion rules.
4. **Analyze the music bed first.** Pick a CC-licensed track with a clear pulse (~100-150 BPM; Wikimedia Commons). Run `bin/beat_grid.py` — require `grid_energy_ratio >= 1.5`, otherwise pick another bed. Lock scene boundaries and hits to the beat grid.
5. **Probe before rendering.** Render ~1 frame per 2 seconds, inspect every frame: overlap, cramped type, edge reveal at max camera excursion, dead beats. Fix, re-probe. See `references/qa-checklist.md`.
6. **Render frames.** `bin/render_frames.py --html index.html --outdir frames/ --duration 61 --fps 60 --subframes 2` (720p: 1280×720 or 720×1280). Assemble per `references/render-pipeline.md` (tmix motion blur → 60fps H.264).
7. **Audio.** Generate narration with the local TTS skill (one file per beat), mix bed with ducking under narration, add UI SFX on beat hits, loudnorm to **-14 LUFS integrated**. Verify with `ffmpeg -af ebur128`. See `references/audio-mix.md`.
8. **Deliver.** Final MP4 + preview JPGs + `subs.srt` sidecar (never burn long subtitles into the video) + keep the HTML source.

## Output Contract
- One MP4: 1280×720 or 720×1280, 60fps, H.264 + AAC, ~60-70s, integrated loudness -14 LUFS (±1).
- Preview frames (one per scene), SRT sidecar timed to narration, single-file HTML source.
- Zero cross-dissolves between scenes; zero burned-in subtitle paragraphs; background never reveals at camera extremes.

## Operating Rules
1. Deterministic rendering only: every frame is a pure function of `t`. Never rely on wall-clock playback.
2. Springs, not eases: closed-form spring step responses with slight overshoot. Linear/CSS eases are banned for element motion.
3. Cross-dissolves between scenes are banned. Use the seam grammar (references/seam-grammar.md).
4. On-screen text is kinetic typography only: big numbers, short phrases (≤8 CJK chars), keyword pills. Full sentences live in narration.
5. Never invent tools, paths, or credentials. Playwright/Chromium/ffmpeg/numpy are the stack; the local TTS skill does narration; music must be CC-licensed with attribution kept.
6. Cost discipline: everything runs locally. No paid APIs, no subscriptions.
