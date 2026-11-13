# Code-Qualität

> **Lädt:** jede Session. **Hardrule:** §8 und §11 in [`00-hardrules.md`](00-hardrules.md).
> **Stack-Details:** liegen im Projekt (`.claude/rules/`), nicht hier.

## Form

- Jede neue öffentliche Funktion: Typannotationen und Docstring.
- Imports sortiert (isort-kompatibel oder das Äquivalent des Stacks).
- Meldet [`../hooks/check_limits.py`](../hooks/check_limits.py) eine Überschreitung
  aus §11: sofort teilen, nicht am Ende.

## Schichten

- Business-Logik in Services, Lesezugriffe in Selectors. Nie in View, Serializer,
  Model-Hook, Template oder Exporter.
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
