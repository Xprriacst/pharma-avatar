# Manon — avatar HeyGen pour titulaires d'officine

Chaîne complète : générer le visage avec Gemini → valider la photo → produire la voix
avec ElevenLabs → animer avec HeyGen Avatar IV.

```
docs/persona-manon.md      la fiche persona — la référence, tout se valide contre elle
docs/heygen-setup.md       branchement HeyGen + ElevenLabs, et les 3 pièges connus
docs/script-test-30s.txt   le script de test qui révèle un avatar raté
prompts/candidates.json    4 portraits maîtres
prompts/derivatives.json   les déclinaisons, à partir du master retenu
scripts/gen_images.py      images Gemini (Nano Banana)
scripts/check_photo.py     contrôle des contraintes Avatar IV avant upload
scripts/tts_elevenlabs.py  audio ElevenLabs
scripts/heygen_avatar4.py  upload photo + génération vidéo + suivi
```

Aucune dépendance : stdlib Python 3.11 uniquement. Pillow est utilisé par
`check_photo.py` s'il est présent, jamais requis.

---

## Parcours complet

```bash
export GEMINI_API_KEY=...        # https://aistudio.google.com/apikey

# 0. Quels modèles image ta clé voit-elle vraiment ?
python3 scripts/gen_images.py models

# 1. Quatre visages candidats, deux variations chacun
python3 scripts/gen_images.py candidates --n 2

# 2. Tu choisis UN visage. Il devient le master, définitif.
cp out/candidates/A_consultante-terrain_1.png out/master.png
python3 scripts/check_photo.py out/master.png

# 3. Toutes les déclinaisons — même personne, garantie par --ref
python3 scripts/gen_images.py derivatives --ref out/master.png

# 4. La voix
export ELEVENLABS_API_KEY=...
python3 scripts/tts_elevenlabs.py voices --search manon
python3 scripts/tts_elevenlabs.py say --voice <voice_id> \
    --file docs/script-test-30s.v3.txt --out out/audio/test-30s.mp3

# 5. La vidéo
export HEYGEN_API_KEY=...
python3 scripts/heygen_avatar4.py upload out/master.png
python3 scripts/heygen_avatar4.py video --image-key <key> --audio out/audio/test-30s.mp3 \
    --motion "calm professional presenter, subtle head movements, occasional slight nod"
```

Voir les prompts sans dépenser un crédit : `--dry-run`.

## Le point qui compte : `--ref`

En mode `derivatives`, `--ref` attache le master à la requête. Sans lui, Gemini regénère
**quelqu'un d'autre** — même prompt, autre visage. C'est ce paramètre, et lui seul, qui
transforme une jolie image en avatar réutilisable sur tous tes supports. Le script refuse
de tourner sans.

## Choix de modèle

`gemini-3-pro-image-preview` (Nano Banana Pro) par défaut, repli automatique sur
`gemini-2.5-flash-image` si la preview n'est pas ouverte sur ta clé. Forçable avec
`--model`. Chaque image est écrite avec un `.json` voisin contenant le prompt exact, le
modèle et les paramètres — de quoi reproduire ou ajuster six mois plus tard.

---

## Ce que je peux faire moi-même, et ce qui me bloque

Testé hôte par hôte depuis la session Claude Code où ce dépôt a été écrit :

| Hôte | État | Détail |
|---|---|---|
| `generativelanguage.googleapis.com` | **joignable** | répond `403 · Method doesn't allow unregistered callers` — c'est Google qui réclame une clé, pas le proxy qui bloque |
| `api.elevenlabs.io` | bloqué | `CONNECT tunnel failed` au niveau du proxy d'egress |
| `api.heygen.com` | bloqué | idem |

Autrement dit : **pour Gemini, il ne me manque que la clé.** Le réseau passe déjà.

### Pour que je génère les images moi-même

Ajouter `GEMINI_API_KEY` aux variables d'environnement Claude Code
(Settings → Environments → variables). Rien d'autre à débloquer. À la session suivante
je lance la chaîne complète ici : les quatre candidates, un coup d'œil, j'écarte les
ratés (reflets sur les lunettes, dents visibles, mains rentrées dans le cadre), je
relance sur les prompts qui méritent un second tour, je te rends les fichiers et le
`check_photo.py` de chacun.

Pour ElevenLabs et HeyGen il faudra en plus autoriser `api.elevenlabs.io`,
`api.heygen.com` et `upload.heygen.com` dans les domaines de l'environnement — ou faire
ces deux étapes à l'interface, ce qui reste de toute façon recommandé pour la première
vidéo.

### Ou tu lances toi-même

Les trois lignes de l'étape 1 ci-dessus, chez toi. Trente secondes, et tu gardes la main
sur la facturation.

Dans les deux cas, **le choix du visage reste le tien**. C'est le seul arbitrage de toute
la chaîne qu'une machine ne doit pas faire à ta place : tu connais tes titulaires, moi je
connais leurs contraintes techniques.
