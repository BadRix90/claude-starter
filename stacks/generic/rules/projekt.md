# Projektregeln, generisch

> Lädt in jeder Session dieses Repos. Baut auf `~/.claude/rules/30-code-quality.md` auf.

- Neue Module bekommen einen Docstring oder Kopfkommentar: was, warum, wer ruft es.
- Öffentliche Schnittstellen ändern sich nur mit Migrationspfad und Eintrag im Changelog.
- Abhängigkeiten nur mit Begründung im Commit-Body. Keine Dependency für fünf Zeilen Code.
- Fehler werden an der Grenze behandelt (API, CLI, UI), innen laufen sie durch.
