# Projekt-Hooks

`.claude/settings.json` dieses Projekts ruft `.claude/hooks/guard_shell.py` auf.
Die Datei liegt im Bauplan unter `home/hooks/guard_shell.py` und wird hierher
kopiert, wenn das ganze Team dieselben Leitplanken bekommen soll:

```bash
cp <bauplan>/home/hooks/guard_shell.py .claude/hooks/
```

Wer nur global absichern will, löscht den `hooks`-Block aus der Projekt-`settings.json`
und verlässt sich auf `~/.claude/settings.json`. Hooks aus beiden Ebenen laufen
sonst doppelt, was harmlos, aber unnötig ist.

Weitere Hook-Ideen und die Exit-Code-Semantik: `docs/HOOKS.md` im Bauplan.
