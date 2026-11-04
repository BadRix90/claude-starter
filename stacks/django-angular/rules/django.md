---
paths:
  - "backend/**/*.py"
  - "**/*.py"
---
# Django

> Lädt bei Python-Dateien. Baut auf `~/.claude/rules/30-code-quality.md` auf.
> Vorbild: HackSoftware Django Styleguide.

## Schichten, verbindlich

| Datei | Enthält | Enthält nie |
|---|---|---|
| `apis.py` | HTTP-Layer: Request annehmen, Serializer, Service rufen, Response | Business-Logik, Queries mit Fachbedeutung |
| `services.py` | alle Schreiboperationen und Geschäftsregeln als Funktionen | HTTP, Serializer |
| `selectors.py` | Lesezugriffe, QuerySets, Filter | Schreibzugriffe |
| `serializers.py` | Ein- und Ausgabeformen | Berechnungen, Entscheidungen |
| `models.py` | Datendefinition, einfache Properties | Geschäftslogik, `save()`-Hooks mit Fachlogik |

Keine Business-Logik in Views, Models, Serializers, Signals oder Management-Commands.
Ein Command ruft einen Service.

## Pflicht in Services und Selectors

- Typannotationen an jeder Funktion, Docstring nach PEP 257.
- Ein Service tut eine Sache. Über 20 Zeilen: aufteilen.
- Transaktionen explizit (`transaction.atomic`), nie implizit über Model-Hooks.
- Tenant- oder Mandantenfilter im Selector, nie im View nachgeschoben.

## Migrationen

- Auf leerer und auf bestehender Datenbank prüfen.
- Datenmigrationen als eigene Migration, mit Rückweg.
- Nie `Edit(**/migrations/**)` durch Claude ohne ausdrücklichen Auftrag (`permissions.deny` im Projekt).

## Tests

`pytest` mit `pytest-django`. Service: Happy Path, zwei Grenzfälle, ein Fehlerfall.
API: Statuscode, Shape, Berechtigung. Validatoren und Storage nie nur gemockt.
