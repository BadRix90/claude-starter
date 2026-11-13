# Modellwahl und Effort

> **Für wen:** alle, die Kosten und Qualität steuern wollen. **Regel dazu:**
> Hardrule §3 in [`home/rules/00-hardrules.md`](../home/rules/00-hardrules.md).
> Quelle: [Modell-Konfiguration](https://code.claude.com/docs/en/model-config). Stand: November 2026, Versionen ändern sich.
> **Geprüft gegen:** Claude Code 2.1.310, Doku-Stand 11/2026.

## Wer wählt

Das Modell der Session wählst du, vor dem Start oder mit `/model` und `/effort`. Claude
kann es nicht selbst umstellen, deshalb steht diese Entscheidung hier und nicht in den
Regeln. Bewusst setzen, nicht den gespeicherten Wert blind übernehmen. Was Claude selbst
entscheidet, ist das Modell seiner Subagenten: das regelt Hardrule §3.

## Aliase

In Konfiguration Aliase schreiben, keine Versionsnummern. Volle Modell-IDs nur, wenn eine
Version gepinnt werden muss.

| Alias | Zeigt auf | Für |
|---|---|---|
| `default` | Standard des Kontos (löscht eine Überschreibung) | Zurücksetzen |
| `best` | `fable`, wo verfügbar, sonst `opus` | „das Beste, was ich habe“ |
| `fable` | Fable 5.1 | schwerste, längste Aufgaben; kein Default auf irgendeinem Plan |
| `opus` | aktuelles Opus | komplexes Reasoning, Architektur |
| `sonnet` | aktuelles Sonnet | Tagesarbeit |
| `haiku` | aktuelles Haiku | schnelle, einfache Aufgaben, Subagenten zum Lesen |
| `opusplan` | Opus im Plan-Modus, dann Sonnet | Analyse teuer, Umsetzung günstig |
| `sonnet[1m]`, `opus[1m]` | 1-Million-Token-Kontext | nur bei Modellen, die es nicht ohnehin haben |

Aliase lösen je Anbieter anders auf. Auf Amazon Bedrock, Google Vertex und
Microsoft Foundry hängen sie teils Versionen hinterher. Wer dort arbeitet, pinnt
mit voller Modell-ID (`claude-opus-5-5`) oder den Variablen `ANTHROPIC_DEFAULT_*_MODEL`.

## Wo das Modell gesetzt wird, Rangfolge

1. `/model <alias>` in der Session (speichert als Default, `s` nur für diese Session)
2. `claude --model <alias>` beim Start
3. Umgebungsvariable `ANTHROPIC_MODEL`
4. `"model"` in einer `settings.json`
5. `ANTHROPIC_DEFAULT_MODEL`

Der Starter setzt `"model": "opus"` in `home/settings.json`. Wer sparen will, nimmt
`sonnet` und schaltet für Architektur-Sessions bewusst hoch (Hardrule §3).

## Effort

Stufen: `low`, `medium`, `high`, `xhigh`, `max`. Neuere Modelle kennen alle fünf,
ältere nicht `xhigh`. Ein nicht unterstützter Wert fällt auf die nächstniedrigere Stufe.

| Stufe | Für |
|---|---|
| `low` | Brainstorm, Umbenennen, schnelle Rückfragen |
| `medium` | gut umrissene Feature-Arbeit (Default bei Opus 5.5, Sonnet 5.5, Haiku 5.5) |
| `high` | Bugfix in Bestandscode, alles, wo Verifikation zählt (Default bei älteren Modellen) |
| `xhigh` | tieferes Reasoning, mehr Tokens |
| `max` | harte Probleme autonom durcharbeiten, Security-Review; kann überdenken |

Rangfolge: `CLAUDE_CODE_EFFORT_LEVEL` → `/effort` in der Session → `--effort` → `modelSettings`
je Modell oder `effortLevel` in `settings.json` → Modell-Default. `max` lässt sich nicht
in `settings.json` setzen. Skills und Subagenten können `effort:` im Frontmatter tragen.

```json
{
  "effortLevel": "high",
  "modelSettings": { "claude-opus-5-5": { "effort": "medium" } }
}
```

## Subagenten und Fallback

- Subagenten erben das Modell der Session, außer das Frontmatter setzt `model:`.
  Umgebungsvariable `CLAUDE_CODE_SUBAGENT_MODEL` setzt einen Default für alle.
- `fallbackModel` in `settings.json` (Liste, höchstens drei) springt ein, wenn das
  Hauptmodell überlastet ist, nur für den laufenden Turn.

## Kosten denken

- Der Kontext kostet bei jeder Anfrage erneut. Kurze `CLAUDE.md`, pfadgebundene Regeln
  und Skills mit `disable-model-invocation` sparen mehr als ein billigeres Modell.
- Ein Subagent kostet Eingabe und Ausgabe in seinem eigenen Fenster. Vier Agenten
  für einen Slice sind etwa vier Sessions. Deshalb das harte Budget in `extras/`.
- `/cost` zeigt den Verbrauch der Session, `/usage` den des Kontos, `/insights`
  erstellt einen Bericht über Muster.
- Fable für einen Umbenennungs-Slice ist Geldverbrennung. Haiku für eine
  Architekturentscheidung ist Zeitverbrennung. Beides kostet.

## Schnellentscheid

```
Lesen, suchen, zusammenfassen       -> haiku, low/medium
Feature, klar umrissen              -> sonnet, medium
Bugfix, Verifikation zählt          -> sonnet oder opus, high
Architektur, Root-Cause             -> opus, high
Längste Aufgabe, Security, Audit    -> opus xhigh oder fable
Analyse teuer, Umsetzung günstig    -> opusplan
```
