# Was lädt wann: wer liest welche Datei

> **Für wen:** alle, die wissen wollen, warum eine Anweisung nicht ankommt oder
> warum der Kontext voll ist. **Vorher:** [`WIE-CLAUDE-CODE-FUNKTIONIERT.md`](WIE-CLAUDE-CODE-FUNKTIONIERT.md).
> Quellen: [Memory](https://code.claude.com/docs/en/memory), [.claude-Verzeichnis](https://code.claude.com/docs/en/claude-directory), [Erweiterungen](https://code.claude.com/docs/en/features-overview).
> **Geprüft gegen:** Claude Code 2.1.310, Doku-Stand 11/2026.

## Die Ebenen

| Ebene | Ort | Gilt für | Committet |
|---|---|---|---|
| Verwaltet | `managed-settings.json` (Organisation) | alle Nutzer | durch die IT |
| Benutzer | `~/.claude/` | alle Projekte dieser Person | nein |
| Projekt | `<repo>/CLAUDE.md`, `<repo>/.claude/` | alle, die das Repo klonen | ja |
| Lokal | `<repo>/CLAUDE.local.md`, `.claude/settings.local.json` | diese Person, dieses Repo | nie |

Der Starter liefert `home/` für die Benutzerebene und `project/` für die Projektebene.

## Wann was in den Kontext kommt

| Datei | Lädt | Kostet Kontext | Darum |
|---|---|---|---|
| `CLAUDE.md` (alle Ebenen) | Session-Start, vollständig | jede Anfrage | unter 200 Zeilen halten |
| `.claude/rules/*.md` ohne `paths:` | Session-Start, vollständig | jede Anfrage | ein Thema je Datei |
| `.claude/rules/*.md` mit `paths:` | erst wenn Claude eine passende Datei anfasst | nur dann | Stack-Regeln hierhin |
| `CLAUDE.md` in Unterordnern | wenn Claude dort Dateien liest | nur dann | für Monorepos |
| `@pfad`-Imports in `CLAUDE.md` | zusammen mit der importierenden Datei | wie `CLAUDE.md` | sparen keinen Kontext |
| Auto-Memory `MEMORY.md` | Session-Start, erste 200 Zeilen oder 25 KB | jede Anfrage | Index kurz halten |
| Skill-Beschreibungen | Session-Start | wenig, jede Anfrage | präzise `description` |
| Skill-Inhalt (`SKILL.md`) | bei `/name` oder wenn Claude die Beschreibung passend findet | nur dann | Referenzwissen hierhin |
| Skill mit `disable-model-invocation: true` | nur bei `/name` | null bis dahin | für Workflows mit Nebenwirkungen |
| Subagent-Beschreibungen | Session-Start | wenig | kurz halten, Detail in den Body |
| Subagent-Body | wenn der Agent startet, in dessen eigenem Kontext | isoliert | Lesearbeit auslagern |
| MCP-Server | Namen beim Start, Schemas bei Nutzung | gering | Tool-Suche ist Standard |
| Hooks | beim Ereignis, außerhalb des Modells | null, außer sie geben Text zurück | Leitplanken hierhin |
| Output-Style | Session-Start | jede Anfrage | Ton und Format, nicht Fakten |
| `settings.json` | Session-Start, nicht in den Kontext | null | steuert, kommt nicht ins Modell |

## Entscheidungshilfe: wohin mit einer Anweisung

| Du willst | Wohin | Nicht wohin |
|---|---|---|
| „Immer X“, in jedem Projekt | `~/.claude/rules/<thema>.md` | Chat |
| „Immer X“, nur in diesem Repo | `<repo>/.claude/rules/<thema>.md` | `~/.claude` |
| „X nur bei Python-Dateien“ | Regel mit `paths: ["**/*.py"]` | `CLAUDE.md` |
| Etwas, das **nie** passieren darf | `permissions.deny` oder `PreToolUse`-Hook | Prosa |
| Ein Ablauf, den du per `/name` startest | Skill mit `disable-model-invocation: true` (so wie `/einrichten`) | `CLAUDE.md` |
| Referenzwissen, das manchmal gebraucht wird | Skill ohne `disable-model-invocation` | `CLAUDE.md` |
| Arbeit mit viel Ausgabe, die den Chat flutet | Subagent | Hauptsession |
| Verbindung zu einem externen System | `.mcp.json` | Skill allein |
| Ton, Länge, Rolle | Output-Style | Regeln |
| Was du nur für dich willst | `CLAUDE.local.md`, `settings.local.json` | committete Dateien |

## Lesereihenfolge im Starter

So liest Claude die Dateien aus `home/`, und so sind sie verlinkt:

```
~/.claude/CLAUDE.md          Identität, Rangordnung, Tabelle "Was wo steht"
  └─ rules/00-hardrules.md   gewinnt immer
     ├─ 10-workflow.md       Ablauf einer Aufgabe
     │   ├─ 11-slices.md     Einordnung, Session-Name
     │   └─ 12-definition-of-done.md   Matrix, Gegenprobe, Bericht
     ├─ 20-kommunikation.md, 21-recherche.md
     ├─ 30-code-quality.md, 31-git.md, 32-security.md, 33-testing.md
     └─ 40-modellwahl.md, 41-graphify.md
<repo>/CLAUDE.md             Stack, Befehle, Branches, Tracking
  ├─ AGENTS.md               Verbraucher, Invarianten (vor der Matrix lesen)
  ├─ SLICES.md               Stand der Arbeit
  └─ .claude/rules/*.md      Stack-Regeln, pfadgebunden
```

Jede Regel beginnt mit einer Zeile, wann sie lädt und worauf sie aufbaut.
Wer eine neue Regel schreibt, hält das so bei.

## Prüfen, ob es ankommt

- `/memory` zeigt alle geladenen `CLAUDE.md` und Regeln.
- `/context` zeigt, was wie viel Platz belegt.
- `/doctor prompt-audit` findet Widersprüche und Dubletten.
- Frag Claude: „Welche Regeln hast du geladen?“ Die Antwort zeigt, was wirklich ankam.
