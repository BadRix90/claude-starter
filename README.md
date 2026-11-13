# Claude Starter

[![CI](https://github.com/BadRix90/claude-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/BadRix90/claude-starter/actions/workflows/ci.yml)

Ich arbeite täglich mit [Claude Code](https://code.claude.com/docs/en/overview) und
habe dabei viele Fehler gemacht. Fehler, die Tokens, Nerven und Stress gekostet haben.
Die habe ich nach und nach zusammen mit Claude abgestellt, bis es richtig gut lief.
Dieses Repo ist das Ergebnis: ein Startpunkt für alle, die mit Claude Code anfangen
oder ihr Setup aufräumen wollen.

Es gibt viele solcher Setups da draußen, und einige erzählen Unsinn. Dieses hier kommt
aus eigener Erfahrung, nicht aus Blogposts. Es ist keine perfekte Lösung. Es ist ein
Anfang mit Regeln, die sich bewährt haben, Hooks, die wirklich blocken, und der
Erklärung, wann Claude was liest. Forken, mit dem eigenen Claude einrichten, streichen,
was nicht passt.

**Was drin ist:** ein `~/.claude`, das in jedem Projekt gilt, eine Projektvorlage für
das Repo, Stack-Varianten, ein Skill, mit dem dein Claude dich befragt und sich selbst
einrichtet, und acht kurze Texte zu Kontext, Modi, Sessions, Modellen, Hooks und Gedächtnis.

**Was nicht drin ist:** Magie. Jede Regel hier ist aus einem konkreten Fehler
entstanden. Tote Regeln verwirren Claude, also weg damit, wenn sie nicht zu dir passen.

## In fünf Minuten

1. **„Use this template“** oben rechts oder Fork.
2. [`INSTALL.md`](INSTALL.md): `home/` nach `~/.claude/`, `project/` in dein Repo.
3. Eine Session starten und **`/einrichten`** tippen. Dein Claude stellt dir Fragen,
   eine nach der anderen: wer du bist, wie du arbeitest, welche Hardrules du behalten
   willst, welches Modell, welcher Stack. Danach füllt er die Dateien aus und zeigt dir
   den Diff, bevor er schreibt. Wer lieber selbst Hand anlegt: [`docs/ANPASSEN.md`](docs/ANPASSEN.md).
4. `/memory` tippen. Deine Regeln müssen in der Liste stehen.

## Das Prinzip in einem Bild

```
~/.claude/                        gilt überall             <repo>/                        gilt im Projekt
├── CLAUDE.md   (< 60 Zeilen)     Identität, Rangordnung   ├── CLAUDE.md  (< 100 Zeilen)  Stack, Befehle, Branches
├── rules/      (eine je Thema)   lädt jede Session        ├── AGENTS.md                  Verbraucher, Invarianten
│   ├── 00-hardrules.md           gewinnt immer            ├── SLICES.md                  Stand der Arbeit
│   ├── 10-workflow.md …                                   └── .claude/
├── settings.json                 Modell, deny, Hooks          ├── settings.json          Team-Permissions
├── hooks/      (Python)          Leitplanken, kein Bitten     ├── rules/  (pfadgebunden) Stack-Regeln
├── statusline.py                 Kontext-Radar ab 50 %        └── hooks/
└── skills/     /einrichten /slice /audit /commit
```

Kurz in `CLAUDE.md`, ein Thema je Regel, harte Grenzen in Hooks, Referenzwissen in
Skills, Lesearbeit in Subagenten. Warum das so ist, steht in
[`docs/WAS-LAEDT-WANN.md`](docs/WAS-LAEDT-WANN.md).

## Was wo liegt

| Ordner | Inhalt | Wird zu |
|---|---|---|
| [`home/`](home/) | `CLAUDE.md`, 10 Regeln, `settings.json` mit Erklärung, 5 Hooks, Statusline mit Kontext-Radar, 4 Skills (`/einrichten`, `/slice`, `/audit`, `/commit`) | `~/.claude/` |
| [`project/`](project/) | Projekt-`CLAUDE.md`, `AGENTS.md`, `SLICES.md`, `.mcp.json`, Projekt-Settings, Vorlagen | `<repo>/` |
| [`stacks/`](stacks/) | Varianten: generisch, Django + Angular, Astro | `<repo>/.claude/rules/` |
| [`extras/`](extras/) | Agenten-Team (5 Rollen), Workflows, Manager-Skill. Opt-in. | `~/.claude/agents/`, `workflows/`, `skills/` |
| [`docs/`](docs/) | die Erklärtexte, siehe unten | zum Lesen |
| [`tests/`](tests/) | Tests für Hooks und Konfiguration (`python -m pytest tests/ -q`), laufen bei jedem Push und Pull Request auf Linux und Windows | bleibt hier |
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
| [`DATENSCHUTZ.md`](docs/DATENSCHUTZ.md) | Was Claude Code im Klartext auf der Platte ablegt, wie man es begrenzt und löscht |
| [`ANPASSEN.md`](docs/ANPASSEN.md) | Reihenfolge nach dem Fork |
| [`AUS-DER-COMMUNITY.md`](docs/AUS-DER-COMMUNITY.md) | Ideen von anderen, geprüft und eingebaut oder als offen markiert, mit Namen |
| [`QUELLEN.md`](docs/QUELLEN.md) | Alle Doku-Links, Werkzeuge, Vergleichs-Repos |

## Die Regeln, in einem Absatz

Eine Aufgabe wird zu Ende gebracht, ohne Zwischenfragen, außer bei Destruktivem,
Security und echter Mehrdeutigkeit. Analyse vor Code. Problem in Klartext. Lösung
an der Wurzel, kein Pflaster. Genau der Scope, kein Beifang. Tests nach jeder
Änderung, Bugfix nur mit vorher rotem Test. Commit mit expliziten Pfaden, Push nur
auf Wort. Fertig ist, was je Akzeptanzpunkt belegt ist, nicht was grün ist. Dateien
bis 400, Funktionen bis 20 Zeilen, vom Hook geprüft. Erst der Graph, dann die Datei.
Kurz antworten, Ergebnis zuerst.
Alles in [`home/rules/`](home/rules/), die Hardrules in
[`00-hardrules.md`](home/rules/00-hardrules.md).

## Woher das kommt

Aus einem echten `~/.claude`, das über Monate in Django-, Angular- und Astro-Projekten
gewachsen ist, ohne die Teile, die nur mich betreffen. Die Regeln zu Definition of Done,
negativer Gegenprobe und Runtime-Pfad-Audit entstanden, nachdem ein Slice als
„fertig“ galt, während ein zweiter Code-Pfad die neue Regel noch umging. Die
Hooks entstanden, nachdem `git add .` ein drittes Mal Fremddateien committet hatte.

## Ideen, Rückmeldung, Mitmachen

Wenn du etwas hast, das bei dir besser läuft, eine Regel, einen Hook, einen Skill,
eine Erklärung, die fehlt: schreib mir. Ich nehme gern auf, was sich bewährt, und
teste es selbst, bevor es hier landet.

- Direkt: Kay Dietrich auf LinkedIn, <https://www.linkedin.com/in/kaydietrich/>.
- Issues und Pull Requests hier im Repo, Regeln dazu in [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Lizenz

MIT, siehe [`LICENSE`](LICENSE). Nimm, was du brauchst. Ein Hinweis auf die Quelle freut.
