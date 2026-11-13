# graphify: erst der Graph, dann die Datei

> **Lädt:** jede Session. **Werkzeug:** [graphify](https://github.com/safishamsi/graphify), Paket `graphifyy` auf PyPI.
> **Skill:** `/graphify` bringt graphify selbst mit. Installation: `INSTALL.md` im Starter.

## Warum

Grep-Serien über ein Repo kosten Kontext und finden Symbole, nicht Zusammenhänge.
Ein Knowledge Graph liefert Aufrufer, Verbraucher und Pfade zwischen Modulen in
einem Aufruf.

## Regel

Der Graph liegt je Repo unter `graphify-out/`.

1. Liegt `graphify-out/graph.json` im Repo-Root, zuerst dort nachsehen:
   `graphify query "<frage>"`, `graphify explain "<symbol>"`, `graphify path "<A>" "<B>"`.
2. Immer aus dem Repo-Root aufrufen. Aus einem Unterordner findet der Graph nichts.
3. Erst danach gezielt lesen, mit `offset` und `limit` auf die Stellen, die der
   Graph nennt. Keine ganzen Dateien ohne Grund.
4. Fehlt der Graph oder ist er veraltet (eine Datei aus dem Diff fehlt darin):
   gezieltes Grep mit Pfad- und Typfilter, und im Ergebnis vermerken, dass ohne
   Graph gearbeitet wurde.
5. Nach jedem Commit, der Code ändert: `graphify update .` (oder `/graphify .`).

## Was der Graph nicht ersetzt

Den Blick in die Datei vor einer Änderung. Den Testlauf. Das Lesen der Karte.
