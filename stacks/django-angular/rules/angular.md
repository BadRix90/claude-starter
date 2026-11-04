---
paths:
  - "frontend/**/*.ts"
  - "frontend/**/*.html"
---
# Angular

> Lädt bei TypeScript- und Template-Dateien im Frontend.
> Baut auf `~/.claude/rules/30-code-quality.md` auf.

## Verbindlich

- Nur Standalone Components. Keine NgModules außer zum Bootstrapping.
- `inject()` statt Constructor-Injection.
- Observables im Template per `async`-Pipe. Manuelles `subscribe` nur mit
  `takeUntilDestroyed()`.
- Kein HTTP-Aufruf in einer Komponente. Immer über einen Service.
- Signals für lokalen UI-Zustand, Observables für Streams. Nicht mischen ohne Grund.
- `console.log` ist im Produktionscode verboten.

## Struktur

```
src/app/
  core/        Singletons: Auth, Interceptors, Guards
  shared/      wiederverwendbare Komponenten, Pipes, Directives
  features/    je Feature ein Ordner mit Routen, Komponenten, Services
```

Eine Komponente, eine Datei je Sorte (`.ts`, `.html`, `.scss`, `.spec.ts`).
Über 400 Zeilen: Komponente teilen.

## Tests

`TestBed` oder Spectator je Komponente. Services mit `HttpTestingController`.
E2E mit Playwright für kritische Pfade. UI-Änderungen zusätzlich im Browser prüfen.
