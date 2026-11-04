# Git

> **Lädt:** jede Session. **Hardrules:** §4, §9.3, §13 in [`00-hardrules.md`](00-hardrules.md).
> **Durchgesetzt von:** [`../hooks/guard_shell.py`](../hooks/guard_shell.py).

## Commits

- Conventional Commits, Englisch:
  `feat|fix|refactor|test|docs|chore|ci(scope): short description`
- Beispiele: `feat(invoices): add PDF attachment`, `fix(validation): correct checksum`.
- Pfade immer explizit: `git add <datei> <datei>`, `git commit -- <pfade>`.
  Nie `git add .`, `-A`, `--all`, nie `git commit -a`.
- Ein Commit pro logischer Änderung. Kein „WIP“, kein „fixes“.
- Git-Hooks werden nie umgangen. Schlägt ein Hook fehl, wird die Ursache behoben.
- Kein Amend auf gepushte Commits.

## Branches

- Kein eigener Branch, kein Worktree (§4). Gearbeitet wird auf dem Branch, der beim
  Start ausgecheckt ist. Welcher das ist, steht im Projekt-`CLAUDE.md`.
- Nie direkt auf den Produktionsbranch. Übernahme nur per Merge und nur auf
  ausdrückliche Freigabe („merge“, „deploy“, „live“).

## Push

- Nur auf ausdrückliches „push“. Ein Commit-Auftrag ist kein Push-Auftrag.
- Nie Force-Push, auch nicht mit Lease.
- Abgelehnter Push: `git fetch`, `git rebase origin/<branch>`, erneut. Kein Force.

## Rücknahme

Exakt der Stand vorher, mit `git diff <ausgangscommit>` belegt. Nichts Fremdes
mit zurückrollen. Fremde ungetrackte oder geänderte Dateien bleiben liegen.

## Parallele Sessions im selben Verzeichnis

Jede Session committet nur ihre eigenen Pfade. Niemand räumt die Dateien
einer anderen Session auf.
