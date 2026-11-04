---
paths:
  - "src/**/*.astro"
  - "src/content/**"
  - "astro.config.*"
---
# Astro

> Lädt bei Astro-Dateien und Content. Baut auf `~/.claude/rules/30-code-quality.md` auf.

- Inhalt in Content Collections mit Schema (`src/content.config.ts`). Kein Text
  hart in Komponenten, der sich redaktionell ändert.
- Null JavaScript im Client, bis ein Grund besteht. Islands nur mit `client:`-Direktive
  und Begründung im Commit.
- Bilder über `astro:assets`, nie `<img src="/…">` für Inhalte.
- Jede Seite hat `title`, `description`, kanonische URL, Open-Graph-Bild.
- Layouts in `src/layouts/`, Komponenten in `src/components/`, eine Komponente je Datei.
- Build ohne Warnungen. Lighthouse Performance und Accessibility über 90, sonst kein Merge.
- Formulare senden an einen dokumentierten Endpunkt, nie an einen US-Dienst mit
  personenbezogenen Daten ohne Prüfung (DSGVO).
