# Anpassen nach dem Fork

> **Für wen:** alle, die den Starter gerade kopiert haben. In dieser Reihenfolge,
> jeder Schritt zehn Minuten oder weniger. **Vorher:** [`../INSTALL.md`](../INSTALL.md).
> **Abkürzung:** `/einrichten` in einer Session macht die Schritte 1 bis 7 als Gespräch,
> Claude fragt und zeigt jeden Diff ([`../home/skills/einrichten/SKILL.md`](../home/skills/einrichten/SKILL.md)).
> **Geprüft gegen:** Claude Code 2.1.310, Doku-Stand 11/2026.

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

## Wenn etwas nicht greift

Erst nachsehen, was wirklich geladen ist, dann suchen.

| Befehl | Zeigt |
|---|---|
| `/memory` | welche `CLAUDE.md` und Regeln geladen sind |
| `/context` | was wie viel Kontext belegt, nach Kategorie |
| `/hooks` | die aktiven Hooks. Leer heißt: Datei am falschen Ort oder ungültiges JSON |
| `/permissions` | die geltenden `allow`- und `deny`-Regeln |
| `/status` | aus welchen Settings-Dateien die Session liest |
| `/doctor` | Prüfung von Installation und Konfiguration mit Vorschlägen |
| `claude --debug` | Log jedes Hook-Laufs mit Exit-Code und Ausgabe |
| `claude --safe-mode` | Session ohne jede Anpassung, zum Gegenprüfen |

Typische Ursachen:

- **Hook erscheint nicht in `/hooks`:** Komma am Ende oder Kommentar in `settings.json`.
  JSON erlaubt beides nicht. Deshalb liegt die Erklärung in `settings.erklaert.jsonc`.
- **Hook läuft, wirkt aber nicht:** die zwei stillen Fallen in [`HOOKS.md`](HOOKS.md).
- **`python` nicht gefunden:** absoluten Pfad eintragen, siehe [`../INSTALL.md`](../INSTALL.md).
- **Regel wird nicht befolgt:** steht sie doppelt oder widersprüchlich in zwei Dateien?
  `/doctor prompt-audit` findet das. Muss sie immer gelten, gehört sie in einen Hook.
- **Regel nach `/compact` weg:** sie stand nur im Chat oder in einer pfadgebundenen
  Regel, die seitdem keine passende Datei gesehen hat.

Die offizielle Tabelle nach Symptomen: [Debug your configuration](https://code.claude.com/docs/en/debug-your-config).

## Was danach regelmäßig ansteht

- Ein wiederholter Fehler wird eine Regel. Eine wiederholte Korrektur im Chat ist ein Zeichen.
- Ein wiederholter Prompt wird ein Skill.
- Eine Regel, die nie greift, fliegt raus.
- `CLAUDE.md` über 200 Zeilen: aufteilen.
- Versionen im Stack-Abschnitt mit Datum pflegen.
