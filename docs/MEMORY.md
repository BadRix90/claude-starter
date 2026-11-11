# Gedächtnis: CLAUDE.md, Regeln, Auto-Memory

> **Für wen:** alle, die sich fragen, warum Claude etwas vergisst oder sich etwas
> falsch merkt. **Dazu:** [`WAS-LAEDT-WANN.md`](WAS-LAEDT-WANN.md).
> Quelle: [Memory-Doku](https://code.claude.com/docs/en/memory).
> **Geprüft gegen:** Claude Code 2.1.310, Doku-Stand 11/2026.

## Zwei Systeme

| | `CLAUDE.md` und `rules/` | Auto-Memory |
|---|---|---|
| Schreibt | der Mensch | Claude |
| Enthält | Anweisungen und Regeln | Gelerntes: Vorlieben, Korrekturen, Projektfakten |
| Ort | Repo und `~/.claude` | `~/.claude/projects/<projekt>/memory/` |
| Lädt | jede Session, vollständig | jede Session, erste 200 Zeilen oder 25 KB von `MEMORY.md` |
| Geteilt | per Git | nein, pro Rechner und Repo |

Beides ist Kontext, keine Durchsetzung. Was immer gelten muss, braucht einen Hook
([`HOOKS.md`](HOOKS.md)).

## CLAUDE.md gut schreiben

- Unter 200 Zeilen je Datei. Länger heißt: weniger Befolgung, mehr Kontext.
- Nur Fakten, die jede Session braucht: Befehle, Konventionen, Layout, „immer X“.
- Mehrschrittige Abläufe in einen Skill. Regeln für einen Teil des Codes in eine
  pfadgebundene Regel.
- Jede Regel hat eine Geschichte: sie entstand aus einem konkreten Fehler. Regeln
  ohne Grund werden ignoriert. Generische Weisheiten („schreib sauberen Code“) raus.
- Widersprüche vermeiden: zwei gegensätzliche Anweisungen, und Claude wählt eine.
  `/doctor prompt-audit` findet sie.
- `@pfad`-Imports gliedern, sparen aber keinen Kontext.

## Regeln in `.claude/rules/`

Eine Datei je Thema, sprechender Name. Mit `paths:` im Frontmatter lädt die Regel
erst, wenn Claude eine passende Datei anfasst:

```markdown
---
paths:
  - "backend/**/*.py"
---
```

Regeln in Unterordnern werden rekursiv gefunden. Symlinks funktionieren, fragen aber
einmal pro Projekt nach Freigabe. Persönliche Regeln für alle Projekte liegen in
`~/.claude/rules/`, so wie im Starter.

## Auto-Memory steuern

Claude legt pro Repo einen Ordner mit Notizdateien an und pflegt `MEMORY.md` als Index.
Nur der Index lädt automatisch; die Einzeldateien liest Claude bei Bedarf.

Was hineingehört: Korrekturen („nicht X, sondern Y, weil …“), Vorlieben, Umgebungsfakten,
die nicht im Repo stehen (Pfade, Werkzeugmacken), Verweise auf externe Systeme.

Was nicht hineingehört: alles, was im Repo steht (Code-Struktur, History, `CLAUDE.md`),
Secrets, Dinge, die nur für eine Session gelten.

Pflege: Index kurz halten (eine Zeile je Notiz). Falsche Notizen löschen, nicht
überschreiben lassen. Bei Umzug auf einen neuen Rechner den Ordner mitnehmen oder
bewusst leer starten. `/memory` zeigt, was geladen ist.

## Gedächtnis für Subagenten

Ein Subagent mit `memory: project` im Frontmatter bekommt einen eigenen Ordner
`.claude/agent-memory/<name>/`, der committet wird. `user` legt ihn unter `~/.claude`,
`local` im Repo ohne Commit. Gut für einen QA-Agenten, der Muster über Slices hinweg
sammelt. Vorsicht: der Agent bekommt damit Schreibrechte auf diesen Ordner.

## Kompaktierung überleben

Nach `/compact` liest Claude Code `CLAUDE.md` im Projekt-Root neu. Pfadgebundene Regeln
laden wieder, sobald eine passende Datei berührt wird. Chat-Anweisungen gehen verloren.
Ein Abschnitt „Compact Instructions“ in `CLAUDE.md` sagt, was die Zusammenfassung
behalten soll. Der Starter nennt dort: Slice, Akzeptanzpunkte, geänderte Dateien,
offene Punkte.

Den Arbeitsstand selbst (Branch, letzte Commits, offene Änderungen, laufende Slices)
spielt der Hook [`reinject.py`](../home/hooks/reinject.py) nach jeder Kompaktierung zurück.
