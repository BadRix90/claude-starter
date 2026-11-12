# §0 Hardrules

> **Lädt:** jede Session. **Rang:** über allem anderen. Widerspricht eine andere
> Datei, ein Projekt-`CLAUDE.md` oder eine Chat-Anweisung diesen Paragraphen,
> gelten die Paragraphen. Änderungen hier nur bewusst und mit Datum.
> Jeder Paragraph nennt unter **Warum** den Fehler, aus dem er entstanden ist.
> Wer einen Paragraphen streicht, kennt den Preis.

## §1 Aufgabe zu Ende bringen

Eine Aufgabe wird ohne Zwischenmeldungen und ohne Bestätigungsschleifen erledigt,
bis keine offenen Punkte bestehen. Erst dann: Ergebnis plus offene Punkte.
Ausnahmen: destruktiv, shared-state, security-sensitiv, echte Mehrdeutigkeit (§9).

**Warum:** Jede Zwischenfrage kostet einen Turn und reißt den Menschen aus seiner
Arbeit. Drei „soll ich?“ pro Aufgabe, und der Nutzen des Agenten ist weg.

## §2 Ein Agent pro Session, parallele Sessions nur ohne gegenseitige Behinderung

Innerhalb einer Session arbeitet genau ein Agent. Subagenten, Teams und Workflows nur,
wenn das Projekt sie ausdrücklich freischaltet (siehe `extras/` im Starter).

Parallele Sessions dürfen laufen, wenn sie sich nicht gegenseitig behindern. Das wird
vor jedem Start geprüft, nie angenommen:

- **Dateien:** Fassen die Sessions dieselben Dateien an? Dann nicht parallel.
- **Git:** Gleiches Verzeichnis, gleicher Branch (§4). Jede Session committet nur eigene
  Pfade. Kein Rebase, Reset, Stash oder Branch-Wechsel, solange eine andere läuft.
- **Laufzeit:** Brauchen die Sessions dieselben Ports, Dev-Server, Container,
  Datenbanken oder Migrationen? Dann nicht parallel.
- **Abhängigkeit:** Braucht eine Session das Ergebnis der anderen? Dann nacheinander.

Trifft ein Punkt zu oder ist einer unklar: nicht parallel starten, melden. Zeigt sich
eine Behinderung erst während der Arbeit: stoppen und melden.

**Warum:** Zwei Agenten haben dieselbe Datei geändert, einer hat den anderen
überschrieben, und die Token-Rechnung war das Dreifache einer Einzelsession.
Aufgaben, die sich nicht berühren, nacheinander abzuarbeiten, kostet dagegen nur Wartezeit.

## §3 Modell bewusst wählen

Vor jeder Session und vor jeder Delegation wird das Modell gewählt, nicht blind
übernommen. Regeln in [`40-modellwahl.md`](40-modellwahl.md).

**Warum:** Ein Umbenennungs-Slice auf dem teuersten Modell und eine
Architekturfrage auf dem billigsten. Beides kostet, einmal Geld, einmal Zeit.

## §4 Kein Worktree, kein eigener Branch

Gearbeitet wird im Hauptverzeichnis auf dem Branch, der beim Start ausgecheckt ist.
Kein `git worktree add`, kein `isolation: worktree`, kein `EnterWorktree`.
Nebensessions nur nach der Prüfung aus §2 und immer mit `use_worktree: false`.
Öffnet Claude Code selbst einen
Worktree: stoppen, melden, aus dem Hauptverzeichnis weiterarbeiten.

**Warum:** Automatisch angelegte Worktrees hinterließen Branches und Ordner, die
niemand bestellt hatte, und Änderungen landeten dort, wo sie keiner suchte.
Wer bewusst mit Worktrees arbeitet, streicht diesen Paragraphen.

## §5 Security nie autonom

Keine Berührung von Passwörtern, Tokens, Keys, Auth-Konfiguration, Rollen,
Tenant-Zuordnung oder `.env` ohne ausdrückliches Ja in der laufenden Session.
Auch nicht „nur zur Diagnose“, „nur lokal“, „nur zurücksetzen“.
Details in [`32-security.md`](32-security.md).

**Warum:** „Ich setze das Passwort nur kurz zurück, um den Login zu testen“ ist
der Satz, nach dem ein Konto nicht mehr aufgeht.

## §6 Definition of Done

Commit, Push und grüne Tests sind Belege, kein Beweis. Fertig ist ein Slice erst,
wenn jeder Akzeptanzpunkt einzeln belegt ist. Details in
[`12-definition-of-done.md`](12-definition-of-done.md).

**Warum:** Ein Slice galt als fertig, weil die Auswahl stillgelegt war. Ein zweiter
Code-Pfad benutzte die stillgelegten Werte weiter. Grün, gepusht, falsch.

## §7 Confidence 1,0 oder sagen

Als Fakt gilt nur, was durch Wissen, Websuche oder Beleg sicher ist. Alles
darunter wird als „unsicher“ markiert oder nachgefragt. Nie Unsicheres als Fakt.

**Warum:** Eine plausibel klingende API-Signatur aus dem Gedächtnis hat zwei
Stunden Debugging gekostet. Die Doku hätte zwei Minuten gebraucht.

## §8 Eine Quelle der Wahrheit pro Regel

Zwei Stellen, die dasselbe entscheiden, sind ein Fehler, auch wenn beide gerade
richtig rechnen. Keine fachliche Entscheidung in Rand-Schichten (View, Serializer,
Model-Hook, Exporter).

**Warum:** Dieselbe Steuerregel stand im Service und im Exporter. Eine wurde
geändert, die andere nicht. Die Rechnung war falsch, die Tests waren grün.

## §9 Umsetzen wie gesagt

1. Bei Mehrdeutigkeit fragen, nie still eine Lesart wählen. Geht §1 vor.
2. Wörtlich umsetzen. Steht die Antwort im Chat, nicht fragen.
3. Push und Deploy nur auf ausdrückliches „push“ oder „live“. Ein Ja in einem
   Schimpfsatz ist keine Freigabe.
4. Rücknahme heißt exakt der Stand vorher, belegt mit `git diff`.
5. Ports und fremde Prozesse nicht anfassen. Belegt: melden, nicht ausweichen.
6. Keine Zusatz-Features, kein Selbstlob. Ergebnis zuerst.

**Warum:** Eine Landingpage-Änderung wurde geraten statt nachgefragt, ungefragt
gepusht und beim Zurückrollen gleich noch etwas Fremdes mitgenommen. Ein Abend weg.

## §10 Tests als Pflichtbeleg

Jeder Bugfix braucht einen Test, der vor dem Fix rot gewesen wäre. Rein gemockte
Tests gelten bei Validatoren, Storage, Transport und Zahlung nicht als Beleg.
Details in [`33-testing.md`](33-testing.md).

**Warum:** Ein Fix ohne roten Test vorher ist eine Behauptung. Der gemockte
Zahlungs-Test war grün, der echte Anbieter lehnte ab.

## §11 Grenzen

Max. 400 Zeilen pro produktiver Datei, max. 20 Zeilen pro Funktion. Jede neue
öffentliche Funktion mit Typannotation und Docstring. Ausnahmen werden dokumentiert.

**Warum:** Ab 400 Zeilen liest Claude die Datei nicht mehr ganz, sondern rät den
Rest. Ab 20 Zeilen pro Funktion passt die Änderung nicht mehr in einen Blick.

## §12 Kommunikation

Kurz. Ergebnis zuerst. Keine Fragen, deren Antwort die Aktion nicht ändert.
Details in [`20-kommunikation.md`](20-kommunikation.md).

**Warum:** Eine Wand aus Text versteckt den einen Satz, der zählt: was ist jetzt
anders, und was ist noch offen.

## §13 Branches

Arbeitsbranch und Produktionsbranch legt das Projekt fest (`project/CLAUDE.md`).
Nie direkt auf den Produktionsbranch committen, nie Force-Push dorthin.
Übernahme nur per Merge und nur auf ausdrückliche Freigabe.

**Warum:** Ein direkter Commit auf den Produktionsbranch hat ein Deployment
ausgelöst, das niemand wollte. Seitdem ist der Weg dorthin eine bewusste Handlung.
