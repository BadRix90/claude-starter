# Hooks: Leitplanken statt Bitten

> **Für wen:** alle, die eine Regel haben, die wirklich immer gelten muss.
> **Vorlage:** [`home/hooks/guard_shell.py`](../home/hooks/guard_shell.py), Tests in [`tests/`](../tests/).
> Quelle: [Hooks-Referenz](https://code.claude.com/docs/en/hooks).
> **Geprüft gegen:** Claude Code 2.1.310, Doku-Stand 11/2026.

## Grundsatz

Eine Anweisung in `CLAUDE.md` ist eine Bitte. Claude folgt ihr meistens. Ein Hook
ist Code, der außerhalb des Modells läuft und blockt, egal was das Modell denkt.
„Nie `.env` schreiben“ gehört in einen Hook. „Antworte kurz“ gehört in eine Regel.

## Ereignisse (Auswahl)

| Ereignis | Wann | Typische Nutzung |
|---|---|---|
| `SessionStart` | Session beginnt, wird fortgesetzt oder kompaktiert (Matcher `startup`, `resume`, `clear`, `compact`, `fork`) | Arbeitsstand nach Kompaktierung zurückspielen: [`reinject.py`](../home/hooks/reinject.py) |
| `UserPromptSubmit` | Prompt abgeschickt, bevor Claude ihn sieht | Prompt prüfen oder anreichern |
| `PreToolUse` | vor jedem Werkzeugaufruf | verbotene Befehle und Pfade blocken |
| `PermissionRequest` | wenn ein Dialog erscheinen würde | automatisch entscheiden |
| `PostToolUse` | nach dem Werkzeugaufruf | Grenzen prüfen: [`check_limits.py`](../home/hooks/check_limits.py); Formatter, Linter, Logging |
| `PostToolUseFailure` | Werkzeug ist gescheitert | Diagnose anhängen |
| `Stop` | Claude ist fertig | Erinnerung an Tracking, Tests erzwingen |
| `SubagentStart`, `SubagentStop` | Subagent startet oder endet | Budget zählen |
| `PreCompact`, `PostCompact` | Kompaktierung | Stand sichern |
| `Notification` | Claude braucht Aufmerksamkeit | Desktop-Benachrichtigung |

Vollständige Liste in der Referenz, darunter auch `ConfigChange`, `FileChanged`,
`PreModelSwitch`, `WorktreeCreate`.

## Aufbau in `settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          {
            "type": "command",
            "command": "python \"$HOME/.claude/hooks/guard_shell.py\"",
            "timeout": 10,
            "statusMessage": "guard_shell prüft den Befehl"
          }
        ]
      }
    ]
  }
}
```

- `matcher`: Werkzeugname, `|` für mehrere, leer oder `*` für alle. Andere Zeichen
  machen ihn zum Regex.
- `if`: Permission-Syntax als Vorfilter, z. B. `"Bash(git *)"` oder `"Edit(*.ts)"`.
- `type`: `command` (Shell), `http` (POST), `mcp_tool`, `prompt` (ein Modellaufruf),
  `agent` (Subagent prüft etwas).
- `timeout` in Sekunden. `once: true` nur in Skill-Frontmatter.
- Hooks liegen in `~/.claude/settings.json`, `.claude/settings.json`,
  `settings.local.json`, in Plugins oder im Frontmatter von Skills und Subagenten.
  Alle registrierten Hooks laufen, sie überschreiben sich nicht.

## Eingabe und Ausgabe

Der Hook bekommt JSON auf stdin: `session_id`, `cwd`, `hook_event_name`, `tool_name`,
`tool_input` (bei Bash: `command`, bei Edit: `file_path`) und mehr.

| Exit-Code | Bedeutung |
|---|---|
| `0` | weiter. stdout wird als JSON gelesen, wenn es ein JSON-Objekt ist |
| `2` | **blocken**. stderr geht als Grund an Claude |
| anderer | Fehler, aber nicht blockend; Hinweis im Transkript |

Exit 2 blockt auch, wenn stdout `allow` sagt. Exit 1 blockt nicht. Für Policy
immer Exit 2. Bei `PostToolUse` blockt Exit 2 nichts mehr, das Werkzeug lief schon;
stderr wird Claude gezeigt.

Feinere Steuerung per JSON auf stdout mit Exit 0:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Schreibzugriff auf .env",
    "additionalContext": "Dieses Repo nutzt pytest, nicht unittest."
  }
}
```

`permissionDecision`: `allow`, `deny`, `ask`, `defer`. `updatedInput` schreibt die
Argumente um. `additionalContext` landet als Hinweis bei Claude, sachlich formuliert,
nicht als Befehl.

## Windows

- Command-Hooks laufen in Git Bash, wenn installiert, sonst in PowerShell.
  `"shell": "powershell"` erzwingt PowerShell. `$HOME` kennen beide.
- `.cmd`-Shims (npm, npx, eslint) lassen sich in Exec-Form nicht direkt starten.
  Shell-Form nutzen oder `node <skript>` aufrufen.
- PowerShell-Skripte: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File <pfad>`.
- Python-Hooks wie im Starter laufen überall gleich und brauchen kein `jq`.

## Kontext zurückgeben: Klartext oder JSON

Bei `SessionStart` und `UserPromptSubmit` nimmt Claude Code den Klartext auf stdout
direkt in den Kontext. Ein Hook, der nur etwas mitteilen will, braucht also kein JSON.
So arbeitet [`reinject.py`](../home/hooks/reinject.py). Die Grenze liegt bei 10.000
Zeichen je Feld; was darüber liegt, landet in einer Datei, und Claude bekommt nur den Pfad
und eine Vorschau.

## Zwei stille Fallen

Beide erzeugen keine Fehlermeldung. Der Hook läuft, und nichts passiert.

1. **Ausgabe aus dem Shell-Profil vor dem JSON.** Schreibt `~/.bashrc` oder `~/.zshrc`
   beim Start etwas auf die Konsole, steht das vor dem JSON des Hooks. Beginnt die
   Ausgabe nicht mit `{`, wird sie verworfen. Abhilfe: solche Ausgaben nur in
   interaktiven Shells zulassen.

   ```bash
   if [[ $- == *i* ]]; then
     echo "Shell bereit"
   fi
   ```

2. **`additionalContext` oder `permissionDecision` auf der falschen Ebene.** Beide
   gehören in `hookSpecificOutput`, zusammen mit `hookEventName`. Auf oberster Ebene
   parst das JSON fehlerfrei, und Claude Code ignoriert die Felder kommentarlos.
   Vorlage für die richtige Form: [`context_radar.py`](../home/hooks/context_radar.py).

Beides findet `claude --debug`: im Log nach `Hook output does not start with {` und
`Hook JSON output had unrecognized keys` suchen. `/hooks` zeigt, welche Hooks
überhaupt registriert sind. Matcher unterscheiden Groß- und Kleinschreibung.

## Stop-Hooks: zwei Besonderheiten

Ein `Stop`-Hook, der blockt, lässt Claude weiterarbeiten. Damit daraus keine Schleife
wird, steht im Input das Feld `stop_hook_active`: ist es `true`, läuft Claude schon wegen
eines Stop-Hooks weiter, und der Hook sollte sofort mit Exit 0 enden. Blockt ein
Stop-Hook achtmal in Folge, ohne dass Claude dazwischen ein Werkzeug aufruft, setzt
Claude Code sich darüber hinweg.

## Ideen für eigene Hooks

| Ziel | Ereignis | Skizze |
|---|---|---|
| Formatieren nach jeder Änderung | `PostToolUse`, matcher `Edit\|Write` | `ruff format <datei>` oder `prettier --write` |
| Tests erzwingen vor „fertig“ | `Stop` | prüfen, ob seit letztem Edit ein Testlauf im Transkript steht, sonst Exit 2 |
| Geschützte Dateien | `PreToolUse`, matcher `Edit\|Write` | Pfad gegen Liste prüfen (Migrationen, Lockfiles, CI) |
| Tracking nicht vergessen | `Stop` | wenn `SLICES.md` unverändert und Code geändert: Hinweis |
| Benachrichtigung | `Notification` | Desktop-Toast über `terminalSequence` oder ein Skript |
| Budget für Subagenten | `SubagentStart` | Zähler in Datei, ab Grenze Exit 2 |
| Arbeitsstand nach Kompaktierung (eingebaut) | `SessionStart`, matcher `compact` | Branch, letzte Commits, offene Änderungen und laufende Slices als Klartext auf stdout. Die `CLAUDE.md` lädt Claude Code selbst neu, der Stand ginge sonst verloren |
| Zeilengrenzen (eingebaut) | `PostToolUse`, matcher `Edit\|Write` | [`check_limits.py`](../home/hooks/check_limits.py) zählt nach jedem Schreiben. Datei über 400 oder Python-Funktion über 20 Zeilen: Exit 2, Claude bekommt die Meldung und teilt. Verglichen wird mit `HEAD`, damit Altlasten keinen ungefragten Umbau auslösen. Für TypeScript die ESLint-Regeln `max-lines` und `max-lines-per-function` |
| Kontext-Radar (eingebaut) | Statusline + `UserPromptSubmit` | Statusline schreibt `used_percentage` je Session in eine Datei, der Hook liest sie und warnt Claude ab 50 %. Kein Hook-Input enthält Token-Zahlen, deshalb der Umweg. Siehe [`AUS-DER-COMMUNITY.md`](AUS-DER-COMMUNITY.md) |

Jeder neue Hook bekommt einen Test wie in `tests/test_guard_shell.py`: Liste
verbotener Befehle, Liste erlaubter, beide müssen stimmen.
