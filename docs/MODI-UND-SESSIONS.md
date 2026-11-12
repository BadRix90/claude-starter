# Modi und Sessions: wie viel Claude allein darf, und wie viele Claudes

> **Für wen:** alle, die zwischen „fragt dauernd“ und „macht zu viel“ den richtigen
> Punkt suchen. **Vorher:** [`WIE-CLAUDE-CODE-FUNKTIONIERT.md`](WIE-CLAUDE-CODE-FUNKTIONIERT.md).
> Quellen: [Permission-Modi](https://code.claude.com/docs/en/permission-modes), [Agenten parallel](https://code.claude.com/docs/en/agents), [Subagenten](https://code.claude.com/docs/en/sub-agents).
> **Geprüft gegen:** Claude Code 2.1.310, Doku-Stand 11/2026.

## Teil 1: Permission-Modi

Der Modus legt fest, was Claude ohne Nachfrage tut. `Shift+Tab` wechselt im
Terminal durch die Modi. Start-Modus: `--permission-mode <modus>` oder
`permissions.defaultMode` in `settings.json`. **`deny`-Regeln gelten in jedem Modus.**

| Modus | Ohne Nachfrage | Fragt bei | Wann sinnvoll | Risiko |
|---|---|---|---|---|
| **Manuell** (`default`) | Lesen | jeder Änderung, jedem Befehl, Netz | unbekannter Code, sensible Arbeit | Prompt-Müdigkeit: man klickt durch |
| **Accept Edits** (`acceptEdits`) | Lesen, Dateiänderungen, `mkdir`, `mv`, `cp`, `rm`, `sed` im Arbeitsverzeichnis | anderen Befehlen | man prüft hinterher per `git diff` | Änderungen landen ohne Blick darauf |
| **Plan** (`plan`) | Lesen, Recherche, Planen | Schreiben ist gesperrt, bis der Plan freigegeben ist | Analyse vor der Umsetzung, Slice-Schritt 1 bis 4 | Planungsgrenze, keine Sicherheitsgrenze |
| **Auto** (`auto`) | alles, was ein Klassifikator-Modell als unbedenklich einstuft | `ask`-Regeln, Klassifikator-Blocks | lange Aufgaben mit klarer Richtung | Klassifikator kann irren; nur in `~/.claude/settings.json` setzbar |
| **Don't Ask** (`dontAsk`) | nur, was `allow`-Regeln erlauben, Rest wird abgelehnt | nie, lehnt still ab | CI, Skripte | Unerwartetes scheitert ohne Rückfrage |
| **Bypass** (`bypassPermissions`) | alles, auch geschützte Pfade | `ask`-Regeln, kritische `rm` | nur isolierte Container ohne Netz | kein Schutz vor Prompt-Injection |

### Auto-Modus genauer

Ein zweites Modell prüft jede Aktion, die nicht schon durch Regeln entschieden ist.
Reihenfolge: `allow`/`ask`/`deny` zuerst, dann Lesen und Ändern im Arbeitsverzeichnis
automatisch, der Rest zum Klassifikator. Der blockt standardmäßig: `curl | bash`,
Datenabfluss an fremde Endpunkte, Produktions-Deploys und -Migrationen, Force-Push,
`git reset --hard`, `terraform destroy`, Rechtevergabe, Merge ohne menschliches Review.
Er erlaubt: lokale Dateiarbeit, Installation deklarierter Abhängigkeiten, Lesen von
`.env` für die passende API, Push auf Branches des eigenen Repos.

Blockt er dreimal hintereinander oder zwanzigmal insgesamt, fällt die Session auf
Nachfragen zurück. Eigene Grenzen zählen: steht „nicht pushen“ im Chat, blockt er Pushes.

Breite `allow`-Regeln wie `Bash(*)` werden im Auto-Modus verworfen, enge wie
`Bash(npm test)` bleiben. Seit Claude Code 2.1.283 ist Auto der Start-Modus für
interaktive Terminal-Sessions.

### Empfehlung des Starters

- Neues Repo, fremder Code: **Plan** für die Analyse, dann **Manuell**.
- Eigener Code, klarer Slice: **Accept Edits** mit `ask` für Push und Merge
  (so in `home/settings.json`).
- Lange, gut beschriebene Aufgabe: **Auto**, mit `deny` für `.env` und Hooks als Netz.
- **Bypass** nie auf dem eigenen Rechner.

## Teil 2: Mehrere Claudes

Eine Session kann weitere Arbeit starten. Fünf Wege, plus drei Hilfsmittel.

| Weg | Wer koordiniert | Kontext | Wann |
|---|---|---|---|
| **Subagent** (`Agent`-Tool, `agents/*.md`) | Claude, in derselben Session | eigenes Fenster, nur Zusammenfassung kommt zurück | Nebenaufgabe mit viel Ausgabe: suchen, lesen, prüfen |
| **Fork-Subagent** (`/subtask`) | Claude | Kopie des bisherigen Chats | Teilaufgabe, die den Verlauf braucht |
| **Agent View** (`claude agents`) | der Mensch | eigene Sessions im Hintergrund, eigener Worktree vor Änderungen | mehrere unabhängige Aufgaben abgeben, später nachsehen |
| **Nebensession** (Desktop-App) | der Mensch, Claude kann vorschlagen | eigene Session, sichtbar in der Seitenleiste | Aufgabe, die eigenes Ergebnis hat (Branch, PR) |
| **Agent-Team** (experimentell) | ein Lead-Claude | mehrere Sessions, gemeinsame Aufgabenliste, Nachrichten | Projekt in Teile zerlegen, Worker synchron halten |
| **Dynamischer Workflow** (`workflows/*.js`) | ein Skript | viele Subagenten, ein Ergebnis | Audit über das ganze Repo, große Migration, Befunde gegenprüfen |
| **Projekt** (claude.ai/code, Desktop) | Claude, in der Cloud | parallele Threads mit Projektanweisungen | Arbeit über Tage, Rechner darf aus sein |

Hilfsmittel: **Worktrees** geben jeder Session einen eigenen Checkout (der Starter
verbietet sie per Hardrule §4, weil sie Branches erzeugen und Aufräumen kosten;
wer sie will, streicht §4 bewusst). **Cross-Session-Messaging** lässt Sessions sich
Befunde schicken. **`/batch`** zerlegt eine große Änderung in 5 bis 30 Subagenten.

Nicht verwechseln: ein **Hintergrund-Bash-Befehl** läuft nur einen Befehl nebenher,
ohne Agent. `/fork` kopiert die ganze Session in eine Hintergrund-Session.

### Wann was

- Ein Subagent, wenn das Ergebnis in diese Session zurück muss und die Zwischenschritte
  niemanden interessieren.
- Eine Nebensession oder Agent View, wenn die Aufgabe ein eigenes Ergebnis hat und
  der Mensch sie getrennt steuern will.
- Ein Workflow, wenn mehr als eine Handvoll Agenten nötig sind oder Befunde
  gegeneinander geprüft werden sollen.
- Ein Team nur, wenn Claude selbst Arbeit verteilen soll und die Dateien sauber
  trennbar sind. Teams isolieren nicht per Worktree.

### Was der Starter daraus macht

Hardrule §2 sagt: innerhalb einer Session arbeitet ein Agent. Das ist der Standard für
Einzelentwickler, weil jeder Subagent Tokens vervielfacht und zwei Schreiber an denselben
Dateien Schaden anrichten.

Parallele Sessions sind erlaubt, wenn sie sich nicht gegenseitig behindern. Geprüft
wird vor jedem Start, nicht angenommen: Fassen sie dieselben Dateien an? Teilen sie
Git-Zustand, Ports, Dev-Server, Datenbanken oder Migrationen? Braucht eine das Ergebnis
der anderen? Ein Ja oder ein Unklar heißt nacheinander. Weil der Starter keine Worktrees
nutzt (§4), teilen sich alle Sessions ein Verzeichnis, und jede committet nur eigene Pfade.

`extras/` schaltet ein kleines Team mit hartem Budget
frei: Analyst, Entwickler, QA, Security, dazu Workflows für Slice und Entscheidung.
Wer das nutzt, liest zuerst [`extras/README.md`](../extras/README.md).

### Subagenten richtig bauen

- `description` kurz; sie lädt jede Session. Detail in den Body, der lädt erst beim Start.
- `tools` als Allowlist für Read-only-Agenten, `disallowedTools: Agent` gegen Kaskaden.
- `model` immer setzen ([`MODELLWAHL.md`](MODELLWAHL.md)). Lesen auf `haiku`, Abnahme auf `opus`.
- `memory: project` gibt einem Agenten Notizen über Sessions hinweg, committet unter `.claude/agent-memory/`.
- Hooks im Frontmatter begrenzen, was der Agent anfassen darf (Vorlage `home/hooks/guard_paths.py`).
- Subagenten starten ohne den Chatverlauf. Alles, was sie wissen müssen, steht im Prompt.
