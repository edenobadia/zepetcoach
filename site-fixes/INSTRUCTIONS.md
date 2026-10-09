# Correctifs zepetcoach.com : mode d'emploi

Comptez environ 20 minutes dans l'admin WordPress. Faites les étapes dans l'ordre.

## Étape 0 : vider et régler le cache (corrige le chat Chloé et le menu mobile)

Dans votre extension de cache (WP Rocket, LiteSpeed, Autoptimize, SiteGround Optimizer…) :

1. **Désactivez** « Retarder l'exécution du JavaScript » (*Delay JS*). Sinon, ajoutez en exclusion :
   `elementor`, `jquery`, `smartmenus` et le nom du script du chat.
2. **Désactivez** « Supprimer le CSS inutilisé » (*Remove Unused CSS*) et « Combiner les CSS ».
3. Videz le cache, puis testez sur iPhone en navigation privée.

Si le chat et le menu remarchent après ça, la cause était le cache.

## Étape 1 : ajouter des classes CSS dans Elementor

Ouvrez la section dans Elementor, puis allez dans **Avancé > Classes CSS** et tapez la classe :

| Élément                                    | Classe à ajouter  |
|--------------------------------------------|-------------------|
| L'en-tête (Modèles > Theme Builder > Header) | `zpc-header`      |
| La bannière bleue du haut de chaque page de service | `zpc-hero`        |
| Le bloc des boutons flottants vert et bleu | `zpc-floating`    |
| Les 2 gros boutons du menu mobile          | `zpc-mobile-cta`  |

## Étape 2 : coller le CSS

Allez dans **Apparence > Personnaliser > CSS additionnel** et collez le contenu de `zepetcoach-fixes.css`.

## Étape 3 : passer l'iPad en menu mobile

Allez dans **Elementor > Réglages du site > Mise en page > Points de rupture** et réglez Tablette sur **1199**.
Ensuite, dans le widget Menu de l'en-tête, choisissez « Menu déroulant » : **Tablette**.

## Étape 4 : le script de secours pour le menu mobile

Avec l'extension **WPCode**, ajoutez un extrait de type JavaScript, avec l'emplacement « Pied de page du site ».
Collez-y `zepetcoach-fixes.js`, puis excluez-le du *Delay JS* (étape 0).

## Étape 5 : contenu

- **Page Téléconseil Assistance** : la phrase « (En dehors de ces horaires voir téléconseil vétérinaire) » ne correspond à aucun horaire. Ajoutez les horaires ou supprimez la phrase.
- **Doublon de chat** : il y a deux chats, la bulle verte et le widget Chloé. Gardez-en un seul.
