# Aus der Community

> **Was das ist:** Ideen, die von außen kamen, geprüft und eingebaut oder als
> offen markiert. Jede Idee nennt, von wem sie stammt, was sie löst, ob sie im
> Starter liegt und was beim Testen herauskam. **Eigene Idee?** Siehe
> [`../CONTRIBUTING.md`](../CONTRIBUTING.md) oder direkt an
> [Kay Dietrich auf LinkedIn](https://www.linkedin.com/in/kaydietrich/).

## Stand-Legende

| Stand | Bedeutung |
|---|---|
| **eingebaut** | liegt im Starter, mit Tests oder Gegenprobe |
| **geprüft, nicht eingebaut** | funktioniert, passt aber nicht zu den Hardrules oder zum Umfang |
| **offen** | noch nicht nachgebaut |

---

## Session Radar: Warnung ab 50 Prozent Kontext

**Von:** Andreas Paehge, Kommentar unter dem Launch-Post auf LinkedIn, November 2026.
**Problem:** Nach dem Kompaktieren ist die halbe Anweisung weg. Wer den Füllstand
nicht sieht, merkt es erst, wenn Claude etwas vergessen hat.
**Seine Lösung:** ein Radar, das ab 50 Prozent warnt. Seitdem macht er früher eine
Übergabe und ein `/clear`.

**Im Starter: eingebaut**, in zwei Teilen, weil Claude Code den Füllstand nur an
einer Stelle herausgibt:

1. [`home/statusline.py`](../home/statusline.py): Balken und Prozent in der
   Statuszeile, Warnung ab 50 Prozent. Die Statusline bekommt nach jeder API-Antwort
   `context_window.used_percentage` auf stdin. Das Skript legt den Wert zusätzlich
   in einer Datei je Session ab.
2. [`home/hooks/context_radar.py`](../home/hooks/context_radar.py): ein
   `UserPromptSubmit`-Hook, der die Datei liest und Claude ab 50 Prozent per
   `additionalContext` sagt, dass eine Übergabe ansteht, ab 75 Prozent dringlicher.
   So sieht es nicht nur der Mensch, Claude schlägt die Übergabe selbst vor.

Warum zwei Teile: Kein Hook-Ereignis bekommt Token-Zahlen im Input, und `PreCompact`
feuert erst, wenn die Kompaktierung schon ansteht. Die Statusline sieht den Wert,
kann aber nur anzeigen. Zusammen können sie beides.

**Getestet:** Rendering und Schwellen mit Beispiel-JSON aus der Doku
(`tests/test_context_radar.py`), Roundtrip Statusline → Datei → Hook. Noch nicht
getestet: eine lange Live-Session bis über 75 Prozent.
**Einschalten:** beide Einträge stehen in [`home/settings.json`](../home/settings.json).
Schwellen in den Skripten (`WARN_AT`, `URGENT_AT`) anpassen.
**Quelle:** [Statusline-Doku](https://code.claude.com/docs/en/statusline),
[Hooks-Referenz](https://code.claude.com/docs/en/hooks).

---

## Push, löschen, veröffentlichen nur mit Freigabe

**Von:** Andreas Paehge, derselbe Kommentar.
**Regel bei ihm:** Im Projektordner darf Claude bauen und testen, so oft er will.
Pushen, löschen oder veröffentlichen nur mit Freigabe.

**Im Starter: eingebaut**, als Hardrule §9.3 (Push nur auf Wort) und als
`permissions.ask` für `git push` und `gh pr merge`. Löschen außerhalb des
Arbeitsverzeichnisses und Veröffentlichen fängt der Auto-Modus-Klassifikator ab;
wer manuell arbeitet, bekommt ohnehin eine Rückfrage. Was fehlt: `rm -rf` auf
Projektordner ist nicht im Shell-Guard. **Offen**, Kandidat für `guard_shell.py`.
