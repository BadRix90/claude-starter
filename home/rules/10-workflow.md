# Workflow einer Aufgabe

> **Lädt:** jede Session. **Vorher lesen:** [`00-hardrules.md`](00-hardrules.md).
> **Slices:** Ablauf, Präfixe und Abschluss liegen im Skill `/slice`
> (`~/.claude/skills/slice/`), nicht hier.

## Reihenfolge, immer

1. **Analyse zuerst.** Ist-Zustand verstehen, betroffene Dateien mit Pfad und
   Zeile benennen. Noch kein Code. Bei unbekanntem Code: erst der Graph
   ([`41-graphify.md`](41-graphify.md)), dann gezielt lesen.
2. **Problem in Klartext.** Was ist kaputt oder fehlt, ohne Jargon.
3. **Lösungsvorschlag an der Wurzel.** Keine Pflasterarbeit: kein `try/except pass`,
   kein Sonderfall-`if` um ein Strukturproblem, kein Workaround, der die Ursache
   stehen lässt.
4. **Direkt anwenden.** Vorab zeigen und auf Freigabe warten nur in den vier
   Fällen aus §1. Sonst steht der Diff im Ergebnis.
5. **Umsetzen im Scope** (§9.6).
6. **Tests nach jeder Änderung**, nicht am Ende gesammelt ([`33-testing.md`](33-testing.md)).
7. **Ergebnis in Klartext.** Was ist jetzt anders, was wurde wie verifiziert.

## Wann fragen

Nur in den vier Fällen aus §1, höchstens eine Frage pro Antwort. Vor jeder
Rückfrage der Selbsttest: Kenne ich die Antwort schon? Gibt es realistisch mehr als
eine Antwort? Ändert die Antwort, was ich tue? Ist eine davon „nein“, ist die Frage
überflüssig.

Überflüssige Fragen: „soll ich committen?“ nach einem Commit-Auftrag · „soll ich
auch X?“ wenn X offensichtlich dazugehört · „A oder B?“ mit klarer Empfehlung ·
Fragen, deren Antwort im Repo oder in der Doku steht.

Unsicherheit über einen Fakt ist kein Grund zu fragen, sondern nachzusehen: Repo,
Doku, Websuche ([`21-recherche.md`](21-recherche.md)). Bleibt sie, wird sie im
Ergebnis als unsicher markiert (§7).

## Ein Thema pro Session

Pro Session genau ein Slice. Eine neue Aufgabe mitten in der Arbeit bekommt eine
neue Session oder wird als Hotfix (H) mit-committet und genannt. Der Session-Titel
beginnt mit der Slice-ID, dann ein kurzes Thema: `F8 Rechnungen — Upload-Dialog`.

## Nichts offen lassen

Keine „TODO später“, keine halben Slices. Was nicht in den Slice gehört, wird als
Tracking-Zeile festgehalten, nicht verschwiegen. Der Abschluss endet mit
„keine offenen Punkte“ oder mit der Liste, was offen ist und warum.
