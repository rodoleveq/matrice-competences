# DECISIONS.md — matrice-competences

> Architecture Decision Records. A jour au 2026-05-02.

## ADR-001 : SvelteKit + FastAPI fullstack decouple

- **Date** : 2026-01-01
- **Statut** : Accepte
- **Decision** : Frontend SvelteKit separe du backend FastAPI — deux processus independants
- **Raison** : Separation des responsabilites, deploiement independant, flexibilite
- **Consequence** : Deux serveurs de dev, CORS requis, communication via REST API

## ADR-002 : SQLite avec schema v2 (matrix_v2.db)

- **Date** : 2026-01-01
- **Statut** : Accepte
- **Decision** : SQLite via SQLAlchemy, schema versionne v2 — matrix.db est obsolete
- **Raison** : Simplicite de deploiement local, pas de serveur DB requis
- **Consequence** : Migration Alembic obligatoire pour tout changement de schema

## ADR-003 : Pydantic pour la validation

- **Date** : 2026-01-01
- **Statut** : Accepte
- **Decision** : Pydantic pour les schemas de validation et serialisation des donnees
- **Raison** : Integration native avec FastAPI, typage fort, validation automatique
- **Consequence** : Chaque endpoint doit avoir ses schemas Pydantic definis
