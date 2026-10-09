# Correctifs zepetcoach.com : état final

Audit fait le 9 octobre 2026 sur le site en ligne avec un vrai navigateur (iPhone SE, iPhone 13, iPad Pro 11, ordinateur 1440 px).

**Tout est corrigé dans le code du thème** (dépôt `ZePetCoach/zepetcoach`), puis déployé en production via staging. Rien n'est à faire dans l'admin WordPress.

## Cause n°1 : WP Rocket « Remove Unused CSS »

WP Rocket retire le CSS dont les classes n'apparaissent pas dans le HTML au chargement.
Or le thème ajoute des classes en JavaScript, et leur CSS était donc supprimé.

| Bug | Avant | Après |
|---|---|---|
| Chat Chloé affiché en vrac en bas de page | `#zpc-chat-widget` en `position: static` | caché, puis fenêtre `fixed` au clic sur le bouton vert |
| Sous-menus Services / Blog ne s'ouvrent pas sur mobile | `.open` ajouté, mais sous-menu `display: none` | sous-menu `display: flex` |
| Header transparent qui recouvre le contenu au défilement | `.blue` : fond transparent | fond `rgb(10, 99, 160)` |

**Correctif (thème, `app/filters.php`) :** le filtre `rocket_rucss_safelist` contient `/app/themes/zepetcoach/public/build/assets/(.*).css`.

Dans WP Rocket 3.19, chaque entrée de la liste sûre est une regex comparée au sélecteur complet. Une entrée courte comme `.open` ne correspondait donc à rien. Une entrée contenant `.css` est traitée comme un motif de fichier : la feuille du thème est gardée en entier.

Le pipeline de déploiement vide aussi la table `wpr_rucss_used_css`, puis le cache de pages.

## Cause n°2 : bugs du thème

| Bug | Cause | Correctif |
|---|---|---|
| Boutons coupés en bas des bannières Téléconseil (iPad) | `.header-teleconseil { max-height: 90vh; overflow: hidden }` | `max-height` supprimé (751 → 878 px) |
| « Se connecter/S'inscrire » dépasse de l'écran sur iPad | menu desktop affiché dès 1025 px | bouton réduit à l'icône entre 1025 et 1366 px |
| Mobile : la flèche « Services » ne fait rien | double déclenchement (flèche + lien `#`) | `e.stopPropagation()` sur la flèche |
| Bouton « Envoyer » du chat coupé sur mobile | l'input en `flex: 1` garde `min-width: auto` | `min-width: 0` sur l'input, `flex-shrink: 0` sur le bouton |
| Cartes de l'accueil : texte écrasé à gauche (iPad) | `grid-template-columns: 1fr auto` | 2 colonnes égales au-delà de 768 px (97/442 → 269/270 px) |

## Reste à faire

- **Contenu** (éditeur de page) : sur « Téléconseil Assistance petcoach », la phrase « (En dehors de ces horaires voir téléconseil vétérinaire) » s'affiche sans horaire au-dessus.
- **À revérifier** après la prochaine régénération du « Used CSS » de WP Rocket : sous-menus mobiles, chat et header au défilement.

## Pas un bug

- Les boutons flottants vert et bleu à droite sont volontairement à moitié cachés : ils sortent au survol ou au premier tap.

## Fichier `zepetcoach-fixes.css`

Ce CSS servait de solution de secours à coller dans l'admin. Il est **inutile** maintenant que les correctifs sont dans le thème : ne pas le coller.
