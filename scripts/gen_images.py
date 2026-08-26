#!/usr/bin/env python3
"""
Genere les portraits de l'avatar Manon via l'API Gemini (Nano Banana).

Deux modes :

  candidates   -> 4 portraits maitres, a partir de prompts/candidates.json
  derivatives  -> declinaisons du master retenu, a partir de prompts/derivatives.json
                  (necessite --ref : l'image de reference qui fixe l'identite du visage)

Exemples
--------
  export GEMINI_API_KEY=...

  # 1. Les 4 candidates, 2 variations chacune
  python3 scripts/gen_images.py candidates --n 2

  # 2. On choisit, on fige le master
  cp out/candidates/A_consultante-terrain_1.png out/master.png

  # 3. Toutes les declinaisons, meme visage
  python3 scripts/gen_images.py derivatives --ref out/master.png

  # 4. Une seule declinaison
  python3 scripts/gen_images.py derivatives --ref out/master.png --id vertical

Aucune dependance : stdlib uniquement.
"""

import argparse
import base64
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API_HOST = "https://generativelanguage.googleapis.com"

# Nano Banana Pro d'abord (meilleur rendu peau/texte), repli sur le modele GA.
DEFAULT_MODELS = [
    "gemini-3-pro-image",        # Nano Banana Pro (GA) : le meilleur sur la peau et le regard
    "gemini-3.1-flash-image",    # Nano Banana 2 : plus rapide, bon pour iterer
    "gemini-2.5-flash-image",    # repli historique
]

ROOT = Path(__file__).resolve().parent.parent


class GeminiError(RuntimeError):
    pass


def api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        sys.exit(
            "GEMINI_API_KEY absente.\n"
            "  export GEMINI_API_KEY=...   (cle sur https://aistudio.google.com/apikey)"
        )
    return key


def post(model: str, payload: dict, timeout: int = 300) -> dict:
    url = f"{API_HOST}/v1beta/models/{model}:generateContent"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key(),
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")[:800]
        raise GeminiError(f"HTTP {exc.code} sur {model}\n{body}") from exc
    except urllib.error.URLError as exc:
        raise GeminiError(
            f"Reseau injoignable ({exc.reason}). "
            "Si tu es derriere un proxy d'entreprise, verifie que "
            "generativelanguage.googleapis.com est autorise."
        ) from exc


def generate(models, payload, retries: int = 3) -> dict:
    """Essaie chaque modele; sur 429/500 on retente avec backoff."""
    last = None
    for model in models:
        for attempt in range(retries):
            try:
                return post(model, payload) | {"_model": model}
            except GeminiError as exc:
                last = exc
                msg = str(exc)
                if "HTTP 404" in msg or "HTTP 400" in msg:
                    print(f"  ! {model} indisponible, modele suivant", file=sys.stderr)
                    break
                if attempt < retries - 1 and any(
                    c in msg for c in ("HTTP 429", "HTTP 500", "HTTP 503")
                ):
                    wait = 2 ** (attempt + 1)
                    print(f"  ~ retry dans {wait}s ({msg.splitlines()[0]})", file=sys.stderr)
                    time.sleep(wait)
                    continue
                break
    raise last if last else GeminiError("aucun modele disponible")


def extract_images(resp: dict):
    out = []
    for cand in resp.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            blob = part.get("inlineData") or part.get("inline_data")
            if blob and blob.get("data"):
                out.append(
                    (
                        base64.b64decode(blob["data"]),
                        blob.get("mimeType") or blob.get("mime_type") or "image/png",
                    )
                )
    if not out:
        reason = ""
        for cand in resp.get("candidates", []):
            if cand.get("finishReason"):
                reason = f" (finishReason={cand['finishReason']})"
            for part in cand.get("content", {}).get("parts", []):
                if part.get("text"):
                    reason += f"\n  modele: {part['text'][:300]}"
        raise GeminiError("aucune image dans la reponse" + reason)
    return out


def ref_part(path: Path) -> dict:
    data = path.read_bytes()
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    return {"inlineData": {"mimeType": mime, "data": base64.b64encode(data).decode()}}


def build_payload(text: str, aspect: str, size: str, ref: Path | None) -> dict:
    parts = []
    if ref:
        parts.append(ref_part(ref))
    parts.append({"text": text})
    return {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
            "imageConfig": {"aspectRatio": aspect, "imageSize": size},
        },
    }


def compose(spec: dict, common: str, negative: str) -> str:
    return "\n".join(
        [
            common.strip(),
            "",
            spec["prompt"].strip(),
            "",
            "Avoid: " + negative.strip(),
        ]
    )


def slug(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", s).strip("-")


def list_models() -> int:
    """Quels modeles image la cle voit-elle reellement ? (la preview n'est pas ouverte a tous)"""
    url = f"{API_HOST}/v1beta/models"
    req = urllib.request.Request(url, headers={"x-goog-api-key": api_key()})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        sys.exit(f"HTTP {exc.code}\n{exc.read().decode('utf-8', 'replace')[:500]}")
    found = False
    for m in data.get("models", []):
        name = m.get("name", "").removeprefix("models/")
        if "image" in name:
            found = True
            mark = " <- defaut" if name == DEFAULT_MODELS[0] else ""
            print(f"{name:<34} {m.get('displayName', '')}{mark}")
    if not found:
        print("aucun modele image visible par cette cle", file=sys.stderr)
        return 1
    return 0


def run(args) -> int:
    book = json.loads((ROOT / "prompts" / f"{args.mode}.json").read_text("utf-8"))
    key = "candidates" if args.mode == "candidates" else "derivatives"
    specs = book[key]

    if args.id:
        wanted = {i.lower() for i in args.id}
        specs = [s for s in specs if s["id"].lower() in wanted]
        if not specs:
            sys.exit(f"aucun prompt ne correspond a {args.id}")

    ref = Path(args.ref) if args.ref else None
    if args.mode == "derivatives" and not ref:
        sys.exit(
            "--ref est obligatoire en mode derivatives.\n"
            "  Sans image de reference, Gemini genere une autre personne.\n"
            "  Ex: --ref out/master.png"
        )
    if ref and not ref.is_file():
        sys.exit(f"reference introuvable : {ref}")

    defaults = book.get("_defaults", {})
    outdir = Path(args.out) if args.out else ROOT / "out" / args.mode
    outdir.mkdir(parents=True, exist_ok=True)

    models = [args.model] if args.model else DEFAULT_MODELS
    written, failed = [], []

    for spec in specs:
        aspect = args.aspect or spec.get("aspectRatio") or defaults.get("aspectRatio", "4:5")
        size = args.size or spec.get("imageSize") or defaults.get("imageSize", "2K")
        text = compose(spec, book.get("_common", ""), book.get("_negative", ""))
        payload = build_payload(text, aspect, size, ref)

        for n in range(1, args.n + 1):
            stem = f"{slug(spec['id'])}_{slug(spec['name'])}_{n}"
            print(f"-> {stem}  [{aspect} {size}]")
            if args.dry_run:
                print(text + "\n")
                continue
            try:
                resp = generate(models, payload)
            except GeminiError as exc:
                print(f"  ECHEC: {exc}", file=sys.stderr)
                failed.append(stem)
                continue

            for idx, (data, mime) in enumerate(extract_images(resp)):
                ext = ".jpg" if "jpeg" in mime else ".png"
                suffix = "" if idx == 0 else f"-{idx}"
                path = outdir / f"{stem}{suffix}{ext}"
                path.write_bytes(data)
                # sidecar : on garde la tracabilite exacte de ce qui a produit l'image
                path.with_suffix(".json").write_text(
                    json.dumps(
                        {
                            "id": spec["id"],
                            "name": spec["name"],
                            "note": spec.get("note", ""),
                            "model": resp.get("_model"),
                            "aspectRatio": aspect,
                            "imageSize": size,
                            "reference": str(ref) if ref else None,
                            "prompt": text,
                        },
                        ensure_ascii=False,
                        indent=2,
                    ),
                    "utf-8",
                )
                print(f"   {path}  ({len(data) // 1024} Ko, {resp.get('_model')})")
                written.append(path)

    if not args.dry_run:
        print(f"\n{len(written)} image(s) dans {outdir}")
        if failed:
            print(f"{len(failed)} echec(s) : {', '.join(failed)}", file=sys.stderr)
            return 1
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mode", choices=["candidates", "derivatives", "models"])
    p.add_argument("--id", nargs="+", help="ne generer que ces ids (ex: A D / vertical)")
    p.add_argument("--ref", help="image de reference (obligatoire en derivatives)")
    p.add_argument("--n", type=int, default=1, help="variations par prompt (defaut 1)")
    p.add_argument("--aspect", help="force le ratio (1:1 4:5 3:4 16:9 9:16 ...)")
    p.add_argument("--size", help="force la resolution (1K 2K 4K)")
    p.add_argument("--model", help=f"force le modele (defaut: {' puis '.join(DEFAULT_MODELS)})")
    p.add_argument("--out", help="dossier de sortie")
    p.add_argument("--dry-run", action="store_true", help="affiche les prompts sans appeler l'API")
    args = p.parse_args()
    try:
        return list_models() if args.mode == "models" else run(args)
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
