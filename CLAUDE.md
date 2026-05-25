# CLAUDE.md — matrice-competences

> Contexte pour les agents IA. Dernière mise à jour : 2026-04-30
> Gouvernance universelle : `~/DEV/.AI_AGENTS.md` · Contexte global : `~/.claude/CLAUDE.md`

## 1. Résumé du projet

Application de gestion de matrice de compétences (Delivery Matrix App). Architecture fullstack découplée : frontend SvelteKit + backend FastAPI + SQLite.

## 2. Stack technique

| Technologie | Usage |
|-------------|-------|
| SvelteKit 2 | Frontend (`frontend/`) |
| TailwindCSS | Styles |
| FastAPI | Backend REST (`backend/`) |
| SQLAlchemy | ORM |
| Pydantic | Validation des données |
| SQLite | Base de données (`matrix_v2.db`) |
| uvicorn | Serveur ASGI |

## 3. Structure

```
matrice-competences/
  frontend/          # SvelteKit app
    src/
    static/
    package.json
  backend/           # FastAPI app
    sql_app/         # Modèles, routes, schemas
    requirements.txt
    matrix_v2.db     # Base SQLite active
```

## 4. Commandes

```bash
# Frontend
cd frontend
npm install
npm run dev          # http://localhost:5173
npm run build        # Build production → /build
npm run preview      # Preview production

# Backend
cd backend
pip install -r requirements.txt
uvicorn sql_app.main:app --reload   # http://localhost:8000
# Docs API auto-générées : http://localhost:8000/docs
```

## 5. Conventions

- **CORS** : configurer explicitement dans FastAPI pour autoriser le frontend dev
- **Base de données** : utiliser `matrix_v2.db` — `matrix.db` est une version obsolète
- `initial_data.json` : données de seed — ne pas modifier sans migration Alembic
- **Séparation stricte** frontend/backend — aucune logique métier dans les composants Svelte
