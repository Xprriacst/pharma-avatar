#!/usr/bin/env python3
"""
Genere l'audio de Manon avec ElevenLabs, pour le donner ensuite a HeyGen.

Pourquoi passer par un fichier audio plutot que par l'integration voix de
HeyGen : Avatar IV lit le ton, le rythme et les respirations de l'audio pour
fabriquer les expressions du visage. Un TTS plat donne une video plate. Un
audio v3 avec des tags d'intonation donne une video qui bouge.

  export ELEVENLABS_API_KEY=...

  # trouver l'id de la voix Manon (elle doit etre ajoutee a "My Voices" d'abord)
  python3 scripts/tts_elevenlabs.py voices --search manon

  # generer l'audio d'un script
  python3 scripts/tts_elevenlabs.py say --voice <voice_id> --file docs/script-test-30s.txt

Stdlib uniquement.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.elevenlabs.io/v1"
ROOT = Path(__file__).resolve().parent.parent


def key() -> str:
    k = os.environ.get("ELEVENLABS_API_KEY")
    if not k:
        sys.exit("ELEVENLABS_API_KEY absente (https://elevenlabs.io/app/settings/api-keys)")
    return k


def call(path: str, data=None, method="GET", accept="application/json"):
    req = urllib.request.Request(
        f"{API}{path}",
        data=json.dumps(data).encode() if data is not None else None,
        headers={"xi-api-key": key(), "Content-Type": "application/json", "Accept": accept},
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            raw = resp.read()
            return json.loads(raw) if accept == "application/json" else raw
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:600]
        if exc.code == 401:
            body += (
                "\n  -> cle invalide, ou permissions insuffisantes. "
                "Desactive 'Restrict Key' ou coche text_to_speech + voices_read."
            )
        sys.exit(f"HTTP {exc.code} sur {path}\n{body}")


def cmd_voices(args) -> int:
    data = call("/voices")
    voices = data.get("voices", [])
    needle = (args.search or "").lower()
    hits = [v for v in voices if needle in v.get("name", "").lower()] if needle else voices
    if not hits:
        print(
            f"Aucune voix ne correspond a '{args.search}' dans My Voices.\n"
            "Manon est une voix de la bibliotheque publique : ouvre la Voice Library\n"
            "dans ElevenLabs et clique 'Add to My Voices'. Tant qu'elle n'y est pas,\n"
            "ni l'API ni HeyGen ne la verront."
        )
        return 1
    for v in hits:
        labels = ", ".join(f"{k}={x}" for k, x in (v.get("labels") or {}).items())
        print(f"{v['voice_id']}  {v['name']:<24} {labels}")
    return 0


def cmd_say(args) -> int:
    text = Path(args.file).read_text("utf-8") if args.file else args.text
    if not text:
        sys.exit("passe --text ou --file")
    if len(text) > 3000 and args.model == "eleven_v3":
        print(f"! {len(text)} caracteres : eleven_v3 plafonne a 3000, decoupe ton script.", file=sys.stderr)

    audio = call(
        f"/text-to-speech/{args.voice}?output_format={args.format}",
        data={
            "text": text,
            "model_id": args.model,
            "voice_settings": {
                "stability": args.stability,
                "similarity_boost": args.similarity,
                "style": args.style,
                "use_speaker_boost": True,
            },
        },
        method="POST",
        accept="audio/mpeg",
    )
    out = Path(args.out or ROOT / "out" / "audio" / "manon.mp3")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(audio)
    print(f"{out}  ({len(audio) // 1024} Ko, {args.model})")
    print("-> a uploader dans HeyGen comme piste audio de l'Avatar IV")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("voices", help="lister les voix de My Voices")
    v.add_argument("--search", help="filtre sur le nom (ex: manon)")
    v.set_defaults(func=cmd_voices)

    s = sub.add_parser("say", help="synthetiser un script")
    s.add_argument("--voice", required=True, help="voice_id (cf. sous-commande voices)")
    s.add_argument("--text")
    s.add_argument("--file", help="fichier texte du script")
    s.add_argument("--out")
    s.add_argument("--model", default="eleven_v3", help="eleven_v3 | eleven_multilingual_v2 | eleven_flash_v2_5")
    s.add_argument("--format", default="mp3_44100_128")
    # stabilite basse = plus d'intonation, ce qu'on veut pour nourrir Avatar IV
    s.add_argument("--stability", type=float, default=0.45)
    s.add_argument("--similarity", type=float, default=0.8)
    s.add_argument("--style", type=float, default=0.35)
    s.set_defaults(func=cmd_say)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
