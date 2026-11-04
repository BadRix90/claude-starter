# Wie Claude Code funktioniert

> **Für wen:** alle, die den Bauplan einsetzen und verstehen wollen, warum die
> Regeln so geschnitten sind. **Danach lesen:** [`WAS-LAEDT-WANN.md`](WAS-LAEDT-WANN.md),
> [`MODI-UND-SESSIONS.md`](MODI-UND-SESSIONS.md). Quelle: [offizielle Doku](https://code.claude.com/docs/en/how-claude-code-works).

## Die Schleife

Claude Code ist ein Agent im Terminal (und in der Desktop-App, IDE, im Browser).
Jede Aufgabe läuft in drei Phasen, die ineinander übergehen:

1. **Kontext sammeln**: Dateien suchen und lesen, Git-Zustand ansehen, Doku holen.
2. **Handeln**: Dateien ändern, Befehle ausführen, Tests starten.
3. **Prüfen**: Ergebnis lesen, nachbessern, wiederholen.

Das Modell entscheidet nach jedem Werkzeugaufruf, was als Nächstes passiert. Der
Mensch kann jederzeit unterbrechen (`Esc`) oder eine Korrektur einwerfen, die
Claude nach dem laufenden Werkzeugaufruf liest.

**Modell + Werkzeuge = Agent.** Das Modell denkt, die Werkzeuge handeln. Ohne
Werkzeuge gäbe es nur Text. Die eingebauten Werkzeuge: Dateien lesen und ändern,
suchen, Shell, Web, Code-Intelligenz über Plugins, Subagenten starten, Fragen stellen.

## Was Claude sieht

- **Das Projekt**: alle Dateien im Verzeichnis und darunter, weitere nur mit Erlaubnis.
- **Das Terminal**: alles, was man selbst dort tun könnte.
- **Git**: Branch, offene Änderungen, History.
- **`CLAUDE.md`** auf jeder Ebene plus `.claude/rules/`.
- **Auto-Memory**: Notizen, die Claude sich selbst gemacht hat (erste 200 Zeilen von `MEMORY.md`).
- **Erweiterungen**: Skills, Subagenten, MCP-Server, Hooks.

## Das Kontextfenster

Alles, was Claude in einer Session weiß, liegt im Kontextfenster: Systemprompt,
`CLAUDE.md`, Regeln, Skill-Beschreibungen, der Chatverlauf, gelesene Dateien,
Befehlsausgaben. Das Fenster ist groß, aber endlich.

Läuft es voll, **kompaktiert** Claude Code: der Verlauf wird zu einer
Zusammenfassung. Anweisungen vom Anfang des Chats können dabei verloren gehen.
Was dauerhaft gelten soll, gehört deshalb in `CLAUDE.md` oder eine Regel, nicht
in den Chat. `CLAUDE.md` im Projekt-Root wird nach `/compact` neu von der Platte
gelesen. Ein Abschnitt „Compact Instructions“ in `CLAUDE.md` steuert, was die
Zusammenfassung behalten soll.

`/context` zeigt, was gerade Platz belegt.

## Sessions

- Jede Session wird lokal als JSONL unter `~/.claude/projects/` gespeichert.
- Vor jeder Änderung macht Claude Code einen **Snapshot** der Datei. `Esc Esc`
  oder „mach das rückgängig“ setzt zurück. Das ist unabhängig von Git und deckt
  nur Dateien ab, keine Datenbanken oder Deployments.
- **Fortsetzen**: `claude --continue` (letzte Session) oder `claude --resume` (Auswahl)
  hängt an dieselbe Session an. **Abzweigen**: `--fork-session` oder `/branch` kopiert
  den Verlauf in eine neue Session.
- Sessions sind an das Verzeichnis gebunden. Branch wechseln ändert die Dateien,
  die Claude sieht, nicht den Chatverlauf.
- Eine neue Session startet leer. Nur `CLAUDE.md`, Regeln und Auto-Memory tragen
  Wissen hinüber. Das ist der Grund für `SLICES.md` und den Abschlussbericht im Bauplan.

## Was Claude Code selbst in den Kontext schiebt

Neben dem, was man schreibt, legt Claude Code eigene Hinweise ein: `CLAUDE.md`,
den aktiven Output-Style, eine Notiz, wenn eine gelesene Datei sich geändert hat,
und die Co-Authored-By-Zeile für Commits. Letztere lässt sich mit `attribution`
in `settings.json` ändern oder abschalten.

## Zwei Sicherheitsnetze

1. **Checkpoints**: Dateiänderungen sind reversibel (siehe oben).
2. **Permissions**: der Modus bestimmt, was ohne Nachfrage passiert. Details in
   [`MODI-UND-SESSIONS.md`](MODI-UND-SESSIONS.md). Was unabhängig vom Modus nie
   passieren darf, gehört in `permissions.deny` oder einen Hook ([`HOOKS.md`](HOOKS.md)),
   nicht in Prosa.

## Effizient arbeiten, kurz

- Delegieren statt diktieren: Kontext und Ziel geben, nicht jede Datei vorkauen.
- Iterieren statt neu starten: „nicht ganz, das Problem liegt in X“ reicht.
- Wiederholte Fehler sind ein `CLAUDE.md`-Eintrag, keine Chat-Korrektur.
- Wiederholte Prompts sind ein Skill. Wiederholte Pflichten sind ein Hook.
- Lange Nebenaufgaben mit viel Ausgabe in einen Subagenten, damit der Hauptkontext sauber bleibt.
- `/init` erzeugt ein erstes `CLAUDE.md`, `/doctor` prüft die Konfiguration,
  `/doctor prompt-audit` findet widersprüchliche Anweisungen.
