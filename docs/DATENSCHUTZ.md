# Datenschutz: was Claude Code auf der Platte ablegt

> **Für wen:** alle, die mit Kundendaten, Zugangsdaten oder vertraulichem Code arbeiten.
> **Dazu:** [`HOOKS.md`](HOOKS.md) für die Durchsetzung, [`home/rules/32-security.md`](../home/rules/32-security.md) für die Regel.
> Quellen: [.claude-Verzeichnis, Abschnitt „Application data“](https://code.claude.com/docs/en/claude-directory), [Settings](https://code.claude.com/docs/en/settings).
> **Geprüft gegen:** Claude Code 2.1.310, Doku-Stand 11/2026.

## Der Punkt, den viele übersehen

Claude Code speichert jede Session im Klartext. Alles, was durch ein Werkzeug läuft,
steht danach unverschlüsselt in einer Datei unter `~/.claude/projects/`:

- Inhalte gelesener Dateien, also auch eine `.env`, wenn Claude sie lesen durfte
- Ausgaben von Befehlen, also auch ein Token, das ein Skript auf die Konsole schreibt
- eingefügter Text aus der Zwischenablage
- der Systemprompt, die Werkzeugdefinitionen und die geladenen `CLAUDE.md`-Dateien

Geschützt ist das nur durch die Dateirechte des Betriebssystems. Wer das Benutzerkonto
lesen kann, kann die Transkripte lesen. Ein Backup des Home-Verzeichnisses nimmt sie mit.

## Was wo liegt

| Pfad unter `~/.claude/` | Inhalt | Wird gelöscht |
|---|---|---|
| `projects/<projekt>/<session>.jsonl` | vollständiges Transkript | nach `cleanupPeriodDays` (Standard 30) |
| `projects/<projekt>/<session>/tool-results/` | große Werkzeugausgaben | mit dem Transkript |
| `file-history/<session>/` | Stand von Dateien vor jeder Änderung | nach `cleanupPeriodDays` |
| `paste-cache/` | große Einfügungen | nach `cleanupPeriodDays` |
| `history.jsonl` | jeder getippte Prompt mit Projektpfad | **nie automatisch** |
| `projects/<projekt>/memory/` | Auto-Memory | nie automatisch |
| Transkripte aus Desktop-App und Cowork | wie oben | **nie**, außer `desktopSessionCleanupPeriodDays` ist gesetzt |

## Was der Starter schon tut

- `permissions.deny` in [`home/settings.json`](../home/settings.json) sperrt das Lesen und
  Ändern von `.env`, `.pem`, `.key` und `id_rsa` über die Datei-Werkzeuge. Was Claude
  nicht liest, landet nicht im Transkript.
- [`home/hooks/guard_shell.py`](../home/hooks/guard_shell.py) blockt Schreib- und
  Lesezugriffe auf `.env` über die Shell: `cat`, `head`, `tail`, `type`, `Get-Content`,
  `grep`, `sed` und verwandte Befehle. Vorlagen wie `.env.example` bleiben lesbar.
- `cleanupPeriodDays` steht auf 30.

**Grenze:** Die Deny-Regeln greifen bei den Datei-Werkzeugen, der Shell-Guard bei den
üblichen Lesebefehlen. Beides ist eine Leitplanke, keine Sandbox. Ein Skript, das die
Datei selbst öffnet und ausgibt, oder ein Programm, das beim Start seine Konfiguration
loggt, kommt daran vorbei. `source .env` bleibt erlaubt, weil dabei nichts ausgegeben wird.

## Was du zusätzlich einstellen kannst

| Ziel | Einstellung |
|---|---|
| Transkripte kürzer aufbewahren | `"cleanupPeriodDays": 7` in `settings.json`. Minimum 1, der Wert 0 ist ungültig |
| Desktop- und Cowork-Transkripte begrenzen | `"desktopSessionCleanupPeriodDays": 30`, ab Claude Code 2.1.248 |
| Gar keine Transkripte und keine Prompt-History | Umgebungsvariable `CLAUDE_CODE_SKIP_PROMPT_HISTORY=1`. Dann gibt es auch kein `--resume` |
| Einzelner Lauf ohne Speicherung | `claude -p "..." --no-session-persistence` |
| Weitere Geheimnisse sperren | eigene `deny`-Einträge, etwa `Read(**/secrets/**)` oder `Read(**/*.pfx)` |

## Aufräumen

Alles zu einem Projekt löschen, erst als Probelauf:

```bash
claude purge ~/pfad/zum/repo --dry-run
```

Dann ohne `--dry-run`. Der Befehl zeigt den Plan und fragt einmal nach. Er entfernt
Transkripte, Auto-Memory, Aufgabenlisten, Datei-Snapshots, die passenden Zeilen in
`history.jsonl` und den Projekteintrag in `~/.claude.json`. `--all` nimmt alle Projekte.
Vor Version 2.1.288 hieß der Befehl `claude project purge`.

Nicht erfasst: `shell-snapshots/`, `backups/` (bis zu fünf alte Kopien von
`~/.claude.json`) und das Scratchpad im Temp-Verzeichnis.

## Drei Dinge, die man wissen sollte

1. **`/heapdump` nie teilen.** Die `.heapsnapshot`-Datei enthält das ganze Gespräch und
   alle Zugangsdaten, die der Prozess im Speicher hatte. Für Fehlerberichte nur die
   `-diagnostics.json` anhängen.
2. **`settings.local.json` und Git.** Legt Claude Code die Datei selbst an, trägt es
   `**/.claude/settings.local.json` in die **globale** Git-Ausschlussdatei ein, nicht in
   die `.gitignore` des Repos. Wer die Datei von Hand anlegt, muss sie selbst ignorieren.
   `CLAUDE.local.md` wird nie automatisch ignoriert. Die Vorlage
   [`project/.gitignore.example`](../project/.gitignore.example) deckt beide ab.
3. **Ein Geheimnis im Transkript ist verbrannt.** Stand ein Schlüssel einmal in einer
   Ausgabe, hilft Löschen der Datei nur lokal. Der Schlüssel wurde an die API gesendet
   und gehört rotiert.
