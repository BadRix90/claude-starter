---
paths:
  - "**/*.scss"
---
# SCSS-Struktur und Kontrast

> Lädt bei SCSS-Dateien. Gilt für jedes Frontend, nicht nur Angular.

## Es gibt nie eine Sammeldatei

| Datei | Inhalt | Regel |
|---|---|---|
| `_tokens.scss` | CSS Custom Properties: Farben, Radien, Schatten, Abstände | einzige Stelle mit Farbwerten; HEX, auch für Transparenz (`#rrggbbaa`), nie `rgba()` |
| `_variables.scss` | Sass-Variablen: Breakpoints, z-index, feste Maße | alles, was zur Buildzeit gebraucht wird |
| `_mixins.scss` | wiederkehrende Blöcke | zweimal dasselbe geschrieben = Mixin |
| `_fonts.scss` | `@font-face`, selbst gehostet | nie über ein CDN |
| `_base.scss` | Reset, `html`/`body`, Grundtypografie | keine Komponenten |
| `_<thema>.scss` | je ein Thema: `_shell`, `_forms`, `_cards` | max. 400 Zeilen, sonst teilen |
| `_index.scss` | nur `@forward` in fester Reihenfolge | Tokens und Variablen zuerst |
| `styles.scss` | nur `@use './index';` | sonst nichts |

- Nie eine Farbe direkt im Stylesheet, immer `var(--token)`.
- Nie eine Schriftfamilie direkt, immer `var(--font-*)`.
- Media Queries über Sass-Variable oder Mixin, nie mit einer Zahl im Code.
- Neues Thema: neue Datei plus eine Zeile in `_index.scss`.

## Kontrast

- Text und Hintergrund eines Elements nie gleiche oder ähnliche Farbe.
- Auf einer gefüllten Akzentfläche steht immer der dunkle Text-Token (`--on-accent`),
  nie der Akzent-Text-Token.
- Mindestkontrast 4,5:1 (WCAG AA) für Text, 3:1 für Icons und funktionale Rahmen
  (Eingabefelder). Rein dekorative Rahmen (Panels, Trennlinien) dürfen dünner sein;
  der Zustand muss dann über Text oder Fläche erkennbar sein, nie allein über den Rahmen.
- Jedes interaktive Element in allen Zuständen prüfen: normal, hover, fokus, aktiv,
  aktiv+hover, aktiv+fokus, disabled.
- Farbpaare als Tokens führen (`--accent` mit `--on-accent`), nie pro Komponente neu wählen.

## Design folgt der Referenz

Ein neues Modul übernimmt Radien, Schriften, Abstände und Linien aus dem
Stylesheet der Referenz-App (Pfad im Projekt-`CLAUDE.md`). Werte lesen, nicht
schätzen, als Tokens ablegen. Vor „fertig“ `getComputedStyle` im Browser gegen
die Referenz vergleichen. Keine eigene Variante erfinden.
