#!/usr/bin/env python3
"""
Regenere prompts/READY-TO-PASTE.md a partir des JSON.

  python3 scripts/build_paste_doc.py

A relancer des qu'on touche a prompts/candidates.json ou prompts/derivatives.json,
sinon le document a coller derive des prompts que le script utilise vraiment.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gen_images import compose  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

DIAL = """---

## Le curseur « plus belle »

Si A+ ne va pas encore assez loin, ajoute UNE ligne a la fois et regenere. Une seule :
empilees, elles basculent d'un coup dans le lisse artificiel.

```
Striking, magnetic presence. Impeccable grooming.
```
```
Softly glowing complexion, subtle highlighter on the cheekbones and brow bone.
```
```
Rich cinematic colour grading, deep navy and warm cream palette, gentle film grain.
```

Ce qu'il ne faut PAS ajouter, meme si la tentation est forte :

| A eviter | Pourquoi |
|---|---|
| `35 years old`, `youthful` | l'age est ce qui la rend credible face a un titulaire |
| `flawless skin`, `porcelain skin` | supprime les pores, et l'oeil detecte le faux en une seconde |
| `beautiful smile`, `bright smile` | ouvre la bouche, et Avatar IV a besoin des levres fermees |
| `supermodel`, `stunning beauty` | fait basculer vers la photo de mode, pas la photo de metier |

"""

TRI = """---

## Trier

Ecarte sans hesiter une image qui presente l'un de ces defauts, ils ne se rattrapent pas :

- **dents visibles** — Avatar IV part de la bouche fermee pour reconstruire toute
  l'animation labiale ; une bouche ouverte sur la source bave sur toute la video
- **reflet ou voile sur les lunettes**
- **une main, un doigt, un poignet dans le cadre**
- **une meche qui traverse le visage** ou masque la machoire
- **moitie de visage dans l'ombre**
- visage de trois quarts : il faut du frontal

Puis : `python3 scripts/check_photo.py ton-image.png`
"""


def block(spec, book, extra=""):
    return [
        f"### {spec['id']} — {spec['name']}",
        "",
        f"> {spec['note']}" + extra,
        "",
        "```",
        compose(spec, book.get("_common", ""), book.get("_negative", "")),
        "```",
        "",
    ]


def main() -> int:
    out = [
        "# Prompts prets a coller",
        "",
        "Genere par `scripts/build_paste_doc.py` depuis `prompts/*.json`. Colle tel quel dans",
        "Google AI Studio, l'app Gemini, ou n'importe quel generateur d'images.",
        "",
        "**Le ratio et la resolution se reglent dans l'interface, pas dans le prompt** :",
        "4:5 en 2K pour les masters. Genere 2 variantes par candidate — le premier tirage est",
        "rarement le bon.",
        "",
        "---",
        "",
        "## Etape 1 — les candidates",
        "",
        "Objectif : choisir UN visage. Ne juge pas la beaute, juge la credibilite face a un",
        "titulaire de 50 ans qui recoit trois commerciaux par semaine.",
        "",
    ]
    book = json.loads((ROOT / "prompts" / "candidates.json").read_text("utf-8"))
    for spec in book["candidates"]:
        out += block(spec, book)

    out += [DIAL]

    out += [
        "---",
        "",
        "## Etape 2 — les declinaisons",
        "",
        "**Ces prompts ne marchent QUE si tu joins le master retenu comme image de reference.**",
        "Dans AI Studio : bouton `+` -> Upload file -> ton master, puis le prompt. Sans l'image",
        "jointe, tu obtiendras une autre femme, avec le meme style. C'est l'erreur qui coute",
        "une demi-journee.",
        "",
    ]
    book = json.loads((ROOT / "prompts" / "derivatives.json").read_text("utf-8"))
    for spec in book["derivatives"]:
        out += block(spec, book, f"  \n> Ratio a regler dans l'interface : **{spec['aspectRatio']}**")

    out += [TRI]

    dest = ROOT / "prompts" / "READY-TO-PASTE.md"
    dest.write_text("\n".join(out), "utf-8")
    print(f"{dest} — {len(dest.read_text())} caracteres")
    return 0


if __name__ == "__main__":
    sys.exit(main())
