# Mitmachen

Der Starter lebt davon, dass Leute ihre Erfahrungen zurückgeben. Drei Wege:

## Ideen und Rückmeldungen

- **GitHub Issues** für Fehler, unklare Stellen, Vorschläge für neue Regeln oder Stacks.
  Vorlage: was hast du erwartet, was ist passiert, welche Datei betrifft es.
- **Direkt an Kay Dietrich** auf LinkedIn: <https://www.linkedin.com/in/kaydietrich/>.
  Gut für „bei mir funktioniert das so besser“, Erfahrungsberichte, Fragen zum Einsatz.

Was aufgenommen wird, landet mit Namen und Prüfergebnis in
[`docs/AUS-DER-COMMUNITY.md`](docs/AUS-DER-COMMUNITY.md). Wer nicht genannt werden
will, sagt es dazu.

## Pull Requests

- Eine Änderung pro PR. Regeln ändern sich einzeln, nicht im Paket.
- Jede neue Regel nennt, aus welchem konkreten Fehler sie entstanden ist. Eine Regel
  ohne Geschichte wird nicht befolgt.
- Neue Hooks kommen mit Tests unter `tests/`. `python -m pytest tests/ -q` muss grün sein.
- Markdown-Links prüfen: `python tools/check_links.py` findet tote relative Links.
- Commits nach Conventional Commits, Englisch, wie in `home/rules/31-git.md`.
- Keine persönlichen Pfade, Ports, Firmennamen oder Hostnamen. Der Starter ist für alle.

## Neue Stack-Variante

Ordner unter `stacks/`, darin `CLAUDE.md`-Abschnitt und `rules/`. Eine Zeile in
`stacks/README.md`. Pfadgebundene Regeln mit `paths:` im Frontmatter.

## Was nicht hineingehört

Regeln, die nur für ein Unternehmen gelten. Werkzeuge, die Geld kosten, als Pflicht.
Prompts, die Claude zum Raten auffordern. Alles, was gegen die Hardrules verstößt.
