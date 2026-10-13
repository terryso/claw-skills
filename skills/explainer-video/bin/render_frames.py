#!/usr/bin/env python3
"""Deterministic frame capture for code-rendered explainer videos.

Loads a self-contained HTML animation in headless Chromium and captures
frames by seeking the page's timeline to exact timestamps -- never by
wall-clock playback. The page must expose a pure function of time:

    seekTo(t)   // renders the frame for time t (seconds), synchronously

If `seekTo` is missing, the helper falls back to reloading with `?t=<t>`.

For motion blur, capture SUBFRAMES per output frame (at t and t+1/(fps*sub)
offsets) and blend later with ffmpeg tmix. See references/render-pipeline.md.

The page's timeline entry point is auto-detected from a candidate list
(seekTo, seek, render, setTime, drawFrame, goTo): the first candidate that
exists as a function on window is used. If none exists, the helper falls
back to reloading with `?t=<t>`.

Playwright is imported with a fallback to ~/workspace/.pylibs (where this
environment keeps it). Chromium comes from the Playwright browser cache.

Usage:
    render_frames.py --html index.html --outdir frames/ --duration 61 \\
        --fps 60 --width 1280 --height 720 --subframes 2
"""
import argparse
import os
import sys

for _p in (os.path.expanduser("~/workspace/.pylibs"),):
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("playwright is required: pip install playwright && playwright install chromium")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True, help="path to self-contained index.html")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--duration", type=float, required=True, help="seconds")
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=720)
    ap.add_argument("--subframes", type=int, default=2,
                    help="captures per output frame for motion-blur blending")
    ap.add_argument("--settle-ms", type=int, default=30,
                    help="wait after each seek before screenshot")
    ap.add_argument("--start", type=float, default=0.0,
                    help="first timestamp (seconds); use to resume ranges")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    html_url = "file://" + os.path.abspath(args.html)
    n_out = int(round((args.duration - args.start) * args.fps))

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": args.width,
                                          "height": args.height})
        page.goto(html_url)
        page.wait_for_timeout(500)
        seek_fn = page.evaluate(
            "() => ['seekTo','seek','render','setTime','drawFrame','goTo']"
            ".find(n => typeof window[n] === 'function') || null")
        if seek_fn:
            print(f"timeline entry: window.{seek_fn}(t)", flush=True)

        idx = 0
        for i in range(n_out):
            base = args.start + i / args.fps
            for j in range(args.subframes):
                t = base + j / (args.fps * args.subframes)
                if seek_fn:
                    page.evaluate(f"window.{seek_fn}({t:.4f})")
                else:
                    page.goto(f"{html_url}?t={t:.4f}")
                    page.wait_for_timeout(200)
                page.wait_for_timeout(args.settle_ms)
                page.screenshot(path=os.path.join(args.outdir,
                                                   f"frame_{idx:06d}.png"))
                idx += 1
            if (i + 1) % 120 == 0:
                print(f"captured {i + 1}/{n_out} frames", flush=True)
        browser.close()
    print(f"done: {idx} captures in {args.outdir}")


if __name__ == "__main__":
    main()
