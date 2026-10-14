#!/usr/bin/env python3
"""Download a video from an Instagram or TikTok link using yt-dlp."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.parse import urlparse


def video_url(value: str) -> str:
    """Validate and normalize a supported Instagram or TikTok URL."""
    candidate = value.strip()
    if not candidate.startswith(("https://", "http://")):
        candidate = "https://" + candidate
    parsed = urlparse(candidate)
    host = (parsed.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    if host == "instagram.com":
        if not any(part in {"reel", "reels", "p", "tv"} for part in parsed.path.split("/")):
            raise argparse.ArgumentTypeError("Instagram link should point to a Reel, post, or TV video.")
    elif host in {"tiktok.com", "vm.tiktok.com", "vt.tiktok.com", "m.tiktok.com"}:
        if parsed.path == "/":
            raise argparse.ArgumentTypeError("Please enter a TikTok video link.")
    else:
        raise argparse.ArgumentTypeError("Please enter an Instagram or TikTok video link.")
    return candidate


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Save a video from an Instagram or TikTok link."
    )
    parser.add_argument("url", type=video_url, help="Instagram or TikTok video link")
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("downloads"),
        help="folder for the downloaded video (default: ./downloads)",
    )
    parser.add_argument(
        "--cookies-from-browser", choices=("chrome", "firefox", "safari", "edge", "brave"),
        help="use your browser login for content that requires sign-in",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        from yt_dlp import YoutubeDL
    except ImportError:
        print("Missing dependency. Install it with: python -m pip install -r requirements.txt", file=sys.stderr)
        return 2

    try:
        args.output.mkdir(parents=True, exist_ok=True)
        options = {
            "outtmpl": str(args.output / "%(title).150B [%(id)s].%(ext)s"),
            "format": "best[ext=mp4]/best",
            "noplaylist": True,
            "retries": 3,
        }
        if args.cookies_from_browser:
            options["cookiesfrombrowser"] = (args.cookies_from_browser,)
        with YoutubeDL(options) as downloader:
            downloader.download([args.url])
    except Exception as exc:  # yt-dlp raises several extractor/network-specific exception types.
        print(f"Could not download this video: {exc}", file=sys.stderr)
        print("Check that the link is public or that your browser login can access it.", file=sys.stderr)
        return 1

    print(f"Finished. Check the {args.output.resolve()} folder.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
