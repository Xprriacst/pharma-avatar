# Manon — fiche persona de l'avatar

Document de référence. Toute image, tout script, toute vidéo se valide contre cette fiche.

## À qui elle parle

Des **titulaires d'officine**. Majoritairement 40-55 ans, une majorité de femmes, chefs
d'une entreprise de 5 à 12 personnes. Sollicités en permanence par des commerciaux
— labos, grossistes, éditeurs de LGO. Ils détectent le faux en quelques secondes et se
ferment devant le marketing trop lisse.

Trois conséquences qui structurent tout le reste :

1. **Elle ne se fait pas passer pour une pharmacienne.** Pas de blouse blanche, pas de
   croix verte dans le dos, pas de stéthoscope. Une fausse consœur est perçue comme une
   tromperie, et la tromperie tue la vente. Elle est une interlocutrice qui connaît leur
   métier, pas une des leurs.
2. **Elle a l'âge de la crédibilité.** 38-45 ans. Assez jeune pour être associée au
   numérique, assez mûre pour parler d'égal à égal à quelqu'un qui dirige une entreprise.
   Un avatar de 25 ans ne sera pas écouté.
3. **Elle parle leur quotidien, pas la techno.** Le décor de pharmacie floutée en fond dit
   « je connais votre monde » sans usurper le rôle.

## Identité

| | |
|---|---|
| Prénom | **Manon** — cohérent avec la voix ElevenLabs, français, ni daté ni adolescent |
| Âge apparent | 42 ans (fourchette acceptable : 38-45) |
| Rôle assumé | consultante / spécialiste qui accompagne des officines. Jamais pharmacienne |
| Registre | tutoiement jamais, vouvoiement toujours. Direct, concret, sans jargon |

## Apparence

- **Cheveux** : châtain foncé, mi-longs, quelques gris naturels assumés. Aucune mèche ne
  doit traverser le visage ni masquer la mâchoire — c'est ce qui fait déraper l'animation.
- **Tenue** : chemisier ou pull fin clair, veste sobre. Pas de blouse. Pas de bijoux
  voyants, pas de motifs à fort contraste (ils moirent à la compression vidéo).
- **Lunettes** : fines, écaille. Optionnelles mais elles ajoutent de la crédibilité et
  Avatar IV les gère bien — à condition qu'il n'y ait **aucun reflet** sur les verres.
- **Expression** : sourire léger **bouche fermée**, regard direct, buste très légèrement
  penché vers l'avant. Surtout pas le sourire dentifrice des banques d'images.
- **Cadrage** : buste, épaules et haut du torse visibles, **mains hors champ** — les mains
  sont le point faible de l'animation photo.

## Décors

| Décor | Usage |
|---|---|
| Back-office de pharmacie flouté | vidéos principales, hero du site |
| Fond uni gris/beige chaud | slides, incrustations, tout support où le décor parasiterait |

Le décor est toujours **fortement flouté** : net, il attire l'œil et il date vite.

## Voix

Voix **Manon** (ElevenLabs, française, catégorie Advertisement, « serious & spontaneous »).
Sérieuse sans être froide : exactement le registre attendu par un titulaire.

Réglages de départ pour Avatar IV : `stability 0.45`, `similarity 0.80`, `style 0.35`.
Stabilité volontairement basse — on veut de l'intonation, parce que **Avatar IV construit
les expressions du visage à partir de l'audio**. Un TTS plat donne une vidéo morte.

## Ce qui la casse

- une blouse blanche
- un sourire trop large, des dents visibles sur la photo source
- des mains dans le cadre
- un décor net et reconnaissable
- un script qui commence par « Bonjour, je suis Manon et aujourd'hui je vais vous parler de… »
- des chiffres invérifiables balancés sans source

## Déclinaisons à produire une fois le visage validé

`master` (4:5) → `plain-bg` (fond uni) → `wide` (16:9) → `vertical` (9:16) →
`alt-outfit` (seconde tenue) → `warm-neutral` (fond uni 16:9).

Toutes générées **à partir du master en référence**, jamais reprompées de zéro : c'est ce
qui rend l'avatar réellement persistant d'un support à l'autre.
