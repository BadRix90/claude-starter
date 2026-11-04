# Stack-Varianten

> Jede Variante ist ein Ordner mit einem `CLAUDE.md`-Abschnitt und Regeln für
> `.claude/rules/`. Inhalt in das Projekt kopieren, Platzhalter füllen.
> Die Varianten ersetzen `project/` nicht, sie ergänzen es.

| Variante | Für | Enthält |
|---|---|---|
| [`generic/`](generic/) | jedes Projekt | minimale Regeln ohne Framework-Bezug |
| [`django-angular/`](django-angular/) | Django-Backend + Angular-Frontend | Schichtenmodell, Angular-Konventionen, SCSS-Struktur mit Kontrastregeln |
| [`astro/`](astro/) | Marketing- und Content-Seiten | Content-Collections, Bilder, Performance |

## Einbau

```bash
cp stacks/django-angular/rules/*.md <repo>/.claude/rules/
# den Abschnitt aus stacks/django-angular/CLAUDE.md in <repo>/CLAUDE.md übernehmen
```

Pfadgebundene Regeln (`paths:` im Frontmatter) laden nur bei passenden Dateien.
Die Globs an das eigene Layout anpassen.

## Eigene Variante

Ordner anlegen, `CLAUDE.md` und `rules/` hinein, eine Zeile in dieser Tabelle.
Gern als Pull Request zurück in den Starter.
