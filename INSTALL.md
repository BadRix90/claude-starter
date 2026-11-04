# Installation

Zwei Ebenen, zwei Ziele. `home/` wird zu `~/.claude/` und gilt für alle Projekte.
`project/` wird in ein Repo kopiert und gilt dort für alle, die es klonen.
Erklärung der Ebenen: [`docs/WAS-LAEDT-WANN.md`](docs/WAS-LAEDT-WANN.md).

## Voraussetzungen

- Claude Code installiert (`claude --version`).
- Python 3.11 oder neuer im `PATH` (für die Hooks).
- Git. Unter Windows Git Bash, damit Hooks in der Shell-Form laufen.

## 1 Vorhandenes sichern

```bash
cp -r ~/.claude ~/.claude.backup-$(date +%Y%m%d)
```

Wer schon eine `~/.claude/CLAUDE.md` oder `settings.json` hat, mischt von Hand.
Der Starter überschreibt nichts automatisch.

## 2 Benutzerebene: `home/` nach `~/.claude/`

```bash
cp home/CLAUDE.md ~/.claude/CLAUDE.md
cp -r home/rules ~/.claude/rules
cp -r home/hooks ~/.claude/hooks
cp -r home/skills/* ~/.claude/skills/
cp home/statusline.py ~/.claude/statusline.py
cp home/settings.json ~/.claude/settings.json
```

`settings.erklaert.jsonc` bleibt im Starter, sie ist nur Doku.

Gibt es schon eine `settings.json`: die Blöcke `permissions.deny`, `permissions.ask`
und `hooks` übernehmen, `model` und `effortLevel` nach Wunsch.

### Windows-Hinweise

- `~` ist `%USERPROFILE%`, also `C:\Users\<name>\.claude`.
- Der Hook-Befehl `python "$HOME/.claude/hooks/guard_shell.py"` läuft in Git Bash
  und in PowerShell. Fehlt Git Bash, trägt man in `settings.json` zusätzlich
  `"shell": "powershell"` im Hook ein oder einen absoluten Pfad.
- `python` muss die richtige Installation sein. `where python` prüfen; der
  Microsoft-Store-Alias ohne Installation blockt still.

## 3 Projektebene: `project/` in ein Repo

```bash
cd <repo>
cp <starter>/project/CLAUDE.md CLAUDE.md
cp <starter>/project/SLICES.md SLICES.md
cp <starter>/project/AGENTS.md.example AGENTS.md
mkdir -p .claude/rules .claude/hooks
cp <starter>/project/.claude/settings.json .claude/settings.json
cp <starter>/project/.claude/rules/README.md .claude/rules/
cp <starter>/home/hooks/guard_shell.py .claude/hooks/
cat <starter>/project/.gitignore.example >> .gitignore
```

Dann die Platzhalter in `CLAUDE.md` und `AGENTS.md` füllen und die passende
Variante aus [`stacks/`](stacks/) nach `.claude/rules/` legen.

Optional: `CLAUDE.local.md.example` zu `CLAUDE.local.md` (nicht committen),
`.mcp.json.example` zu `.mcp.json`, `.claude/team.md.example` zu `.claude/team.md`
(nur mit [`extras/`](extras/)).

## 4 Einrichten lassen

Eine Session starten und `/einrichten` tippen. Claude fragt nach Rolle, Stack, Sprache,
Arbeitsweise, Modell, geht die Hardrules einzeln durch und liest Befehle und Branches
aus dem Repo. Er zeigt jeden Diff, bevor er schreibt. Nur `~/.claude`: `/einrichten home`.
Nur das Repo: `/einrichten projekt`.

## 5 Prüfen

Danach in derselben Session:

```
/memory          alle CLAUDE.md und Regeln gelistet?
/context         wie viel Kontext belegen die Regeln?
/doctor          Konfiguration in Ordnung?
```

Und eine Probe für die Hooks: Claude bitten, `git add .` auszuführen. Die Antwort
muss „Blockiert durch guard_shell“ enthalten.

## 6 Weiter

[`docs/ANPASSEN.md`](docs/ANPASSEN.md): dieselben Schritte von Hand, für alle, die
lieber selbst in den Dateien arbeiten oder später nachjustieren.

## Deinstallation

Dateien aus `~/.claude/` entfernen, die aus `home/` kamen, und das Backup aus Schritt 1
zurückspielen. Im Projekt die kopierten Dateien löschen. Auto-Memory bleibt unberührt.
