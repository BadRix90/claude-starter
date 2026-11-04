# Security-sensitive Operationen

> **Lädt:** jede Session. **Hardrule:** §5 in [`00-hardrules.md`](00-hardrules.md).
> **Durchgesetzt von:** `permissions.deny` und Hooks in [`../settings.json`](../settings.json).

## Nie ohne ausdrückliches Ja

- Passwörter: `set_password`, Hashes, Resets, unusable-password.
- 2FA: TOTP-Secrets, Recovery-Codes, Enable-Toggles.
- Tokens und Keys: JWT, Refresh-Tokens, Session-Keys, API-Keys, OAuth-Grants,
  Zahlungsanbieter-Keys, Verschlüsselungs-Keys, `SECRET_KEY`.
- Auth-Konfiguration: Auth-Backends, Middleware-Reihenfolge, Permission-Klassen.
- Rollen und Besitz: `is_staff`, `is_superuser`, Tenant-Zuordnung, Tenant-Löschung.
- Datensätze mit Credentials, Tokens oder personenbezogenen Daten.
- `.env`, Compose-Umgebungen mit Secret-Injection, Prod-Secrets.
- Git-History-Rewrite auf getrackten Secrets (`filter-repo`, `bfg`).

Gilt gleich für Dev, lokales Docker, Staging und Prod. „Nur lokal“ ist keine Ausnahme.

## Stattdessen

1. Lesen, nicht schreiben. Evidenz sammeln.
2. Fund melden mit Datei, Zeile, beobachtetem Zustand.
3. Änderung als Diff oder Kommandofolge vorschlagen.
4. Auf klares „ja, mach“ warten.
5. Verlangt ein Auftrag implizit eine Security-Änderung („fix login“):
   erst die Implikation benennen, dann fragen.

## Für Hook-Autoren

Eine Regel, die immer gelten muss, gehört in einen `PreToolUse`-Hook, nicht in
Prosa. Vorlage: [`../hooks/guard_shell.py`](../hooks/guard_shell.py).
