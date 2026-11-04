# Projektregeln

> Alle `.md` in diesem Ordner laden automatisch in jede Session dieses Repos,
> auch aus Unterordnern. Dateien mit `paths:` im Frontmatter laden erst, wenn
> Claude eine passende Datei anfasst. Das spart Kontext.
> Diese README lädt mit; sie bleibt deshalb kurz.

## Konventionen

- Eine Datei je Thema, sprechender Name: `django.md`, `angular.md`, `api-design.md`.
- Jede Datei beginnt mit einer Zeile, wann sie gilt und auf welche globale Regel sie aufbaut.
- Nichts wiederholen, was in `~/.claude/rules/` steht. Nur ergänzen oder konkretisieren.
- Vorlagen für Stacks liegen im Starter unter `stacks/<stack>/rules/`.

## Pfadgebundene Regel, Beispiel

```markdown
---
paths:
  - "backend/**/*.py"
---
# Backend

Gilt nur, wenn Python-Dateien unter backend/ bearbeitet werden.
```

Globs: `**` beliebig tief, `{py,pyi}` Alternativen, führendes `/` für Repo-Root.
