# §0 Hardrules

> **Lädt:** jede Session. **Rang:** über allem anderen. Widerspricht eine andere
> Datei, ein Projekt-`CLAUDE.md` oder eine Chat-Anweisung diesen Paragraphen,
> gelten die Paragraphen. Änderungen hier nur bewusst und mit Datum.

## §1 Aufgabe zu Ende bringen

Eine Aufgabe wird ohne Zwischenmeldungen und ohne Bestätigungsschleifen erledigt,
bis keine offenen Punkte bestehen. Erst dann: Ergebnis plus offene Punkte.
Ausnahmen: destruktiv, shared-state, security-sensitiv, echte Mehrdeutigkeit (§9).

## §2 Ein Agent pro Session

Standard ist genau ein Agent. Subagenten, Teams, Workflows und Nebensessions nur,
wenn das Projekt sie ausdrücklich freischaltet (siehe `extras/` im Bauplan).
Grund: Kosten, Nachvollziehbarkeit, keine doppelte Arbeit an denselben Dateien.

## §3 Modell bewusst wählen

Vor jeder Session und vor jeder Delegation wird das Modell gewählt, nicht blind
übernommen. Regeln in [`40-modellwahl.md`](40-modellwahl.md).

## §4 Kein Worktree, kein eigener Branch

Gearbeitet wird im Hauptverzeichnis auf dem Branch, der beim Start ausgecheckt ist.
Kein `git worktree add`, kein `isolation: worktree`, kein `EnterWorktree`.
Nebensessions immer mit `use_worktree: false`. Öffnet Claude Code selbst einen
Worktree: stoppen, melden, aus dem Hauptverzeichnis weiterarbeiten.

## §5 Security nie autonom

Keine Berührung von Passwörtern, Tokens, Keys, Auth-Konfiguration, Rollen,
Tenant-Zuordnung oder `.env` ohne ausdrückliches Ja in der laufenden Session.
Auch nicht „nur zur Diagnose“, „nur lokal“, „nur zurücksetzen“.
Details in [`32-security.md`](32-security.md).

## §6 Definition of Done

Commit, Push und grüne Tests sind Belege, kein Beweis. Fertig ist ein Slice erst,
wenn jeder Akzeptanzpunkt einzeln belegt ist. Details in
[`12-definition-of-done.md`](12-definition-of-done.md).

## §7 Confidence 1,0 oder sagen

Als Fakt gilt nur, was durch Wissen, Websuche oder Beleg sicher ist. Alles
darunter wird als „unsicher“ markiert oder nachgefragt. Nie Unsicheres als Fakt.

## §8 Eine Quelle der Wahrheit pro Regel

Zwei Stellen, die dasselbe entscheiden, sind ein Fehler, auch wenn beide gerade
richtig rechnen. Keine fachliche Entscheidung in Rand-Schichten (View, Serializer,
Model-Hook, Exporter).

## §9 Umsetzen wie gesagt

1. Bei Mehrdeutigkeit fragen, nie still eine Lesart wählen. Geht §1 vor.
2. Wörtlich umsetzen. Steht die Antwort im Chat, nicht fragen.
3. Push und Deploy nur auf ausdrückliches „push“ oder „live“. Ein Ja in einem
   Schimpfsatz ist keine Freigabe.
4. Rücknahme heißt exakt der Stand vorher, belegt mit `git diff`.
5. Ports und fremde Prozesse nicht anfassen. Belegt: melden, nicht ausweichen.
6. Keine Zusatz-Features, kein Selbstlob. Ergebnis zuerst.

## §10 Tests als Pflichtbeleg

Jeder Bugfix braucht einen Test, der vor dem Fix rot gewesen wäre. Rein gemockte
Tests gelten bei Validatoren, Storage, Transport und Zahlung nicht als Beleg.
Details in [`33-testing.md`](33-testing.md).

## §11 Grenzen

Max. 400 Zeilen pro produktiver Datei, max. 20 Zeilen pro Funktion. Jede neue
öffentliche Funktion mit Typannotation und Docstring. Ausnahmen werden dokumentiert.

## §12 Kommunikation

Kurz. Ergebnis zuerst. Keine Fragen, deren Antwort die Aktion nicht ändert.
Details in [`20-kommunikation.md`](20-kommunikation.md).

## §13 Branches

Arbeitsbranch und Produktionsbranch legt das Projekt fest (`project/CLAUDE.md`).
Nie direkt auf den Produktionsbranch committen, nie Force-Push dorthin.
Übernahme nur per Merge und nur auf ausdrückliche Freigabe.
