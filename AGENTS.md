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

### 2.3bis Discipline des fichiers d'etat

- `STATE.md` decrit l'etat fonctionnel et le dernier controle connu ; il ne doit pas pretendre etre le registre exact du commit courant.
- Git reste la source de verite pour les SHA, l'alignement exact local/distant et l'historique.
- Eviter les formulations fragiles du type "`main` et `origin/main` sont alignes au commit X" comme verite durable, car le commit qui modifie `STATE.md` rend cette phrase obsolete.
- Preferer documenter une "derniere verification distante" datee, le resultat fonctionnel observe, et les commandes permettant de verifier l'etat exact (`git status --short --branch`, `git rev-parse HEAD`, `git rev-parse origin/main`).
- Apres commit/push, verifier Git directement plutot que modifier `STATE.md` uniquement pour actualiser un SHA.

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

## 7bis. CI/CD — GitHub Actions

> Filet de sécurité : à chaque push/PR, un runner neutre compile + lint + teste. Attrape ce que le poste local masque (ex. dérive de toolchain).

Fichier `.github/workflows/ci.yml` : un job par stack, `runs-on: ubuntu-latest` (Linux ×1 ; **jamais macOS ×10** sauf iOS). Toujours `actions/cache` (coût + vitesse) et actions épinglées (`@v4`). `permissions: { contents: read }`.

| Stack | Gate CI |
|-------|---------|
| Rust/Tauri | `cargo clippy --all-targets -- -D warnings` + `cargo test` (apt : `libgtk-3-dev libwebkit2gtk-4.1-dev libayatana-appindicator3-dev librsvg2-dev`) |
| Node/Svelte | `pnpm check` + `pnpm test:unit` |
| Python | `ruff check` + `pytest` |
| iOS/Swift | `xcodebuild test` (runner macOS, ×10) |

**Pièges vécus** :
- `@stable` installe le dernier toolchain → un nouveau lint peut rougir du code valide. Corriger ponctuellement, ou épingler la version pour reproductibilité.
- `cargo fmt --check` : à n'ajouter que si le repo est déjà 100 % fmt-clean (sinon échec global).

**Coût** : repo privé = 2000 min/mois offertes (Free), public = illimité. **Rendre bloquant** : branch protection sur `main` → *Require status checks*.

---

## 7ter. Supply-Chain Security — Vérifications Périodiques

> Cadence : **mensuelle** (ou ad-hoc si une CVE majeure est annoncée).  
> Objectif : détecter les packages vulnérables, dépendances compromises et extensions dangereuses **avant** qu'elles n'atteignent la production.  
> Philosophie : deux niveaux complémentaires — **inventaire** (Bumblebee, read-only, sans réseau) + **lookup CVE** (outils natifs, en ligne).

### Niveau 1 — Inventaire Global (Bumblebee)

Bumblebee scanne **tous les projets de `~/DEV/`** en read-only (pas d'exécution de packages).  
Binary : `~/go/bin/bumblebee` (v0.1.1+). Résultats : `~/DEV/99-HORS\ SCOPE/bumblebee-scans/`.

# Scan complet — 3 profils (à lancer depuis n'importe où)
SCAN_DIR=~/DEV/99-HORS\ SCOPE/bumblebee-scans
bumblebee scan --profile baseline --root ~/DEV --output file --output-file "$SCAN_DIR/baseline.ndjson"
bumblebee scan --profile project  --root ~/DEV --output file --output-file "$SCAN_DIR/project.ndjson"
bumblebee scan --profile deep     --root ~/DEV --output file --output-file "$SCAN_DIR/deep.ndjson"

# Interroger les résultats (exemples)
jq -r 'select(.record_type=="package" and .has_lifecycle_scripts==true) | .package_name' "$SCAN_DIR/baseline.ndjson" | sort -u

| Profil | Scope | Cas d'usage |
|--------|-------|-------------|
| `baseline` | Répertoires racine connus (pnpm, npm, pip…) | Monitoring mensuel standard |
| `project` | Lockfiles et manifests de projets | Vérification ciblée post-ajout de dépendance |
| `deep` | Tous les répertoires accessibles | Incident response si CVE critique annoncée |

### Niveau 2 — Lookup CVE par Écosystème (outils natifs)

Ces outils consultent des bases CVE en ligne et **complètent** Bumblebee (qui est inventory-only sans catalog).

| Écosystème | Outil | Commande |
|------------|-------|----------|
| npm / pnpm | `pnpm audit` | `cd <projet> && pnpm audit --audit-level moderate` |
| npm (fallback) | `npm audit` | `cd <projet> && npm audit --audit-level moderate` |
| Python (pip) | `pip-audit` | `pip-audit -r requirements.txt` |
| Python (conda) | `pip-audit` | `pip-audit --require-hashes -r requirements.txt` |
| Go | `govulncheck` | `cd <projet> && govulncheck ./...` |
| Multi-écosystèmes | `osv-scanner` | `osv-scanner --recursive ~/DEV` |

> **Installation one-shot** des outils manquants :
> ```bash
> pip install pip-audit          # Python
> go install golang.org/x/vuln/cmd/govulncheck@latest  # Go
> # osv-scanner : https://github.com/google/osv-scanner/releases
> ```

### Procédure Mensuelle (checklist agent)

Quand un agent est chargé du scan mensuel supply-chain :

1. [ ] Lancer les 3 profils Bumblebee sur `~/DEV/` (commandes ci-dessus)
2. [ ] Pour chaque projet Node.js actif : `pnpm audit --audit-level moderate`
3. [ ] Pour chaque projet Python actif : `pip-audit -r requirements.txt`
4. [ ] Pour chaque projet Go actif : `govulncheck ./...`
5. [ ] Stocker les résultats dans `~/DEV/99-HORS\ SCOPE/bumblebee-scans/YYYY-MM/`
6. [ ] Mettre à jour le rapport HTML + `SCAN_SUMMARY.md`
7. [ ] Si **findings > 0** : escalader à l'humain immédiatement (ne pas patcher sans accord)

### Règles de Conduite

- **Ne jamais patcher automatiquement** une dépendance vulnérable sans confirmation humaine
- **Toujours archiver** les fichiers NDJSON bruts (preuve d'audit, comparaison future)
- **En cas de CVE critique** (CVSS ≥ 9.0) annoncée publiquement → lancer un scan `deep` ad-hoc immédiatement
- **Lifecycle scripts suspects** (`has_lifecycle_scripts: true`) → signaler à l'humain pour revue manuelle

---

## 7quater. Ponytail — Minimisation de Code (Lazy Senior Dev)

> Objectif : tous les agents IA écrivent du code **minimal et nécessaire** (YAGNI, stdlib d'abord, pas d'abstraction non demandée).
> Philosophie : « le meilleur code est celui qu'on n'écrit pas ». Installé en **plugin** sur chaque agent ; le ruleset s'injecte automatiquement à chaque session.
> Repo : `DietrichGebert/ponytail` — version **4.7.0** — mode par défaut `full`.

### État d'installation (vérifié 2026-06-19)

| Agent | Méthode | Vérification |
|-------|---------|--------------|
| Claude Code | `claude plugin` (marketplace) | `claude plugin list \| grep ponytail` → `enabled` |
| Codex | `codex plugin` (marketplace) | `codex plugin list \| grep ponytail` → `installed, enabled` |
| Gemini CLI | `gemini extensions install` | `gemini extensions list \| grep ponytail` → `4.7.0` |
| Antigravity (`agy`) | `agy plugin import gemini` | `agy plugin list` → import `ponytail` |
| OpenCode | entrée `plugin` dans `~/.config/opencode/opencode.json` | tableau `plugin` contient `opencode-ponytail` |

> ⚠️ **Piège (vérifié)** : installer/activer un plugin ne prend effet qu'au **redémarrage complet** de l'agent. Les sessions enfant / `--print` héritent du snapshot figé au lancement.
> ⚠️ **Syntaxe Claude Code** : `claude plugin …` (CLI, sans slash). `claude /plugin …` (avec slash) n'existe qu'en session interactive.

### Commandes (toutes plateformes)

| Skill / commande | Effet |
|------------------|-------|
| `/ponytail [lite\|full\|ultra\|off]` | Afficher / changer le niveau de minimisation |
| `/ponytail-review` | Revue du diff courant : ce qui est sur-conçu, à supprimer |
| `/ponytail-audit` | Audit sur-ingénierie de tout le repo |
| `/ponytail-debt` | Récolte les commentaires `ponytail:` (dette/raccourcis assumés) |
| `/ponytail-gain` | Impact mesuré (code %, coût %, vitesse %) |
| `/ponytail-help` | Aide complète |

### Installation & validation

Procédure détaillée + étapes de validation manuelle par agent :
**`~/DEV/docs/superpowers/plans/2026-06-19-ponytail-multiagent-setup.md`**

### Règles de Conduite

- **Convention de code** : marquer une simplification délibérée par un commentaire `ponytail:` (ex. `// ponytail: global lock, per-account si besoin de débit`) — signale l'intention, pas l'ignorance.
- **Désactivation** : seulement si une tâche l'exige (ex. prototype volontairement sur-équipé) → `/ponytail off`, justifier dans le message de commit, réactiver après.
- **La sécurité n'est jamais coupée** : validation, gestion d'erreurs, garde-fous restent intacts (ponytail réduit le superflu, pas la robustesse).

---

## 8. Workflow Multi-Agents CLI

> Ce systeme repose sur 6 agents CLI : Claude Code, Gemini CLI, Codex CLI, Vibe (Mistral), OpenCode, Antigravity (AGY).
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

- [2026-06-24] [RTK] : RTK (0.42.4) n'a de hook PreToolUse automatique que pour Claude Code (`rtk hook claude` dans ~/.claude/settings.json). Les autres agents (Gemini, Codex, Vibe, OpenCode, AGY) ont les règles §2.4 + docs dédiées (RTK.md ou section dans GEMINI.md) et doivent appeler manuellement `rtk <cmd>` ou `rtk proxy`. Stats globales actives (75,7 % sur 10k+ cmds).
- [2026-06-24] [ponytail] : 4.7.0 actif et vérifié sur Claude (plugin + .ponytail-active), Codex (marketplace + hooks), Gemini (config/plugins/ponytail hub avec cross intégrations), AGY (import gemini-cli), OpenCode (opencode-ponytail + .ponytail-active). Vibe n'a que le texte des règles (UNIVERSAL) — pas de plugin/skills dédié. Toujours redémarrer l'agent après enable.
- [2026-06-24] [onboarding] : Protocole agent bien documenté (README + START_HERE.md), mais .AI_AGENTS.md est dotfile (invisible au ls normal). AGENTS.md non-dot aide la découverte. Pas de STATE.md racine ni checklist minimale "Agent Arrival". La reprise passe par OPERATIONS.md + healthcheck + HANDOFF explicites.
- [2026-06-24] [gouvernance] : Cross-benefit excellent sur les règles et leçons (§11 + sync + @import + vault). Partiel sur les outils runtime (RTK auto seulement Claude ; ponytail par-agent). La source de vérité reste .AI_AGENTS.md ; les plugins/tools restent spécifiques à chaque harness.

- [2026-05-30] [another-tool] : Une autre leçon pour tester le nettoyage automatique.

- [2026-05-30] [test-tool] : Ceci est une leçon d'audit transverse hautement sécurisée.

- [2026-05-30] [make] : `make doctor` detecte les venv herites d'un autre checkout — `make rebuild` corrige. Toujours utiliser `make verify` en debut de session.
- [2026-05-30] [pytest] : Un import editable pointant vers un worktree supprime cause 26 erreurs de collection. Symptome : `ModuleNotFoundError` au collect. Correction : `make rebuild`.
- [2026-05-30] [providers] : Le mock `patch("anthropic.Anthropic", ...)` fonctionne car `AnthropicBackend.__init__` fait `from anthropic import Anthropic`. Ne pas utiliser `patch("...backends.Anthropic")`.
- [2026-05-30] [httpx] : `response.iter_lines()` retourne des strings (pas des bytes) dans httpx. Les tests SSE doivent mocker avec des strings, pas des `b"..."`.
- [2026-05-30] [google-auth-httpx] : Le package `google-auth-httpx` n'existe pas sur PyPI. `GeminiOAuthBackend` utilise `google.auth.transport.requests.Request()` pour le refresh, et `httpx` pour les appels API streaming. Pas besoin d'adaptateur tiers.

### [2026-05-29] Claude Code (subagent-driven-development) — CWD des sous-agents dans un worktree

**Problème rencontré** : lors d'une session `subagent-driven-development` avec un worktree git, les sous-agents recevaient l'instruction `Work from: /chemin/worktree` en texte libre, mais leurs commandes shell s'exécutaient dans le répertoire courant du processus (le repo principal). Les `git commit` atterrissaient donc sur la mauvaise branche (le repo principal au lieu du worktree).

**Règle permanente — Obligation pour tout dispatch de sous-agent sur worktree** :

Le prompt d'un sous-agent implémenteur DOIT contenir un bloc de vérification CWD **au tout début**, avant toute instruction de travail :

## ⚠️ Répertoire de travail OBLIGATOIRE

AVANT TOUT, exécute ces commandes de vérification :

cd /chemin/absolu/vers/le/worktree
pwd          # doit afficher /chemin/absolu/vers/le/worktree
git branch --show-current  # doit afficher "feature/ma-branche"

Si l'un des deux résultats ne correspond pas → STOP, rapport NEEDS_CONTEXT immédiat.

TOUTES tes commandes bash doivent commencer par :
cd /chemin/absolu/vers/le/worktree && <commande>
Ou utiliser le flag git : `git -C /chemin/absolu/vers/le/worktree <commande>`

**Pourquoi** : le shell des sous-agents ne hérite pas du CWD de la session parente. Sans `cd` explicite en début de chaque commande, les commits, tests et fichiers créés peuvent atterrir dans n'importe quel répertoire — typiquement la racine du projet ou `~/.claude/`.

**Impact si ignoré** : commits sur la mauvaise branche, historique git pollué, nécessité de cherry-pick ou rebase pour corriger.

**Format recommandé dans le prompt du contrôleur** :
Work from: /chemin/absolu/vers/le/worktree
Branch: feature/ma-branche
Venv: /chemin/absolu/vers/le/.venv/bin/python
Run tests: cd /chemin/absolu/vers/le/worktree && /chemin/absolu/vers/le/.venv/bin/python -m pytest -q

⚠️ Verify CWD before starting:
  cd /chemin/absolu/vers/le/worktree && git branch --show-current
  Must show "feature/ma-branche". If not: STOP and report NEEDS_CONTEXT.

### [2026-05-30] Leçons Apprises — Projet `agentic-slide-factory`

*   **[make] : Protection contre les venv fantômes**  
    Dans les environnements multi-branches ou worktrees, `make doctor` permet de détecter les environnements virtuels obsolètes hérités d'un autre checkout ou d'un install editable pointant vers un worktree supprimé (qui cause des dizaines d'erreurs pytest insolubles au collect). L'usage de `make rebuild` permet de nettoyer proprement le `.venv` (déplacement vers la Corbeille macOS au lieu de `rm -rf` direct pour préserver les performances d'écriture) et de réinstaller proprement. Il est recommandé de lancer systématiquement `make verify` en début de session de codage.
*   **[pytest] : Imports editables orphelins**  
    Un paquet installé en editable (`pip install -e .`) dont le répertoire physique d'origine a été supprimé provoque 26 erreurs de collection pytest silencieuses (avec un `ModuleNotFoundError` au collect). Solution : Lancer `make rebuild` pour régénérer proprement les liens symboliques et le package local de métadonnées.
*   **[providers] : Résolution des mocks unitaires Anthropic**  
    Le mock global `patch("anthropic.Anthropic", ...)` fonctionne parfaitement car `AnthropicBackend.__init__` effectue l'import local `from anthropic import Anthropic`. Ne pas tenter de patcher localement `...backends.Anthropic`, qui échoue en raison du lazy loading de la dépendance.
*   **[httpx] : Streaming SSE et mocking de types**  
    La méthode `response.iter_lines()` d'un client `httpx` de streaming retourne des chaînes de caractères (`str`) et non des octets (`bytes`). Les tests unitaires simulant le flux de streaming SSE doivent obligatoirement mocker les trames réseau avec des chaînes de caractères, sous peine de crashs de type-mismatch au décodage.
*   **[google-auth-httpx] : Rapprochement d'API streaming OAuth**  
    Étant donné que le package `google-auth-httpx` n'est pas disponible de façon fiable sur PyPI, la solution la plus propre et la plus robuste consiste à utiliser `google.auth.transport.requests.Request()` exclusivement pour le rafraîchissement d'accès OAuth en arrière-plan, et à employer un client `httpx` standardisé pour les requêtes streaming de jetons. Cela élimine le besoin d'adaptateurs tiers.

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
| Config OpenCode | `~/.config/opencode/AGENTS.md` | sync-agents.sh (auto) |
| Config Antigravity (AGY) | règles globales `agy` + `AGENTS.md` du workspace | sync-agents.sh (auto) + lecture workspace |
| Vault de connaissance | `~/DEV/active/knowledge-vault/` (OKF) | Lecture par tous (grep) ; §12bis |
| Projets opt-in | `~/DEV/active/*/AGENTS.md` | sync-agents.sh si marqueurs |
| Skills partagees | `~/.agents/skills/` | Symlinks vers ~/.claude/skills/ |
| Passations | `~/DEV/HANDOFF-*.md` | Fichiers temporaires par session |

### Infrastructure d'Automatisation

> 🗺️ **Carte unique de TOUS les automatismes** (launchd, hooks, crons, kill-switches) : `~/DEV/OPERATIONS.md`. Lire en premier pour reprendre le contrôle.

| Fichier | Role |
|---------|------|
| `~/DEV/OPERATIONS.md` | Runbook — inventaire de tous les jobs/hooks + comment inspecter/désactiver |
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

---

## 12bis. Vault de Connaissance (OKF) — Mémoire Partagée

> Mémoire partagée homme/IA au format **OKF** (Open Knowledge Format, Google Cloud) : dossiers de `.md` + frontmatter YAML, 1 concept/fichier, liens markdown = graphe. Lisible par l'humain (Obsidian) **et** par tout agent (grep). **Tous les agents doivent l'utiliser.**

- **Emplacement** : `~/DEV/active/knowledge-vault/`
- **Schéma & types** : `~/DEV/active/knowledge-vault/okf.schema.md` (types : `concept`, `lesson`, `idea`, `session`, `reference`, `project-pointer`, `adr`, `moc`).

**Protocole de LECTURE** (économie de tokens — grep d'abord, jamais de Read massif) :
1. `knowledge-vault/index.md` (L0) → `knowledge-vault/CRITICAL_FACTS.md`.
2. Cibler : `grep -rn "^type: <type>" ~/DEV/active/knowledge-vault/` ou ouvrir l'`index.md` du bundle voulu.
3. Suivre les liens `[[...]]` pour traverser le graphe.

**Protocole d'ÉCRITURE** :
- Capture rapide → `inbox/` (frontmatter minimal, `type` requis).
- Échange/session → *append* dans `journal/AAAA/MM/AAAA-MM-JJ.md` (type `session`). **Ne jamais réécrire une session passée** (append-only).
- Savoir durable → `knowledge/{concepts,lessons,references}/` en phrases complètes, avec `description` et liens.
- Idée → `ideas/` (`status: seed|sprouting|ready`).

**Règle d'or anti-hallucination** : pour les faits du vault, n'utilise **que** les notes ; si une note ne couvre pas le sujet, **dis-le** ; **cite la note source `[[...]]`**.

**Propagation** : les `lessons` du vault remontent vers `§11` via le skill `vault-sync`, puis `sync-agents.sh` diffuse à tous les agents (Codex, Vibe, OpenCode, Gemini, AGY).

**Vérifier / interroger le vault (commandes universelles, tout agent).** Outil stdlib sans dépendance, exécutable par n'importe quel agent capable de lancer un shell :
cd ~/DEV/active/knowledge-vault
python3 meta/okf-graph.py --health     # bilan structurel (schéma, liens cassés, orphelins, fraîcheur) ; exit 1 si bloquant
python3 meta/okf-graph.py --type lesson | --tag <tag> | --neighbors <note> | --hubs 10 | --orphans
python3 meta/okf-graph.py --check      # exit 1 si liens [[...]] cassés (utilisé par le pre-commit du vault)
Quand l'utilisateur demande « le bilan de santé / interroge le vault », lancer ces commandes (pas besoin d'un skill spécifique). Un cron mensuel (`com.rodolphe.vault-health`) peut aussi écrire `meta/health-latest.md`.

**Maintenir sans dénaturer (TOUT agent éditant le vault).** Invariants à respecter sous peine de dégrader la base :
- 1 concept = 1 fichier ; `type` ∈ liste fermée (`concept`, `lesson`, `idea`, `session`, `reference`, `project-pointer`, `adr`, `moc`) ; frontmatter requis `type` + `title` + `description`. Ajouter un `type` = créer un ADR dans `decisions/`.
- Notes-concepts en `kebab-case.md` ; MOC en `index.md`. Détail : `knowledge-vault/okf.schema.md`.
- `journal/` = **append-only** : ne JAMAIS réécrire une session passée. `projects/` = pointeurs, jamais dupliquer un repo.
- Chaque note pointe vers ≥ 1 hub (zéro orphelin) ; citer la note source `[[...]]` (anti-hallucination).
- Éditions **ciblées**, pas de réécriture en masse ; suppression → `mv ~/.Trash/` (jamais `rm`) ; aucun secret.
- **Avant tout commit du vault** : `python3 meta/okf-graph.py --check` doit passer (le pre-commit le force). Vérifier la santé : `--health`.
- Après une session : `vault-session-save` (trace) puis `vault-sync` (propage les leçons vers §11 + agents).

<!-- END:UNIVERSAL -->
