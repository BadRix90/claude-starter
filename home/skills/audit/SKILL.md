---
name: audit
description: Read-only Bestandsaufnahme eines Repos oder Ordners gegen die Regeln in ~/.claude/rules und das Projekt-CLAUDE.md. Ändert nichts. Nutzen bei "Audit", "prüf das Repo gegen die Regeln", "Compliance-Check", Slice-Typ A.
argument-hint: "[Pfad oder Thema, z. B. backend/ oder security]"
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash(git log *), Bash(git diff *), Bash(git show *), Bash(graphify *), Bash(wc *)
---

# Audit

Du änderst nichts. Du schreibst keine Datei außer dem Bericht, und den nur,
wenn der Auftrag einen Pfad dafür nennt.

Umfang: $ARGUMENTS (leer = ganzes Repo)

## Prüffelder

| Feld | Regel | Wie prüfen |
|---|---|---|
| Dateigrößen | `00-hardrules.md` §11: 400 Zeilen | `wc -l` über produktive Dateien, Treffer listen |
| Funktionslängen | 20 Zeilen | Stichprobe der größten Dateien |
| Schichtung | Logik nicht in View, Serializer, Model, Exporter | Grep nach Berechnungen und Bedingungen in diesen Schichten |
| Doppelte Semantik | `00-hardrules.md` §8 | gleiche Entscheidung an zwei Stellen, `graphify path` nutzen |
| Secrets | `32-security.md` | Grep nach Keys, Tokens, Passwörtern, `.env`-Zugriffen im Code |
| Tests | `33-testing.md` | Services ohne Test, Fixes ohne roten Test in der History |
| Commits | `31-git.md` | `git log --oneline -30`: Conventional Commits, Pfade statt `.` |
| Doku | Projekt-`CLAUDE.md`, `AGENTS.md`, Slice-Tabelle | vorhanden, aktuell, widerspruchsfrei zum Code |
| Konfiguration | `.claude/settings.json`, Hooks | vorhanden, Hooks lauffähig |

Stack-spezifische Felder stehen in den Rules des Projekts (`.claude/rules/`).

## Bericht

Pro Befund eine Zeile: `Schwere · Datei:Zeile · Regel · Befund · Vorschlag`.
Schwere: `hoch` (Security, Datenverlust, Hardrule), `mittel` (Regelverstoß),
`niedrig` (Stil). Höchstens 20 Befunde, wichtigste zuerst. Am Ende drei Zeilen:
was gut ist, was zuerst zu tun ist, was ohne Graph geprüft wurde.
