# Abschnitt für das Projekt-CLAUDE.md: Django + Angular

<!-- In <repo>/CLAUDE.md unter "Stack" einfügen. Versionen mit Datum pflegen. -->

## Stack (Stand: <Datum>)

- Python `<3.x>`, Django `<6.x>`, Django REST Framework
- Angular `<21.x>`, TypeScript `<6.x>`, Standalone Components
- PostgreSQL `<18.x>`, Node.js `<24.x LTS>`

## Befehle

```bash
cd backend && python -m pytest -q          # Tests Backend
cd backend && ruff check . && ruff format   # Lint Backend
cd frontend && npm test                      # Tests Frontend
cd frontend && ng serve --port <port>        # Dev-Server, Port steht hier, nicht raten
```

## Architektur in einem Satz

Backend nach dem HackSoftware-Styleguide: `apis.py` nur HTTP, `services.py`
schreibt, `selectors.py` liest, `models.py` definiert. Frontend standalone,
`inject()`, Observables per `async`-Pipe. Details in `.claude/rules/`.

## Ports

| App | Port |
|---|---|
| Frontend | `<4200>` |
| Backend | `<8000>` |

Belegter Port: Prozess melden, nicht ausweichen, nicht beenden.
