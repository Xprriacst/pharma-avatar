# Prompts prêts à coller

Assemblés depuis `prompts/*.json`. Colle tel quel dans Google AI Studio, l'app Gemini,
ou n'importe quel générateur d'images.

**Le ratio et la résolution se règlent dans l'interface, pas dans le prompt** :
4:5 en 2K pour les masters. Génère 2 variantes par candidate — le premier tirage est
rarement le bon.

---

## Étape 1 — les 4 candidates

Objectif : choisir UN visage. Ne juge pas la beauté, juge la crédibilité face à un
titulaire de 50 ans qui reçoit trois commerciaux par semaine.

### A — consultante-terrain

> Le pari par defaut. Lunettes = credibilite, blazer = interlocutrice de chef d'entreprise, decor pharmacie = 'je connais votre monde'.

```
Photorealistic editorial portrait photograph, shot on Canon EOS R5, 85mm lens at f/2.0, shallow depth of field. Medium shot: head and shoulders, upper chest visible, body turned slightly (about 15 degrees) but face fully frontal to the camera, eyes looking directly into the lens. Closed-mouth confident smile, relaxed jaw, warm and attentive expression, natural skin texture with visible pores and fine lines. Soft natural window light from the left, gentle fill on the right, no hard shadows across the face. Even lighting on the entire face. Clear separation between subject and background.

French woman, 42 years old, shoulder-length dark brown hair with a few natural greys, side part, loosely tucked behind one ear. Wearing a light cream silk blouse under a well-cut navy blazer, no necklace, small simple stud earrings, thin tortoiseshell rectangular glasses. Background: the back-office of a French pharmacy, softly blurred, shelves of white and pale-green medicine boxes, warm neutral tones.

Avoid: No text, no watermark, no logo, no signature. No exaggerated makeup, no stock-photo grin, no teeth showing. No white lab coat, no medical scrubs, no stethoscope, no caduceus. Hands not visible. No motion blur, no lens flare, no glasses glare or reflections, no harsh specular highlights on skin. No hair strands crossing the face, no hair covering the jawline. Not a 3D render, not an illustration, not AI-plastic skin.
```

### B — proche-sans-lunettes

> Variante plus chaleureuse, sans lunettes. A tester si A parait trop 'commerciale grand compte'.

```
Photorealistic editorial portrait photograph, shot on Canon EOS R5, 85mm lens at f/2.0, shallow depth of field. Medium shot: head and shoulders, upper chest visible, body turned slightly (about 15 degrees) but face fully frontal to the camera, eyes looking directly into the lens. Closed-mouth confident smile, relaxed jaw, warm and attentive expression, natural skin texture with visible pores and fine lines. Soft natural window light from the left, gentle fill on the right, no hard shadows across the face. Even lighting on the entire face. Clear separation between subject and background.

French woman, 40 years old, dark chestnut hair gathered in a low loose bun, a few strands framing the face, no glasses. Wearing a fine-knit warm grey round-neck sweater, a thin gold chain barely visible at the collar. Warm approachable expression, slight head tilt. Background: a French pharmacy counter area, heavily blurred, warm wood and soft green signage tones, bokeh highlights.

Avoid: No text, no watermark, no logo, no signature. No exaggerated makeup, no stock-photo grin, no teeth showing. No white lab coat, no medical scrubs, no stethoscope, no caduceus. Hands not visible. No motion blur, no lens flare, no glasses glare or reflections, no harsh specular highlights on skin. No hair strands crossing the face, no hair covering the jawline. Not a 3D render, not an illustration, not AI-plastic skin.
```

### C — senior-fond-neutre

> Plus agee, decor neutre. La plus transposable (site, slides, LinkedIn) car aucun decor a assumer.

```
Photorealistic editorial portrait photograph, shot on Canon EOS R5, 85mm lens at f/2.0, shallow depth of field. Medium shot: head and shoulders, upper chest visible, body turned slightly (about 15 degrees) but face fully frontal to the camera, eyes looking directly into the lens. Closed-mouth confident smile, relaxed jaw, warm and attentive expression, natural skin texture with visible pores and fine lines. Soft natural window light from the left, gentle fill on the right, no hard shadows across the face. Even lighting on the entire face. Clear separation between subject and background.

French woman, 45 years old, short layered dark brown hair with visible natural greys at the temples. Wearing a soft charcoal blazer over a white shirt with an open collar, no jewelry. Calm, assured, slightly serious expression with a faint smile. Background: seamless warm grey studio backdrop, subtle vignette, no props.

Avoid: No text, no watermark, no logo, no signature. No exaggerated makeup, no stock-photo grin, no teeth showing. No white lab coat, no medical scrubs, no stethoscope, no caduceus. Hands not visible. No motion blur, no lens flare, no glasses glare or reflections, no harsh specular highlights on skin. No hair strands crossing the face, no hair covering the jawline. Not a 3D render, not an illustration, not AI-plastic skin.
```

### D — digitale-pharmacie-moderne

> La plus jeune, decor pharmacie moderne (automate). Signale 'numerique' plus fort, mais risque de paraitre trop jeune face a un titulaire de 50 ans.

```
Photorealistic editorial portrait photograph, shot on Canon EOS R5, 85mm lens at f/2.0, shallow depth of field. Medium shot: head and shoulders, upper chest visible, body turned slightly (about 15 degrees) but face fully frontal to the camera, eyes looking directly into the lens. Closed-mouth confident smile, relaxed jaw, warm and attentive expression, natural skin texture with visible pores and fine lines. Soft natural window light from the left, gentle fill on the right, no hard shadows across the face. Even lighting on the entire face. Clear separation between subject and background.

French woman, 38 years old, long dark brown hair worn down and straight, no glasses. Wearing a crisp white shirt under a thin dark taupe cardigan, minimal jewelry. Confident, direct, slightly amused expression. Background: a modern French pharmacy dispensary, blurred, pale grey robotic drawer cabinets and soft LED strip lighting, cool-neutral tones balanced by warm key light on the face.

Avoid: No text, no watermark, no logo, no signature. No exaggerated makeup, no stock-photo grin, no teeth showing. No white lab coat, no medical scrubs, no stethoscope, no caduceus. Hands not visible. No motion blur, no lens flare, no glasses glare or reflections, no harsh specular highlights on skin. No hair strands crossing the face, no hair covering the jawline. Not a 3D render, not an illustration, not AI-plastic skin.
```

---

## Étape 2 — les déclinaisons

**Ces prompts ne marchent QUE si tu joins le master retenu comme image de référence.**
Dans AI Studio : bouton `+` → Upload file → ton master, puis le prompt. Sans l'image
jointe, tu obtiendras une autre femme, avec le même style. C'est l'erreur qui coûte
une demi-journée.

### plain-bg — fond-uni-gris-chaud

> La version passe-partout : slides, site, miniatures, incrustation.  
> Ratio à régler dans l'interface : **4:5**

```
Keep the exact same woman as in the reference image: identical face, identical bone structure, identical eye colour, identical hairstyle and hair colour, identical age. Do not restyle, do not beautify, do not change her apparent age. Same photographic treatment: 85mm lens, shallow depth of field, soft natural light from the left, photorealistic skin texture.

Same person, same face, same outfit as the reference. Replace the background with a clean seamless warm grey studio backdrop (#D8D3CC), evenly lit, subtle soft vignette, no props, no texture. Keep the same head size and framing (head and shoulders).

Avoid: No text, no watermark. No change of identity, no different person, no younger or older face. No teeth showing, no exaggerated smile. Hands not visible. No glasses glare, no motion blur.
```

### wide — 16-9-horizontal

> Base des videos web / emails. Sujet decale a droite pour laisser de la place au texte a gauche.  
> Ratio à régler dans l'interface : **16:9**

```
Keep the exact same woman as in the reference image: identical face, identical bone structure, identical eye colour, identical hairstyle and hair colour, identical age. Do not restyle, do not beautify, do not change her apparent age. Same photographic treatment: 85mm lens, shallow depth of field, soft natural light from the left, photorealistic skin texture.

Same person, same face, same outfit, same background environment as the reference. Recompose as a horizontal 16:9 frame: the subject occupies the right third, head and shoulders, eyes on the upper third line, generous negative space on the left for overlaid text. Extend the background naturally to fill the wider frame.

Avoid: No text, no watermark. No change of identity, no different person, no younger or older face. No teeth showing, no exaggerated smile. Hands not visible. No glasses glare, no motion blur.
```

### vertical — 9-16-linkedin-reels

> LinkedIn / reels. Cadrage un peu plus serre, tete dans le tiers superieur.  
> Ratio à régler dans l'interface : **9:16**

```
Keep the exact same woman as in the reference image: identical face, identical bone structure, identical eye colour, identical hairstyle and hair colour, identical age. Do not restyle, do not beautify, do not change her apparent age. Same photographic treatment: 85mm lens, shallow depth of field, soft natural light from the left, photorealistic skin texture.

Same person, same face, same outfit, same background environment as the reference. Recompose as a vertical 9:16 frame: head and shoulders centred horizontally, top of the head in the upper fifth of the frame, chest visible at the bottom, background extended naturally above and below.

Avoid: No text, no watermark. No change of identity, no different person, no younger or older face. No teeth showing, no exaggerated smile. Hands not visible. No glasses glare, no motion blur.
```

### alt-outfit — tenue-alternative

> Pour varier les videos sans refaire un avatar (utile si tu publies plusieurs fois par semaine).  
> Ratio à régler dans l'interface : **4:5**

```
Keep the exact same woman as in the reference image: identical face, identical bone structure, identical eye colour, identical hairstyle and hair colour, identical age. Do not restyle, do not beautify, do not change her apparent age. Same photographic treatment: 85mm lens, shallow depth of field, soft natural light from the left, photorealistic skin texture.

Same person, same face, same hairstyle, same background as the reference. Change only the clothing: a deep forest-green fine-knit sweater with a simple round neckline, no visible jewelry. Keep the same lighting and framing.

Avoid: No text, no watermark. No change of identity, no different person, no younger or older face. No teeth showing, no exaggerated smile. Hands not visible. No glasses glare, no motion blur.
```

### warm-neutral — fond-neutre-chaud-16-9

> Fond uni ET horizontal : la version la plus reutilisable pour de l'habillage.  
> Ratio à régler dans l'interface : **16:9**

```
Keep the exact same woman as in the reference image: identical face, identical bone structure, identical eye colour, identical hairstyle and hair colour, identical age. Do not restyle, do not beautify, do not change her apparent age. Same photographic treatment: 85mm lens, shallow depth of field, soft natural light from the left, photorealistic skin texture.

Same person, same face, same outfit as the reference. Seamless warm beige studio backdrop (#E3DCD2), horizontal 16:9 composition, subject in the right third, head and shoulders, large clean negative space on the left. Even soft studio lighting, no props.

Avoid: No text, no watermark. No change of identity, no different person, no younger or older face. No teeth showing, no exaggerated smile. Hands not visible. No glasses glare, no motion blur.
```

---

## Étape 3 — trier

Écarte sans hésiter une image qui présente l'un de ces défauts, ils ne se rattrapent pas :

- **dents visibles** — Avatar IV part de la bouche fermée pour reconstruire toute
  l'animation labiale ; une bouche ouverte sur la source bave sur toute la vidéo
- **reflet ou voile sur les lunettes**
- **une main, un doigt, un poignet dans le cadre**
- **une mèche qui traverse le visage** ou masque la mâchoire
- **moitié de visage dans l'ombre**
- visage de trois quarts : il faut du frontal

Puis : `python3 scripts/check_photo.py ton-image.png`
