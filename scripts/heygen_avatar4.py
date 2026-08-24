#!/usr/bin/env python3
"""
Chaine HeyGen Avatar IV : upload de la photo -> generation video -> attente -> telechargement.

  export HEYGEN_API_KEY=...

  # 1. envoyer le master et recuperer sa cle
  python3 scripts/heygen_avatar4.py upload out/master.png

  # 2a. video pilotee par un audio ElevenLabs (recommande : meilleures expressions)
  python3 scripts/heygen_avatar4.py video --image-key <key> --audio out/audio/manon.mp3 \
      --motion "calm professional presenter, subtle head movements, occasional slight nod"

  # 2b. ou pilotee par un texte + une voix HeyGen
  python3 scripts/heygen_avatar4.py video --image-key <key> \
      --file docs/script-test-30s.txt --voice-id <voice_id>

  # 3. suivre / recuperer
  python3 scripts/heygen_avatar4.py status <video_id> --wait --download

ATTENTION : je n'ai pas pu executer ce script contre l'API depuis l'environnement
ou il a ete ecrit (egress bloque). Les endpoints suivent la doc HeyGen, mais si un
nom de champ a bouge, lance avec --dry-run pour voir le payload exact et ajuste.
L'interface web reste le chemin le plus sur pour la toute premiere video.

Stdlib uniquement.
"""

import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.heygen.com"
UPLOAD = "https://upload.heygen.com/v1/asset"
ROOT = Path(__file__).resolve().parent.parent


def key() -> str:
    k = os.environ.get("HEYGEN_API_KEY")
    if not k:
        sys.exit("HEYGEN_API_KEY absente (Settings > API dans HeyGen)")
    return k


def request(url: str, data=None, headers=None, method="GET", timeout=180):
    req = urllib.request.Request(
        url,
        data=data,
        headers={"X-Api-Key": key(), **(headers or {})},
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:800]
        sys.exit(f"HTTP {exc.code} sur {url}\n{body}")


def cmd_upload(args) -> int:
    path = Path(args.image)
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    print(f"upload {path} ({path.stat().st_size // 1024} Ko, {mime})")
    res = request(UPLOAD, data=path.read_bytes(), headers={"Content-Type": mime}, method="POST")
    data = res.get("data", res)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    ident = data.get("image_key") or data.get("asset_id") or data.get("id")
    if ident:
        print(f"\n-> cle a reutiliser : {ident}")
    return 0


def cmd_video(args) -> int:
    payload = {
        "image_key": args.image_key,
        "dimension": {"width": args.width, "height": args.height},
    }
    if args.audio or args.audio_url:
        # l'audio pilote a la fois les levres et les expressions
        payload["audio_url"] = args.audio_url or _upload_audio(args.audio)
    else:
        text = Path(args.file).read_text("utf-8") if args.file else args.text
        if not text:
            sys.exit("passe --audio, --audio-url, --text ou --file")
        if not args.voice_id:
            sys.exit("--voice-id est requis quand on pilote par du texte")
        payload["voice_id"] = args.voice_id
        payload["text"] = text.strip()
    if args.motion:
        payload["custom_motion_prompt"] = args.motion
        payload["enhance_custom_motion_prompt"] = True

    if args.dry_run:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    res = request(
        f"{API}/v2/video/av4/generate",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    data = res.get("data", res)
    vid = data.get("video_id") or data.get("id")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    if vid:
        print(f"\n-> python3 scripts/heygen_avatar4.py status {vid} --wait --download")
    return 0


def _upload_audio(path_str: str) -> str:
    path = Path(path_str)
    mime = mimetypes.guess_type(path.name)[0] or "audio/mpeg"
    print(f"upload audio {path} ({path.stat().st_size // 1024} Ko)")
    res = request(UPLOAD, data=path.read_bytes(), headers={"Content-Type": mime}, method="POST")
    data = res.get("data", res)
    url = data.get("url") or data.get("asset_url")
    if not url:
        sys.exit(f"pas d'URL dans la reponse d'upload audio :\n{json.dumps(data, indent=2)}")
    return url


def cmd_status(args) -> int:
    deadline = time.time() + args.timeout
    while True:
        res = request(f"{API}/v1/video_status.get?video_id={args.video_id}")
        data = res.get("data", res)
        state = data.get("status")
        print(f"[{time.strftime('%H:%M:%S')}] {state}")
        if state in ("completed", "success"):
            url = data.get("video_url")
            print(url)
            if args.download and url:
                out = Path(args.out or ROOT / "out" / "video" / f"{args.video_id}.mp4")
                out.parent.mkdir(parents=True, exist_ok=True)
                with urllib.request.urlopen(url, timeout=600) as r:
                    out.write_bytes(r.read())
                print(f"-> {out}")
            return 0
        if state in ("failed", "error"):
            print(json.dumps(data, indent=2, ensure_ascii=False), file=sys.stderr)
            return 1
        if not args.wait or time.time() > deadline:
            return 0
        time.sleep(args.interval)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    u = sub.add_parser("upload", help="uploader la photo de l'avatar")
    u.add_argument("image")
    u.set_defaults(func=cmd_upload)

    v = sub.add_parser("video", help="lancer une generation Avatar IV")
    v.add_argument("--image-key", required=True)
    v.add_argument("--text")
    v.add_argument("--file")
    v.add_argument("--voice-id")
    v.add_argument("--audio", help="fichier audio local (ElevenLabs)")
    v.add_argument("--audio-url", help="audio deja heberge")
    v.add_argument("--motion", help="custom_motion_prompt : gestes et expressions")
    v.add_argument("--width", type=int, default=1920)
    v.add_argument("--height", type=int, default=1080)
    v.add_argument("--dry-run", action="store_true")
    v.set_defaults(func=cmd_video)

    s = sub.add_parser("status", help="suivre une generation")
    s.add_argument("video_id")
    s.add_argument("--wait", action="store_true")
    s.add_argument("--download", action="store_true")
    s.add_argument("--out")
    s.add_argument("--interval", type=int, default=15)
    s.add_argument("--timeout", type=int, default=1800)
    s.set_defaults(func=cmd_status)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
