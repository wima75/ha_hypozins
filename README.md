# Hypozinsen

Home Assistant Custom Integration, welche die aktuellen Festhypothek- und SARON-Zinssätze
von [Postfinance](https://www.postfinance.ch/de/privat/finanzieren/hypotheken/zinssaetze-hypotheken.html),
[BPK](https://bpk.ch/hypotheken/aktuelle-zinssaetze),
[Swissquote](https://www.swissquote.com/de-ch/private/bank/products/mortgage) und der
[SNB](https://www.snb.ch/public/rss/de/interestRates) abruft.

## Sensoren

Beim Start von Home Assistant und danach täglich um 16:30 aktualisiert, gruppiert in vier Devices:

**Postfinance Hypotheken**
- Festhypothek 2 Jahre
- Festhypothek 5 Jahre

**BPK Hypotheken**
- Festhypothek 3 Jahre
- Festhypothek 5 Jahre
- SARON Hypothek Marge

**Swissquote Hypotheken**
- Festhypothek 2 Jahre
- Festhypothek 5 Jahre
- SARON Hypothek 2 Jahre (Gesamtzinssatz inkl. Marge)
- SARON Hypothek 5 Jahre (Gesamtzinssatz inkl. Marge)

(Das Datum, auf das sich die Swissquote-Zinssätze beziehen, steht im Attribut `stand`.)

**SNB Referenzzinssätze**
- SARON Basiszinssatz (tägliches Fixing, Handelsschluss; hat üblicherweise 1 Tag Verzögerung –
  das Datum des zugrunde liegenden Fixings steht im Attribut `stand`)

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
