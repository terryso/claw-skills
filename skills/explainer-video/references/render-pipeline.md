# Render Pipeline

## HTML authoring contract
- One self-contained file: inline CSS/JS, no external requests (fonts must be system or base64-embedded).
- Expose a **synchronous pure function of time** on `window`. `bin/render_frames.py` probes these names in order: `seekTo`, `seek`, `render`, `setTime`, `drawFrame`, `goTo`. Fallback: `?t=<seconds>` reload.
- No CSS transitions/animations, no `setTimeout`/`setInterval`, no state carried between frames. Parallel capture must be frame-identical.
- Backgrounds overscan ≥30% beyond the viewport on all sides (camera moves must never reveal the page background).

## Frame capture
```bash
# 60fps output with motion blur: 2 subframes per frame at t and t+1/120
python3 bin/render_frames.py --html index.html --outdir frames/ \
  --duration 61 --fps 60 --width 1280 --height 720 --subframes 2
# 9:16 vertical:
python3 bin/render_frames.py --html index_9x16.html --outdir frames_9x16/ \
  --duration 70 --fps 60 --width 720 --height 1280 --subframes 2
```
Playwright is imported with a fallback to `~/workspace/.pylibs`. Chromium comes from the Playwright browser cache (`~/.cache/ms-playwright`).

## Assembly (motion-blurred 60fps)
```bash
cd frames/
# 120fps subframes -> tmix blend -> 60fps with real motion blur
ffmpeg -y -framerate 120 -i frame_%06d.png \
  -vf "tmix=frames=2,scale=1280:720" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -r 60 silent.mp4
# mux with the final audio mix (see audio-mix.md)
ffmpeg -y -i silent.mp4 -i final_audio.m4a \
  -c:v copy -c:a aac -b:a 160k -shortest final.mp4
```

## Verification
```bash
ffprobe -v error -show_entries format=duration \
  -show_entries stream=codec_name,width,height,avg_frame_rate \
  -of default=noprint_wrappers=1 final.mp4
# expect: 60/1 fps, h264+aac, duration ~= timeline length
```
