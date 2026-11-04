# Modellwahl

> **Lädt:** jede Session. **Hardrule:** §3 in [`00-hardrules.md`](00-hardrules.md).
> **Hintergrund und Kosten:** [`docs/MODELLWAHL.md`](https://github.com/BadRix90/claude-starter/blob/main/docs/MODELLWAHL.md).

## Vor jeder Session

Modell und Effort bewusst setzen (`/model`, `/effort`), nicht den gespeicherten
Wert blind übernehmen. Ein Audit braucht kein Spitzenmodell, eine
Architekturentscheidung kein Sparmodell.

## Faustregeln

| Aufgabe | Modell | Effort |
|---|---|---|
| Tagesarbeit, klar umrissenes Feature | `sonnet` | `medium` |
| Bugfix in Bestandscode, Verifikation zählt | `sonnet` oder `opus` | `high` |
| Architektur, Root-Cause, schwierige Debug-Sitzung | `opus` | `high` |
| Längste, schwerste Aufgaben, Security-Review | `fable` oder `opus` | `xhigh` bis `max` |
| Lesen, Suchen, Zusammenfassen (Subagent) | `haiku` | `low` bis `medium` |
| Brainstorm, Umbenennen, Kleinkram | beliebig | `low` |

`opusplan`: Opus im Plan-Modus, Sonnet in der Umsetzung. Gut für Sessions, die
mit Analyse beginnen und dann lange bauen.

## Aliase statt Versionsnummern

In Konfiguration `sonnet`, `opus`, `haiku`, `fable` schreiben. Aliase zeigen
immer auf die empfohlene Version des Anbieters. Volle Modell-IDs nur, wenn eine
Version gepinnt werden muss. Auf Bedrock, Vertex und Foundry lösen Aliase anders
auf als auf der Anthropic-API. Nachsehen, nicht annehmen.

## Delegation

Jeder Subagent bekommt sein Modell im Frontmatter (`model:`), nie `inherit`
ohne Grund. Read-only-Agenten auf `haiku` oder `sonnet`, Abnahme und Design auf `opus`.
`fable` ist kein Default und wird nur bewusst gewählt.

## Effort

`effortLevel` in `settings.json` gilt als Default. `max` lässt sich dort nicht
setzen, nur per `/effort` oder `--effort`. Bei `max` vorher testen, ob das Modell
überdenkt statt liefert.
