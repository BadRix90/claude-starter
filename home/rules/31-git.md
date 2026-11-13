# Git

> **Lädt:** jede Session. **Hardrules:** §4 (Branch, Worktree), §9.3 (Push nur auf Wort),
> §13 (Produktionsbranch) in [`00-hardrules.md`](00-hardrules.md).
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

## Push

- Nie Force-Push, auch nicht mit Lease.
- Abgelehnter Push: `git fetch`, `git rebase origin/<branch>`, erneut. Kein Force.

## Rücknahme

Der Vergleich für §9.4 ist `git diff <ausgangscommit>`. Nichts Fremdes mit
zurückrollen. Fremde ungetrackte oder geänderte Dateien bleiben liegen.
