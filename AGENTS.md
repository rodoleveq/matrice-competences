# AGENTS.md — matrice-competences
> Gouvernance universelle : ~/DEV/.AI_AGENTS.md | Sync : ~/DEV/sync-agents.sh
> Derniere mise a jour : 2026-05-02

<!-- BEGIN:UNIVERSAL -->

## 1. Principes Fondamentaux

### 1.1 Pas d'Estimations de Temps

- **NE JAMAIS** donner d'estimations de temps (jours, semaines, "quick fix", "ce sera rapide")
- Travailler en iterations courtes et mesurables
- Laisser l'humain juger du timing selon son contexte
- Se concentrer sur le **quoi** faire, pas sur le **quand**

### 1.2 Determinisme

- Documents a jour = previsibilite
- **Toujours** lire les fichiers d'etat avant de travailler
- Chaque changement significatif -> mise a jour des docs
- Le silence des documents ne signifie pas permission

### 1.3 Validation Continue

- Build passe **AVANT** de se considerer fini
- Tests passent **AVANT** de commiter
- Verifier l'existant avant de creer
- "Ca compile" n'est pas une validation complete

### 1.4 Responsabilite

- Un agent qui commence un travail en est responsable jusqu'a validation
- Ne pas abandonner un travail a moitie fait
- Si bloque, documenter le blocage avant de passer a autre chose

---

## 2. Protocole Universel de Travail

### 2.1 Avant de Commencer

1. Lire CLAUDE.md (contexte projet)
2. Lire STATE.md (etat actuel)
3. Lire DECISIONS.md (ADR si pertinent)
4. Verifier les issues ouvertes : `gh issue list --state open`
5. Verifier la branche : `git branch --show-current`
6. Verifier que le build passe avant toute modification

**Ordre de priorite des fichiers :**
1. `CLAUDE.md` - Contexte lu par TOUS les agents
2. `STATE.md` -Etat actuel du code
3. `DECISIONS.md` - ADR en vigueur
4. `AGENTS.md` - Conventions specifiques projet

### 2.2 Pendant le Travail

1. Travailler sur une branche dediee : `feature/xxx` ou `fix/xxx`
2. Commits conventionnels : `type(scope): message`
   - Types valides : `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
   - Exemples : `feat(ui): add dark mode`, `fix(models): correct SRS algorithm`
3. Ne pas modifier les fichiers de config d'un autre agent sans accord explicite
4. Respecter les ADR documentees
5. Ne pas creer de fichiers de documentation redondants

### 2.3 Apres le Travail

1. Mettre a jour `STATE.md` si changements de features/modeles/services
2. Mettre a jour `CLAUDE.md` si changement d'architecture
3. Ajouter une ADR si decision architecturale nouvelle
4. Verifier build + tests passent
5. Laisser `git status` propre (ou expliciter ce qui doit l'etre)

### 2.4 Discipline d'Optimisation de Tokens (RTK)

- **Usage Obligatoire** de `rtk` pour filtrer ou emballer les sorties de commandes verbeuses :
  - Les résultats de `git diff` et de `git status`
  - Les rapports et logs de compilation ou de build (ex: `xcodebuild`)
  - Les longs listings de fichiers ou de répertoires
- **Interdiction** d'utiliser `rtk` pour masquer des erreurs ou des diagnostics critiques :
  - Les erreurs du compilateur brut (Swift, Rust, Node, etc.)
  - Les stack traces de plantage ou échecs de tests unitaires
  - Les logs liés à des secrets ou à la sécurité
- **Secours Brut** : En cas de besoin de débogage sans filtrage ou en cas de dysfonctionnement du hook, utiliser : `rtk proxy <cmd>`

---

## 3. Conventions Cross-Langage

### 3.1 Nommage

| Element | Convention | Exemple |
|---------|------------|---------|
| Fichiers | kebab-case | `data-loader.ts`, `question-model.swift` |
| Classes/Types | PascalCase | `QuizViewModel`, `Question` |
| Fonctions | camelCase | `loadQuestions()`, `calculateReadiness()` |
| Constantes | SCREAMING_SNAKE_CASE | `MAX_QUESTIONS`, `DEFAULT_EASE_FACTOR` |
| Variables | camelCase | `currentIndex`, `isCorrect` |
| Composants UI | PascalCase + suffixe | `HomeView`, `QuestionCard` |
| ViewModels | PascalCase + suffixe | `QuizViewModel`, `ProgressViewModel` |

### 3.2 Structure des Commits

```
feat(ui): add progress bar component
fix(services): correct SRS interval calculation
docs(readme): update installation instructions
refactor(models): extract shared logic to base class
test(viewmodels): add coverage for QuizViewModel
chore(ci): update GitHub Actions workflow
```

### 3.3 Langue

- **Code** : Anglais (noms de variables, fonctions, classes)
- **UI/Texte** : Langue du projet (francais pour LAPL, anglais sinon)
- **Commentaires** : Au choix, mais coherent dans un meme fichier

### 3.4 Patterns Communs

| Langage | Pattern | Exemple |
|---------|---------|---------|
| Swift | MVVM + @Observable | Views @Observable, UI SwiftUI |
| TypeScript/JS | Feature-based | `features/auth/`, `components/` |
| Python | Clean Architecture | `domain/`, `application/`, `infrastructure/` |

---

## 4. Gestion des Conflits

### Regle d'Or

> **Le code qui compile + passe les tests a la priorite**

### Hierarchie en Cas de Conflit

1. Les ADR validees (`DECISIONS.md`) font autorite sur les decisions architecturales
2. Le code qui compile et passe les tests est prioritaire sur le code qui ne compile pas
3. En dernier recours : **demander a l'humain** (Product Owner)

### Signaux d'Escalade (requierent l'humain)

- Conflit entre deux ADR validees
- Decision technique avec impact majeur (changement de stack, refactor massif)
- Modification de formules de calcul (ex: Exam Readiness)
- Ajout de dependance externe
- Changement de version minimale (iOS, Node, etc.)
- Besoin de supprimer ou renommer un fichier existant sans consensus

---

## 5. Anti-Patterns Universels

### A EVITER Absolument

| Anti-Pattern | Risque | Alternative |
|--------------|--------|-------------|
| Hardcoder des chemins | Break cross-platform | Utiliser `path.join()` ou abstraction |
| Ajouter des secrets dans le code | Fuite credentials | Variables d'environnement, `.env` |
| Creer sans verifier l'existant | Code duplique | `grep`/`glob` avant de creer |
| Modifier sans tester | Bugs en production | build + tests avant commit |
| Estimer le temps | Mauvaise planification | Iterations mesurables |
| Ignorer STATE.md | Incoherence avec l'historique | Lecture obligatoire |
| Contourner la couche d'acces aux donnees | Violation SRP | Passer par le repository/service |
| Ajouter des dependances sans accord | Dette technique | Demander validation |

---

## 6. Structure Standard d'un Projet Multi-Agents

```
<repo>/
  CLAUDE.md              # Contexte projet (TOUS les agents lisent)
  STATE.md              #Etat actuel du code
  DECISIONS.md          # Architecture Decision Records
  AGENTS.md             # Conventions specifiques au projet
  .claude/              # Config Claude Code
    settings.json
    skills/
      <project>/SKILL.md
  .gemini/              # Config Gemini
    skills/
      <project>/SKILL.md
  .mistral/             # Config Mistral
    skills/
      <project>/SKILL.md
```

---

## 7. Verifications Obligatoires

### Build

| Projet | Commande |
|--------|----------|
| iOS (Xcode) | `xcodebuild -scheme <Scheme> -sdk iphonesimulator build` |
| Node.js | `npm run build` |
| Python | `python -m py_compile *.py` |
| Go | `go build ./...` |

### Tests

| Projet | Commande |
|--------|----------|
| iOS | `xcodebuild test -scheme <Scheme> -destination 'platform=iOS Simulator,name=iPhone 16e Test'` |
| Node.js | `npm test` |
| Python | `pytest` |

### Linting

| Projet | Commande |
|--------|----------|
| Swift | `swiftlint` |
| TypeScript | `npm run lint` ou `eslint` |
| Python | `ruff check .` |

---

## 8. Workflow Multi-Agents CLI

> Ce systeme repose sur 4 agents CLI : Claude Code, Gemini CLI, Codex CLI, Vibe (Mistral).
> L'humain orchestre. Les agents executent. Chaque agent lit `.AI_AGENTS.md` avant tout.

### Principes de Coordination

1. **Source unique** : `~/DEV/.AI_AGENTS.md` — lire avant toute session, quelle que soit l'origine
2. **Un agent = une tache** — pas de duplication de travail entre agents
3. **Passation explicite** — jamais de relais implicite entre agents
4. **Capitalisation** — toute regle utile decouverte en session va dans `§11 Lecons Apprises`

### Passation Inter-Agents (HANDOFF)

Quand l'humain passe le relais d'un agent a un autre :
1. **Standard Général** : Ecrire (ou faire ecrire) un fichier `HANDOFF-[description].md` dans `~/DEV/` ou la racine du projet.
   - **Objectif** : ce qu'on cherche a accomplir
   - **Etat actuel** : ce qui est fait, ce qui reste
   - **Fichiers cles** : chemins a lire en priorite
   - **Prochaine action** : instruction concrete pour l'agent suivant
2. **⚠️ Exceptions aux Standards** : Les projets dotés de frameworks d'orchestration ou de swarm dédiés (comme le workflow **BMAD** dans `autoclaude-test` ou le modèle **Hub-and-Spoke** d'`align-ios`) utilisent leurs propres templates de handoffs locaux (ex: insertion structurée dans `STATE.md` sous le jeton, ou bloc de 15 lignes max dans le chat). Ces règles spécifiques priment sur ce standard universel.
3. L'agent suivant lit obligatoirement le handoff approprié EN PREMIER avant toute action.

### Resolution de Conflit

1. Consulter `git log --oneline -10` pour voir qui a travaille en dernier
2. Consulter `DECISIONS.md` pour les decisions architecturales
3. Si conflit sur un fichier : garder la version qui compile + passe les tests
4. En cas de doute : **demander a l'humain**

### Propagation des Changements

Apres toute modification de `~/DEV/.AI_AGENTS.md` :
```bash
~/DEV/sync-agents.sh   # Propage vers Codex + Vibe
                        # Gemini recoit via @import natif
```

---

## 9. Templates de Fichiers de Projet

### CLAUDE.md (minimum)

```markdown
# CLAUDE.md - [Nom du Projet]

> Contexte pour les agents IA. Derniere mise a jour : YYYY-MM-DD

## 1. Resume du Projet
[Description courte]

## 2. Stack Technique
| Technologie | Usage |
|-------------|-------|
| [Tech] | [Usage] |

## 3. Commandes
```bash
# Build
[commande]

# Test
[commande]
```

## 4. Conventions
- [Convention 1]
- [Convention 2]
```

### STATE.md (minimum)

```markdown
# STATE.md -Etat du Projet

> Derniere mise a jour : YYYY-MM-DD

## Branche active
- [nom de branche]

## Features implementees
- [ ] Feature 1
- [ ] Feature 2

## Features en cours
- [ ] Feature 3

## Issues ouvertes
| # | Titre |
|---|-------|
| 1 | [Issue] |
```

### DECISIONS.md (minimum)

```markdown
# DECISIONS.md - Architecture Decision Records

## ADR-001 : [Titre]
- **Date** : YYYY-MM-DD
- **Statut** : Accepte
- **Decision** : [Ce qui a ete decide]
```

### AGENTS.md projet (opt-in sync UNIVERSAL)

```markdown
# AGENTS.md — [Nom du Projet]

> Gouvernance universelle : ~/DEV/.AI_AGENTS.md — lire avant tout travail.
> Sync : ~/DEV/sync-agents.sh | Derniere mise a jour : YYYY-MM-DD

<!-- BEGIN:UNIVERSAL -->
<!-- END:UNIVERSAL -->

## Contexte Projet

Delivery Matrix App — gestion de matrice de competences. Architecture fullstack decouple :
frontend SvelteKit + backend FastAPI + SQLite.

## Stack

| Technologie | Usage |
|-------------|-------|
| SvelteKit 2 | Frontend (`frontend/`) |
| TailwindCSS | Styles |
| FastAPI | Backend REST (`backend/`) |
| SQLAlchemy | ORM |
| Pydantic | Validation des donnees |
| SQLite | Base de donnees (`matrix_v2.db`) |
| uvicorn | Serveur ASGI |

## Structure

```
matrice-competences/
  frontend/          # SvelteKit app (port 5173)
  backend/           # FastAPI app (port 8000)
    sql_app/         # Modeles, routes, schemas
    matrix_v2.db     # Base SQLite active
```

## Regles Specifiques

- Utiliser `matrix_v2.db` — `matrix.db` est obsolete
- Ne pas modifier `initial_data.json` sans migration Alembic
- CORS explicite cote FastAPI pour autoriser le frontend dev
- Separation stricte frontend (port 5173) / backend (port 8000) — aucune logique metier dans les composants Svelte

---

## Leçons Apprises Locales

> Bloc vivant — noter ici toute règle utile découverte lors du travail sur ce projet.
> Format : `- [YYYY-MM-DD] [outil] : règle apprise`
> **Remontée obligatoire** → copier dans `~/DEV/.AI_AGENTS.md` → §11, puis `~/DEV/sync-agents.sh`

<!-- Aucune leçon enregistrée pour l instant. -->
