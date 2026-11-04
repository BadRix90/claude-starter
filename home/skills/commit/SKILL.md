---
name: commit
description: Schreibt aus dem aktuellen Diff einen Conventional Commit mit expliziten Pfaden. Nutzen bei "commit", "committe das", "mach einen Commit". Pusht nicht.
argument-hint: "[Scope oder Slice-ID]"
disable-model-invocation: true
allowed-tools: Bash(git status *), Bash(git diff *), Bash(git add *), Bash(git commit *), Bash(git log *)
---

# Commit

Regeln: `~/.claude/rules/31-git.md`. Kein Push, auch nicht auf Nachfrage im
selben Aufruf. Push ist ein eigener, ausdrücklicher Auftrag.

Hinweis des Nutzers: $ARGUMENTS

## Ablauf

1. `git status --porcelain` und `git diff --stat`. Fremde Dateien, die nicht zur
   aktuellen Aufgabe gehören, bleiben liegen und werden genannt.
2. Zusammengehörige Änderungen bestimmen. Mehr als eine logische Änderung:
   mehrere Commits, nacheinander.
3. Typ wählen: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `ci`.
   Scope: Modul oder Slice-ID. Beschreibung: Englisch, Imperativ, unter 72 Zeichen.
4. Body nur, wenn das Warum nicht aus der Beschreibung hervorgeht.
5. `git add <pfade>` mit jedem Pfad einzeln, dann `git commit -m "..." -- <pfade>`.
6. `git log --oneline -1` zeigen. Fertig.

## Nie

`git add .`, `-A`, `--all`, `git commit -a`, Umgehen von Git-Hooks, Amend auf
gepushte Commits, Secrets oder `.env` im Diff. Taucht so etwas auf: stoppen, melden.
