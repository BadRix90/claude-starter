# Extras: Agenten-Team, Workflows, Manager-Skill

> **Nicht automatisch aktiv.** Hardrule §2 sagt: ein Agent pro Session. Diese
> Extras schalten bewusst Mehr-Agenten-Arbeit frei. Sie kosten ein Mehrfaches an
> Tokens und lohnen sich erst, wenn ein Slice mehr als eine Stunde Einzelarbeit wäre
> oder eine unabhängige Abnahme Pflicht ist.
> **Vorher lesen:** [`docs/MODI-UND-SESSIONS.md`](../docs/MODI-UND-SESSIONS.md), Abschnitt „Mehrere Claudes“.

## Was drin ist

| Ordner | Inhalt | Wird zu |
|---|---|---|
| [`agents/`](agents/) | fünf Rollen: analyst, implementer, doc-writer, qa, security-auditor | `~/.claude/agents/` oder `<repo>/.claude/agents/` |
| [`workflows/`](workflows/) | `slice.js` (Entwickler → QA → eine Korrektur), `council.js` (Entscheidung ohne Rückfrage) | `~/.claude/workflows/` |
| [`skills/auftrag/`](skills/auftrag/) | Manager-Skill: Analyse, Karte einfrieren, Slices fahren, Bericht | `~/.claude/skills/auftrag/` |

## Aktivieren

1. Kopieren (siehe Tabelle).
2. Im Projekt `.claude/team.md` aus `project/.claude/team.md.example` füllen.
3. In `~/.claude/rules/00-hardrules.md` §2 um einen Satz ergänzen:
   „Ausnahme: `/auftrag` und die Agenten aus extras, wenn das Projekt eine `team.md` hat.“
4. Modelle im Frontmatter der Agenten prüfen ([`40-modellwahl.md`](../home/rules/40-modellwahl.md)).

## Prinzipien

- **Implementierer ≠ Abnehmer.** `qa` sieht nur Karte, Commit-SHA und Testausgabe,
  nie die Zusammenfassung des Entwicklers.
- **Budget hart.** Code-Slice höchstens 4 Agenten (5 mit Security), Text-Slice 3.
  Lieber `BLOCKED` mit Grund als ein zweiter teurer Lauf.
- **Pfade begrenzt.** `guard_paths.py` verhindert, dass ein Subagent CI, Container,
  Settings oder `.env` anfasst, und trennt Test- von Produktivdateien.
- **Entscheidungen ohne Rückfrage.** Fehlt eine fachliche Festlegung, entscheidet
  `council` (zwei Berater, ein Vorsitz), nicht der Mensch im Chat. Ausnahme:
  security-sensitive Mutationen, die bleiben eine Frage.
