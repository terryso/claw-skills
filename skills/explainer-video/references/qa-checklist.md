# QA Checklist

Run these before the full render. A failed check stops the build.

## 1. Probe frames (~1 per 2 seconds of timeline)
Render probes across the whole timeline and inspect every one:
- [ ] No overlapping text/cards; no cramped type; nothing clipped by frame edges
- [ ] On-screen text ≤ keyword level (big numbers, ≤8 CJK chars per phrase, pills)
- [ ] No burned-in subtitle paragraphs

## 2. Seam verification (every scene boundary)
For each cut, check the frames at cut ±0.25s:
- [ ] Zero cross-dissolves in the timeline code (`grep -i crossfade` → no hits)
- [ ] A is still moving at the cut frame; B is mid-flight (not starting from rest)
- [ ] Exit/entry vectors match (axis + direction); carriers cross the cut
- [ ] No dead beats: something is in motion at every cut

## 3. Camera edge check
- [ ] All backgrounds overscan ≥30% beyond viewport on every side
- [ ] Probe frames at each scene's maximum camera excursion show no page background

## 4. Beat alignment
- [ ] Scene boundaries sit on downbeats; visual hits sit on beats (from `grid.json`)
- [ ] No section longer than ~2 beats without motion or a hit

## 5. Audio verification
- [ ] `ebur128` integrated loudness = -14 LUFS (±1)
- [ ] Bed audible in gaps, ducked under narration; SFX on beats, quiet under bed
- [ ] Narration takes are clean (no glitches, consistent voice)

## 6. Final file check
- [ ] `ffprobe`: 60fps, H.264 + AAC, duration ≈ timeline length
- [ ] Preview JPGs exported (one per scene + opening/closing)
- [ ] `subs.srt` sidecar timed to narration; HTML source kept
