# Feedback API

API Flask + PostgreSQL qui collecte les avis des visiteurs d'un portfolio (note de 1 à 5 + commentaire) et un dashboard protégé affichant les statistiques (note moyenne, répartition des notes, avis par mois).

## Stack

- Python / Flask, gunicorn en production
- PostgreSQL, requêtes SQL brutes via psycopg2
- Architecture en couches : `Controllers` → `Services` → `Repositories` → `Config`
- Chart.js pour le dashboard

## Endpoints

| Méthode | Route | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/api/reviews` | Crée un avis. Corps JSON : `rating` (entier 1-5, requis), `comment` (500 car. max, requis), `name` (100 car. max, optionnel) |
| GET | `/api/reviews/stats` | Statistiques. Authentification Basic requise |
| GET | `/dashboard` | Dashboard avec graphiques. Authentification Basic requise |

Exemple de réponse de `/api/reviews/stats` :

```json
{
  "count": 12,
  "average": 4.25,
  "distribution": {"1": 0, "2": 1, "3": 2, "4": 4, "5": 5},
  "timeline": [{"month": "2026-09", "count": 7}, {"month": "2026-10", "count": 5}]
}
```

Le champ `website` dans le corps de `POST /api/reviews` est un piège à bots : s'il est rempli, la requête renvoie 201 sans rien enregistrer.

## Lancer en local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # puis renseigner les valeurs
```

Créer la base et la table :

```bash
psql -U postgres -c "CREATE DATABASE feedback;"
psql -U postgres -d feedback -f db/schema.sql
```

Démarrer le serveur :

```bash
python -m Controllers.review_controller
```

## Variables d'environnement

| Variable | Rôle |
|---|---|
| `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Connexion PostgreSQL |
| `DASHBOARD_USER`, `DASHBOARD_PASSWORD` | Identifiants Basic Auth du dashboard et des stats |

## Déploiement (Render)

Le `Procfile` lance `gunicorn Controllers.review_controller:app`. Sur Render : un Web Service relié à ce repo et une base PostgreSQL, les variables ci-dessus renseignées, et `db/schema.sql` exécuté une fois sur la base.
