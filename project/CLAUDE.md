# <Projektname>

> **Lädt:** jede Session in diesem Repo, zusätzlich zu `~/.claude/CLAUDE.md`.
> **Regel:** unter 100 Zeilen. Was länger ist, kommt in [`.claude/rules/`](.claude/rules/) oder einen Skill.
> Globale Regeln überstimmt diese Datei nicht; Hardrules gelten immer.

## Was das ist

<!-- Zwei Sätze. Was tut die Software, für wen. -->

## Stack

<!-- Nur Fakten, die Claude jede Session braucht. Versionen mit Datum. -->
- Backend: `<Sprache, Framework, Version>`
- Frontend: `<Framework, Version>`
- Datenbank: `<System, Version>`
- Laufzeit: `<Node/Python-Version>`

## Befehle

```bash
# Tests
<z. B. python -m pytest -q>
# Lint
<z. B. ruff check .>
# Dev-Server (Port festlegen, nicht raten)
<z. B. ng serve --port 4200>
```

## Layout

```
<ordner>/   <was liegt hier>
<ordner>/   <was liegt hier>
```

## Branches

- Arbeitsbranch: `<z. B. develop>`. Alle Commits gehen hierhin.
- Produktionsbranch: `<z. B. main>`. Nur per Merge, nur auf Freigabe.

## Tracking

- Slice-Tabelle: [`SLICES.md`](SLICES.md). Jede Session trägt sich dort ein.
- Verbraucher und Invarianten: `AGENTS.md` (Vorlage: [`AGENTS.md.example`](AGENTS.md.example)). Pflichtlektüre vor der Pflichtmatrix.
- Agenten-Profil (falls Extras aktiv): `.claude/team.md` (Vorlage: [`team.md.example`](.claude/team.md.example)).

## Projektregeln

Liegen in [`.claude/rules/`](.claude/rules/) und laden automatisch, pfadgebundene
nur bei passenden Dateien. Stack-Vorlagen: `stacks/` im Starter.

## Erlaubte externe Dienste

<!-- DSGVO: wohin dürfen Nutzerdaten? Leer = nirgendwohin. -->
- KI-Anbieter: `<z. B. nur EU-Region, nie direkt api.anthropic.com in Produktion>`
- Sonstige: `<…>`

## Compact Instructions

<!-- Was bei /compact erhalten bleiben muss. Kurz. -->
- Aktueller Slice, Akzeptanzpunkte, geänderte Dateien, offene Punkte.
