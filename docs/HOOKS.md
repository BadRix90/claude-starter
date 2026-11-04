# Hooks: Leitplanken statt Bitten

> **Für wen:** alle, die eine Regel haben, die wirklich immer gelten muss.
> **Vorlage:** [`home/hooks/guard_shell.py`](../home/hooks/guard_shell.py), Tests in [`tests/`](../tests/).
> Quelle: [Hooks-Referenz](https://code.claude.com/docs/en/hooks).

## Grundsatz

Eine Anweisung in `CLAUDE.md` ist eine Bitte. Claude folgt ihr meistens. Ein Hook
ist Code, der außerhalb des Modells läuft und blockt, egal was das Modell denkt.
„Nie `.env` schreiben“ gehört in einen Hook. „Antworte kurz“ gehört in eine Regel.

## Ereignisse (Auswahl)

| Ereignis | Wann | Typische Nutzung |
|---|---|---|
| `SessionStart` | Session beginnt | Branch und `git status` ausgeben, Kontext laden |
| `UserPromptSubmit` | Prompt abgeschickt, bevor Claude ihn sieht | Prompt prüfen oder anreichern |
| `PreToolUse` | vor jedem Werkzeugaufruf | verbotene Befehle und Pfade blocken |
| `PermissionRequest` | wenn ein Dialog erscheinen würde | automatisch entscheiden |
| `PostToolUse` | nach dem Werkzeugaufruf | Formatter, Linter, Logging |
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

## Ideen für eigene Hooks

| Ziel | Ereignis | Skizze |
|---|---|---|
| Formatieren nach jeder Änderung | `PostToolUse`, matcher `Edit\|Write` | `ruff format <datei>` oder `prettier --write` |
| Tests erzwingen vor „fertig“ | `Stop` | prüfen, ob seit letztem Edit ein Testlauf im Transkript steht, sonst Exit 2 |
| Geschützte Dateien | `PreToolUse`, matcher `Edit\|Write` | Pfad gegen Liste prüfen (Migrationen, Lockfiles, CI) |
| Tracking nicht vergessen | `Stop` | wenn `SLICES.md` unverändert und Code geändert: Hinweis |
| Benachrichtigung | `Notification` | Desktop-Toast über `terminalSequence` oder ein Skript |
| Budget für Subagenten | `SubagentStart` | Zähler in Datei, ab Grenze Exit 2 |

Jeder neue Hook bekommt einen Test wie in `tests/test_guard_shell.py`: Liste
verbotener Befehle, Liste erlaubter, beide müssen stimmen.
