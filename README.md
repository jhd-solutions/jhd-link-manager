# JHD Link Manager — v1.2

Gestionnaire de liens courts pour JHD Solutions. Un fichier JSON décrit les liens ; GitHub Actions construit des pages HTML de redirection. Ce dépôt est indépendant du site BabyShow.


## Cloudflare Pages — URL gratuite plus courte

La configuration Cloudflare Pages est détaillée dans **[CLOUDFLARE.md](CLOUDFLARE.md)**. Le dépôt peut être publié sur GitHub Pages **et** Cloudflare Pages, avec **la même source de liens**.

Sur Cloudflare, `python3 build.py` crée aussi `_site/_redirects`, qui effectue des **redirections HTTP 302 directement sur le serveur**, alors que GitHub Pages utilise la redirection HTML. Choisir un nom de projet court (par exemple `jhdgo` s'il est libre) et le répertoire de sortie `_site`.

## Installation
1. Dans **Settings → Pages → Build and deployment → Source**, sélectionner **GitHub Actions**.
2. Dans **Actions**, consulter le workflow **Publier JHD Link Manager** et éventuellement lancer **Run workflow**.
3. Quand le site est publié, tester **https://jhd-solutions.github.io/jhd-link-manager/demo/** (redirection de démonstration vers https://example.org/).

## Administration simplifiée (recommandée)
Sur GitHub, ouvrir **Actions → Gerer les liens JHD → Run workflow** :
- `operation = set` pour créer ou modifier un lien (alias, destination et titre facultatif).
- `operation = delete` pour désactiver un lien existant (alias uniquement).
- Le formulaire refuse les alias invalides et les URL autres que HTTP/HTTPS.
- Le workflow enregistre la modification dans `links.json` et déploie les nouveaux liens **dans la même exécution**, parce qu'un commit généré avec le `GITHUB_TOKEN` ne déclenche pas automatiquement un autre workflow.

Lien direct du formulaire : https://github.com/jhd-solutions/jhd-link-manager/actions/workflows/manage.yml

Tableau de consultation public : https://jhd-solutions.github.io/jhd-link-manager/manager/

**Attention :** ce tableau public permet de consulter et de copier, pas d'écrire. Les modifications nécessitent une connexion GitHub ayant droit d'écriture.

## Gestion manuelle (alternative)
Éditer `links.json` depuis GitHub puis valider avec **Commit changes** sur la branche `main`.

Exemple :

```json
{
  "demo": {
    "destination": "https://example.org/",
    "title": "Lien de démonstration"
  },
  "b26": {
    "destination": "https://www.gaelle-accompagnante-parentale.fr/",
    "title": "Salon Baby"
  }
}
```

Chaque entrée produit une adresse `/alias/` sous le site GitHub Pages. Pour conserver une URL imprimée tout en changeant sa cible, garder l'alias et modifier uniquement `destination`.

- Alias : 1 à 32 caractères minuscules, chiffres et tirets ; certains noms sont réservés.
- Destination : URL `https://` ou `http://`.
- Un alias retiré de `links.json` cesse d'être publié après le prochain déploiement et renvoie une erreur 404.

## Limites et sécurité
- Le dépôt est **public** : les alias et destinations sont visibles. Ne jamais y stocker de données privées ou de jetons.
- Ces redirections sont effectuées **dans le navigateur** (JavaScript + meta refresh), pas par une vraie réponse HTTP 301 ou 302.
- La gestion se fait depuis GitHub ; il n'y a pas de tableau de bord d'administration public.
- Sans domaine personnalisé court, les liens `jhd-solutions.github.io/jhd-link-manager/…` restent assez longs pour un QR imprimé.
- Une URL déjà imprimée ne fonctionne que tant que le domaine, le site et la configuration restent actifs.
- **Ne pas modifier** le dépôt `jhd-solutions.github.io` de BabyShow.

## Test local
Exécuter `python build.py` avec Python 3.10+. Les fichiers générés se trouvent dans `_site/`, qui ne doit pas être commité.

## Domaine court personnalisé

Sans domaine court, la longueur de `https://jhd-solutions.github.io/jhd-link-manager/b26/` pénalise la densité des QR codes.

Après acquisition d'un nom de domaine court **dont tu es propriétaire** :
1. Dans **Settings → Pages → Custom domain** de CE dépôt uniquement, indiquer le domaine ou sous-domaine souhaité, puis enregistrer.
2. Pour un sous-domaine tel que `go.exemple.fr` : configurer chez ton prestataire DNS un CNAME `go` vers `jhd-solutions.github.io`.
3. Vérifier la propriété du domaine dans GitHub avant configuration DNS quand cela est possible.
4. Attendre la propagation DNS, puis activer **Enforce HTTPS** et tester `https://go.exemple.fr/b26/`.
5. Ne pas modifier le domaine du dépôt `jhd-solutions.github.io` utilisé par BabyShow.

Pour un domaine racine (par exemple `exemple.fr`), GitHub demande des enregistrements A/AAAA ou ALIAS/ANAME selon le fournisseur, **pas le même CNAME que pour un sous-domaine**.

**Attention :** ne pas imprimer d'adresse sur un tampon avant d'être certain de conserver le nom de domaine sur la durée.
