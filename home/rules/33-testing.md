# Tests

> **Lädt:** jede Session. **Hardrule:** §10 in [`00-hardrules.md`](00-hardrules.md).
> **Abnahme:** `~/.claude/skills/slice/definition-of-done.md`.

## Mindestumfang

- Jeder Service: Happy Path, mindestens zwei Grenzfälle, ein Fehlerfall.
- Jeder Fix an historischen Daten: Test für bestehende und für neue Datensätze.
- Migrationen: auf leerer und auf bestehender Datenbank prüfen.
- OpenAPI, Runtime-Response und SDK-Typen gemeinsam prüfen, nie einzeln.

## Was nicht als Beleg gilt

- Ausschließlich gemockte Tests bei Validatoren, Storage, Transport, Zahlungsanbietern.
- „Verwandte Tests sind grün“ als Beleg für einen anderen Akzeptanzpunkt.
- Ein Testlauf, dessen Ausgabe nicht im Bericht steht.

## Wann laufen

Der Befehl steht im Projekt-`CLAUDE.md` oder in `.claude/team.md`.

## Frontend und E2E

Komponententests pro Komponente. E2E für kritische Nutzerpfade. UI-Änderungen
zusätzlich im Browser prüfen, nicht nur per Test.
