# Brancher Manon dans HeyGen

Deux chemins. **Fais la première vidéo à l'interface** — tu vois immédiatement ce que
donne l'animation et tu ajustes. Passe à l'API quand tu industrialises.

---

## 1. Récupérer la voix Manon

Manon est une voix de la **bibliothèque publique** ElevenLabs. Tant qu'elle n'est pas dans
tes voix, ni l'API ni HeyGen ne la voient.

1. ElevenLabs → Voice Library → chercher **Manon** → **Add to My Voices**.
2. Vérifier qu'elle est bien là :
   ```bash
   export ELEVENLABS_API_KEY=...
   python3 scripts/tts_elevenlabs.py voices --search manon
   ```
   La commande imprime le `voice_id` à réutiliser partout.

### Les trois pièges

| Symptôme | Cause | Correctif |
|---|---|---|
| HeyGen ne liste pas Manon | pas ajoutée à *My Voices* | étape 1 ci-dessus |
| `Invalid API key` côté HeyGen | clé ElevenLabs restreinte | désactiver **Restrict Key**, ou cocher `text_to_speech` + `voices_read` |
| Voix importée muette | crédits ElevenLabs à zéro | les voix tierces cessent de fonctionner dans HeyGen, sans message clair |

---

## 2. Deux façons d'alimenter la voix — et pourquoi je recommande la seconde

**a) Intégration native.** HeyGen → *Integrate 3rd Party Voice* → *Import Voice* →
ElevenLabs → coller la clé API → confirmer. Les voix apparaissent dans AI Studio.
Simple, mais tu obtiens un TTS par défaut, sans direction d'intonation.

**b) Audio généré en amont, puis uploadé.** ⭐

```bash
python3 scripts/tts_elevenlabs.py say \
  --voice <voice_id> \
  --file docs/script-test-30s.txt \
  --out out/audio/test-30s.mp3
```

Avatar IV **analyse le ton, le rythme et les respirations de l'audio** pour fabriquer les
expressions faciales. Un audio Eleven v3 avec ses tags d'intonation produit une vidéo
nettement plus vivante que le même texte passé en TTS plat. C'est le seul levier gratuit
de qualité sur toute la chaîne.

Les tags s'écrivent en ligne, entre crochets minuscules : `[warm]`, `[thoughtful]`,
`[slight pause]`. Eleven v3 ne gère pas SSML — les tags, une ligne vide ou des points de
suspension sont les seuls moyens de placer une respiration. Limite : 3 000 caractères par
requête, soit environ 3 minutes de parole.

---

## 3. Créer l'avatar

**Interface :** Avatars → *Create Virtual Character* → *Upload Photo* → charger
`out/master.png` → Avatar → **Motion Engine → Avatar IV** → *Advanced Settings* pour
l'expressivité et la description des gestes.

Prompt de mouvement qui marche bien pour ce persona :

```
Calm professional presenter. Subtle head movements, occasional slight nod on key points.
Shoulders relaxed and stable. Direct eye contact with the camera, brief natural blinks.
No large gestures, no leaning back.
```

**API :**

```bash
export HEYGEN_API_KEY=...
python3 scripts/heygen_avatar4.py upload out/master.png          # -> image_key

python3 scripts/heygen_avatar4.py video \
  --image-key <image_key> \
  --audio out/audio/test-30s.mp3 \
  --motion "calm professional presenter, subtle head movements, occasional slight nod" \
  --width 1920 --height 1080

python3 scripts/heygen_avatar4.py status <video_id> --wait --download
```

> Le script API n'a pas pu être exécuté contre HeyGen depuis l'environnement où il a été
> écrit (accès réseau bloqué). Les endpoints suivent la doc, mais lance d'abord
> `--dry-run` pour inspecter le payload, et corrige un nom de champ si l'API a bougé.

---

## 4. Valider la photo avant de l'uploader

```bash
python3 scripts/check_photo.py out/master.png
```

Le script contrôle format, résolution, ratio, poids, netteté, exposition, puis affiche la
checklist visuelle. **La bouche fermée sur la photo source est le point numéro un** :
Avatar IV part de cette position pour reconstruire toute l'animation labiale. Une photo
dents visibles donne une bouche qui bave sur toute la vidéo.

---

## 5. Le test qui tranche

Ne juge pas l'avatar sur « bonjour je suis Manon ». Prends
[`docs/script-test-30s.txt`](script-test-30s.txt) : 30 secondes, une **question
rhétorique** et une **pause marquée**. C'est exactement là que les avatars ratés se
trahissent — le regard décroche pendant le silence, ou la bouche continue de bouger.

Si l'avatar tient ces deux moments, il tiendra n'importe quel script.
