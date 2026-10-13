# Audio Mix

Target: **-14 LUFS integrated** (±1). Verify every final mix; never ship on guesswork.

## Narration
- Generate with the local TTS skill (see `/opt/hatch/skills/tts/SKILL.md`): one file per scene/beat, same voice throughout.
- If a line synthesizes badly (wrong speed, repeated words), split it into two shorter segments and concatenate — do not ship a glitchy take.
- Pace: ~10s per beat for a 60s video. Trim copy before stretching timing.

## Bed + ducking
- Bed clearly audible in gaps, ducked under narration (sidechain or manual volume envelope, ~0.3-0.4x under voice, 0.1-0.15s attack, ~0.6s release).
- Fade bed in/out at head and tail (1-2s).

## UI sound effects
- Synthesize or use CC0 samples: whoosh (scene transitions), pop (card/badge entrances), click (cursor clicks), thud (stamp/impact moments).
- Every SFX lands **on a beat** from the beat grid. Keep them quiet under the bed.

## Mix + verify
```bash
# example: narration + ducked bed + sfx -> loudnorm to -14 LUFS
ffmpeg -y -i narration.m4a -i bed_ducked.ogg -i sfx.m4a \
  -filter_complex "[0:a][1:a][2:a]amix=inputs=3:duration=longest,loudnorm=I=-14:TP=-1.5:LRA=11" \
  -c:a aac -b:a 160k final_audio.m4a
# verify (read the I: line)
ffmpeg -i final_audio.m4a -af ebur128 -f null - 2>&1 | grep "I:"
```
If integrated loudness is off by more than 1 LU, re-run loudnorm (two-pass) rather than hand-tuning gains.

## Subtitles
Emit `subs.srt` as a **sidecar** timed to the narration. Never burn long subtitle paragraphs into the video.
