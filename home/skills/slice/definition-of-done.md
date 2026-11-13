# Definition of Done

> **Lädt:** mit dem Skill `/slice`, und wenn Hardrule §6 vor einem Abschluss hierher schickt.
> **Hardrule:** §6 in `~/.claude/rules/00-hardrules.md`. **Ablauf:** [`SKILL.md`](SKILL.md).
> **Verbraucherliste:** steht pro Projekt in `AGENTS.md` (Vorlage: `project/AGENTS.md.example`).

## Grundsatz

Commit, Push, Migration und grüne Tests sind Belege, kein Beweis. DONE ist ein Slice
erst, wenn jeder explizite Akzeptanzpunkt einzeln mit konkretem Beleg erfüllt ist.
„Tests grün“ genügt für keinen einzigen Punkt.

- Fehlt ein Beleg: Status `OPEN` oder `PARTIAL`, nicht aus Plausibilität ableiten.
- Ein offener Punkt wandert nicht per Folgekarte aus dem Slice. Folgekarte nur,
  wenn der Punkt nachweislich außerhalb des Scopes lag.
- Ein während der Arbeit gefundener Fehler blockiert DONE, wenn er Ziel, Invariante,
  Akzeptanzpunkt oder Runtime-Pfad betrifft.
- Scope wird nie still verengt. Jede Scope-Änderung ist eine ausdrückliche Entscheidung.

## Zustände

| Zustand | Bedeutung |
|---|---|
| `OPEN` | nicht begonnen |
| `IN_PROGRESS` | Analyse oder Umsetzung läuft |
| `CODE_READY` | implementiert, nicht abgenommen |
| `VERIFIED` | Akzeptanzpunkte lokal nachgewiesen |
| `RELEASED` | im Produktionsbranch |
| `PROD_VERIFIED` | Verhalten auf Produktion nachgewiesen |
| `BLOCKED` | konkretes Hindernis dokumentiert |
| `PARTIAL` | nur ein Teil erfüllt, nie „Done“ |
| `OBSOLETE` | Anforderung nachweislich nicht mehr relevant |

Stufen sind nicht synonym: implemented → committed → pushed → released → deployed → prod-verified.

## Pflichtmatrix (vor der Umsetzung anlegen, am Ende füllen)

| Akzeptanzpunkt | Relevante Pfade | Positivtest | Negativtest | Historischer Fall | Ergebnis |
|---|---|---|---|---|---|

Alle Verbraucher aus `AGENTS.md` prüfen. Nicht betroffene Pfade als N/A begründen, nicht weglassen.

## Negative Gegenprobe, sieben Fragen

1. Was muss funktionieren?
2. Was muss ausdrücklich abgelehnt werden?
3. Was darf nicht automatisch abgeleitet werden?
4. Was passiert bei fehlenden Fakten?
5. Was passiert mit bestehenden Datensätzen?
6. Gibt es einen zweiten Pfad, der die Regel umgeht?
7. Was passiert bei erneutem Speichern oder erneutem Verarbeiten?

## Runtime-Pfad-Audit, sieben Fragen

1. Wo beginnt der Vorgang? 2. Welche Services werden gerufen? 3. Welche alternativen
Einstiege gibt es? 4. Wer konsumiert das Ergebnis? 5. Gibt es alte parallele
Implementierungen? 6. Kann gespeicherter Output später als Eingabe gelesen werden?
7. Können inaktive oder historische Datensätze in neue Vorgänge gelangen?

Import-Linter beweisen Struktur, nicht gleiche Geschäftsregel.

## Implementierer ist nicht Abnehmer

Originalanforderung einfrieren → Matrix → implementieren → Tests und Gegenproben →
kontextfreie Read-only-Abnahme gegen die Originalkarte → erst dann DONE.
Die Abnahme beginnt bei der Karte, nicht bei der eigenen Zusammenfassung.

## Dokumentationskonsistenz

Vor DONE vergleichen: Karte · Tracking · Architektur-Doku · OpenAPI und SDK ·
Benutzertexte · Code · Migrationen · Produktionsstand. Bei Widerspruch sind Code
und Laufzeit die Wahrheit, der Widerspruch wird ausgewiesen.

## Abschlussbericht, festes Format

```
Slice:
Ausgangsproblem:
Explizite Akzeptanzpunkte:
Erfüllte Punkte mit Beleg:
Nicht erfüllte Punkte:
Nicht geprüfte Punkte:
Geänderte Runtime-Pfade:
Geprüfte Verbraucher:
Migrationen:
Tests und genaue Ergebnisse:
Manuelle Gegenproben:
Branch-/Release-/Prod-Stand:
Dokumentationsabgleich:
Neu entdeckte Risiken:
Endstatus:
```

Für DONE sind „Nicht erfüllte Punkte“ und „Nicht geprüfte Punkte“ leer.
