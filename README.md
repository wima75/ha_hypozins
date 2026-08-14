# Hypozinsen

Home Assistant Custom Integration, welche die aktuellen Festhypothek- und SARON-Zinssätze
von [Postfinance](https://www.postfinance.ch/de/privat/finanzieren/hypotheken/zinssaetze-hypotheken.html)
und [BPK](https://bpk.ch/hypotheken/aktuelle-zinssaetze) abruft.

## Sensoren

Alle 12 Stunden aktualisiert, gruppiert in zwei Devices:

**Postfinance Hypotheken**
- Festhypothek 2 Jahre
- Festhypothek 5 Jahre

**BPK Hypotheken**
- Festhypothek 3 Jahre
- Festhypothek 5 Jahre
- SARON Hypothek Marge

Da alle Sensoren als `state_class: measurement` markiert sind, speichert Home Assistant automatisch
den Verlauf (History-Tab und Statistics-Karten in Lovelace) – es ist keine zusätzliche Konfiguration nötig.

## Installation

1. Kopiere `custom_components/hypozins` in dein Home Assistant `custom_components`-Verzeichnis
   (oder installiere über HACS als custom repository).
2. Starte Home Assistant neu.
3. Füge die Integration über **Einstellungen → Geräte & Dienste → Integration hinzufügen → Hypozinsen** hinzu.
   Es sind keine weiteren Einstellungen nötig.

## Entwicklung

Siehe [CONTRIBUTING.md](CONTRIBUTING.md). Zum lokalen Testen: `scripts/setup` gefolgt von `scripts/develop`.
