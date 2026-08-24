#!/usr/bin/env python3
"""
Verifie qu'une photo est exploitable par HeyGen Avatar IV avant de l'uploader.

  python3 scripts/check_photo.py out/master.png
  python3 scripts/check_photo.py out/candidates/*.png

Ce que le script controle automatiquement : format, resolution, ratio, poids,
et (si Pillow est installe) la nettete et l'exposition du cadre. Ce qu'il ne
peut pas controler tout seul est rappele en fin de sortie sous forme de
checklist visuelle : c'est la que se jouent 90 % des mauvaises animations.

Stdlib uniquement ; Pillow est utilise s'il est present, jamais requis.
"""

import struct
import sys
from pathlib import Path

MIN_WIDTH = 1024          # plancher HeyGen ; en dessous l'animation bave
GOOD_WIDTH = 2048         # cible
MAX_BYTES = 30 * 1024 * 1024

try:
    from PIL import Image, ImageFilter, ImageStat  # type: ignore

    HAS_PIL = True
except ImportError:  # pragma: no cover
    HAS_PIL = False

OK, WARN, BAD = "  ok  ", " warn ", " BAD  "


def dims_from_header(path: Path):
    """Lit largeur/hauteur sans dependance, pour PNG et JPEG."""
    data = path.read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return "PNG", w, h
    if data[:2] == b"\xff\xd8":
        i = 2
        while i < len(data) - 9:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB):
                h, w = struct.unpack(">HH", data[i + 5 : i + 9])
                return "JPEG", w, h
            if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                i += 2
                continue
            (seg,) = struct.unpack(">H", data[i + 2 : i + 4])
            i += 2 + seg
    return None, 0, 0


def analyse(path: Path) -> int:
    print(f"\n{path}")
    problems = 0

    if not path.is_file():
        print(f"{BAD} fichier introuvable")
        return 1

    size = path.stat().st_size
    fmt, w, h = dims_from_header(path)

    if fmt is None:
        print(f"{BAD} format non reconnu — HeyGen attend un PNG ou un JPEG")
        return 1
    print(f"{OK} format {fmt}")

    if size > MAX_BYTES:
        print(f"{BAD} {size // 1024 // 1024} Mo — trop lourd pour l'upload")
        problems += 1
    else:
        print(f"{OK} poids {size // 1024} Ko")

    if w < MIN_WIDTH:
        print(f"{BAD} {w}x{h} — sous le plancher de {MIN_WIDTH} px de large")
        problems += 1
    elif w < GOOD_WIDTH:
        print(f"{WARN} {w}x{h} — exploitable, mais vise {GOOD_WIDTH} px pour du 1080p net")
    else:
        print(f"{OK} resolution {w}x{h}")

    ratio = w / h if h else 0
    if ratio > 1.05:
        print(f"{WARN} cadre paysage ({ratio:.2f}) — Avatar IV preferera un portrait ou un carre")
    elif ratio < 0.6:
        print(f"{WARN} cadre tres vertical ({ratio:.2f}) — verifie que la tete n'est pas minuscule")
    else:
        print(f"{OK} ratio {ratio:.2f}")

    if HAS_PIL:
        img = Image.open(path).convert("L")
        if max(img.size) > 1600:  # on normalise pour que le seuil reste comparable
            img = img.resize((img.width * 1600 // max(img.size), img.height * 1600 // max(img.size)))
        sharp = ImageStat.Stat(img.filter(ImageFilter.FIND_EDGES)).stddev[0]
        if sharp < 8:
            print(f"{BAD} image molle (nettete {sharp:.1f}) — flou de bouge ou upscale rate")
            problems += 1
        elif sharp < 14:
            print(f"{WARN} nettete limite ({sharp:.1f})")
        else:
            print(f"{OK} nettete {sharp:.1f}")

        mean = ImageStat.Stat(img).mean[0]
        if mean < 60:
            print(f"{BAD} image sous-exposee ({mean:.0f}/255) — le visage manquera de detail")
            problems += 1
        elif mean > 200:
            print(f"{WARN} image tres claire ({mean:.0f}/255) — attention aux hautes lumieres cramees")
        else:
            print(f"{OK} exposition {mean:.0f}/255")
    else:
        print(f"{WARN} Pillow absent — nettete et exposition non verifiees (pip install Pillow)")

    return problems


CHECKLIST = """
A verifier a l'oeil, le script ne peut pas le faire :
  [ ] visage franchement de face, regard dans l'objectif
  [ ] bouche FERMEE, dents non visibles  -> c'est le point n1, Avatar IV part
      de la bouche fermee pour construire toute l'animation labiale
  [ ] aucun reflet ni voile sur les verres de lunettes
  [ ] aucune meche ne traverse le visage ni ne masque la machoire
  [ ] mains hors champ
  [ ] epaules et haut du buste visibles (pas un gros plan visage seul)
  [ ] eclairage homogene, pas de moitie de visage dans l'ombre
  [ ] separation nette entre le sujet et l'arriere-plan
"""


def main() -> int:
    paths = [Path(a) for a in sys.argv[1:]]
    if not paths:
        print(__doc__)
        return 2
    total = sum(analyse(p) for p in paths)
    print(CHECKLIST)
    if total:
        print(f"{total} probleme(s) bloquant(s). Regenere avant d'uploader.")
        return 1
    print("Aucun probleme automatique detecte.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
