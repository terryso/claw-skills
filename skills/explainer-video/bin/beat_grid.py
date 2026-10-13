#!/usr/bin/env python3
"""Beat-grid analysis for explainer-video music beds.

Decodes audio with ffmpeg, builds a high-frequency-content onset envelope
with numpy, then folds it into candidate periods to find the most reliable
pulse grid.

Outputs JSON: {bpm, beat_period_s, offset_s, beats: [t0, t1, ...], grid_energy_ratio}

The `grid_energy_ratio` (phase-profile peak/mean) tells you how trustworthy
the grid is. < 1.5 means the track has no usable pulse -- pick a different
bed instead of forcing it. Percussive beds (e.g. Kevin MacLeod's Hitman)
typically score > 2.0; ambient beds (e.g. Komiku's Ambiant Hope) score ~1.4.

Usage:
    beat_grid.py BED_FILE [--min-bpm 90] [--max-bpm 160] [--duration 61] [-o grid.json]
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

try:
    import numpy as np
except ImportError:
    sys.exit("numpy is required: pip install numpy")


def decode_mono(path, sr=22050):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav = tmp.name
    try:
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", path,
             "-ac", "1", "-ar", str(sr), "-f", "wav", wav],
            check=True)
        raw = open(wav, "rb").read()
    finally:
        os.unlink(wav)
    # skip 44-byte WAV header
    pcm = np.frombuffer(raw[44:], dtype=np.int16).astype(np.float32)
    peak = np.max(np.abs(pcm))
    if peak > 0:
        pcm /= peak
    return pcm, sr


def onset_envelope(pcm, sr, hop=256, n_fft=1024):
    # High-frequency-content spectral flux: percussive attacks are broadband,
    # so weighting magnitude bins by frequency isolates kick/hat transients
    # far better than plain spectral flux (which drowns in dense textures).
    if len(pcm) < n_fft:
        pcm = np.pad(pcm, (0, n_fft - len(pcm)))
    window = np.hanning(n_fft)
    n_frames = 1 + (len(pcm) - n_fft) // hop
    shape = (n_frames, n_fft)
    strides = (pcm.strides[0] * hop, pcm.strides[0])
    frames = np.lib.stride_tricks.as_strided(pcm, shape=shape, strides=strides)
    spec = np.abs(np.fft.rfft(frames * window, axis=1))
    freqs = np.fft.rfftfreq(n_fft, 1.0 / sr)
    hfc = (spec * freqs).sum(axis=1)
    flux = np.diff(hfc, prepend=hfc[0])
    return np.clip(flux, 0, None)


def phase_profile_score(env, hop_s, period):
    """Fold the onset envelope into one period; return (peak/mean, offset_s).

    A real pulse concentrates energy in one phase bin: peak/mean >> 1.
    The hottest bin's time position is the grid offset. No separate offset
    search needed -- folding IS the offset search.
    """
    ph = int(round(period / hop_s))
    if ph < 2:
        return 0.0, 0.0
    idx = np.arange(len(env)) % ph
    acc = np.bincount(idx, weights=env, minlength=ph).astype(float)
    mean = acc.mean()
    if mean <= 0:
        return 0.0, 0.0
    hot = int(np.argmax(acc))
    return float(acc[hot] / mean), float(hot * hop_s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bed")
    ap.add_argument("--min-bpm", type=float, default=90)
    ap.add_argument("--max-bpm", type=float, default=170)
    ap.add_argument("--duration", type=float, default=61.0,
                    help="seconds of beat times to emit")
    ap.add_argument("-o", "--output", default=None)
    args = ap.parse_args()

    pcm, sr = decode_mono(args.bed)
    hop = 256
    env = onset_envelope(pcm, sr, hop)
    hop_s = hop / sr

    best_bpm, best_score, best_off = None, 0.0, 0.0
    bpm = args.min_bpm
    while bpm <= args.max_bpm:
        score, off = phase_profile_score(env, hop_s, 60.0 / bpm)
        if score > best_score:
            best_score, best_bpm, best_off = score, bpm, off
        bpm += 1.0

    period = 60.0 / best_bpm
    beats = [round(float(t), 3)
             for t in np.arange(best_off, args.duration, period)]
    result = {
        "bpm": round(best_bpm, 1),
        "beat_period_s": round(period, 4),
        "offset_s": round(best_off, 3),
        "beats": beats,
        "grid_energy_ratio": round(best_score, 2),
    }
    out = json.dumps(result, indent=2)
    if args.output:
        open(args.output, "w").write(out + "\n")
    print(out)


if __name__ == "__main__":
    main()
