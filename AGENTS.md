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

### 2.5 Règles d'optimisation MCP / Reads — TRANSVERSE

> Ces 4 règles s'appliquent à **tous les agents** (Claude, Gemini, Codex, Vibe, OpenCode) — pas seulement Claude. Elles réduisent la consommation de tokens de 30-50 % sans perte de fonctionnalité. Le détail complet (checklist, coûts comparés, patterns avancés) est dans `~/.claude/rules/mcp-optimization.md` (chargé nativement par Claude Code) — mais les principes ci-dessous valent partout.

**Règle 1 — Bash d'abord, MCP/Read après**

Si `grep`, `find`, `jq`, `awk`, `sed` peuvent accomplir la tâche, utiliser Bash (de préférence via `rtk`). Pas de `Read` inutile sur fichier entier.

# ❌ Cher : Read ~/DEV/.AI_AGENTS.md (charge ~2000 tokens en contexte)
# ✅ Sobre : grep "Leçons Apprises" ~/DEV/.AI_AGENTS.md (~100 tokens)

**Règle 2 — Limiter avant de lire**

Pour les fichiers > 5 KB, utiliser `Read` avec `--limit`/`--offset`, ou `grep -A/-B/-n` ciblé. Lire le fichier complet seulement si nécessaire.

# ❌ Cher : Read ~/DEV/.AI_AGENTS.md (500+ lignes, ~5K tokens)
# ✅ Sobre : Read ... --limit 30 --offset 100 (~200 tokens)

**Règle 3 — CLI > MCP pour la documentation**

Pour Context7 : `npx ctx7@latest docs <id>` au lieu du MCP. Pour GitHub : `gh` CLI plutôt que les MCP GitHub si la requête peut être ciblée.

# ❌ MCP : mcp__context7__query-docs (~5000 tokens)
# ✅ CLI : npx ctx7@latest docs /vercel/next.js "App Router" (~1000 tokens)

**Règle 4 — Agréger avant d'afficher**

Pour parcourir N fichiers, préférer un grep agrégé à N Reads séquentiels.

# ❌ Cher : for f in *.md; do Read $f; done  (N × 2K tokens)
# ✅ Sobre : grep -h "^#" *.md | sort -u  (~300 tokens)

**Mesure et discipline**

- Suivi côté Claude : `rtk gain` / `rtk gain --history` (cible ≥ 70 %, mesuré 72,1 % au 2026-05-24).
- Autres agents : pas d'instrumentation native ; appliquer les règles par discipline, valider qualitativement.
- Avant chaque appel MCP coûteux, **checklist mentale** :
  1. Bash peut-il le faire ?
  2. Puis-je filtrer (grep, head, limit) ?
  3. Une CLI est-elle plus légère que le MCP ?
  4. Ai-je vraiment besoin du fichier complet ?

Si toutes les réponses sont NON → MCP justifié.

---

## 3. Conventions Cross-Langage

### 3.1 Nommage (code)

| Element | Convention | Exemple |
|---------|------------|---------|
| Fichiers code | kebab-case | `data-loader.ts`, `question-model.swift` |
| Classes/Types | PascalCase | `QuizViewModel`, `Question` |
| Fonctions | camelCase | `loadQuestions()`, `calculateReadiness()` |
| Constantes | SCREAMING_SNAKE_CASE | `MAX_QUESTIONS`, `DEFAULT_EASE_FACTOR` |
| Variables | camelCase | `currentIndex`, `isCorrect` |
| Composants UI | PascalCase + suffixe | `HomeView`, `QuestionCard` |
| ViewModels | PascalCase + suffixe | `QuizViewModel`, `ProgressViewModel` |

### 3.1bis Nommage (documents et dossiers)

| Element | Convention | Exemple |
|---------|------------|---------|
| Documents canoniques (audits, rapports, gouvernance) | UPPER_SNAKE_CASE.md | `ANALYSIS_REPORT.md`, `EXECUTIVE_SUMMARY.md`, `DEPENDENCIES_MAP.md` |
| Inventaires auto-générés | UPPER_SNAKE_CASE.md, suffixe `_INVENTORY` | `MCPS_INVENTORY.md`, `SKILLS_INVENTORY.md`, `PROJECTS_INVENTORY.md` |
| Templates | UPPER_SNAKE_CASE.md, suffixe `_TEMPLATE` | `INVENTORY_MCP_TEMPLATE.md`, `CHECKLIST_TEMPLATE.md` |
| Scripts | kebab-case.sh / .py | `sync-agents.sh`, `update-readme-status.py` |
| Règles Claude / instructions | kebab-case.md | `mcp-optimization.md`, `context7.md` |
| Métadonnées / config | snake_case.yaml / kebab-case.json | `_metadata.yaml`, `audit-metadata.json` |
| README local | `README.md` (exact) | — |
| Dossiers projet | kebab-case | `agentic-slide-factory/`, `matrice-competences/` |
| Dossiers hors scope | préfixe `99-` | `99-HORS SCOPE/`, `99-archives/` |
| Dossiers d'archive | préfixe `.archive` ou `.audit-history` | `.archive/`, `.audit-history/` |

**Convention de préfixe `99-*` pour dossiers hors scope :**

Tout dossier à la racine de `~/DEV/` préfixé par `99-` est considéré hors scope du système agentique :
- Les scripts (`sync-agents.sh`, `update_readme_status.py`, `scripts/collectors/*`) ne le scannent pas (ils ciblent explicitement `active/`, `collab/`, `experiments/`).
- Les agents IA doivent l'ignorer sauf demande explicite de l'utilisateur.
- Préfixe numérique `99-` : pousse le dossier en fin de listing alphabétique (visuel net).

Exemple : `~/DEV/99-HORS SCOPE/` contient assets professionnels, captures hors contexte, archives personnelles. Voir `README.md` local du dossier pour le détail.

Cette convention est extensible : `99-personnel/`, `99-clients/`, `99-archives-anciennes/`, etc.

### 3.2 Structure des Commits

feat(ui): add progress bar component
fix(services): correct SRS interval calculation
docs(readme): update installation instructions
refactor(models): extract shared logic to base class
test(viewmodels): add coverage for QuizViewModel
chore(ci): update GitHub Actions workflow

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
~/DEV/scripts/sync-agents.sh   # Propage vers Codex + Vibe
                        # Gemini recoit via @import natif

### Cycle d'audit

Un audit est un cycle structuré : diagnostic → recommandations → plan d'actions → exécution → suivi post-impl.

**Convention de structure** :
- **Audit principal** : un dossier `~/DEV/audits/YYYY-MM/` par cycle, avec :
  - Un rapport pivot (`ANALYSIS_REPORT.md`, `FULL_AUDIT.md`, ou équivalent)
  - Un `INDEX.md` (navigation) et un `_metadata.yaml` (inventaire)
  - Sous-dossiers thématiques recommandés : `inventories/`, `decisions/`, `investigations/`, `implementations/`
  - Un dashboard de pilotage (`dashboard-data.json` + `dashboard.html`) si plan d'actions complexe
  - Archives sous `.archive/` (cachées, non trackées Git via `.gitignore`)

**Convention de suivi post-impl** :
- **`~/DEV/audits/POST_IMPLEMENTATION_TRACKING.md`** est la source unique transverse pour toute action **survivant à un cycle d'audit** (Q-Post, I-Post, F-Post, décisions différées, items reportés, items requalifiés, etc.).
- Format : une section `## Audit YYYY-MM` par cycle, items typés avec statuts standards (PENDING / IN_PROGRESS / COMPLETED / CLOSED / DEFERRED).
- **Pas de fichiers post-impl par audit** : tout converge vers ce fichier unique pour éviter la fragmentation et faciliter le bilan inter-cycles.
- Voir le fichier pour la convention détaillée (format d'item, statuts, cycle de vie).

**Documents transverses** (racine `~/DEV/audits/`) :
- `AUDITS_INDEX.md` — index des audits multi-millésimes
- `AUDIT_COMPARISON_STRATEGY.md` — méthodologie de comparaison entre cycles
- `AUDIT_COMPARISON_REPORT.md` — rapport de couverture cross-audit (produit à chaque clôture de cycle)
- `POST_IMPLEMENTATION_TRACKING.md` — suivi des actions post-impl (vivant, mis à jour à chaque cycle)

---

## 9. Templates de Fichiers de Projet

### CLAUDE.md (minimum)

# CLAUDE.md - [Nom du Projet]

> Contexte pour les agents IA. Derniere mise a jour : YYYY-MM-DD

## 1. Resume du Projet
[Description courte]

## 2. Stack Technique
| Technologie | Usage |
|-------------|-------|
| [Tech] | [Usage] |

## 3. Commandes
# Build
[commande]

# Test
[commande]

## 4. Conventions
- [Convention 1]
- [Convention 2]

### STATE.md (minimum)

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

### DECISIONS.md (minimum)

# DECISIONS.md - Architecture Decision Records

## ADR-001 : [Titre]
- **Date** : YYYY-MM-DD
- **Statut** : Accepte
- **Decision** : [Ce qui a ete decide]

### AGENTS.md projet (opt-in sync UNIVERSAL)

# AGENTS.md — [Nom du Projet]

> Gouvernance universelle : ~/DEV/.AI_AGENTS.md — lire avant tout travail.
> Sync : ~/DEV/scripts/sync-agents.sh | Derniere mise a jour : YYYY-MM-DD


## Contexte Projet

[Description courte — copier depuis CLAUDE.md]

## Stack

| Technologie | Usage |
|-------------|-------|
| [Tech]      | [Usage] |

## Regles Specifiques

- [Uniquement ce qui differe du standard universel]

---

## 10. Cartographie des Projets

> L'inventaire de tous les projets présents sur cette machine (dans `active/`, `collab/` ou `experiments/`) est **mis à jour automatiquement** en temps réel.
> **Obligation :** Consulter le fichier de synthèse globale de l'espace de travail [README.md](file:///Users/rodolphelevesque/DEV/README.md) pour obtenir la cartographie à jour, les stacks techniques employées, ainsi que l'indicateur visuel de gouvernance active (`🟢 Transverse` ou `🔒 Isolé`).

---

## 11. Lecons Apprises

> Bloc vivant — ajouter toute nouvelle regle issue de l'experience terrain.
> Format : `- [YYYY-MM-DD] [outil] : regle apprise`
> Propager via `./sync-agents.sh` apres ajout.

<!-- Aucune lecon enregistree pour l'instant. -->

---

## 12. Roles et Orchestration des Agents CLI

> L'humain choisit l'agent selon la nature de la tache.
> Les agents ne s'orchestrent pas entre eux — ils se passent le relais via HANDOFF.

### Forces de Chaque Agent

| Agent | CLI | Forces principales | Eviter |
|-------|-----|--------------------|--------|
| Claude Code | `claude` | Architecture, multi-fichiers, memory persistante, planification, review | Taches repetitives sans contexte |
| Gemini CLI | `gemini` | Grand contexte (1M tokens), analyse, synthese, recherche | Modifications fichiers complexes multi-etapes |
| Codex CLI | `codex` | Generation de code, taches focalisees, shell integre | Decisions architecturales, fichiers nombreux |
| Vibe (Mistral) | `vibe` | Redaction FR, reformulation, documentation, questions rapides | Taches de code longues |

### Regles d'Orchestration

1. **Lire `.AI_AGENTS.md`** — obligation universelle avant toute session
2. **Un HANDOFF par passation** — format standard, fichier nomme explicitement
3. **Pas de reinvention** — un agent qui arrive verifie l'existant avant de creer
4. **Capitaliser en sortie** — si une session revele une regle utile, la noter dans `§11`
5. **Sync apres chaque ajout** — `~/DEV/scripts/sync-agents.sh` puis commit

### Cycle d'Amelioration Continue

Session agent
    │
    ├─ Decouverte d'une regle utile
    │       │
    │       └─> Ajout dans §11 de .AI_AGENTS.md
    │               │
    │               └─> sync-agents.sh   (Codex + Vibe mis a jour)
    │                       │
    │                       └─> Gemini : @import (auto)
    │
    └─ Passation a un autre agent
            │
            └─> HANDOFF-[desc].md dans ~/DEV/ ou racine projet

### Perimetre des Fichiers Geres

| Categorie | Fichier(s) | Mecanisme |
|-----------|-----------|-----------|
| Source de verite | `~/DEV/.AI_AGENTS.md` | Edition directe |
| Config Claude | `~/.claude/CLAUDE.md` + `rules/*.md` | Edition directe |
| Config Gemini | `~/.gemini/GEMINI.md` | @import natif (auto) |
| Config Codex | `~/.codex/AGENTS.md` | sync-agents.sh (auto) |
| Config Vibe | `~/.vibe/instructions.md` | sync-agents.sh (auto) |
| Projets opt-in | `~/DEV/active/*/AGENTS.md` | sync-agents.sh si marqueurs |
| Skills partagees | `~/.agents/skills/` | Symlinks vers ~/.claude/skills/ |
| Passations | `~/DEV/HANDOFF-*.md` | Fichiers temporaires par session |

### Infrastructure d'Automatisation

| Fichier | Role |
|---------|------|
| `~/DEV/scripts/sync-agents.sh` | Script de propagation (global + projets opt-in) |
| `~/DEV/scripts/hook-claude-sync.sh` | Hook Claude Code — sync apres Write/Edit sur .AI_AGENTS.md |
| `~/.claude/settings.json` | Enregistrement du hook PostToolUse |
| `~/Library/LaunchAgents/com.rodolphe.sync-agents.plist` | Daemon macOS — surveille .AI_AGENTS.md, declenche sync auto |
| `~/DEV/.sync-agents.log` | Log horodate de toutes les sync |

**Declenchements de sync (sans intervention manuelle) :**
- Tout agent modifie `.AI_AGENTS.md` → launchd le detecte → sync
- Claude Code modifie `.AI_AGENTS.md` → hook PostToolUse → sync (en sus)
- `touch ~/DEV/.AI_AGENTS.md` suffit a forcer une sync manuelle

**Opt-in projet** : ajouter les marqueurs `BEGIN:UNIVERSAL` / `END:UNIVERSAL` (balises HTML en commentaires) en debut de tout `AGENTS.md` de projet → il sera mis a jour automatiquement a chaque sync.

**Monitoring** : `tail -f ~/DEV/.sync-agents.log`

---

### Gestion Git du répertoire DEV

Depuis le 2026-05-24 (Vague 2), le répertoire `~/DEV/` est un dépôt Git **local** (pas de remote distant pour l'instant).

**Périmètre tracké** : gouvernance racine (`.AI_AGENTS.md`, `README.md`, `GLOSSARY.md`, `HANDOFF-AGENT-CONFIG.md`), dossiers `scripts/`, `audits/`, `docs/`. Tout le reste (`active/`, `collab/`, `experiments/`, `99-*/`, logs, caches) est **ignoré par défaut**.

**Configuration** : `~/DEV/.gitignore` utilise une stratégie **allowlist défensive** (`*` ignore tout, puis `!nom` track explicitement). Un nouveau dossier ou fichier à la racine est ignoré jusqu'à ajout explicite d'une ligne `!nom` dans `.gitignore`.

**Hook pre-commit** : un filet de sécurité refuse les commits contenant :
- fichiers > 5 Mo
- fichiers sensibles (`.env`, `*.key`, `*.pem`, `oauth*`, `credentials*`, `secrets*`)
- fichiers `.log`
- fichiers dans `active/`, `collab/`, `experiments/`, `99-*/`

Le hook est versionné sous `~/DEV/scripts/git-hooks/pre-commit`. Pour le (ré)installer : `bash ~/DEV/scripts/git-hooks/install-hooks.sh`.

**Discipline pour les agents et l'humain** :

1. **Toujours `git add <fichier-précis>`**, jamais `git add .` ni `git add -A`. Vérifier `git status` avant chaque commit.
2. **Nouveau dossier à la racine** : décider track ou ignore. Si à tracker : éditer `.gitignore` (ajouter `!nouveau-dossier/`). Si à ignorer : ne rien faire (le wildcard initial l'ignore par défaut).
3. **Convention de commit** : `type(scope): message` conforme à Conventional Commits (`feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `arch`).
4. **Ne jamais bypass le hook** (`--no-verify`) sauf cas exceptionnel justifié.
5. **Pas de remote distant configuré** à ce stade : tout reste local. À reconsidérer si le besoin de backup distant émerge.
6. **Historique d'avant Git** : les 17 commits de l'ancien dépôt `scripts/` sont archivés dans `~/DEV/audits/2026-05/.archive/scripts-git-history/`. Consultation : `git --git-dir=~/DEV/audits/2026-05/.archive/scripts-git-history/.git log`.

**Pour un nouvel agent IA arrivant** : `cd ~/DEV && git status` pour comprendre l'état courant. Tout commit doit respecter la discipline ci-dessus.

<!-- END:UNIVERSAL -->
- `sync-agents.sh` **ignore** ce projet (pas de marqueur `<!-- BEGIN:UNIVERSAL -->` attendu)
- N'apparaît **pas** dans les inventaires d'agents (intentionnel)
- Peut avoir ses propres AGENTS.md ou guidelines ISO-spécifiques

**Vérification** : `grep -r "BEGIN:UNIVERSAL" ~/DEV/active/align-ios/` doit retourner vide

---

## Procédure pour Ajouter un Nouveau Projet opt-out

Si un nouveau projet doit être exclu :

1. **Documenter dans cette section** : raison, status, conséquences
2. **Ajouter un commentaire en tête du projet** :
   ```
   # align-ios — ISOLÉ — Exclusion intentionnelle
   # Voir ~/DEV/.AI_AGENTS.md § "Projets opt-out" pour contexte
   ```
3. **Mettre à jour CLAUDE.md** : ajouter un tableau des projets isolés
4. **Vérifier dans le log sync** : `grep -c "SKIP" ~/.sync-agents.log` ne doit contenir **aucune** mention du projet isolé une fois documenté (sinon = oubli)

---

## 13. Glossaire et Nomenclature Canonique

> **Pourquoi ?** Chaque outil (Claude, Gemini, Codex, OpenCode, Vibe, Antigravity) utilise des mots différents pour les mêmes concepts. Cette section stabilise notre vocabulaire interne et crée une table de correspondance par outil.

### Métamodèle Interne (7 Concepts Fondamentaux)

**1. Harness** — L'enveloppe d'exécution agentique (runtime complet qui contient modèle, tools, permissions, contexte, logs)

**2. Instructions Files** — Fichiers de contexte durable (CLAUDE.md, GEMINI.md, AGENTS.md) — mémoire persistante, pas des capacités actives

**3. Skill** — Capacité réutilisable orientée workflow (recette opératoire spécialisée, invocable explicitement)

**4. Plugin** — Package d'extension pouvant contenir skills, hooks, agents, MCP, règles, etc.

**5. MCP Integration** — Protocole standard pour connecter systèmes externes (Model Context Protocol)  
   *Note: MCP integration = "quoi connecter". Voir `~/.claude/rules/mcp-optimization.md` pour "comment l'utiliser efficacement".*

**6. Hooks** — Automatismes événementiels (déclenchés sur événements du lifecycle agentique)

**7. Agents / Subagents** — Instances autonomes avec modèle, tools, permissions, contexte indépendant

### Table Rapide de Correspondance

| Concept | Claude | Gemini | Codex | OpenCode | Vibe |
|---------|--------|--------|-------|----------|------|
| Instructions | CLAUDE.md | GEMINI.md | AGENTS.md | AGENTS.md | config.toml |
| Skill | skill | agent skill | skill | agent skill | skill |
| Plugin | plugin | extension | plugin | plugin | — |
| MCP | MCP server | mcpServers | MCP server | MCP server | mcp_servers |
| Harness | Claude Code | Gemini CLI | Codex | OpenCode | Vibe CLI |

**Voir aussi:** `~/DEV/GLOSSARY.md` pour détail complet (7 concepts + table détaillée par outil + surfaces) + exemples + ambiguïtés résolues.

### Règles d'Écriture Documentaire

1. **Au premier usage d'un terme produit**, ajouter le terme canonique: "Gemini extension (plugin)", "Mistral connector (external integration backed by MCP)"

2. **Ne jamais confondre** MCP integration et mcp-optimization:  
   ✅ "MCP integration allows connecting external systems"  
   ❌ "Configure your MCP optimization rules" (mcp-optimization = operational discipline, not configuration)

3. **Ne jamais appeler** "skill" un fichier de règles passif  
   ✅ "CLAUDE.md contains instructions"  
   ❌ "CLAUDE.md is a skill"

4. **Ne jamais appeler** "plugin" un serveur MCP  
   ✅ "MCP server for external integration"  
   ❌ "MCP plugin"

5. **Ne jamais appeler** "harness" un connecteur ou plugin  
   ✅ "Claude Code harness provides the execution environment"  
   ❌ "MCP harness"

---
- `sync-agents.sh` **ignore** ce projet (pas de marqueur `<!-- BEGIN:UNIVERSAL -->` attendu)
- N'apparaît **pas** dans les inventaires d'agents (intentionnel)
- Peut avoir ses propres AGENTS.md ou guidelines ISO-spécifiques

**Vérification** : `grep -r "BEGIN:UNIVERSAL" ~/DEV/active/align-ios/` doit retourner vide

---

## Procédure pour Ajouter un Nouveau Projet opt-out

Si un nouveau projet doit être exclu :

1. **Documenter dans cette section** : raison, status, conséquences
2. **Ajouter un commentaire en tête du projet** :
   ```
   # align-ios — ISOLÉ — Exclusion intentionnelle
   # Voir ~/DEV/.AI_AGENTS.md § "Projets opt-out" pour contexte
   ```
3. **Mettre à jour CLAUDE.md** : ajouter un tableau des projets isolés
4. **Vérifier dans le log sync** : `grep -c "SKIP" ~/.sync-agents.log` ne doit contenir **aucune** mention du projet isolé une fois documenté (sinon = oubli)

---

## 13. Glossaire et Nomenclature Canonique

> **Pourquoi ?** Chaque outil (Claude, Gemini, Codex, OpenCode, Vibe, Antigravity) utilise des mots différents pour les mêmes concepts. Cette section stabilise notre vocabulaire interne et crée une table de correspondance par outil.

### Métamodèle Interne (7 Concepts Fondamentaux)

**1. Harness** — L'enveloppe d'exécution agentique (runtime complet qui contient modèle, tools, permissions, contexte, logs)

**2. Instructions Files** — Fichiers de contexte durable (CLAUDE.md, GEMINI.md, AGENTS.md) — mémoire persistante, pas des capacités actives

**3. Skill** — Capacité réutilisable orientée workflow (recette opératoire spécialisée, invocable explicitement)

**4. Plugin** — Package d'extension pouvant contenir skills, hooks, agents, MCP, règles, etc.

**5. MCP Integration** — Protocole standard pour connecter systèmes externes (Model Context Protocol)  
   *Note: MCP integration = "quoi connecter". Voir `~/.claude/rules/mcp-optimization.md` pour "comment l'utiliser efficacement".*

**6. Hooks** — Automatismes événementiels (déclenchés sur événements du lifecycle agentique)

**7. Agents / Subagents** — Instances autonomes avec modèle, tools, permissions, contexte indépendant

### Table Rapide de Correspondance

| Concept | Claude | Gemini | Codex | OpenCode | Vibe |
|---------|--------|--------|-------|----------|------|
| Instructions | CLAUDE.md | GEMINI.md | AGENTS.md | AGENTS.md | config.toml |
| Skill | skill | agent skill | skill | agent skill | skill |
| Plugin | plugin | extension | plugin | plugin | — |
| MCP | MCP server | mcpServers | MCP server | MCP server | mcp_servers |
| Harness | Claude Code | Gemini CLI | Codex | OpenCode | Vibe CLI |

**Voir aussi:** `~/DEV/GLOSSARY.md` pour détail complet (7 concepts + table détaillée par outil + surfaces) + exemples + ambiguïtés résolues.

### Règles d'Écriture Documentaire

1. **Au premier usage d'un terme produit**, ajouter le terme canonique: "Gemini extension (plugin)", "Mistral connector (external integration backed by MCP)"

2. **Ne jamais confondre** MCP integration et mcp-optimization:  
   ✅ "MCP integration allows connecting external systems"  
   ❌ "Configure your MCP optimization rules" (mcp-optimization = operational discipline, not configuration)

3. **Ne jamais appeler** "skill" un fichier de règles passif  
   ✅ "CLAUDE.md contains instructions"  
   ❌ "CLAUDE.md is a skill"

4. **Ne jamais appeler** "plugin" un serveur MCP  
   ✅ "MCP server for external integration"  
   ❌ "MCP plugin"

5. **Ne jamais appeler** "harness" un connecteur ou plugin  
   ✅ "Claude Code harness provides the execution environment"  
   ❌ "MCP harness"

---
- `sync-agents.sh` **ignore** ce projet (pas de marqueur `<!-- BEGIN:UNIVERSAL -->` attendu)
- N'apparaît **pas** dans les inventaires d'agents (intentionnel)
- Peut avoir ses propres AGENTS.md ou guidelines ISO-spécifiques

**Vérification** : `grep -r "BEGIN:UNIVERSAL" ~/DEV/active/align-ios/` doit retourner vide

---

## Procédure pour Ajouter un Nouveau Projet opt-out

Si un nouveau projet doit être exclu :

1. **Documenter dans cette section** : raison, status, conséquences
2. **Ajouter un commentaire en tête du projet** :
   ```
   # align-ios — ISOLÉ — Exclusion intentionnelle
   # Voir ~/DEV/.AI_AGENTS.md § "Projets opt-out" pour contexte
   ```
3. **Mettre à jour CLAUDE.md** : ajouter un tableau des projets isolés
4. **Vérifier dans le log sync** : `grep -c "SKIP" ~/.sync-agents.log` ne doit contenir **aucune** mention du projet isolé une fois documenté (sinon = oubli)

---

## 13. Glossaire et Nomenclature Canonique

> **Pourquoi ?** Chaque outil (Claude, Gemini, Codex, OpenCode, Vibe, Antigravity) utilise des mots différents pour les mêmes concepts. Cette section stabilise notre vocabulaire interne et crée une table de correspondance par outil.

### Métamodèle Interne (7 Concepts Fondamentaux)

**1. Harness** — L'enveloppe d'exécution agentique (runtime complet qui contient modèle, tools, permissions, contexte, logs)

**2. Instructions Files** — Fichiers de contexte durable (CLAUDE.md, GEMINI.md, AGENTS.md) — mémoire persistante, pas des capacités actives

**3. Skill** — Capacité réutilisable orientée workflow (recette opératoire spécialisée, invocable explicitement)

**4. Plugin** — Package d'extension pouvant contenir skills, hooks, agents, MCP, règles, etc.

**5. MCP Integration** — Protocole standard pour connecter systèmes externes (Model Context Protocol)  
   *Note: MCP integration = "quoi connecter". Voir `~/.claude/rules/mcp-optimization.md` pour "comment l'utiliser efficacement".*

**6. Hooks** — Automatismes événementiels (déclenchés sur événements du lifecycle agentique)

**7. Agents / Subagents** — Instances autonomes avec modèle, tools, permissions, contexte indépendant

### Table Rapide de Correspondance

| Concept | Claude | Gemini | Codex | OpenCode | Vibe |
|---------|--------|--------|-------|----------|------|
| Instructions | CLAUDE.md | GEMINI.md | AGENTS.md | AGENTS.md | config.toml |
| Skill | skill | agent skill | skill | agent skill | skill |
| Plugin | plugin | extension | plugin | plugin | — |
| MCP | MCP server | mcpServers | MCP server | MCP server | mcp_servers |
| Harness | Claude Code | Gemini CLI | Codex | OpenCode | Vibe CLI |

**Voir aussi:** `~/DEV/GLOSSARY.md` pour détail complet (7 concepts + table détaillée par outil + surfaces) + exemples + ambiguïtés résolues.

### Règles d'Écriture Documentaire

1. **Au premier usage d'un terme produit**, ajouter le terme canonique: "Gemini extension (plugin)", "Mistral connector (external integration backed by MCP)"

2. **Ne jamais confondre** MCP integration et mcp-optimization:  
   ✅ "MCP integration allows connecting external systems"  
   ❌ "Configure your MCP optimization rules" (mcp-optimization = operational discipline, not configuration)

3. **Ne jamais appeler** "skill" un fichier de règles passif  
   ✅ "CLAUDE.md contains instructions"  
   ❌ "CLAUDE.md is a skill"

4. **Ne jamais appeler** "plugin" un serveur MCP  
   ✅ "MCP server for external integration"  
   ❌ "MCP plugin"

5. **Ne jamais appeler** "harness" un connecteur ou plugin  
   ✅ "Claude Code harness provides the execution environment"  
   ❌ "MCP harness"

---
- `sync-agents.sh` **ignore** ce projet (pas de marqueur `<!-- BEGIN:UNIVERSAL -->` attendu)
- N'apparaît **pas** dans les inventaires d'agents (intentionnel)
- Peut avoir ses propres AGENTS.md ou guidelines ISO-spécifiques

**Vérification** : `grep -r "BEGIN:UNIVERSAL" ~/DEV/active/align-ios/` doit retourner vide

---

## Procédure pour Ajouter un Nouveau Projet opt-out

Si un nouveau projet doit être exclu :

1. **Documenter dans cette section** : raison, status, conséquences
2. **Ajouter un commentaire en tête du projet** :
   ```
   # align-ios — ISOLÉ — Exclusion intentionnelle
   # Voir ~/DEV/.AI_AGENTS.md § "Projets opt-out" pour contexte
   ```
3. **Mettre à jour CLAUDE.md** : ajouter un tableau des projets isolés
4. **Vérifier dans le log sync** : `grep -c "SKIP" ~/.sync-agents.log` ne doit contenir **aucune** mention du projet isolé une fois documenté (sinon = oubli)

---

## 13. Glossaire et Nomenclature Canonique

> **Pourquoi ?** Chaque outil (Claude, Gemini, Codex, OpenCode, Vibe, Antigravity) utilise des mots différents pour les mêmes concepts. Cette section stabilise notre vocabulaire interne et crée une table de correspondance par outil.

### Métamodèle Interne (7 Concepts Fondamentaux)

**1. Harness** — L'enveloppe d'exécution agentique (runtime complet qui contient modèle, tools, permissions, contexte, logs)

**2. Instructions Files** — Fichiers de contexte durable (CLAUDE.md, GEMINI.md, AGENTS.md) — mémoire persistante, pas des capacités actives

**3. Skill** — Capacité réutilisable orientée workflow (recette opératoire spécialisée, invocable explicitement)

**4. Plugin** — Package d'extension pouvant contenir skills, hooks, agents, MCP, règles, etc.

**5. MCP Integration** — Protocole standard pour connecter systèmes externes (Model Context Protocol)  
   *Note: MCP integration = "quoi connecter". Voir `~/.claude/rules/mcp-optimization.md` pour "comment l'utiliser efficacement".*

**6. Hooks** — Automatismes événementiels (déclenchés sur événements du lifecycle agentique)

**7. Agents / Subagents** — Instances autonomes avec modèle, tools, permissions, contexte indépendant

### Table Rapide de Correspondance

| Concept | Claude | Gemini | Codex | OpenCode | Vibe |
|---------|--------|--------|-------|----------|------|
| Instructions | CLAUDE.md | GEMINI.md | AGENTS.md | AGENTS.md | config.toml |
| Skill | skill | agent skill | skill | agent skill | skill |
| Plugin | plugin | extension | plugin | plugin | — |
| MCP | MCP server | mcpServers | MCP server | MCP server | mcp_servers |
| Harness | Claude Code | Gemini CLI | Codex | OpenCode | Vibe CLI |

**Voir aussi:** `~/DEV/GLOSSARY.md` pour détail complet (7 concepts + table détaillée par outil + surfaces) + exemples + ambiguïtés résolues.

### Règles d'Écriture Documentaire

1. **Au premier usage d'un terme produit**, ajouter le terme canonique: "Gemini extension (plugin)", "Mistral connector (external integration backed by MCP)"

2. **Ne jamais confondre** MCP integration et mcp-optimization:  
   ✅ "MCP integration allows connecting external systems"  
   ❌ "Configure your MCP optimization rules" (mcp-optimization = operational discipline, not configuration)

3. **Ne jamais appeler** "skill" un fichier de règles passif  
   ✅ "CLAUDE.md contains instructions"  
   ❌ "CLAUDE.md is a skill"

4. **Ne jamais appeler** "plugin" un serveur MCP  
   ✅ "MCP server for external integration"  
   ❌ "MCP plugin"

5. **Ne jamais appeler** "harness" un connecteur ou plugin  
   ✅ "Claude Code harness provides the execution environment"  
   ❌ "MCP harness"

---
- `sync-agents.sh` **ignore** ce projet (pas de marqueur `<!-- BEGIN:UNIVERSAL -->` attendu)
- N'apparaît **pas** dans les inventaires d'agents (intentionnel)
- Peut avoir ses propres AGENTS.md ou guidelines ISO-spécifiques

**Vérification** : `grep -r "BEGIN:UNIVERSAL" ~/DEV/active/align-ios/` doit retourner vide

---

## Procédure pour Ajouter un Nouveau Projet opt-out

Si un nouveau projet doit être exclu :

1. **Documenter dans cette section** : raison, status, conséquences
2. **Ajouter un commentaire en tête du projet** :
   ```
   # align-ios — ISOLÉ — Exclusion intentionnelle
   # Voir ~/DEV/.AI_AGENTS.md § "Projets opt-out" pour contexte
   ```
3. **Mettre à jour CLAUDE.md** : ajouter un tableau des projets isolés
4. **Vérifier dans le log sync** : `grep -c "SKIP" ~/.sync-agents.log` ne doit contenir **aucune** mention du projet isolé une fois documenté (sinon = oubli)

---

## 13. Glossaire et Nomenclature Canonique

> **Pourquoi ?** Chaque outil (Claude, Gemini, Codex, OpenCode, Vibe, Antigravity) utilise des mots différents pour les mêmes concepts. Cette section stabilise notre vocabulaire interne et crée une table de correspondance par outil.

### Métamodèle Interne (7 Concepts Fondamentaux)

**1. Harness** — L'enveloppe d'exécution agentique (runtime complet qui contient modèle, tools, permissions, contexte, logs)

**2. Instructions Files** — Fichiers de contexte durable (CLAUDE.md, GEMINI.md, AGENTS.md) — mémoire persistante, pas des capacités actives

**3. Skill** — Capacité réutilisable orientée workflow (recette opératoire spécialisée, invocable explicitement)

**4. Plugin** — Package d'extension pouvant contenir skills, hooks, agents, MCP, règles, etc.

**5. MCP Integration** — Protocole standard pour connecter systèmes externes (Model Context Protocol)  
   *Note: MCP integration = "quoi connecter". Voir `~/.claude/rules/mcp-optimization.md` pour "comment l'utiliser efficacement".*

**6. Hooks** — Automatismes événementiels (déclenchés sur événements du lifecycle agentique)

**7. Agents / Subagents** — Instances autonomes avec modèle, tools, permissions, contexte indépendant

### Table Rapide de Correspondance

| Concept | Claude | Gemini | Codex | OpenCode | Vibe |
|---------|--------|--------|-------|----------|------|
| Instructions | CLAUDE.md | GEMINI.md | AGENTS.md | AGENTS.md | config.toml |
| Skill | skill | agent skill | skill | agent skill | skill |
| Plugin | plugin | extension | plugin | plugin | — |
| MCP | MCP server | mcpServers | MCP server | MCP server | mcp_servers |
| Harness | Claude Code | Gemini CLI | Codex | OpenCode | Vibe CLI |

**Voir aussi:** `~/DEV/GLOSSARY.md` pour détail complet (7 concepts + table détaillée par outil + surfaces) + exemples + ambiguïtés résolues.

### Règles d'Écriture Documentaire

1. **Au premier usage d'un terme produit**, ajouter le terme canonique: "Gemini extension (plugin)", "Mistral connector (external integration backed by MCP)"

2. **Ne jamais confondre** MCP integration et mcp-optimization:  
   ✅ "MCP integration allows connecting external systems"  
   ❌ "Configure your MCP optimization rules" (mcp-optimization = operational discipline, not configuration)

3. **Ne jamais appeler** "skill" un fichier de règles passif  
   ✅ "CLAUDE.md contains instructions"  
   ❌ "CLAUDE.md is a skill"

4. **Ne jamais appeler** "plugin" un serveur MCP  
   ✅ "MCP server for external integration"  
   ❌ "MCP plugin"

5. **Ne jamais appeler** "harness" un connecteur ou plugin  
   ✅ "Claude Code harness provides the execution environment"  
   ❌ "MCP harness"

---
- `sync-agents.sh` **ignore** ce projet (pas de marqueur `<!-- BEGIN:UNIVERSAL -->` attendu)
- N'apparaît **pas** dans les inventaires d'agents (intentionnel)
- Peut avoir ses propres AGENTS.md ou guidelines ISO-spécifiques

**Vérification** : `grep -r "BEGIN:UNIVERSAL" ~/DEV/active/align-ios/` doit retourner vide

---

## Procédure pour Ajouter un Nouveau Projet opt-out

Si un nouveau projet doit être exclu :

1. **Documenter dans cette section** : raison, status, conséquences
2. **Ajouter un commentaire en tête du projet** :
   ```
   # align-ios — ISOLÉ — Exclusion intentionnelle
   # Voir ~/DEV/.AI_AGENTS.md § "Projets opt-out" pour contexte
   ```
3. **Mettre à jour CLAUDE.md** : ajouter un tableau des projets isolés
4. **Vérifier dans le log sync** : `grep -c "SKIP" ~/.sync-agents.log` ne doit contenir **aucune** mention du projet isolé une fois documenté (sinon = oubli)

---

## 13. Glossaire et Nomenclature Canonique

> **Pourquoi ?** Chaque outil (Claude, Gemini, Codex, OpenCode, Vibe, Antigravity) utilise des mots différents pour les mêmes concepts. Cette section stabilise notre vocabulaire interne et crée une table de correspondance par outil.

### Métamodèle Interne (7 Concepts Fondamentaux)

**1. Harness** — L'enveloppe d'exécution agentique (runtime complet qui contient modèle, tools, permissions, contexte, logs)

**2. Instructions Files** — Fichiers de contexte durable (CLAUDE.md, GEMINI.md, AGENTS.md) — mémoire persistante, pas des capacités actives

**3. Skill** — Capacité réutilisable orientée workflow (recette opératoire spécialisée, invocable explicitement)

**4. Plugin** — Package d'extension pouvant contenir skills, hooks, agents, MCP, règles, etc.

**5. MCP Integration** — Protocole standard pour connecter systèmes externes (Model Context Protocol)  
   *Note: MCP integration = "quoi connecter". Voir `~/.claude/rules/mcp-optimization.md` pour "comment l'utiliser efficacement".*

**6. Hooks** — Automatismes événementiels (déclenchés sur événements du lifecycle agentique)

**7. Agents / Subagents** — Instances autonomes avec modèle, tools, permissions, contexte indépendant

### Table Rapide de Correspondance

| Concept | Claude | Gemini | Codex | OpenCode | Vibe |
|---------|--------|--------|-------|----------|------|
| Instructions | CLAUDE.md | GEMINI.md | AGENTS.md | AGENTS.md | config.toml |
| Skill | skill | agent skill | skill | agent skill | skill |
| Plugin | plugin | extension | plugin | plugin | — |
| MCP | MCP server | mcpServers | MCP server | MCP server | mcp_servers |
| Harness | Claude Code | Gemini CLI | Codex | OpenCode | Vibe CLI |

**Voir aussi:** `~/DEV/GLOSSARY.md` pour détail complet (7 concepts + table détaillée par outil + surfaces) + exemples + ambiguïtés résolues.

### Règles d'Écriture Documentaire

1. **Au premier usage d'un terme produit**, ajouter le terme canonique: "Gemini extension (plugin)", "Mistral connector (external integration backed by MCP)"

2. **Ne jamais confondre** MCP integration et mcp-optimization:  
   ✅ "MCP integration allows connecting external systems"  
   ❌ "Configure your MCP optimization rules" (mcp-optimization = operational discipline, not configuration)

3. **Ne jamais appeler** "skill" un fichier de règles passif  
   ✅ "CLAUDE.md contains instructions"  
   ❌ "CLAUDE.md is a skill"

4. **Ne jamais appeler** "plugin" un serveur MCP  
   ✅ "MCP server for external integration"  
   ❌ "MCP plugin"

5. **Ne jamais appeler** "harness" un connecteur ou plugin  
   ✅ "Claude Code harness provides the execution environment"  
   ❌ "MCP harness"

---
- `sync-agents.sh` **ignore** ce projet (pas de marqueur `<!-- BEGIN:UNIVERSAL -->` attendu)
- N'apparaît **pas** dans les inventaires d'agents (intentionnel)
- Peut avoir ses propres AGENTS.md ou guidelines ISO-spécifiques

**Vérification** : `grep -r "BEGIN:UNIVERSAL" ~/DEV/active/align-ios/` doit retourner vide

---

## Procédure pour Ajouter un Nouveau Projet opt-out

Si un nouveau projet doit être exclu :

1. **Documenter dans cette section** : raison, status, conséquences
2. **Ajouter un commentaire en tête du projet** :
   ```
   # align-ios — ISOLÉ — Exclusion intentionnelle
   # Voir ~/DEV/.AI_AGENTS.md § "Projets opt-out" pour contexte
   ```
3. **Mettre à jour CLAUDE.md** : ajouter un tableau des projets isolés
4. **Vérifier dans le log sync** : `grep -c "SKIP" ~/.sync-agents.log` ne doit contenir **aucune** mention du projet isolé une fois documenté (sinon = oubli)

---

## 13. Glossaire et Nomenclature Canonique

> **Pourquoi ?** Chaque outil (Claude, Gemini, Codex, OpenCode, Vibe, Antigravity) utilise des mots différents pour les mêmes concepts. Cette section stabilise notre vocabulaire interne et crée une table de correspondance par outil.

### Métamodèle Interne (7 Concepts Fondamentaux)

**1. Harness** — L'enveloppe d'exécution agentique (runtime complet qui contient modèle, tools, permissions, contexte, logs)

**2. Instructions Files** — Fichiers de contexte durable (CLAUDE.md, GEMINI.md, AGENTS.md) — mémoire persistante, pas des capacités actives

**3. Skill** — Capacité réutilisable orientée workflow (recette opératoire spécialisée, invocable explicitement)

**4. Plugin** — Package d'extension pouvant contenir skills, hooks, agents, MCP, règles, etc.

**5. MCP Integration** — Protocole standard pour connecter systèmes externes (Model Context Protocol)  
   *Note: MCP integration = "quoi connecter". Voir `~/.claude/rules/mcp-optimization.md` pour "comment l'utiliser efficacement".*

**6. Hooks** — Automatismes événementiels (déclenchés sur événements du lifecycle agentique)

**7. Agents / Subagents** — Instances autonomes avec modèle, tools, permissions, contexte indépendant

### Table Rapide de Correspondance

| Concept | Claude | Gemini | Codex | OpenCode | Vibe |
|---------|--------|--------|-------|----------|------|
| Instructions | CLAUDE.md | GEMINI.md | AGENTS.md | AGENTS.md | config.toml |
| Skill | skill | agent skill | skill | agent skill | skill |
| Plugin | plugin | extension | plugin | plugin | — |
| MCP | MCP server | mcpServers | MCP server | MCP server | mcp_servers |
| Harness | Claude Code | Gemini CLI | Codex | OpenCode | Vibe CLI |

**Voir aussi:** `~/DEV/GLOSSARY.md` pour détail complet (7 concepts + table détaillée par outil + surfaces) + exemples + ambiguïtés résolues.

### Règles d'Écriture Documentaire

1. **Au premier usage d'un terme produit**, ajouter le terme canonique: "Gemini extension (plugin)", "Mistral connector (external integration backed by MCP)"

2. **Ne jamais confondre** MCP integration et mcp-optimization:  
   ✅ "MCP integration allows connecting external systems"  
   ❌ "Configure your MCP optimization rules" (mcp-optimization = operational discipline, not configuration)

3. **Ne jamais appeler** "skill" un fichier de règles passif  
   ✅ "CLAUDE.md contains instructions"  
   ❌ "CLAUDE.md is a skill"

4. **Ne jamais appeler** "plugin" un serveur MCP  
   ✅ "MCP server for external integration"  
   ❌ "MCP plugin"

5. **Ne jamais appeler** "harness" un connecteur ou plugin  
   ✅ "Claude Code harness provides the execution environment"  
   ❌ "MCP harness"

---
- `sync-agents.sh` **ignore** ce projet (pas de marqueur `<!-- BEGIN:UNIVERSAL -->` attendu)
- N'apparaît **pas** dans les inventaires d'agents (intentionnel)
- Peut avoir ses propres AGENTS.md ou guidelines ISO-spécifiques

**Vérification** : `grep -r "BEGIN:UNIVERSAL" ~/DEV/active/align-ios/` doit retourner vide

---

## Procédure pour Ajouter un Nouveau Projet opt-out

Si un nouveau projet doit être exclu :

1. **Documenter dans cette section** : raison, status, conséquences
2. **Ajouter un commentaire en tête du projet** :
   ```
   # align-ios — ISOLÉ — Exclusion intentionnelle
   # Voir ~/DEV/.AI_AGENTS.md § "Projets opt-out" pour contexte
   ```
3. **Mettre à jour CLAUDE.md** : ajouter un tableau des projets isolés
4. **Vérifier dans le log sync** : `grep -c "SKIP" ~/.sync-agents.log` ne doit contenir **aucune** mention du projet isolé une fois documenté (sinon = oubli)

---

## 13. Glossaire et Nomenclature Canonique

> **Pourquoi ?** Chaque outil (Claude, Gemini, Codex, OpenCode, Vibe, Antigravity) utilise des mots différents pour les mêmes concepts. Cette section stabilise notre vocabulaire interne et crée une table de correspondance par outil.

### Métamodèle Interne (7 Concepts Fondamentaux)

**1. Harness** — L'enveloppe d'exécution agentique (runtime complet qui contient modèle, tools, permissions, contexte, logs)

**2. Instructions Files** — Fichiers de contexte durable (CLAUDE.md, GEMINI.md, AGENTS.md) — mémoire persistante, pas des capacités actives

**3. Skill** — Capacité réutilisable orientée workflow (recette opératoire spécialisée, invocable explicitement)

**4. Plugin** — Package d'extension pouvant contenir skills, hooks, agents, MCP, règles, etc.

**5. MCP Integration** — Protocole standard pour connecter systèmes externes (Model Context Protocol)  
   *Note: MCP integration = "quoi connecter". Voir `~/.claude/rules/mcp-optimization.md` pour "comment l'utiliser efficacement".*

**6. Hooks** — Automatismes événementiels (déclenchés sur événements du lifecycle agentique)

**7. Agents / Subagents** — Instances autonomes avec modèle, tools, permissions, contexte indépendant

### Table Rapide de Correspondance

| Concept | Claude | Gemini | Codex | OpenCode | Vibe |
|---------|--------|--------|-------|----------|------|
| Instructions | CLAUDE.md | GEMINI.md | AGENTS.md | AGENTS.md | config.toml |
| Skill | skill | agent skill | skill | agent skill | skill |
| Plugin | plugin | extension | plugin | plugin | — |
| MCP | MCP server | mcpServers | MCP server | MCP server | mcp_servers |
| Harness | Claude Code | Gemini CLI | Codex | OpenCode | Vibe CLI |

**Voir aussi:** `~/DEV/GLOSSARY.md` pour détail complet (7 concepts + table détaillée par outil + surfaces) + exemples + ambiguïtés résolues.

### Règles d'Écriture Documentaire

1. **Au premier usage d'un terme produit**, ajouter le terme canonique: "Gemini extension (plugin)", "Mistral connector (external integration backed by MCP)"

2. **Ne jamais confondre** MCP integration et mcp-optimization:  
   ✅ "MCP integration allows connecting external systems"  
   ❌ "Configure your MCP optimization rules" (mcp-optimization = operational discipline, not configuration)

3. **Ne jamais appeler** "skill" un fichier de règles passif  
   ✅ "CLAUDE.md contains instructions"  
   ❌ "CLAUDE.md is a skill"

4. **Ne jamais appeler** "plugin" un serveur MCP  
   ✅ "MCP server for external integration"  
   ❌ "MCP plugin"

5. **Ne jamais appeler** "harness" un connecteur ou plugin  
   ✅ "Claude Code harness provides the execution environment"  
   ❌ "MCP harness"

---
- `sync-agents.sh` **ignore** ce projet (pas de marqueur `<!-- BEGIN:UNIVERSAL -->` attendu)
- N'apparaît **pas** dans les inventaires d'agents (intentionnel)
- Peut avoir ses propres AGENTS.md ou guidelines ISO-spécifiques

**Vérification** : `grep -r "BEGIN:UNIVERSAL" ~/DEV/active/align-ios/` doit retourner vide

---

## Procédure pour Ajouter un Nouveau Projet opt-out

Si un nouveau projet doit être exclu :

1. **Documenter dans cette section** : raison, status, conséquences
2. **Ajouter un commentaire en tête du projet** :
   ```
   # align-ios — ISOLÉ — Exclusion intentionnelle
   # Voir ~/DEV/.AI_AGENTS.md § "Projets opt-out" pour contexte
   ```
3. **Mettre à jour CLAUDE.md** : ajouter un tableau des projets isolés
4. **Vérifier dans le log sync** : `grep -c "SKIP" ~/.sync-agents.log` ne doit contenir **aucune** mention du projet isolé une fois documenté (sinon = oubli)

---

## 13. Glossaire et Nomenclature Canonique

> **Pourquoi ?** Chaque outil (Claude, Gemini, Codex, OpenCode, Vibe, Antigravity) utilise des mots différents pour les mêmes concepts. Cette section stabilise notre vocabulaire interne et crée une table de correspondance par outil.

### Métamodèle Interne (7 Concepts Fondamentaux)

**1. Harness** — L'enveloppe d'exécution agentique (runtime complet qui contient modèle, tools, permissions, contexte, logs)

**2. Instructions Files** — Fichiers de contexte durable (CLAUDE.md, GEMINI.md, AGENTS.md) — mémoire persistante, pas des capacités actives

**3. Skill** — Capacité réutilisable orientée workflow (recette opératoire spécialisée, invocable explicitement)

**4. Plugin** — Package d'extension pouvant contenir skills, hooks, agents, MCP, règles, etc.

**5. MCP Integration** — Protocole standard pour connecter systèmes externes (Model Context Protocol)  
   *Note: MCP integration = "quoi connecter". Voir `~/.claude/rules/mcp-optimization.md` pour "comment l'utiliser efficacement".*

**6. Hooks** — Automatismes événementiels (déclenchés sur événements du lifecycle agentique)

**7. Agents / Subagents** — Instances autonomes avec modèle, tools, permissions, contexte indépendant

### Table Rapide de Correspondance

| Concept | Claude | Gemini | Codex | OpenCode | Vibe |
|---------|--------|--------|-------|----------|------|
| Instructions | CLAUDE.md | GEMINI.md | AGENTS.md | AGENTS.md | config.toml |
| Skill | skill | agent skill | skill | agent skill | skill |
| Plugin | plugin | extension | plugin | plugin | — |
| MCP | MCP server | mcpServers | MCP server | MCP server | mcp_servers |
| Harness | Claude Code | Gemini CLI | Codex | OpenCode | Vibe CLI |

**Voir aussi:** `~/DEV/GLOSSARY.md` pour détail complet (7 concepts + table détaillée par outil + surfaces) + exemples + ambiguïtés résolues.

### Règles d'Écriture Documentaire

1. **Au premier usage d'un terme produit**, ajouter le terme canonique: "Gemini extension (plugin)", "Mistral connector (external integration backed by MCP)"

2. **Ne jamais confondre** MCP integration et mcp-optimization:  
   ✅ "MCP integration allows connecting external systems"  
   ❌ "Configure your MCP optimization rules" (mcp-optimization = operational discipline, not configuration)

3. **Ne jamais appeler** "skill" un fichier de règles passif  
   ✅ "CLAUDE.md contains instructions"  
   ❌ "CLAUDE.md is a skill"

4. **Ne jamais appeler** "plugin" un serveur MCP  
   ✅ "MCP server for external integration"  
   ❌ "MCP plugin"

5. **Ne jamais appeler** "harness" un connecteur ou plugin  
   ✅ "Claude Code harness provides the execution environment"  
   ❌ "MCP harness"

---
- `sync-agents.sh` **ignore** ce projet (pas de marqueur `<!-- BEGIN:UNIVERSAL -->` attendu)
- N'apparaît **pas** dans les inventaires d'agents (intentionnel)
- Peut avoir ses propres AGENTS.md ou guidelines ISO-spécifiques

**Vérification** : `grep -r "BEGIN:UNIVERSAL" ~/DEV/active/align-ios/` doit retourner vide

---

## Procédure pour Ajouter un Nouveau Projet opt-out

Si un nouveau projet doit être exclu :

1. **Documenter dans cette section** : raison, status, conséquences
2. **Ajouter un commentaire en tête du projet** :
   ```
   # align-ios — ISOLÉ — Exclusion intentionnelle
   # Voir ~/DEV/.AI_AGENTS.md § "Projets opt-out" pour contexte
   ```
3. **Mettre à jour CLAUDE.md** : ajouter un tableau des projets isolés
4. **Vérifier dans le log sync** : `grep -c "SKIP" ~/.sync-agents.log` ne doit contenir **aucune** mention du projet isolé une fois documenté (sinon = oubli)

---

## 13. Glossaire et Nomenclature Canonique

> **Pourquoi ?** Chaque outil (Claude, Gemini, Codex, OpenCode, Vibe, Antigravity) utilise des mots différents pour les mêmes concepts. Cette section stabilise notre vocabulaire interne et crée une table de correspondance par outil.

### Métamodèle Interne (7 Concepts Fondamentaux)

**1. Harness** — L'enveloppe d'exécution agentique (runtime complet qui contient modèle, tools, permissions, contexte, logs)

**2. Instructions Files** — Fichiers de contexte durable (CLAUDE.md, GEMINI.md, AGENTS.md) — mémoire persistante, pas des capacités actives

**3. Skill** — Capacité réutilisable orientée workflow (recette opératoire spécialisée, invocable explicitement)

**4. Plugin** — Package d'extension pouvant contenir skills, hooks, agents, MCP, règles, etc.

**5. MCP Integration** — Protocole standard pour connecter systèmes externes (Model Context Protocol)  
   *Note: MCP integration = "quoi connecter". Voir `~/.claude/rules/mcp-optimization.md` pour "comment l'utiliser efficacement".*

**6. Hooks** — Automatismes événementiels (déclenchés sur événements du lifecycle agentique)

**7. Agents / Subagents** — Instances autonomes avec modèle, tools, permissions, contexte indépendant

### Table Rapide de Correspondance

| Concept | Claude | Gemini | Codex | OpenCode | Vibe |
|---------|--------|--------|-------|----------|------|
| Instructions | CLAUDE.md | GEMINI.md | AGENTS.md | AGENTS.md | config.toml |
| Skill | skill | agent skill | skill | agent skill | skill |
| Plugin | plugin | extension | plugin | plugin | — |
| MCP | MCP server | mcpServers | MCP server | MCP server | mcp_servers |
| Harness | Claude Code | Gemini CLI | Codex | OpenCode | Vibe CLI |

**Voir aussi:** `~/DEV/GLOSSARY.md` pour détail complet (7 concepts + table détaillée par outil + surfaces) + exemples + ambiguïtés résolues.

### Règles d'Écriture Documentaire

1. **Au premier usage d'un terme produit**, ajouter le terme canonique: "Gemini extension (plugin)", "Mistral connector (external integration backed by MCP)"

2. **Ne jamais confondre** MCP integration et mcp-optimization:  
   ✅ "MCP integration allows connecting external systems"  
   ❌ "Configure your MCP optimization rules" (mcp-optimization = operational discipline, not configuration)

3. **Ne jamais appeler** "skill" un fichier de règles passif  
   ✅ "CLAUDE.md contains instructions"  
   ❌ "CLAUDE.md is a skill"

4. **Ne jamais appeler** "plugin" un serveur MCP  
   ✅ "MCP server for external integration"  
   ❌ "MCP plugin"

5. **Ne jamais appeler** "harness" un connecteur ou plugin  
   ✅ "Claude Code harness provides the execution environment"  
   ❌ "MCP harness"

---
- `sync-agents.sh` **ignore** ce projet (pas de marqueur `<!-- BEGIN:UNIVERSAL -->` attendu)
- N'apparaît **pas** dans les inventaires d'agents (intentionnel)
- Peut avoir ses propres AGENTS.md ou guidelines ISO-spécifiques

**Vérification** : `grep -r "BEGIN:UNIVERSAL" ~/DEV/active/align-ios/` doit retourner vide

---

## Procédure pour Ajouter un Nouveau Projet opt-out

Si un nouveau projet doit être exclu :

1. **Documenter dans cette section** : raison, status, conséquences
2. **Ajouter un commentaire en tête du projet** :
   ```
   # align-ios — ISOLÉ — Exclusion intentionnelle
   # Voir ~/DEV/.AI_AGENTS.md § "Projets opt-out" pour contexte
   ```
3. **Mettre à jour CLAUDE.md** : ajouter un tableau des projets isolés
4. **Vérifier dans le log sync** : `grep -c "SKIP" ~/.sync-agents.log` ne doit contenir **aucune** mention du projet isolé une fois documenté (sinon = oubli)

---

## 13. Glossaire et Nomenclature Canonique

> **Pourquoi ?** Chaque outil (Claude, Gemini, Codex, OpenCode, Vibe, Antigravity) utilise des mots différents pour les mêmes concepts. Cette section stabilise notre vocabulaire interne et crée une table de correspondance par outil.

### Métamodèle Interne (7 Concepts Fondamentaux)

**1. Harness** — L'enveloppe d'exécution agentique (runtime complet qui contient modèle, tools, permissions, contexte, logs)

**2. Instructions Files** — Fichiers de contexte durable (CLAUDE.md, GEMINI.md, AGENTS.md) — mémoire persistante, pas des capacités actives

**3. Skill** — Capacité réutilisable orientée workflow (recette opératoire spécialisée, invocable explicitement)

**4. Plugin** — Package d'extension pouvant contenir skills, hooks, agents, MCP, règles, etc.

**5. MCP Integration** — Protocole standard pour connecter systèmes externes (Model Context Protocol)  
   *Note: MCP integration = "quoi connecter". Voir `~/.claude/rules/mcp-optimization.md` pour "comment l'utiliser efficacement".*

**6. Hooks** — Automatismes événementiels (déclenchés sur événements du lifecycle agentique)

**7. Agents / Subagents** — Instances autonomes avec modèle, tools, permissions, contexte indépendant

### Table Rapide de Correspondance

| Concept | Claude | Gemini | Codex | OpenCode | Vibe |
|---------|--------|--------|-------|----------|------|
| Instructions | CLAUDE.md | GEMINI.md | AGENTS.md | AGENTS.md | config.toml |
| Skill | skill | agent skill | skill | agent skill | skill |
| Plugin | plugin | extension | plugin | plugin | — |
| MCP | MCP server | mcpServers | MCP server | MCP server | mcp_servers |
| Harness | Claude Code | Gemini CLI | Codex | OpenCode | Vibe CLI |

**Voir aussi:** `~/DEV/GLOSSARY.md` pour détail complet (7 concepts + table détaillée par outil + surfaces) + exemples + ambiguïtés résolues.

### Règles d'Écriture Documentaire

1. **Au premier usage d'un terme produit**, ajouter le terme canonique: "Gemini extension (plugin)", "Mistral connector (external integration backed by MCP)"

2. **Ne jamais confondre** MCP integration et mcp-optimization:  
   ✅ "MCP integration allows connecting external systems"  
   ❌ "Configure your MCP optimization rules" (mcp-optimization = operational discipline, not configuration)

3. **Ne jamais appeler** "skill" un fichier de règles passif  
   ✅ "CLAUDE.md contains instructions"  
   ❌ "CLAUDE.md is a skill"

4. **Ne jamais appeler** "plugin" un serveur MCP  
   ✅ "MCP server for external integration"  
   ❌ "MCP plugin"

5. **Ne jamais appeler** "harness" un connecteur ou plugin  
   ✅ "Claude Code harness provides the execution environment"  
   ❌ "MCP harness"

---
- `sync-agents.sh` **ignore** ce projet (pas de marqueur `<!-- BEGIN:UNIVERSAL -->` attendu)
- N'apparaît **pas** dans les inventaires d'agents (intentionnel)
- Peut avoir ses propres AGENTS.md ou guidelines ISO-spécifiques

**Vérification** : `grep -r "BEGIN:UNIVERSAL" ~/DEV/active/align-ios/` doit retourner vide

---

## Procédure pour Ajouter un Nouveau Projet opt-out

Si un nouveau projet doit être exclu :

1. **Documenter dans cette section** : raison, status, conséquences
2. **Ajouter un commentaire en tête du projet** :
   ```
   # align-ios — ISOLÉ — Exclusion intentionnelle
   # Voir ~/DEV/.AI_AGENTS.md § "Projets opt-out" pour contexte
   ```
3. **Mettre à jour CLAUDE.md** : ajouter un tableau des projets isolés
4. **Vérifier dans le log sync** : `grep -c "SKIP" ~/.sync-agents.log` ne doit contenir **aucune** mention du projet isolé une fois documenté (sinon = oubli)

---

## 13. Glossaire et Nomenclature Canonique

> **Pourquoi ?** Chaque outil (Claude, Gemini, Codex, OpenCode, Vibe, Antigravity) utilise des mots différents pour les mêmes concepts. Cette section stabilise notre vocabulaire interne et crée une table de correspondance par outil.

### Métamodèle Interne (7 Concepts Fondamentaux)

**1. Harness** — L'enveloppe d'exécution agentique (runtime complet qui contient modèle, tools, permissions, contexte, logs)

**2. Instructions Files** — Fichiers de contexte durable (CLAUDE.md, GEMINI.md, AGENTS.md) — mémoire persistante, pas des capacités actives

**3. Skill** — Capacité réutilisable orientée workflow (recette opératoire spécialisée, invocable explicitement)

**4. Plugin** — Package d'extension pouvant contenir skills, hooks, agents, MCP, règles, etc.

**5. MCP Integration** — Protocole standard pour connecter systèmes externes (Model Context Protocol)  
   *Note: MCP integration = "quoi connecter". Voir `~/.claude/rules/mcp-optimization.md` pour "comment l'utiliser efficacement".*

**6. Hooks** — Automatismes événementiels (déclenchés sur événements du lifecycle agentique)

**7. Agents / Subagents** — Instances autonomes avec modèle, tools, permissions, contexte indépendant

### Table Rapide de Correspondance

| Concept | Claude | Gemini | Codex | OpenCode | Vibe |
|---------|--------|--------|-------|----------|------|
| Instructions | CLAUDE.md | GEMINI.md | AGENTS.md | AGENTS.md | config.toml |
| Skill | skill | agent skill | skill | agent skill | skill |
| Plugin | plugin | extension | plugin | plugin | — |
| MCP | MCP server | mcpServers | MCP server | MCP server | mcp_servers |
| Harness | Claude Code | Gemini CLI | Codex | OpenCode | Vibe CLI |

**Voir aussi:** `~/DEV/GLOSSARY.md` pour détail complet (7 concepts + table détaillée par outil + surfaces) + exemples + ambiguïtés résolues.

### Règles d'Écriture Documentaire

1. **Au premier usage d'un terme produit**, ajouter le terme canonique: "Gemini extension (plugin)", "Mistral connector (external integration backed by MCP)"

2. **Ne jamais confondre** MCP integration et mcp-optimization:  
   ✅ "MCP integration allows connecting external systems"  
   ❌ "Configure your MCP optimization rules" (mcp-optimization = operational discipline, not configuration)

3. **Ne jamais appeler** "skill" un fichier de règles passif  
   ✅ "CLAUDE.md contains instructions"  
   ❌ "CLAUDE.md is a skill"

4. **Ne jamais appeler** "plugin" un serveur MCP  
   ✅ "MCP server for external integration"  
   ❌ "MCP plugin"

5. **Ne jamais appeler** "harness" un connecteur ou plugin  
   ✅ "Claude Code harness provides the execution environment"  
   ❌ "MCP harness"

---
- `sync-agents.sh` **ignore** ce projet (pas de marqueur `<!-- BEGIN:UNIVERSAL -->` attendu)
- N'apparaît **pas** dans les inventaires d'agents (intentionnel)
- Peut avoir ses propres AGENTS.md ou guidelines ISO-spécifiques

**Vérification** : `grep -r "BEGIN:UNIVERSAL" ~/DEV/active/align-ios/` doit retourner vide

---

## Procédure pour Ajouter un Nouveau Projet opt-out

Si un nouveau projet doit être exclu :

1. **Documenter dans cette section** : raison, status, conséquences
2. **Ajouter un commentaire en tête du projet** :
   ```
   # align-ios — ISOLÉ — Exclusion intentionnelle
   # Voir ~/DEV/.AI_AGENTS.md § "Projets opt-out" pour contexte
   ```
3. **Mettre à jour CLAUDE.md** : ajouter un tableau des projets isolés
4. **Vérifier dans le log sync** : `grep -c "SKIP" ~/.sync-agents.log` ne doit contenir **aucune** mention du projet isolé une fois documenté (sinon = oubli)

---

## 13. Glossaire et Nomenclature Canonique

> **Pourquoi ?** Chaque outil (Claude, Gemini, Codex, OpenCode, Vibe, Antigravity) utilise des mots différents pour les mêmes concepts. Cette section stabilise notre vocabulaire interne et crée une table de correspondance par outil.

### Métamodèle Interne (7 Concepts Fondamentaux)

**1. Harness** — L'enveloppe d'exécution agentique (runtime complet qui contient modèle, tools, permissions, contexte, logs)

**2. Instructions Files** — Fichiers de contexte durable (CLAUDE.md, GEMINI.md, AGENTS.md) — mémoire persistante, pas des capacités actives

**3. Skill** — Capacité réutilisable orientée workflow (recette opératoire spécialisée, invocable explicitement)

**4. Plugin** — Package d'extension pouvant contenir skills, hooks, agents, MCP, règles, etc.

**5. MCP Integration** — Protocole standard pour connecter systèmes externes (Model Context Protocol)  
   *Note: MCP integration = "quoi connecter". Voir `~/.claude/rules/mcp-optimization.md` pour "comment l'utiliser efficacement".*

**6. Hooks** — Automatismes événementiels (déclenchés sur événements du lifecycle agentique)

**7. Agents / Subagents** — Instances autonomes avec modèle, tools, permissions, contexte indépendant

### Table Rapide de Correspondance

| Concept | Claude | Gemini | Codex | OpenCode | Vibe |
|---------|--------|--------|-------|----------|------|
| Instructions | CLAUDE.md | GEMINI.md | AGENTS.md | AGENTS.md | config.toml |
| Skill | skill | agent skill | skill | agent skill | skill |
| Plugin | plugin | extension | plugin | plugin | — |
| MCP | MCP server | mcpServers | MCP server | MCP server | mcp_servers |
| Harness | Claude Code | Gemini CLI | Codex | OpenCode | Vibe CLI |

**Voir aussi:** `~/DEV/GLOSSARY.md` pour détail complet (7 concepts + table détaillée par outil + surfaces) + exemples + ambiguïtés résolues.

### Règles d'Écriture Documentaire

1. **Au premier usage d'un terme produit**, ajouter le terme canonique: "Gemini extension (plugin)", "Mistral connector (external integration backed by MCP)"

2. **Ne jamais confondre** MCP integration et mcp-optimization:  
   ✅ "MCP integration allows connecting external systems"  
   ❌ "Configure your MCP optimization rules" (mcp-optimization = operational discipline, not configuration)

3. **Ne jamais appeler** "skill" un fichier de règles passif  
   ✅ "CLAUDE.md contains instructions"  
   ❌ "CLAUDE.md is a skill"

4. **Ne jamais appeler** "plugin" un serveur MCP  
   ✅ "MCP server for external integration"  
   ❌ "MCP plugin"

5. **Ne jamais appeler** "harness" un connecteur ou plugin  
   ✅ "Claude Code harness provides the execution environment"  
   ❌ "MCP harness"

---
- `sync-agents.sh` **ignore** ce projet (pas de marqueur `<!-- BEGIN:UNIVERSAL -->` attendu)
- N'apparaît **pas** dans les inventaires d'agents (intentionnel)
- Peut avoir ses propres AGENTS.md ou guidelines ISO-spécifiques

**Vérification** : `grep -r "BEGIN:UNIVERSAL" ~/DEV/active/align-ios/` doit retourner vide

---

## Procédure pour Ajouter un Nouveau Projet opt-out

Si un nouveau projet doit être exclu :

1. **Documenter dans cette section** : raison, status, conséquences
2. **Ajouter un commentaire en tête du projet** :
   ```
   # align-ios — ISOLÉ — Exclusion intentionnelle
   # Voir ~/DEV/.AI_AGENTS.md § "Projets opt-out" pour contexte
   ```
3. **Mettre à jour CLAUDE.md** : ajouter un tableau des projets isolés
4. **Vérifier dans le log sync** : `grep -c "SKIP" ~/.sync-agents.log` ne doit contenir **aucune** mention du projet isolé une fois documenté (sinon = oubli)

---

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
