---
name: einrichten
description: Richtet den Claude Starter für diese Person und dieses Projekt ein. Claude stellt Fragen, eine nach der anderen, und füllt danach CLAUDE.md, Regeln, Settings und Projektdateien aus. Nutzen direkt nach der Installation oder wenn der Nutzer "einrichten", "Setup", "stell dich auf mich ein" sagt.
argument-hint: "[home | projekt | alles]"
disable-model-invocation: true
---

# Einrichten

Du richtest den Starter ein, indem du fragst, nicht indem du rätst. Eine Frage pro
Nachricht, mit Antwortvorschlägen, wo es welche gibt. Nach jeder Antwort sagst du
in einem Satz, was du daraus machst. Du schreibst erst, wenn ein Abschnitt
abgefragt ist, und zeigst vorher, welche Datei sich wie ändert.

Umfang: $ARGUMENTS (leer = alles; `home` nur `~/.claude`, `projekt` nur dieses Repo)

Bestehende Dateien überschreibst du nie still. Gibt es schon eine `~/.claude/CLAUDE.md`
oder ein Projekt-`CLAUDE.md` mit Inhalt: zeigen, fragen, mischen.

## Teil A: die Person (`~/.claude`)

**A1 Rolle und Stack.** „Womit arbeitest du hauptsächlich?“ Freitext. Daraus:
Abschnitt „Wer ich bin“ in `~/.claude/CLAUDE.md`, drei Zeilen.

**A2 Sprache.** Antworten auf Deutsch oder Englisch? Code bleibt Englisch.
Daraus: `language` in `settings.json` und die Zeile in `CLAUDE.md`.

**A3 Hardrules durchgehen.** Lies `~/.claude/rules/00-hardrules.md` vor, Paragraph
für Paragraph. Je Paragraph zuerst in einem Satz, **welcher Fehler ohne diese Regel
passiert** (steht unter „Warum“ im Paragraphen), dann die Frage: behalten, ändern,
streichen? Nacheinander, nicht als Block. Wer streicht, streicht mit Wissen, nicht aus
Bequemlichkeit. Du redest niemandem eine Regel ein, du nennst nur den Preis.
Besonders nachhaken bei:
- §2 (ein Agent pro Session): Will die Person Subagenten nutzen? Wenn ja, Satz ergänzen.
  Parallele Sessions sind nach Prüfung erlaubt; wer sie nie will, streicht den Absatz.
- §4 (kein Worktree): Arbeitet sie bewusst mit Worktrees? Dann streichen.
- §9.3 (Push nur auf Wort): Wird gestrichen, dann `Bash(git push *)` aus `ask`
  nehmen, damit Regel und Settings zusammenpassen.
- §13 (Branches): Welches Branch-Modell? Kommt ins Projekt-`CLAUDE.md`.
Gestrichene Paragraphen löschst du, du kommentierst sie nicht aus. Was gestrichen
wurde, listest du am Ende der Einrichtung einmal auf, mit dem genannten Preis.

**A4 Arbeitsweise.** „Soll ich vor jeder Änderung einen Diff zeigen, oder reicht es,
wenn du hinterher `git diff` liest?“ Daraus: `permissions.defaultMode`
(`default` oder `acceptEdits`) in `settings.json`. Erkläre den Unterschied in zwei Sätzen,
Details in `docs/MODI-UND-SESSIONS.md`.

**A5 Modell und Kosten.** „Eher schnell und günstig (`sonnet`), eher gründlich (`opus`),
oder je nach Aufgabe wechseln?“ Daraus: `model` und `effortLevel` in `settings.json`.
Bei „wechseln“: `sonnet` als Default, Hinweis auf `/model` und `docs/MODELLWAHL.md` im Starter.

**A6 Push-Verhalten.** „Darf ich pushen, wenn du ‚push‘ sagst, oder willst du jedes
Mal eine Rückfrage?“ Daraus: `Bash(git push *)` in `permissions.ask` behalten oder
nach `allow` verschieben.

**A7 graphify.** „Willst du graphify nutzen (Knowledge Graph statt Grep-Serien)?“
Nein: `41-graphify.md` löschen, Zeile in `CLAUDE.md` entfernen. Ja: Installationsbefehl
aus `INSTALL.md` im Starter zeigen, nicht selbst ausführen.

**A8 Extras.** „Brauchst du ein Agenten-Team (Analyst, Entwickler, QA)?“ Standard ist
nein. Bei ja: auf `extras/README.md` verweisen, nichts kopieren, bis die Person es
gelesen hat.

Dann: alle Änderungen an `~/.claude` als Diff zeigen, Freigabe abwarten, schreiben.

## Teil B: das Projekt (nur wenn ein Repo offen ist)

**B1 Was ist das.** Zwei Sätze für den Kopf des Projekt-`CLAUDE.md`. Vorschlag aus
README, `package.json` oder `pyproject.toml` ableiten und bestätigen lassen.

**B2 Stack und Versionen.** Aus den Manifesten lesen, nicht fragen. Nur bestätigen
lassen und das Datum setzen.

**B3 Befehle.** Test, Lint, Dev-Server. Aus `Makefile`, `package.json`, `pyproject.toml`
ableiten, vorschlagen, bestätigen lassen. Ports ausdrücklich fragen.

**B4 Branches.** Arbeitsbranch und Produktionsbranch. Aus `git branch -a` vorschlagen.

**B5 Stack-Variante.** Passende Regeln aus `stacks/` anbieten (generic, django-angular,
astro). Pfad-Globs an das Layout anpassen und zeigen, bevor sie nach `.claude/rules/`
kommen.

**B6 Verbraucher.** „Wer liest und schreibt die zentralen Daten? API, Jobs, Exporte,
Frontend, externe SDKs?“ Daraus: Tabelle in `AGENTS.md`. Lieber zwei echte Zeilen als
sechs geratene.

**B7 Erlaubte externe Dienste.** „Wohin dürfen Nutzerdaten? KI-Anbieter, Region?“
Daraus: Abschnitt im Projekt-`CLAUDE.md`. Leer ist eine gültige Antwort.

**B8 Erster Slice.** „Woran arbeitest du als Nächstes?“ Daraus: erste Zeile in `SLICES.md`
mit Typ und ID.

Dann: Diff aller Projektdateien zeigen, Freigabe abwarten, schreiben.
`.gitignore` um die Zeilen aus `project/.gitignore.example` ergänzen, wenn sie fehlen.

## Teil C: Prüfen

1. `/memory` ausführen lassen oder selbst prüfen, welche Dateien geladen sind.
2. Zusammenfassen, was jetzt gilt: fünf Zeilen, keine Wiederholung der Dateien.
3. Probe: „Bitte mich, `git add .` auszuführen.“ Der Hook muss blocken. Blockt er nicht,
   Pfad im Hook-Eintrag prüfen (`settings.erklaert.jsonc`).
4. Nennen, was offen blieb, oder: „Keine offenen Punkte.“

## Nie

Fragen stellen, deren Antwort in einer Datei steht. Mehr als eine Frage pro Nachricht.
Dateien schreiben, ohne den Diff gezeigt zu haben. Regeln hinzufügen, die die Person
nicht genannt hat. Secrets oder `.env` anfassen.
