# Correctifs zepetcoach.com

Audit fait sur le site en ligne avec un vrai navigateur (iPhone 13 et iPad Pro 11), le 9 octobre 2026.

## Cause n°1 : WP Rocket « Remove Unused CSS » (corrige 3 bugs)

WP Rocket retire tout le CSS dont les classes n'apparaissent pas dans le HTML au chargement.
Or le thème ajoute beaucoup de classes **en JavaScript** : le chat, l'ouverture des menus et le fond du header.
Leur CSS est donc supprimé.

| Bug | Preuve (avec WP Rocket → sans WP Rocket) |
|---|---|
| Chat Chloé affiché en vrac en bas de page | `#zpc-chat-widget` : `position: static` → `fixed` |
| Sous-menus mobiles qui ne s'ouvrent pas | classe `.open` bien ajoutée, mais sous-menu `display: none` → `flex` |
| Header transparent qui recouvre le contenu et le pied de page au défilement | header `.blue` : fond `transparent` → `rgb(10, 99, 160)` |

### À faire (2 minutes)

Allez dans **WP Rocket > Optimisation des fichiers > CSS > Supprimer le CSS inutilisé > Liste sûre CSS** (*CSS safelist*) et collez :

```
.open
.blue
.white
.lock
.show
.hide
.active
.is-(.*)
.zpc-(.*)
#zpc-(.*)
.iti(.*)
```

Enregistrez, puis allez dans **WP Rocket > Vider et précharger le cache** (la liste du CSS utilisé se régénère).

Si ça ne suffit pas, vous pouvez à la place mettre la ligne suivante dans la même liste. Elle garde tout le CSS du thème, ce qui est un peu moins optimisé mais sans risque :

```
/app/themes/zepetcoach/public/build/assets/(.*).css
```

## Cause n°2 : bugs du thème (CSS à coller)

Allez dans **Apparence > Personnaliser > CSS additionnel** et collez le contenu de `zepetcoach-fixes.css`.

| Bug | Cause dans le thème | Vérifié |
|---|---|---|
| Boutons coupés en bas des bannières Téléconseil (iPad, portables) | `.header-teleconseil { max-height: 90vh; overflow: hidden }` : le contenu fait 878 px, la bannière 751 px | bannière 751 → 878 px, tout visible |
| « Se connecter/S'inscrire » dépasse de l'écran sur iPad | le menu ordinateur s'affiche dès 1025 px, mais il lui faut environ 1300 px | bouton réduit à l'icône entre 1025 et 1366 px |
| Mobile : la flèche de « Services » ne fait rien | le JS est déclenché 2 fois (sur la flèche **et** sur le lien `#`), donc ça ouvre et referme aussitôt | ouvre bien ; la flèche de Blog marche toujours |

## Contenu à corriger (éditeur de page)

- **Téléconseil Assistance petcoach** : « (En dehors de ces horaires voir téléconseil vétérinaire) » s'affiche sans aucun horaire au-dessus. Ajoutez les horaires ou supprimez la phrase.

## Pas un bug

- Les boutons flottants vert et bleu à droite sont **volontairement** à moitié cachés : ils sortent au survol ou au premier tap (`.floating-buttons .button:hover`).

## Correctif durable (dans le code du thème)

Le vrai code du thème est dans le dépôt `ZePetCoach/zepetcoach`. Il faudrait y corriger :
1. La règle `max-height: 90vh` de `.header-teleconseil`.
2. Le point de rupture du menu (1024 → environ 1300 px, dans le CSS **et** dans le JS `window.innerWidth<=1024`).
3. Le double déclenchement de `.menu-item-has-children > a, .chevron` : ajouter `e.stopPropagation()` sur la flèche.
4. Le filtre `rocket_rucss_safelist`, pour que la liste sûre ne dépende plus des réglages de l'admin.
