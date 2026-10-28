# Activer Cloudflare Pages gratuitement pour JHD Link Manager

Le dépôt GitHub reste **jhd-solutions/jhd-link-manager**. Ne pas renommer le dépôt et ne pas modifier celui de BabyShow.

## Connexion

1. Ouvrir https://dash.cloudflare.com/ et créer un compte gratuit (ou se connecter).
2. Dans **Workers & Pages**, choisir **Create application**, puis **Pages** et **Import an existing Git repository** (libellés susceptibles d'évoluer).
3. Autoriser l'application Cloudflare Pages sur GitHub en limitant son accès au dépôt **jhd-solutions/jhd-link-manager**.
4. Sélectionner ce dépôt, puis la branche **main**.

## Paramètres de build

| Champ Cloudflare | Valeur |
| --- | --- |
| **Project name** | `jhdgo` (à tenter, selon disponibilité) |
| **Framework preset** | `None` / aucun |
| **Production branch** | `main` |
| **Build command** | `python3 build.py` |
| **Build output directory** | `_site` |
| **Root directory** | `/` (racine du dépôt) |
| **Environment variables** | aucune |

Choisir ensuite **Save and Deploy** ou **Deploy**. Le nom retenu par Cloudflare déterminera l'URL, par exemple `https://jhdgo.pages.dev`. Ne pas supposer que ce nom est disponible avant confirmation par Cloudflare.

## Tests après publication

- `https://<nom-projet>.pages.dev/` : page d'accueil.
- `https://<nom-projet>.pages.dev/manager/` : liste des liens actifs avec copie de l'URL courte.
- `https://<nom-projet>.pages.dev/b26` : redirection **HTTP 302** vers le site de Gaëlle (destination temporaire).
- `https://<nom-projet>.pages.dev/demo` : redirection HTTP 302 vers `https://example.org/`.

Le fichier `_redirects` est **généré automatiquement** dans `_site` à partir de `links.json`. Cloudflare le traite côté serveur. Les pages HTML `/b26/` restent également générées pour GitHub Pages.

## Modifier un lien sans changer le QR imprimé

1. Ouvrir https://github.com/jhd-solutions/jhd-link-manager/actions/workflows/manage.yml
2. **Run workflow**, `operation=set`.
3. Reprendre **exactement le même alias**, par exemple `b26`, et changer la destination.
4. Vérifier la publication dans Cloudflare Pages. Les commits GitHub doivent déclencher le déploiement via l'intégration Git.
5. Tester le lien avant de réutiliser le QR : la destination est modifiable, mais **l'adresse courte doit rester la même**.

## Avertissements

- Les raccourcis ne sont pas confidentiels : dépôt, codes et destinations sont publics.
- Le nom `*.pages.dev` est gratuit tant que le projet et les conditions du service existent, mais ce n'est pas un domaine personnalisé dont JHD Solutions est propriétaire.
- GitHub Pages reste actif ; ne pas désactiver BabyShow ni changer le domaine de son dépôt.
- Un lien raccourci **ne garantit pas** qu'un tampon imprimé en PETG produira un QR lisible : tester sa vraie empreinte avec un téléphone, et envisager une surface plus souple.
- Avant d'imprimer un lot, conserver une copie des URL et vérifier que le domaine Cloudflare retenu est définitif.

Documentation officielle : https://developers.cloudflare.com/pages/framework-guides/deploy-anything/ et https://developers.cloudflare.com/pages/configuration/redirects/
