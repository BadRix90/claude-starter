# Workflow einer Aufgabe

> **Lädt:** jede Session. **Vorher lesen:** [`00-hardrules.md`](00-hardrules.md).
> **Danach:** [`11-slices.md`](11-slices.md) für die Einordnung, [`12-definition-of-done.md`](12-definition-of-done.md) für den Abschluss.

## Reihenfolge, immer

1. **Analyse zuerst.** Ist-Zustand verstehen, betroffene Dateien mit Pfad und
   Zeile benennen. Noch kein Code. Bei unbekanntem Code: erst der Graph
   ([`41-graphify.md`](41-graphify.md)), dann gezielt lesen.
2. **Problem in Klartext.** Was ist kaputt oder fehlt, ohne Jargon.
3. **Lösungsvorschlag an der Wurzel.** Keine Pflasterarbeit: kein `try/except pass`,
   kein Sonderfall-`if` um ein Strukturproblem, kein Workaround, der die Ursache
   stehen lässt.
4. **Diff zeigen, dann anwenden.** Bei Aufgaben, die mehr als eine Datei berühren,
   oder bei allem, was das Verhalten ändert.
5. **Umsetzen im Scope.** Genau X liefern, kein Y oder Z, keine Gelegenheits-Refactors.
6. **Tests sofort nach jeder Änderung.** Nicht am Ende gesammelt.
7. **Ergebnis in Klartext.** Was ist jetzt anders, was wurde wie verifiziert.

## Selbsttest vor jeder Rückfrage

Kenne ich die Antwort schon? Gibt es realistisch mehr als eine Antwort? Ändert die
Antwort, was ich tue? Ist eine davon „nein“, ist die Frage überflüssig.

Überflüssige Fragen: „soll ich committen?“ nach einem Commit-Auftrag · „soll ich
auch X?“ wenn X offensichtlich dazugehört · „A oder B?“ mit klarer Empfehlung ·
Fragen, deren Antwort im Repo oder in der Doku steht.

Berechtigte Fragen: destruktiv, shared-state, security-sensitiv, echte Mehrdeutigkeit,
bei der jede Lesart zu deutlich anderer Arbeit führt.

## Confidence-Score

Vor jeder Aktion: Score 0 bis 1. Nur 1,0 wird ausgeführt. Unter 1,0 wird gefragt,
höchstens eine Frage pro Antwort. Trigger für unter 1,0: „vermutlich“, mehrere
plausible Optionen, Aktion würde mehr tun als beauftragt, destruktiv oder
shared-state ohne genau diesen Auftrag.

## Nichts offen lassen

Keine „TODO später“, keine halben Slices. Was nicht in den Slice gehört, wird als
Tracking-Zeile festgehalten, nicht verschwiegen. Der Abschluss endet mit
„keine offenen Punkte“ oder mit der Liste, was offen ist und warum.
