# Code-Qualität

> **Lädt:** jede Session. **Hardrule:** §8 und §11 in [`00-hardrules.md`](00-hardrules.md).
> **Stack-Details:** liegen im Projekt (`.claude/rules/`), nicht hier.

## Grenzen

- Max. 400 Zeilen pro produktiver Datei. Wird es mehr, wird das Thema geteilt.
- Max. 20 Zeilen pro Funktion.
- Jede neue öffentliche Funktion: Typannotationen und Docstring.
- Imports sortiert (isort-kompatibel oder das Äquivalent des Stacks).

## Schichten

- Business-Logik in Services, Lesezugriffe in Selectors. Nie in View, Serializer,
  Model-Hook, Template oder Exporter.
- Keine zweite Berechnung derselben Semantik. Eine Quelle der Wahrheit pro Regel.
- Keine impliziten fachlichen Defaults ohne benannte Policy.

## Verboten

- `console.log`, `print`-Debugging und auskommentierter Code im Produktionscode.
- Hardcodierte Secrets, Credentials, Hostnamen.
- Externe API-Calls mit Nutzerdaten an Anbieter außerhalb der vereinbarten
  Rechtsräume (DSGVO). Das Projekt-`CLAUDE.md` nennt die erlaubten Anbieter.
- Workarounds, die eine Ursache stehen lassen ([`10-workflow.md`](10-workflow.md), Schritt 3).

## Stil

Lesbar vor clever. Namen sagen, was ein Ding ist. Kommentare sagen, warum,
nicht was. Ein Kommentar, der den Code wiederholt, wird gelöscht.
