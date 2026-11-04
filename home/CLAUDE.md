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

| Thema | Datei | Wann lesen |
|---|---|---|
| Nicht verhandelbare Regeln | [`00-hardrules.md`](rules/00-hardrules.md) | immer, zuerst |
| Ablauf einer Aufgabe | [`10-workflow.md`](rules/10-workflow.md) | vor jeder Änderung |
| Slices und Session-Namen | [`11-slices.md`](rules/11-slices.md) | beim Start einer Session |
| Wann etwas „fertig“ ist | [`12-definition-of-done.md`](rules/12-definition-of-done.md) | vor dem Abschlussbericht |
| Kommunikation | [`20-kommunikation.md`](rules/20-kommunikation.md) | bei jeder Antwort |
| Recherche und Quellen | [`21-recherche.md`](rules/21-recherche.md) | bei veränderlichen Fakten |
| Code-Qualität | [`30-code-quality.md`](rules/30-code-quality.md) | beim Schreiben von Code |
| Git | [`31-git.md`](rules/31-git.md) | vor Commit und Push |
| Security | [`32-security.md`](rules/32-security.md) | bei Secrets, Auth, Rechten |
| Tests | [`33-testing.md`](rules/33-testing.md) | bei jedem Fix und Feature |
| Modellwahl | [`40-modellwahl.md`](rules/40-modellwahl.md) | vor Session und Delegation |
| graphify | [`41-graphify.md`](rules/41-graphify.md) | bevor Dateien gesucht werden |

## Werkzeuge, die ich erwarte

- Skills: `/slice`, `/audit`, `/commit` (siehe [`skills/`](skills/)); `/graphify` kommt von graphify selbst ([`41-graphify.md`](rules/41-graphify.md)).
- Hooks in [`settings.json`](settings.json) blocken `git add .`, Force-Push, das
  Umgehen von Git-Hooks und Schreibzugriffe auf `.env`. Das sind Leitplanken, keine Bitten.
