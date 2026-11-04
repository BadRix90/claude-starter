# Claude Starter

Ein forkbares Starter-Setup für [Claude Code](https://code.claude.com/docs/en/overview):
Regeln, Hooks, Skills, Agenten und die Erklärung dazu, wann Claude was liest.
Auf Deutsch. Ohne persönliche Pfade. Gedacht für Leute, die mit Claude effizient
arbeiten wollen, statt jede Session neu zu erklären, wie sie ticken.

**Was du bekommst:** ein `~/.claude`, das in jedem Projekt gilt, eine Projektvorlage,
die mit dem Team im Repo liegt, Stack-Varianten zum Kopieren, und acht kurze
Erklärtexte zu Kontext, Modi, Sessions, Modellen, Hooks und Gedächtnis.

**Was du nicht bekommst:** Magie. Jede Regel hier ist aus einem konkreten Fehler
entstanden. Was nicht zu dir passt, streichst du. Tote Regeln verwirren Claude.

## In fünf Minuten

1. **„Use this template“** oben rechts oder Fork.
2. [`INSTALL.md`](INSTALL.md): `home/` nach `~/.claude/`, `project/` in dein Repo.
3. [`docs/ANPASSEN.md`](docs/ANPASSEN.md): Identität, Hardrules, Modell, in dieser Reihenfolge.
4. Eine Session starten, `/memory` tippen. Deine Regeln müssen in der Liste stehen.

## Das Prinzip in einem Bild

```
~/.claude/                        gilt überall             <repo>/                        gilt im Projekt
├── CLAUDE.md   (< 60 Zeilen)     Identität, Rangordnung   ├── CLAUDE.md  (< 100 Zeilen)  Stack, Befehle, Branches
├── rules/      (eine je Thema)   lädt jede Session        ├── AGENTS.md                  Verbraucher, Invarianten
│   ├── 00-hardrules.md           gewinnt immer            ├── SLICES.md                  Stand der Arbeit
│   ├── 10-workflow.md …                                   └── .claude/
├── settings.json                 Modell, deny, Hooks          ├── settings.json          Team-Permissions
├── hooks/      (Python)          Leitplanken, kein Bitten     ├── rules/  (pfadgebunden) Stack-Regeln
└── skills/     /slice /audit /commit                          └── hooks/
```

Kurz in `CLAUDE.md`, ein Thema je Regel, harte Grenzen in Hooks, Referenzwissen in
Skills, Lesearbeit in Subagenten. Warum das so ist, steht in
[`docs/WAS-LAEDT-WANN.md`](docs/WAS-LAEDT-WANN.md).

## Was wo liegt

| Ordner | Inhalt | Wird zu |
|---|---|---|
| [`home/`](home/) | `CLAUDE.md`, 13 Regeln, `settings.json` mit Erklärung, 2 Hooks, 3 Skills | `~/.claude/` |
| [`project/`](project/) | Projekt-`CLAUDE.md`, `AGENTS.md`, `SLICES.md`, `.mcp.json`, Projekt-Settings, Vorlagen | `<repo>/` |
| [`stacks/`](stacks/) | Varianten: generisch, Django + Angular, Astro | `<repo>/.claude/rules/` |
| [`extras/`](extras/) | Agenten-Team (5 Rollen), Workflows, Manager-Skill. Opt-in. | `~/.claude/agents/`, `workflows/`, `skills/` |
| [`docs/`](docs/) | die Erklärtexte, siehe unten | zum Lesen |
| [`tests/`](tests/) | Tests für die Hooks (`python -m pytest tests/ -q`) | bleibt hier |
| [`tools/`](tools/) | `check_links.py` prüft alle Markdown-Links | bleibt hier |

## Die Erklärtexte, in Lesereihenfolge

| Datei | Beantwortet |
|---|---|
| [`WIE-CLAUDE-CODE-FUNKTIONIERT.md`](docs/WIE-CLAUDE-CODE-FUNKTIONIERT.md) | Was ist die Schleife, was ist das Kontextfenster, was passiert bei Kompaktierung, wie leben Sessions |
| [`WAS-LAEDT-WANN.md`](docs/WAS-LAEDT-WANN.md) | Welche Datei lädt wann, was kostet Kontext, wohin gehört welche Anweisung |
| [`MODI-UND-SESSIONS.md`](docs/MODI-UND-SESSIONS.md) | Manuell, Accept Edits, Plan, Auto, Bypass. Und: Subagenten, Hintergrund-Sessions, Nebensessions, Teams, Workflows |
| [`MODELLWAHL.md`](docs/MODELLWAHL.md) | Fable, Opus, Sonnet, Haiku, Effort-Stufen, Kosten, Subagenten-Modelle |
| [`HOOKS.md`](docs/HOOKS.md) | Ereignisse, Exit-Codes, JSON-Ausgabe, Windows, Ideen für eigene Hooks |
| [`MEMORY.md`](docs/MEMORY.md) | `CLAUDE.md` gegen Auto-Memory, Regeln, Gedächtnis für Agenten |
| [`ANPASSEN.md`](docs/ANPASSEN.md) | Reihenfolge nach dem Fork |
| [`QUELLEN.md`](docs/QUELLEN.md) | Alle Doku-Links, Werkzeuge, Vergleichs-Repos |

## Die Regeln, in einem Absatz

Eine Aufgabe wird zu Ende gebracht, ohne Zwischenfragen, außer bei Destruktivem,
Security und echter Mehrdeutigkeit. Analyse vor Code. Problem in Klartext. Lösung
an der Wurzel, kein Pflaster. Genau der Scope, kein Beifang. Tests nach jeder
Änderung, Bugfix nur mit vorher rotem Test. Commit mit expliziten Pfaden, Push nur
auf Wort. Fertig ist, was je Akzeptanzpunkt belegt ist, nicht was grün ist. Modell
bewusst wählen. Erst der Graph, dann die Datei. Kurz antworten, Ergebnis zuerst.
Alles in [`home/rules/`](home/rules/), die Hardrules in
[`00-hardrules.md`](home/rules/00-hardrules.md).

## Woher das kommt

Aus einem echten `~/.claude`, das über Monate in Django-, Angular- und Astro-Projekten
gewachsen ist, bereinigt um alles Persönliche. Die Regeln zu Definition of Done,
negativer Gegenprobe und Runtime-Pfad-Audit entstanden, nachdem ein Slice als
„fertig“ galt, während ein zweiter Code-Pfad die neue Regel noch umging. Die
Hooks entstanden, nachdem `git add .` ein drittes Mal Fremddateien committet hatte.

## Mitmachen, Ideen, Rückmeldung

- Issues und Pull Requests hier im Repo, Regeln dazu in [`CONTRIBUTING.md`](CONTRIBUTING.md).
- Direkt an Kay Dietrich: <https://www.linkedin.com/in/kaydietrich/>.
  Erfahrungen, Fragen, „bei mir geht das so besser“: alles willkommen.

## Lizenz

MIT, siehe [`LICENSE`](LICENSE). Nimm, was du brauchst. Ein Hinweis auf die Quelle freut.
