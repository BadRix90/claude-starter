---
paths:
  - "**/*.py"
  - "frontend/**/*.ts"
  - "frontend/**/*.html"
---
# Performance

> Lädt bei Python-Dateien und im Frontend. Baut auf [`django.md`](django.md) und
> [`angular.md`](angular.md) auf. Abschnitte 1 bis 3 gelten im Backend, 4 und 5 im Frontend.

## 1 N+1-Abfragen

- Jedes QuerySet, das Relationen ausliefert, nutzt `select_related` (FK, OneToOne)
  oder `prefetch_related` (M2M, Reverse-FK).
- Das Laden passiert im Service-/Selector-Layer, nie im Serializer.
- Jeder List-Endpoint hat einen Test mit `assertNumQueries`.
- Keine Queries in Schleifen oder `SerializerMethodField`s.

## 2 Datenbank-Indizes

- Felder aus `filter()`, `order_by()` und Joins bekommen einen Index in `Meta.indexes`.
- Bei Multi-Tenant-Tabellen steht `tenant_id` im Composite-Index vorn.
- Ein Index wird nur mit `EXPLAIN ANALYZE` als Beleg angelegt.
- Große Tabellen: `AddIndexConcurrently` in eigener Migration.

## 3 Caching mit Redis

- Gecacht werden nur lesehäufige, selten geänderte Daten.
- Jeder Cache-Key enthält die Tenant-ID, jeder Eintrag eine TTL.
- Invalidierung erfolgt im Service-Layer beim Schreibvorgang.
- Die Datenbank bleibt die Quelle der Wahrheit; fällt Redis aus, läuft die App weiter.

## 4 Lazy Loading

- Bilder laufen über `NgOptimizedImage` (`ngSrc`) mit `width` und `height`.
- Nur das LCP-Bild erhält `priority`, alle anderen laden lazy.
- Schwere Komponenten unterhalb des sichtbaren Bereichs: `@defer`.
- Feature-Routen werden per `loadComponent` nachgeladen.

## 5 Optimistische UI

- Ablauf: Snapshot des Signals, sofortiges Update, Request, bei Fehler Rollback plus
  Fehlermeldung.
- Erlaubt nur für umkehrbare Aktionen (Toggle, Favorit, Sortierung).
- Verboten für finanziell oder rechtlich relevante Aktionen; dort wartet die UI auf
  die Serverbestätigung.
- Die Serverantwort überschreibt den optimistischen Zustand.
