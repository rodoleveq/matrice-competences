# START HERE

Welcome. Use this when arriving fresh to this project.

## 1. What Is This Project?

See `CLAUDE.md` → **Project** or **Resume du Projet** section.

## 2. Where Am I?

Read `STATE.md` for:
- Current branch
- Features implemented/in-progress  
- Open issues
- Latest blockers

## 3. How Do I Start Coding?

From `CLAUDE.md` → **Stack** and **Commandes**:
```bash
# Setup (if first time)
cd ~/DEV/active/<project-name>

# Build/Run
<see CLAUDE.md for exact command>

# Test
<see CLAUDE.md for exact command>
```

## 4. Key Files to Read (in order)

1. **`CLAUDE.md`** — Project context, stack, commands
2. **`STATE.md`** — Current state & blockers
3. **`DECISIONS.md`** — Architecture decisions (if exists)
4. **`AGENTS.md`** — Project-specific rules (if exists)

## 5. Universal Rules

All projects follow **`~/DEV/.AI_AGENTS.md`** for:
- Commit conventions (`feat`, `fix`, `docs`, etc.)
- File naming (kebab-case, PascalCase, camelCase)
- Build/test/lint commands
- Conflict resolution

## 6. If Stuck

1. Check `DECISIONS.md` for ADRs
2. Run tests/build to verify local state: `npm run build` or `xcodebuild build`
3. Read recent commits: `git log --oneline -10`
4. Ask the human (see `CLAUDE.md` → contacts if specified)

---

**Last Update**: auto-generated template
