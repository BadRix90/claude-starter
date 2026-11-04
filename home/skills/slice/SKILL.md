---
name: slice
description: Führt einen Slice nach dem festen Ablauf aus - Analyse, Klartext, Dateien, Lösungsvorschlag, Umsetzung, Abschlussbericht. Nutzen, wenn eine Aufgabe mit Slice-ID (F12, B3, R7a) startet oder der Nutzer "Slice" sagt.
argument-hint: "<Slice-ID> <Auftrag in Klartext>"
disable-model-invocation: true
---

# Slice-Ablauf

Regeln, die hier gelten: `~/.claude/rules/10-workflow.md`, `11-slices.md`,
`12-definition-of-done.md`. Bei Widerspruch gewinnt `00-hardrules.md`.

Auftrag: $ARGUMENTS

## 1 Einordnen

- Slice-ID und Typ aus dem Auftrag lesen. Fehlt die ID: aus der Slice-Tabelle des
  Projekts fortzählen (Pfad steht im Projekt-`CLAUDE.md`), nie raten.
- Session-Titel setzen: `<Slice-ID> <Thema>`.
- Typ bestimmt die Zielstufe: F, B, H brauchen `PROD_VERIFIED`; A, C, R, D `VERIFIED`.

## 2 Analyse, noch kein Code

- Liegt `graphify-out/graph.json` vor: `graphify query` aus dem Repo-Root, dann
  gezielt lesen. Sonst Grep mit Pfadfilter und im Bericht vermerken.
- Betroffene Dateien mit Pfad und Zeile benennen.
- Akzeptanzpunkte als Matrix anlegen (Vorlage in `12-definition-of-done.md`).
- Verbraucher aus `AGENTS.md` des Projekts durchgehen, nicht betroffene als N/A begründen.

## 3 Klartext und Vorschlag

Problem in zwei Sätzen ohne Jargon. Lösung an der Wurzel, keine Pflasterarbeit.
Bei echter Mehrdeutigkeit: eine Frage, dann warten. Sonst weiter.

## 4 Umsetzen

- Bugfix: erst der Test, der rot ist. Dann der Fix. Dann grün zeigen.
- Nur die Dateien aus der Analyse. Kein Gelegenheits-Refactor.
- Tests nach jeder Änderung, Befehl aus dem Projekt-`CLAUDE.md` oder `.claude/team.md`.
- Commit mit expliziten Pfaden, Conventional Commit, Slice-ID im Scope oder Body.
- Push nur, wenn der Auftrag „push“ enthält.

## 5 Gegenprobe

Sieben Fragen der negativen Gegenprobe und sieben Fragen des Runtime-Pfad-Audits
aus `12-definition-of-done.md` beantworten. Dann die Originalkarte noch einmal
lesen und jeden Punkt gegen den Code prüfen, nicht gegen die eigene Zusammenfassung.

## 6 Abschluss

Abschlussbericht im festen Format aus `12-definition-of-done.md`. Slice-Tabelle
und Historie des Projekts aktualisieren, mit-committen. Letzte Zeile:
„Keine offenen Punkte.“ oder die Liste der offenen Punkte mit Grund.
