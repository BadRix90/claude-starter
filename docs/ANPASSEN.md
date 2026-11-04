# Anpassen nach dem Fork

> **Für wen:** alle, die den Starter gerade kopiert haben. In dieser Reihenfolge,
> jeder Schritt zehn Minuten oder weniger. **Vorher:** [`../INSTALL.md`](../INSTALL.md).

## 1 Identität

`home/CLAUDE.md`, Abschnitt „Wer ich bin“: Rolle, Stack, Sprache. Drei Zeilen.

## 2 Hardrules durchgehen

`home/rules/00-hardrules.md`. Jeden Paragraphen lesen und entscheiden: behalten,
anpassen, streichen. Besonders:

- §2 (ein Agent): streichen oder ergänzen, wenn `extras/` genutzt wird.
- §4 (kein Worktree): streichen, wer bewusst mit Worktrees arbeitet.
- §13 (Branches): an das eigene Branch-Modell anpassen.

Was gestrichen wird, wird gestrichen, nicht auskommentiert. Tote Regeln verwirren.

## 3 Modell und Effort

`home/settings.json`: `model`, `effortLevel`. Entscheidungshilfe in
[`MODELLWAHL.md`](MODELLWAHL.md). Wer über Bedrock oder Vertex arbeitet, pinnt
Modell-IDs.

## 4 Hooks aktivieren

`home/settings.json` nach `~/.claude/settings.json`, `home/hooks/` nach `~/.claude/hooks/`.
Prüfen: in einer Session `git add .` tippen lassen. Der Hook muss blocken.
Klappt `$HOME` nicht: absoluten Pfad eintragen (siehe `settings.erklaert.jsonc`).

## 5 Skills

`home/skills/` nach `~/.claude/skills/`. `/slice`, `/audit`, `/commit` erscheinen im
`/`-Menü. graphify nach [`home/rules/41-graphify.md`](../home/rules/41-graphify.md)
installieren oder die Regel und den Eintrag in `CLAUDE.md` entfernen.

## 6 Erstes Projekt

`project/` in das Repo: `CLAUDE.md` füllen (Stack, Befehle, Branches), `AGENTS.md.example`
zu `AGENTS.md` mit den echten Verbrauchern, `SLICES.md` mit dem ersten Slice,
`.gitignore.example` in die eigene `.gitignore` mischen. Passende Variante aus
`stacks/` nach `.claude/rules/`.

## 7 Prüfen

In einer Session: `/memory` (alles geladen?), `/context` (wie viel Platz?),
`/doctor prompt-audit` (Widersprüche?). Claude fragen: „Welche Hardrules gelten?“
Die Antwort muss aus `00-hardrules.md` kommen, nicht aus dem Gedächtnis.

## 8 Extras, nur bei Bedarf

[`../extras/README.md`](../extras/README.md). Erst, wenn ein Slice regelmäßig eine
unabhängige Abnahme braucht.

## Was danach regelmäßig ansteht

- Ein wiederholter Fehler wird eine Regel. Eine wiederholte Korrektur im Chat ist ein Zeichen.
- Ein wiederholter Prompt wird ein Skill.
- Eine Regel, die nie greift, fliegt raus.
- `CLAUDE.md` über 200 Zeilen: aufteilen.
- Versionen im Stack-Abschnitt mit Datum pflegen.
