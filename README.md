# Instagram and TikTok video extractor

A small command-line program for saving a video from an Instagram Reel, post, or TV link, or a TikTok video link. It uses `yt-dlp` to retrieve videos you can access.

## Setup

Python 3.10 or newer is recommended.

```sh
python -m pip install -r requirements.txt
```

## Use

```sh
python instagram_video.py 'https://www.instagram.com/reel/REEL_ID/'
```

TikTok links work the same way:

```sh
python instagram_video.py 'https://www.tiktok.com/@username/video/VIDEO_ID'
```

By default, the video is saved in `./downloads`. Choose another folder with `-o`:

```sh
python instagram_video.py 'https://www.instagram.com/p/POST_ID/' -o ~/Videos/instagram
```

If Instagram or TikTok requires a login, use cookies from a browser where you are already signed in:

```sh
python instagram_video.py 'https://www.instagram.com/reel/REEL_ID/' --cookies-from-browser chrome
```

Supported browser names are `chrome`, `firefox`, `safari`, `edge`, and `brave`. Keep your browser profile and cookies private; this program does not upload them itself.

## Limits

The extractor cannot access private posts or content your account is not allowed to view. Instagram or TikTok may change their sites and break extraction; updating `yt-dlp` can help. Only download content you own or have permission to save, and follow each platform's terms and applicable copyright rules.
