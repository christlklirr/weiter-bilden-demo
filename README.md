# Weiter bilden · Demo

Demo einer Kurssuche für wba-anrechenbare Bildungsangebote, mit persönlicher Kursliste.
**Alle 50 Kurse, Anbieter, Texte und Links sind erfunden.** Die Verteilung (Termine, Lernformat, Ort, Bundesländer, Abschlüsse) ist an die echten wba-Daten angelehnt. Nur die Namen der Kompetenzbereiche stammen aus den öffentlichen Qualifikationsprofilen der Weiterbildungsakademie Österreich (wba). Kein offizielles wba-Angebot.

Online: **https://christlklirr.github.io/weiter-bilden-demo/**

## Was die Demo zeigt

- **Volltextsuche** über Angebots- und Anbietertexte: mehrere Wörter müssen alle vorkommen, „Anführungszeichen“ suchen feste Wortfolgen, optional nur ganze Wörter. Fundstellen werden hervorgehoben.
- **Ein Filter für die Anrechnung:** wba-Abschluss und Kompetenzbereich in einem Feld, gegliedert nach Abschluss.
- **Typ:** Kurs/Seminar oder Lehrgang, wie in der wba-Suche.
- **Lernformat** (abgeleitet) und **Ort** (Bundesland, online, österreichweit) als je ein Filter.
- **Starttermin** als kombinierbare Umschalt-Buttons; bereits gestartete Angebote sind hervorgehoben, beendete zurückgenommen.
- **Meine Kursliste:** Kurse merken (♡), als „angemeldet“ oder „absolviert“ vermerken; der Stand ergibt sich aus dem Termin. Mit Link zur Anmeldung, Kopieren, Sichern und Laden.
- Erklärungen direkt an den Feldern (Info-Symbol), Handy-tauglich, keine Anmeldung, keine Daten verlassen den Browser.

## Lokal starten

`index.html` im Browser öffnen oder `npm start` und `http://127.0.0.1:8765`. Tests: `npm test`.

Die Beispieldaten erzeugt `python scripts/build_demo_data.py` (schreibt `data.js`).
