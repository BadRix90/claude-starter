# Slices und Session-Namen

> **Lädt:** jede Session. **Gehört zu:** [`10-workflow.md`](10-workflow.md), [`12-definition-of-done.md`](12-definition-of-done.md).
> **Projektseite:** die Slice-Tabelle liegt im Projekt (`SLICES.md` oder die Datei, die das Projekt-`CLAUDE.md` nennt).

## Ein Slice pro Session

Pro Session genau ein Thema. Kein Mischen. Eine neue Aufgabe mitten in der Arbeit
bekommt eine neue Session oder wird als Hotfix (H) mit-committet und genannt.

## Präfixe

| Präfix | Art | Typische Inhalte |
|---|---|---|
| **F** | Feature | neue Funktion, neuer Endpunkt, Frontend-Port |
| **R** | Refactor | Struktur ohne Verhaltensänderung |
| **B** | Bug | Fix mit Stack-Trace, Root-Cause und Test |
| **A** | Audit | read-only Bestandsaufnahme |
| **H** | Hotfix | kleiner unaufschiebbarer Fix während einer anderen Session |
| **C** | Chore | Tooling, Config, Deps, Doku ohne fachlichen Inhalt |
| **D** | DevOps | Infra, Container, CI, Deployment |
| **M** | Meta | Triage, Aufräumen, Planung ohne Slice |

Sub-Slices mit Kleinbuchstaben: `F15a`, `F15b`. Der Hauptpräfix bleibt.

## Session-Namen

Jeder Session-Titel beginnt mit dem Slice, dann ein kurzes Thema:
`F8 Rechnungen — Upload-Dialog`, `B Zeitzonen-Fehler im Export`, `A15 Compliance-Audit`.
Vergibt Claude Code den Namen automatisch, gilt dieselbe Form.

## Was ein Slice braucht, bevor er beginnt

- Ausgangsproblem in einem Satz.
- Akzeptanzpunkte, einzeln und prüfbar.
- Betroffene Dateien, nachgesehen, nicht geraten.
- Slice-Typ, damit klar ist, ob `PROD_VERIFIED` verlangt ist (F, B, H: ja; A, C, R, D: `VERIFIED` genügt).
