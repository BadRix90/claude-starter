# Globale Arbeitsregeln

> **Lädt:** jede Session, in jedem Projekt (`~/.claude/CLAUDE.md`).
> **Zweck:** nur das, was Claude immer wissen muss. Alles Weitere liegt in
> [`rules/`](rules/) und wird automatisch mitgeladen. Diese Datei bleibt unter 60 Zeilen.

## Wer ich bin

<!-- Ausfüllen. Zwei bis vier Zeilen, keine Lebensgeschichte. -->
- Rolle: `<z. B. Full-Stack-Entwickler, Backend Python, Frontend TypeScript>`
- Hauptstack: `<z. B. Django + Angular, Astro für Marketing-Seiten>`
- Sprache: Antworten auf Deutsch, Code und Commits auf Englisch.

## Rangordnung der Regeln

1. [`rules/00-hardrules.md`](rules/00-hardrules.md) gewinnt bei jedem Widerspruch.
2. Die übrigen Dateien in `rules/` in Nummernreihenfolge.
3. Projekt-`CLAUDE.md` und `.claude/rules/` des jeweiligen Repos ergänzen, überstimmen aber keine Hardrule.
4. `CLAUDE.local.md` im Projekt: persönliche Abweichungen, nie committet.

## Was wo steht

Alle Dateien in `rules/` laden in jeder Session vollständig. Abläufe, die nur manchmal
gebraucht werden, liegen in Skills und laden erst beim Aufruf.

| Thema | Datei |
|---|---|
| Nicht verhandelbare Regeln | [`00-hardrules.md`](rules/00-hardrules.md) |
| Ablauf einer Aufgabe, wann fragen | [`10-workflow.md`](rules/10-workflow.md) |
| Kommunikation | [`20-kommunikation.md`](rules/20-kommunikation.md) |
| Recherche und Quellen | [`21-recherche.md`](rules/21-recherche.md) |
| Code-Qualität | [`30-code-quality.md`](rules/30-code-quality.md) |
| Git | [`31-git.md`](rules/31-git.md) |
| Security | [`32-security.md`](rules/32-security.md) |
| Tests | [`33-testing.md`](rules/33-testing.md) |
| graphify | [`41-graphify.md`](rules/41-graphify.md) |
| Slices, Definition of Done, Abschlussbericht | Skill `/slice` ([`skills/slice/`](skills/slice/)) |

## Werkzeuge, die ich erwarte

- Skills: `/einrichten` (Ersteinrichtung per Fragen), `/slice`, `/audit`, `/commit` (siehe [`skills/`](skills/)); `/graphify` kommt von graphify selbst ([`41-graphify.md`](rules/41-graphify.md)).
- Hooks in [`settings.json`](settings.json) blocken `git add .`, Force-Push, das
  Umgehen von Git-Hooks sowie Lese- und Schreibzugriffe auf `.env` über die Shell
  und melden nach jedem Schreiben Dateien über 400 und Funktionen über 20 Zeilen.
  Das sind Leitplanken, keine Bitten.
