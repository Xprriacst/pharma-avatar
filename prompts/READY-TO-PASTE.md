# Prompts prets a coller

Genere par `scripts/build_paste_doc.py` depuis `prompts/*.json`. Colle tel quel dans
Google AI Studio, l'app Gemini, ou n'importe quel generateur d'images.

**Le ratio et la resolution se reglent dans l'interface, pas dans le prompt** :
4:5 en 2K pour les masters. Genere 2 variantes par candidate — le premier tirage est
rarement le bon.

---

## Etape 1 — les candidates

Objectif : choisir UN visage. Ne juge pas la beaute, juge la credibilite face a un
titulaire de 50 ans qui recoit trois commerciaux par semaine.

### A+ — consultante-terrain-soignee

> A, en version photo de magazine. On monte la lumiere, le coiffage, le maquillage et la coupe du blazer. On NE touche PAS a l'age ni a la texture de peau : c'est ce qui la garde credible.

```
Photorealistic editorial portrait photograph, shot on Canon EOS R5, 85mm lens at f/2.0, shallow depth of field. Medium shot: head and shoulders, upper chest visible, body turned slightly (about 15 degrees) but face fully frontal to the camera, eyes looking directly into the lens. Closed-mouth confident smile, relaxed jaw, warm and attentive expression, natural skin texture with visible pores and fine lines. Soft natural window light from the left, gentle fill on the right, no hard shadows across the face. Even lighting on the entire face. Clear separation between subject and background.

French woman, 42 years old, elegant and photogenic, refined bone structure with defined cheekbones. Shoulder-length dark brown hair with a few natural greys, freshly styled with soft volume and healthy shine, side part, one side loosely tucked behind her ear. Well-groomed natural eyebrows, discreet everyday makeup: subtle neutral eyeshadow, softly defined lashes, muted rose lip. Luminous well-hydrated skin that keeps real pores, fine expression lines around the eyes, and natural facial asymmetry. Wearing an impeccably tailored navy blazer over a light cream silk blouse that catches the light, small gold stud earrings, thin tortoiseshell rectangular glasses. Beauty-grade lighting: large soft key light from the left, gentle fill on the right, subtle rim light separating her hair from the background, clear catchlights in both eyes. Editorial magazine portrait quality, professionally retouched but never airbrushed. Background: the back-office of a French pharmacy, softly blurred, shelves of white and pale-green medicine boxes, warm neutral tones.

Avoid: No text, no watermark, no logo, no signature. No exaggerated makeup, no stock-photo grin, no teeth showing. No white lab coat, no medical scrubs, no stethoscope, no caduceus. Hands not visible. No motion blur, no lens flare, no glasses glare or reflections, no harsh specular highlights on skin. No hair strands crossing the face, no hair covering the jawline. Not a 3D render, not an illustration, not AI-plastic skin.
```

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


---

## Etape 2 — les declinaisons

**Ces prompts ne marchent QUE si tu joins le master retenu comme image de reference.**
Dans AI Studio : bouton `+` -> Upload file -> ton master, puis le prompt. Sans l'image
jointe, tu obtiendras une autre femme, avec le meme style. C'est l'erreur qui coute
une demi-journee.

### plain-bg — fond-uni-gris-chaud

> La version passe-partout : slides, site, miniatures, incrustation.  
> Ratio a regler dans l'interface : **4:5**

```
Keep the exact same woman as in the reference image: identical face, identical bone structure, identical eye colour, identical hairstyle and hair colour, identical age. Do not restyle, do not beautify, do not change her apparent age. Same photographic treatment: 85mm lens, shallow depth of field, soft natural light from the left, photorealistic skin texture.

Same person, same face, same outfit as the reference. Replace the background with a clean seamless warm grey studio backdrop (#D8D3CC), evenly lit, subtle soft vignette, no props, no texture. Keep the same head size and framing (head and shoulders).

Avoid: No text, no watermark. No change of identity, no different person, no younger or older face. No teeth showing, no exaggerated smile. Hands not visible. No glasses glare, no motion blur.
```

### wide — 16-9-horizontal

> Base des videos web / emails. Sujet decale a droite pour laisser de la place au texte a gauche.  
> Ratio a regler dans l'interface : **16:9**

```
Keep the exact same woman as in the reference image: identical face, identical bone structure, identical eye colour, identical hairstyle and hair colour, identical age. Do not restyle, do not beautify, do not change her apparent age. Same photographic treatment: 85mm lens, shallow depth of field, soft natural light from the left, photorealistic skin texture.

Same person, same face, same outfit, same background environment as the reference. Recompose as a horizontal 16:9 frame: the subject occupies the right third, head and shoulders, eyes on the upper third line, generous negative space on the left for overlaid text. Extend the background naturally to fill the wider frame.

Avoid: No text, no watermark. No change of identity, no different person, no younger or older face. No teeth showing, no exaggerated smile. Hands not visible. No glasses glare, no motion blur.
```

### vertical — 9-16-linkedin-reels

> LinkedIn / reels. Cadrage un peu plus serre, tete dans le tiers superieur.  
> Ratio a regler dans l'interface : **9:16**

```
Keep the exact same woman as in the reference image: identical face, identical bone structure, identical eye colour, identical hairstyle and hair colour, identical age. Do not restyle, do not beautify, do not change her apparent age. Same photographic treatment: 85mm lens, shallow depth of field, soft natural light from the left, photorealistic skin texture.

Same person, same face, same outfit, same background environment as the reference. Recompose as a vertical 9:16 frame: head and shoulders centred horizontally, top of the head in the upper fifth of the frame, chest visible at the bottom, background extended naturally above and below.

Avoid: No text, no watermark. No change of identity, no different person, no younger or older face. No teeth showing, no exaggerated smile. Hands not visible. No glasses glare, no motion blur.
```

### alt-outfit — tenue-alternative

> Pour varier les videos sans refaire un avatar (utile si tu publies plusieurs fois par semaine).  
> Ratio a regler dans l'interface : **4:5**

```
Keep the exact same woman as in the reference image: identical face, identical bone structure, identical eye colour, identical hairstyle and hair colour, identical age. Do not restyle, do not beautify, do not change her apparent age. Same photographic treatment: 85mm lens, shallow depth of field, soft natural light from the left, photorealistic skin texture.

Same person, same face, same hairstyle, same background as the reference. Change only the clothing: a deep forest-green fine-knit sweater with a simple round neckline, no visible jewelry. Keep the same lighting and framing.

Avoid: No text, no watermark. No change of identity, no different person, no younger or older face. No teeth showing, no exaggerated smile. Hands not visible. No glasses glare, no motion blur.
```

### warm-neutral — fond-neutre-chaud-16-9

> Fond uni ET horizontal : la version la plus reutilisable pour de l'habillage.  
> Ratio a regler dans l'interface : **16:9**

```
Keep the exact same woman as in the reference image: identical face, identical bone structure, identical eye colour, identical hairstyle and hair colour, identical age. Do not restyle, do not beautify, do not change her apparent age. Same photographic treatment: 85mm lens, shallow depth of field, soft natural light from the left, photorealistic skin texture.

Same person, same face, same outfit as the reference. Seamless warm beige studio backdrop (#E3DCD2), horizontal 16:9 composition, subject in the right third, head and shoulders, large clean negative space on the left. Even soft studio lighting, no props.

Avoid: No text, no watermark. No change of identity, no different person, no younger or older face. No teeth showing, no exaggerated smile. Hands not visible. No glasses glare, no motion blur.
```

---

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
