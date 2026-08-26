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

`gemini-3-pro-image` (Nano Banana Pro) par défaut, repli automatique sur
`gemini-3.1-flash-image` puis `gemini-2.5-flash-image`. Forçable avec `--model`. Chaque
image est écrite avec un `.json` voisin contenant le prompt exact, le modèle et les
paramètres — de quoi reproduire ou ajuster six mois plus tard.

**Si tu vois `429 · free_tier_requests, limit: 0`** : ce n'est pas un rate limit, c'est
l'absence de facturation sur le projet. Voir la section suivante.

---

## Ce que je peux faire moi-même, et ce qui me bloque

Testé depuis la session Claude Code, avec une clé fournie :

| Vérification | Résultat |
|---|---|
| `generativelanguage.googleapis.com` joignable | oui |
| Clé API valide | oui |
| Génération de **texte** (`gemini-3.6-flash`) | fonctionne |
| Génération d'**images**, 1er test | refusée — `free_tier_requests, limit: 0` (pas de facturation) |
| Génération d'**images**, 2e test | refusée — `Your prepayment credits are depleted` (facturation active, solde à zéro) |
| `api.elevenlabs.io` / `api.heygen.com` | bloqués par le proxy d'egress |

### Le blocage actuel : la facturation Gemini

Les modèles image ont un quota gratuit de **zéro**. Ce n'est pas un quota épuisé qui se
recharge, c'est une absence d'allocation : la génération d'images n'existe pas sur le
free tier. Le message est le même sur les six modèles image, du Pro au Flash Lite.

Le correctif est côté Google, pas côté code, et il s'est fait en deux temps :

1. **activer la facturation** sur le projet — fait, le message d'erreur a changé ;
2. **recharger le solde prépayé** sur [ai.studio/projects](https://ai.studio/projects) —
   c'est le blocage actuel. Le compte est en mode prépayé et le solde est à zéro.

Le texte continue de tourner en gratuit ; seules les images sont facturées, à l'image
générée.

### Une image reçue en conversation n'est pas une image sur le disque

Un tirage envoyé dans le fil de discussion n'atterrit dans aucun fichier du container.
Les déclinaisons ont besoin du master **en fichier** pour l'attacher à la requête. Donc
tant que le master vit seulement dans la conversation, `--ref` ne peut pas le viser :
il faut le générer ou le déposer côté machine qui exécute le script.

Une fois la facturation active, la chaîne part sans rien changer : les six modèles image
sont déjà visibles par la clé (`gen_images.py models` les liste).

### Modèles disponibles au 26/08/2026

```
gemini-3-pro-image              Nano Banana Pro        <- défaut
gemini-3.1-flash-image          Nano Banana 2
gemini-3.1-flash-lite-image     Nano Banana 2 Lite
gemini-3-pro-image-preview      Nano Banana Pro (preview)
gemini-3.1-flash-image-preview  Nano Banana 2 (preview)
gemini-2.5-flash-image          Nano Banana
```

### Une fois la facturation active

Deux options : tu lances les commandes ci-dessus chez toi, ou tu me redonnes une clé et
je génère ici — le réseau passe déjà, il ne manquait que le droit de facturer.

Dans les deux cas, **le choix du visage reste le tien**. C'est le seul arbitrage de toute
la chaîne qu'une machine ne doit pas faire à ta place : tu connais tes titulaires, moi je
connais leurs contraintes techniques.
