"""Erzeugt data.js mit erfundenen Beispielkursen für die öffentliche Demo.

Alle Anbieter, Kurse, Texte und Links sind fiktiv. Die Kompetenzbereiche tragen die
öffentlich bekannten Bezeichnungen der wba-Qualifikationsprofile, damit die Filter
realistisch wirken. Links zeigen auf example.org.
"""
import json, pathlib, re, datetime

OUT = pathlib.Path(__file__).resolve().parents[1] / 'data.js'

Z, B, LGT, BER, BM, BIB, DU = ('wba-Zertifikat', 'wba-Basisbildungszertifikat', 'wba-Diplom Lehren/Gruppenleitung/Training',
                               'wba-Diplom Beratung', 'wba-Diplom Bildungsmanagement', 'wba-Diplom Bibliothekswesen', 'Diplomübergreifend')

# (titel, anbieter, ort, termin, ue, ects, format, anrechnung, beschreibung, inhalte, anbietertext?)
COURSES = [
 ('Grundlagen der Erwachsenendidaktik', 'Bildungshaus Sonnberg', 'Steiermark, Graz', '12.03.2027 - 24.04.2027', 40, 4, 'Präsenz',
  [(Z, 'Didaktische Kompetenz', 2.5), (Z, 'Grundlagen der Pädagogik', 1.5)],
  'Wie lernen Erwachsene – und was heißt das für die Planung von Kursen? Der Lehrgang verbindet Lerntheorie mit vielen praktischen Übungen. Sie planen eine eigene Kurseinheit und erhalten Feedback aus der Gruppe.',
  ['Lerntheorien und ihre Bedeutung für die Praxis', 'Lernziele formulieren und Einheiten planen', 'Methodenvielfalt und Sozialformen', 'Feedback geben und annehmen'], True),
 ('Moderation von Gruppen und Workshops', 'Akademie am Kogel', 'Tirol, Innsbruck', '19.01.2027 - 20.01.2027', 16, 1.5, 'Präsenz',
  [(Z, 'Soziale Kompetenz', 1.0), (LGT, 'Wahlpflichtteil: Gruppenprozesse und -dynamik', 1.5)],
  'Gute Moderation macht Gruppen arbeitsfähig. Sie lernen, Besprechungen und Workshops zielorientiert zu strukturieren, alle Beteiligten einzubinden und Ergebnisse sichtbar zu machen.',
  ['Rolle und Haltung der Moderation', 'Visualisierung am Flipchart und digital', 'Umgang mit Vielredner:innen und Konflikten', 'Entscheidungen in Gruppen herbeiführen'], True),
 ('Konflikte im Kursraum konstruktiv lösen', 'Lernwerk Lindenhof', 'Wien', 'wird laufend angeboten', 8, 0.5, 'unklar',
  [(Z, 'Soziale Kompetenz', 0.5), (DU, 'Soziale Kompetenz', 0.5)],
  'Störungen und Konflikte gehören zum Kursalltag. Im Selbstlernkurs analysieren Sie typische Konfliktsituationen und erproben Gesprächstechniken, mit denen Sie deeskalierend reagieren.',
  ['Konfliktarten und Eskalationsstufen', 'Ich-Botschaften und aktives Zuhören', 'Fallbeispiele aus der Erwachsenenbildung'], True),
 ('Mediendidaktik kompakt: Digitale Werkzeuge im Unterricht', 'Online-Campus Weitblick', 'online', 'wird laufend angeboten', 12, 1, 'unklar',
  [(Z, 'Medienkompetenz', 1.0), (Z, 'Wahlteil: Medienkompetenz', 0.5)],
  'Welche digitalen Werkzeuge passen zu welchem Lernziel? Sie testen Umfragetools, digitale Pinnwände und Lernplattformen und entwickeln einen kleinen Baustein für Ihren eigenen Kurs.',
  ['Mediendidaktische Modelle', 'Werkzeuge für Aktivierung und Zusammenarbeit', 'Datenschutz und Urheberrecht im Unterricht'], True),
 ('Live-Online unterrichten: Webinare lebendig gestalten', 'Online-Campus Weitblick', 'online', '02.02.2027 - 23.02.2027', 16, 1.5, 'Live-Webinar',
  [(Z, 'Medienkompetenz', 1.0), (LGT, 'Wahlpflichtteil: Gestaltung von Lernräumen', 1.5)],
  'Vier Live-Termine im virtuellen Klassenzimmer: Sie üben Breakout-Räume, Whiteboards und Aktivierungsmethoden und moderieren am Ende selbst eine kurze Webinar-Sequenz.',
  ['Technik und Rollen im Webinar', 'Aktivierung online', 'Zusammenarbeit in Kleingruppen', 'Eigene Webinar-Sequenz mit Feedback'], True),
 ('Beratungsgespräche professionell führen', 'Institut Brückenschlag', 'Oberösterreich, Linz', '05.10.2026 - 06.10.2026', 16, 1.5, 'Präsenz',
  [(Z, 'Beratungskompetenz', 1.5), (BER, 'Generelles Beratungs-Know-how', 1.5)],
  'Ein zweitägiges Seminar zu Struktur, Haltung und Gesprächstechniken in der Bildungs- und Berufsberatung – mit vielen Übungssequenzen in Kleingruppen.',
  ['Phasen eines Beratungsgesprächs', 'Fragetechniken', 'Ressourcenorientierung', 'Grenzen der Beratung'], True),
 ('Diplomlehrgang Bildungs- und Berufsberatung', 'Institut Brückenschlag', 'Oberösterreich, Linz', '16.10.2026 - 18.06.2027', 240, 18, 'Blended',
  [(BER, 'Beratungskompetenz in Theorie und Praxis', 6.0), (BER, 'Generelles Beratungs-Know-how', 6.0), (BER, 'Fachkompetenz', 4.0), (Z, 'Beratungskompetenz', 2.0)],
  'Der berufsbegleitende Lehrgang verbindet Präsenzmodule mit Online-Phasen und einer begleiteten Praxisphase. Abschluss mit Fallarbeit und Reflexionsgespräch.',
  ['Beratungsansätze und -modelle', 'Bildungs- und Arbeitsmarkt in Österreich', 'Diagnostik und Kompetenzbilanzierung', 'Praxisreflexion und Supervision'], True),
 ('Projektmanagement in Bildungseinrichtungen', 'Netzwerk Erwachsenenbildung Mustertal', 'Salzburg, Salzburg', '08.04.2027 - 10.04.2027', 24, 2, 'Präsenz',
  [(BM, 'Projektmanagement', 2.0), (Z, 'Managementkompetenz', 1.0)],
  'Von der Idee zum Förderantrag: Sie planen ein eigenes Bildungsprojekt mit Zielen, Meilensteinen, Budget und Risikoanalyse.',
  ['Projektauftrag und Ziele', 'Zeit- und Ressourcenplanung', 'Förderlandschaft und Anträge', 'Abschluss und Evaluation'], True),
 ('Qualitätsmanagement und Evaluation', 'Netzwerk Erwachsenenbildung Mustertal', 'online', 'wird laufend angeboten', 20, 2, 'Blended',
  [(BM, 'Wahlpflichtteil: Qualitätsmanagement', 1.5), (BM, 'Wahlpflichtteil: Evaluation', 1.0)],
  'Welche Qualitätsmodelle gibt es in der Erwachsenenbildung, und wie evaluiert man Kurse sinnvoll? Selbstlernphasen wechseln mit zwei Online-Treffen.',
  ['Qualitätsmodelle im Überblick', 'Feedbackbögen und Kennzahlen', 'Ergebnisse auswerten und nutzen'], False),
 ('Bildungsmarketing mit kleinem Budget', 'Lernwerk Lindenhof', 'Wien', '22.01.2027', 8, 0.5, 'Präsenz',
  [(BM, '(Bildungs-)Marketing', 0.5)],
  'Wie erreichen Sie neue Zielgruppen, ohne viel Geld auszugeben? Ein Praxistag zu Kursbeschreibungen, Social Media und Kooperationen.',
  ['Zielgruppen verstehen', 'Gute Kursbeschreibungen schreiben', 'Social Media und Newsletter'], True),
 ('Basisbildung: Alphabetisierung in der Praxis', 'Bildungswerk Talblick', 'Kärnten, Klagenfurt', '13.11.2026 - 29.01.2027', 60, 5, 'Präsenz',
  [(B, 'Alphabetisierung', 2.5), (B, 'Fachdidaktik Alphabetisierung', 2.5)],
  'Für Trainer:innen in der Basisbildung: Sie lernen, wie Erwachsene lesen und schreiben lernen, und erproben Materialien für heterogene Gruppen.',
  ['Schriftspracherwerb bei Erwachsenen', 'Diagnostik und Lernstandsfeststellung', 'Materialien für heterogene Gruppen'], True),
 ('Mathematik im Alltag vermitteln', 'Bildungswerk Talblick', 'online', 'wird laufend angeboten', 24, 2, 'unklar',
  [(B, 'Fachdidaktik Mathematik', 2.0)],
  'Rechnen mit Bezug zum Alltag: Einkaufen, Fahrpläne, Haushaltsbudget. Sie entwickeln Übungen, die an die Lebenswelt der Teilnehmenden anknüpfen.',
  ['Alltagsmathematik', 'Rechenschwierigkeiten erkennen', 'Spielerische Übungsformen'], False),
 ('Digitale Grundkompetenzen vermitteln', 'Online-Campus Weitblick', 'österreichweit', 'wird laufend angeboten', 16, 1.5, 'unklar',
  [(B, 'Fachdidaktik Digitale Kompetenz', 1.5), (Z, 'Medienkompetenz', 0.5)],
  'Smartphone, E-Mail, Online-Formulare: Der Kurs zeigt, wie Sie digitale Grundkompetenzen niederschwellig und ohne Fachjargon vermitteln.',
  ['Digitale Kompetenzmodelle', 'Niederschwellige Lernsettings', 'Sicherheit im Netz'], True),
 ('Tiergestützte Pädagogik: Mit Hund im Kursraum', 'Akademie am Kogel', 'Tirol, Innsbruck', '14.05.2027 - 15.05.2027', 16, 1, 'Präsenz',
  [(DU, 'Wahlteil: Fachkompetenz', 1.0)],
  'Ein gut ausgebildeter Hund kann Lernatmosphäre und Motivation spürbar verbessern. Sie erfahren, welche Voraussetzungen Mensch und Hund mitbringen sollten, was rechtlich und hygienisch zu beachten ist und wie Sie Hunde sinnvoll in Kurse einbinden.',
  ['Wirkung von Tieren auf Lernprozesse', 'Voraussetzungen und Ausbildung des Hundes', 'Rechtliches, Hygiene, Allergien', 'Praxisbeispiele aus der Erwachsenenbildung'], True),
 ('Gruppendynamik verstehen und steuern', 'Bildungshaus Sonnberg', 'Steiermark, Graz', '15.10.2026 - 12.12.2026', 32, 3, 'Präsenz',
  [(LGT, 'Lernprozesse und Gruppenprozesse steuern', 2.0), (LGT, 'Wahlpflichtteil: Gruppenprozesse und -dynamik', 1.0)],
  'Gruppen entwickeln sich in Phasen. Sie lernen Modelle der Gruppendynamik kennen und erleben in Übungen, wie Rollen, Normen und Vertrauen entstehen.',
  ['Phasenmodelle', 'Rollen in Gruppen', 'Interventionen der Leitung', 'Reflexion der eigenen Wirkung'], True),
 ('Feedback und Leistungsbeurteilung in Kursen', 'Lernwerk Lindenhof', 'Wien', '03.03.2027 - 04.03.2027', 16, 1.5, 'Präsenz',
  [(LGT, 'Feedback und Evaluation', 1.5)],
  'Wie geben Sie Rückmeldungen, die motivieren? Und wie beurteilen Sie fair? Ein Seminar mit Werkzeugen für Feedback, Selbsteinschätzung und Prüfungen.',
  ['Feedbackregeln', 'Formative und summative Beurteilung', 'Selbst- und Peer-Assessment'], True),
 ('Train the Trainer: Lehrgang für Kursleiter:innen', 'Akademie am Kogel', 'Tirol, Innsbruck', '18.09.2026 - 14.05.2027', 160, 12, 'Blended',
  [(LGT, 'Pflichtteil: Didaktische Planung und Durchführung', 6.0), (Z, 'Didaktische Kompetenz', 3.0), (Z, 'Personale Kompetenz', 1.5), (LGT, 'Wahlpflichtteil: Professionelle Haltung und Rollenreflexion', 1.5)],
  'Der Lehrgang bereitet auf die Tätigkeit als Trainer:in vor: Planung, Durchführung und Reflexion von Kursen, Auftreten und Rollenverständnis. Mit Lehrauftritt und Abschlussgespräch.',
  ['Didaktische Planung', 'Präsentation und Auftreten', 'Methodenwerkstatt', 'Lehrauftritt mit Feedback'], True),
 ('Wissenschaftliches Arbeiten für Praktiker:innen', 'Online-Campus Weitblick', 'online', 'wird laufend angeboten', 20, 2, 'unklar',
  [(DU, 'Wissenschaftsorientiertes Arbeiten', 2.0)],
  'Recherchieren, zitieren, argumentieren: Der Selbstlernkurs hilft beim Verfassen von Abschlussarbeiten und Fachartikeln in der Erwachsenenbildung.',
  ['Literaturrecherche', 'Zitierregeln', 'Aufbau einer Arbeit'], False),
 ('Führen in Bildungsorganisationen', 'Netzwerk Erwachsenenbildung Mustertal', 'Salzburg, Salzburg', '11.06.2027 - 26.06.2027', 32, 3, 'Präsenz',
  [(DU, 'Leitungs- und Führungskompetenz', 2.0), (BM, 'Wahlpflichtteil: Personalentwicklung', 1.0)],
  'Für Programmverantwortliche und Teamleitungen: Führungsrollen klären, Teams entwickeln, schwierige Gespräche führen.',
  ['Führungsverständnis', 'Teamentwicklung', 'Mitarbeitendengespräche'], True),
 ('Bibliothek als Lernort gestalten', 'Bücherei-Akademie Nordwald', 'Niederösterreich, St. Pölten', '20.04.2027 - 21.04.2027', 16, 1.5, 'Präsenz',
  [(BIB, 'Zielgruppenarbeit und Benutzungsdienst', 1.0), (BIB, 'Bibliotheksorganisation und -management', 0.5)],
  'Öffentliche Bibliotheken werden zu Orten des Lernens und der Begegnung. Sie entwickeln Ideen für Veranstaltungen, Lernecken und Kooperationen.',
  ['Bibliothek als dritter Ort', 'Veranstaltungsformate', 'Kooperationen mit Bildungseinrichtungen'], True),
 ('Digitale Bibliothek: E-Medien vermitteln', 'Bücherei-Akademie Nordwald', 'online', '09.12.2026 - 16.12.2026', 8, 0.5, 'Live-Webinar',
  [(BIB, 'Digitale Bibliothek', 0.5)],
  'Zwei Online-Abende zu E-Books, Hörbüchern und Datenbanken – und wie Sie Leser:innen bei den ersten Schritten begleiten.',
  ['Angebote der digitalen Ausleihe', 'Häufige Fragen von Leser:innen', 'Schulungsformate'], True),
 ('Selbstreflexion und Resilienz für Trainer:innen', 'Bildungshaus Sonnberg', 'Steiermark, Graz', '11.03.0027 - 13.03.2027', 16, 1, 'Präsenz',
  [(Z, 'Personale Kompetenz', 1.0), (DU, 'Personale Kompetenz', 0.5)],
  'Ein Wochenende zum Durchatmen: eigene Stärken und Grenzen reflektieren, mit Belastungen umgehen und die Freude an der Arbeit mit Gruppen erhalten.',
  ['Eigene Ressourcen erkennen', 'Stress und Erholung', 'Kollegiale Beratung'], True),
 ('Gesellschaft und Bildung: Erwachsenenbildung in Österreich', 'Online-Campus Weitblick', 'online', 'wird laufend angeboten', 8, 1, 'unklar',
  [(Z, 'Gesellschaft und Bildung', 1.0)],
  'Ein Überblick über Geschichte, Strukturen und Akteur:innen der österreichischen Erwachsenenbildung – kompakt im Selbststudium.',
  ['Geschichte der Erwachsenenbildung', 'Strukturen und Finanzierung', 'Aktuelle bildungspolitische Themen'], True),
 ('Präsentieren mit Wirkung', 'Lernwerk Lindenhof', 'Wien', '05.11.2026', 8, 0.5, 'Präsenz',
  [(Z, 'Wahlteil: Personale Kompetenz', 0.5)],
  'Ein Tag für sicheres Auftreten: Stimme, Körpersprache und Aufbau einer überzeugenden Präsentation – mit Videofeedback.',
  ['Aufbau einer Präsentation', 'Stimme und Körpersprache', 'Videofeedback'], True),
 # --- Ergänzung: mehr Lehrgänge, mehr „laufend angeboten“, mehr Oberösterreich und Wien – wie in den echten Daten ---
 ('Diplomlehrgang Systemisches Coaching', 'Weiterbildungszentrum Traunviertel', 'Oberösterreich, Steyr', 'wird laufend angeboten', 220, 16, 'unklar',
  [(Z, 'Beratungskompetenz', 2.0), (Z, 'Wahlteil: Beratungskompetenz', 2.5), (BER, 'Beratungskompetenz in Theorie und Praxis', 6.0), (BER, 'Wahlteil: Beratungskompetenz', 3.0), (DU, 'Personale Kompetenz', 1.5)],
  'Der Lehrgang vermittelt systemische Haltung und Methoden für Coaching im beruflichen Kontext. Lehrcoaching und Peergruppen begleiten die Ausbildung.',
  ['Systemische Grundannahmen', 'Auftragsklärung und Kontrakt', 'Aufstellungsarbeit', 'Lehrcoaching'], True),
 ('Diplomlehrgang Systemisches Coaching', 'Weiterbildungszentrum Traunviertel', 'Oberösterreich, Steyr', '06.11.2026 - 25.06.2027', 220, 16, 'unklar',
  [(Z, 'Beratungskompetenz', 2.0), (Z, 'Wahlteil: Beratungskompetenz', 2.5), (BER, 'Beratungskompetenz in Theorie und Praxis', 6.0), (BER, 'Wahlteil: Beratungskompetenz', 3.0), (DU, 'Personale Kompetenz', 1.5)],
  'Der Lehrgang vermittelt systemische Haltung und Methoden für Coaching im beruflichen Kontext. Lehrcoaching und Peergruppen begleiten die Ausbildung.',
  ['Systemische Grundannahmen', 'Auftragsklärung und Kontrakt', 'Aufstellungsarbeit', 'Lehrcoaching'], False),
 ('Lehrgang Erwachsenenbildung kompakt', 'Akademie Donaublick', 'Oberösterreich, Linz', 'wird laufend angeboten', 120, 9, 'unklar',
  [(Z, 'Grundlagen der Pädagogik', 2.0), (Z, 'Didaktische Kompetenz', 2.5), (Z, 'Gesellschaft und Bildung', 1.0), (Z, 'Soziale Kompetenz', 1.5), (DU, 'Bildungstheoretische Kompetenz', 2.0)],
  'Ein Einstieg in die Erwachsenenbildung für Quereinsteiger:innen: pädagogische Grundlagen, Didaktik und das österreichische Bildungssystem.',
  ['Pädagogische Grundbegriffe', 'Didaktik der Erwachsenenbildung', 'Bildungslandschaft Österreich'], True),
 ('Trainer:innenausbildung mit Praxisprojekt', 'Akademie Donaublick', 'Oberösterreich, Linz', 'wird laufend angeboten', 180, 13, 'unklar',
  [(Z, 'Didaktische Kompetenz', 3.0), (Z, 'Personale Kompetenz', 1.5), (LGT, 'Pflichtteil: Didaktische Planung und Durchführung', 6.0), (LGT, 'Feedback und Evaluation', 1.5), (DU, 'Wahlteil: Didaktische Kompetenz', 1.0)],
  'Die Ausbildung führt in Planung, Durchführung und Reflexion von Trainings. Ein eigenes Praxisprojekt wird während der Ausbildung begleitet.',
  ['Trainingsdesign', 'Methoden und Medien', 'Praxisprojekt mit Begleitung', 'Abschlusspräsentation'], True),
 ('Kommunikation und Gesprächsführung', 'Volksbildungswerk Seenland', 'Oberösterreich, Gmunden', 'wird laufend angeboten', 24, 2, 'unklar',
  [(Z, 'Soziale Kompetenz', 1.5), (DU, 'Soziale Kompetenz', 1.0)],
  'Grundlagen guter Kommunikation: zuhören, nachfragen, klar formulieren. Mit vielen Übungen aus dem Arbeitsalltag in Kursen und Beratung.',
  ['Kommunikationsmodelle', 'Gesprächstechniken', 'Schwierige Gespräche'], True),
 ('Interkulturelle Kompetenz im Kurs', 'Volksbildungswerk Seenland', 'Oberösterreich, Gmunden', 'wird laufend angeboten', 16, 1.5, 'unklar',
  [(Z, 'Soziale Kompetenz', 1.0), (DU, 'Wahlteil: Soziale Kompetenz', 1.0)],
  'Wie gelingt Lernen in Gruppen mit unterschiedlichen kulturellen Hintergründen? Der Kurs sensibilisiert für Unterschiede und zeigt praktische Wege.',
  ['Kultur und Kommunikation', 'Vorurteile erkennen', 'Methoden für vielfältige Gruppen'], False),
 ('Deutsch als Zweitsprache unterrichten', 'Weiterbildungszentrum Traunviertel', 'Oberösterreich, Wels', 'wird laufend angeboten', 160, 12, 'unklar',
  [(Z, 'Didaktische Kompetenz', 2.0), (LGT, 'Fachkompetenz', 6.0), (LGT, 'Vertieftes Wissen zu Didaktik', 2.0), (DU, 'Fachkompetenz', 2.0)],
  'Für Lehrende in DaZ-Kursen: Spracherwerb, Kursplanung nach Niveaustufen und Prüfungsvorbereitung. Mit Hospitationen in laufenden Kursen.',
  ['Spracherwerbstheorien', 'Niveaustufen und Prüfungen', 'Grammatik vermitteln', 'Hospitation'], True),
 ('Lernbegleitung im Selbststudium', 'Online-Campus Weitblick', 'österreichweit', 'wird laufend angeboten', 30, 2.5, 'unklar',
  [(Z, 'Didaktische Kompetenz', 1.0), (LGT, 'Wahlpflichtteil: Lernprozessbegleitung, Feedback und Bewertung', 1.5), (DU, 'Wahlteil: Didaktische Kompetenz', 0.5)],
  'Wie begleitet man Lernende, die überwiegend allein lernen? Der Kurs zeigt Methoden für Motivation, Rückmeldung und Lernvereinbarungen.',
  ['Selbstgesteuertes Lernen', 'Lernvereinbarungen', 'Online-Feedback'], True),
 ('Bildungsberatung für Erwachsene', 'Lernhaus Am Kanal', 'Wien', 'wird laufend angeboten', 140, 10, 'unklar',
  [(Z, 'Beratungskompetenz', 2.0), (BER, 'Generelles Beratungs-Know-how', 4.0), (BER, 'Fachkompetenz', 3.0), (DU, 'Fachkompetenz', 1.0)],
  'Der Lehrgang qualifiziert für Bildungs- und Berufsberatung mit Erwachsenen: Beratungsprozesse, Kompetenzerfassung und Wissen über Förderungen.',
  ['Beratungsprozess', 'Kompetenzbilanz', 'Förderungen und Anlaufstellen', 'Fallarbeit'], True),
 ('Gender und Diversität in der Erwachsenenbildung', 'Lernhaus Am Kanal', 'Wien', 'wird laufend angeboten', 16, 1, 'unklar',
  [(Z, 'Gesellschaft und Bildung', 0.5), (DU, 'Bildungstheoretische Kompetenz', 1.0)],
  'Der Kurs zeigt, wie Gender und Vielfalt in Planung, Sprache und Materialien berücksichtigt werden können.',
  ['Begriffe und Konzepte', 'Gendergerechte Sprache', 'Materialien prüfen'], False),
 ('Lerncoaching für Erwachsene', 'Lernhaus Am Kanal', 'Wien', '10.02.2027 - 30.11.2027', 120, 9, 'unklar',
  [(Z, 'Beratungskompetenz', 1.5), (LGT, 'Wahlpflichtteil: Lernprozessbegleitung, Feedback und Bewertung', 2.0), (BER, 'Wahlteil: Beratungskompetenz', 3.0), (DU, 'Personale Kompetenz', 1.0)],
  'Lerncoaches unterstützen Erwachsene beim Lernen lernen. Der Lehrgang verbindet Lernpsychologie mit Coachingmethoden.',
  ['Lernpsychologie', 'Lernstrategien', 'Coachinggespräche', 'Supervision'], True),
 ('E-Learning-Kurse gestalten mit Moodle', 'Online-Campus Weitblick', 'online', 'wird laufend angeboten', 40, 3, 'unklar',
  [(Z, 'Medienkompetenz', 1.5), (Z, 'Wahlteil: Medienkompetenz', 1.0), (DU, 'Wahlteil: Didaktische Kompetenz', 0.5)],
  'Schritt für Schritt zum eigenen Online-Kurs: Aufbau, Aktivitäten, Tests und Rückmeldungen in Moodle.',
  ['Kursaufbau', 'Aktivitäten und Tests', 'Bewertung und Rückmeldung'], True),
 ('Erlebnispädagogik in der Erwachsenenbildung', 'Wanderakademie Alpenrand', 'österreichweit', 'wird laufend angeboten', 100, 7, 'unklar',
  [(Z, 'Personale Kompetenz', 1.0), (LGT, 'Wahlteil: Didaktische Kompetenz', 2.0), (DU, 'Wahlteil: Personale Kompetenz', 1.0)],
  'Lernen durch Erleben: Outdoor-Übungen, Reflexion und Transfer in den Arbeitsalltag. Module an wechselnden Orten.',
  ['Grundlagen der Erlebnispädagogik', 'Sicherheit und Verantwortung', 'Reflexion und Transfer'], False),
 ('Politische Bildung für Erwachsene', 'Forum Demokratie lernen', 'österreichweit', '09.03.2027 - 19.10.2027', 96, 7, 'unklar',
  [(Z, 'Gesellschaft und Bildung', 1.5), (DU, 'Bildungstheoretische Kompetenz', 2.0), (DU, 'Wahlteil: Bildungstheoretische Kompetenz', 1.0)],
  'Der Lehrgang vermittelt Grundlagen und Methoden politischer Bildung – von Demokratie über Medienbildung bis zur Moderation kontroverser Themen.',
  ['Demokratie und Teilhabe', 'Methoden politischer Bildung', 'Kontroverse Themen moderieren'], True),
 ('Grundlagen der Organisationsentwicklung', 'Akademie Donaublick', 'Oberösterreich, Linz', 'wird laufend angeboten', 48, 4, 'unklar',
  [(Z, 'Managementkompetenz', 1.0), (BM, 'Wahlpflichtteil: Organisationen und Organisationsentwicklung', 2.0), (DU, 'Leitungs- und Führungskompetenz', 1.0)],
  'Wie verändern sich Bildungsorganisationen? Modelle, Werkzeuge und Fallbeispiele für Veränderungsprozesse.',
  ['Organisationsmodelle', 'Veränderungsprozesse begleiten', 'Fallbeispiele'], True),
 ('Rechtliche Grundlagen für Bildungsanbieter', 'Akademie Donaublick', 'Oberösterreich, Linz', '12.10.2026 - 14.10.2026', 24, 2, 'unklar',
  [(BM, 'Wahlpflichtteil: Rechtliches', 1.5), (Z, 'Managementkompetenz', 0.5)],
  'Verträge, Datenschutz, Urheberrecht und Haftung: das Wichtigste für Bildungsanbieter und selbständige Trainer:innen.',
  ['Verträge mit Teilnehmenden', 'Datenschutz im Kurs', 'Urheberrecht bei Materialien'], True),
 ('Achtsamkeit im Lehralltag', 'Volksbildungswerk Seenland', 'Oberösterreich, Vöcklabruck', 'wird laufend angeboten', 12, 1, 'unklar',
  [],
  'Kurze Übungen für mehr Gelassenheit vor und während des Unterrichts. Ein offener Abendkurs ohne Anrechnung.',
  ['Atemübungen', 'Pausen gestalten', 'Achtsam kommunizieren'], False),
 ('Stimmtraining für Vortragende', 'Volksbildungswerk Seenland', 'Oberösterreich, Vöcklabruck', 'wird laufend angeboten', 8, 0.5, 'unklar',
  [],
  'Stimme schonen, deutlich sprechen, Pausen setzen: ein Praxisabend für alle, die viel sprechen.',
  ['Atmung und Stimme', 'Artikulation', 'Stimmhygiene'], False),
 ('Kursleiter:innen-Basis für Volksbildung', 'Volksbildungswerk Seenland', 'Oberösterreich, Bad Ischl', 'wird laufend angeboten', 60, 4, 'unklar',
  [(Z, 'Didaktische Kompetenz', 1.5), (Z, 'Grundlagen der Pädagogik', 1.0), (DU, 'Wahlteil: Didaktische Kompetenz', 1.0)],
  'Für neue Kursleiter:innen in der regionalen Erwachsenenbildung: Kurse planen, Gruppen leiten, Teilnehmende gewinnen.',
  ['Kursplanung', 'Gruppen leiten', 'Werbung für Kurse'], True),
 ('Personalentwicklung in kleinen Organisationen', 'Weiterbildungszentrum Traunviertel', 'Oberösterreich, Wels', 'wird laufend angeboten', 32, 2.5, 'unklar',
  [(BM, 'Wahlpflichtteil: Personalentwicklung', 2.0), (Z, 'Managementkompetenz', 0.5)],
  'Mitarbeitende fördern, auch ohne große Personalabteilung: Gespräche, Entwicklungspläne und Weiterbildungsbudgets.',
  ['Entwicklungsgespräche', 'Kompetenzmodelle', 'Weiterbildung planen'], False),
 ('Supervision und Intervision für Beratende', 'Lernhaus Am Kanal', 'Wien', 'wird laufend angeboten', 20, 1.5, 'unklar',
  [(BER, 'Wahlteil: Beratungskompetenz', 1.0), (DU, 'Personale Kompetenz', 0.5)],
  'Regelmäßige Fallbesprechung in einer festen Gruppe – zur Qualitätssicherung der eigenen Beratungsarbeit.',
  ['Fallbesprechung', 'Kollegiale Beratung', 'Selbstreflexion'], True),
 ('Coaching mit Pferden', 'Coachingakademie Feldrand', 'Vorarlberg, Dornbirn', '15.03.2027 - 20.03.2027', 40, 3, 'unklar',
  [(Z, 'Wahlteil: Personale Kompetenz', 1.0), (DU, 'Wahlteil: Fachkompetenz', 1.5)],
  'Pferde reagieren unmittelbar auf Haltung und Stimmung. Der Kurs nutzt diese Rückmeldung für Führungs- und Persönlichkeitsentwicklung.',
  ['Wirkung von Tieren im Coaching', 'Übungen mit Pferden', 'Transfer in den Beruf'], True),
 ('Basisbildung im ländlichen Raum', 'Pannonia Lernwerkstatt', 'Burgenland, Oberwart', 'wird laufend angeboten', 40, 3, 'unklar',
  [(B, 'Fachdidaktik Alphabetisierung', 1.5), (B, 'Digitale Kompetenz', 1.0), (Z, 'Gesellschaft und Bildung', 0.5)],
  'Wie erreicht man Lernende in kleinen Gemeinden? Aufsuchende Bildungsarbeit, Kooperationen und mobile Lernangebote.',
  ['Zielgruppen erreichen', 'Kooperation mit Gemeinden', 'Mobile Lernangebote'], True),
 ('Outdoor-Training und Teamentwicklung', 'Wanderakademie Alpenrand', 'Steiermark, Wien', 'wird laufend angeboten', 32, 2, 'unklar',
  [(LGT, 'Wahlpflichtteil: Gruppenprozesse und -dynamik', 1.5), (DU, 'Wahlteil: Soziale Kompetenz', 0.5)],
  'Teamübungen im Freien mit anschließender Reflexion. Termine in der Steiermark und in Wien.',
  ['Kooperative Übungen', 'Reflexion', 'Teamrollen'], False),
 ('Wissensmanagement in Bildungseinrichtungen', 'Akademie Donaublick', 'Oberösterreich, Online', '20.11.2026 - 21.01.2027', 24, 2, 'unklar',
  [(BM, 'Wahlpflichtteil: Wissensmanagement', 1.5), (Z, 'Medienkompetenz', 0.5)],
  'Wissen sichern und teilen: Dokumentation, Wikis und Übergaben. Erster Termin in Linz, danach online.',
  ['Wissensarten', 'Werkzeuge für Dokumentation', 'Übergaben gestalten'], True),
 ('Mentaltraining für Trainer:innen', 'Coachingakademie Feldrand', 'österreichweit', 'wird laufend angeboten', 16, 1, 'unklar',
  [],
  'Techniken aus dem Mentaltraining für mehr Fokus und Sicherheit im Training. Ohne Anrechnung, als persönliche Weiterbildung.',
  ['Visualisierung', 'Selbstgespräche', 'Fokus halten'], True),
]

# Wie im echten wba-Feld „Zusatzinformationen“: bei manchen Angeboten steht dort, wie der Kurs stattfindet.
EXTRA_INFO = {
    'Lehrgang Erwachsenenbildung kompakt': 'Auch online via Zoom / MS Teams',
    'Trainer:innenausbildung mit Praxisprojekt': 'Es gibt Termine in Präsenz und einige Online-Live',
    'Bildungsberatung für Erwachsene': 'Modul 3 "Live-Online"',
    'E-Learning-Kurse gestalten mit Moodle': 'Lernen im eigenen Tempo, Start jederzeit möglich',
    'Supervision und Intervision für Beratende': 'Kursort Online via Zoom',
    'Kommunikation und Gesprächsführung': 'Kursort Online via Zoom',
    'Kursleiter:innen-Basis für Volksbildung': 'Der Kurs findet als Präsenzveranstaltung in Bad Ischl statt',
}

# Wie in den echten wba-Daten fehlt bei den meisten Angeboten ein eindeutiges Lernformat.
UNCLEAR_FORMAT = {'Beratungsgespräche professionell führen', 'Projektmanagement in Bildungseinrichtungen', 'Bildungsmarketing mit kleinem Budget',
                  'Basisbildung: Alphabetisierung in der Praxis', 'Gruppendynamik verstehen und steuern', 'Feedback und Leistungsbeurteilung in Kursen',
                  'Führen in Bildungsorganisationen', 'Bibliothek als Lernort gestalten', 'Selbstreflexion und Resilienz für Trainer:innen'}

PROFILE_ORDER = [Z, B, LGT, BER, BM, BIB, DU]
REASONS = {
 'Präsenz': ('mittel', 'Fiktive Beispielangabe: Durchführung vor Ort ausdrücklich genannt.'),
 'Live-Webinar': ('mittel', 'Fiktive Beispielangabe: synchrone Online-Termine ausdrücklich genannt.'),
 'Blended': ('mittel', 'Fiktive Beispielangabe: Präsenz- und Online-Anteile genannt.'),
 'unklar': ('niedrig', 'Fiktive Beispielangabe: kein eindeutiger Hinweis auf das Lernformat.'),
}
STATES = ['Burgenland', 'Kärnten', 'Niederösterreich', 'Oberösterreich', 'Salzburg', 'Steiermark', 'Tirol', 'Vorarlberg', 'Wien']

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')).strip('-')

def span(term):
    d = re.findall(r'(\d{2})\.(\d{2})\.(\d{4})', term)
    if len(d) < 2 or any(int(y) < 2000 for _, _, y in d):
        return None
    a, b = (datetime.date(int(y), int(m), int(t)) for t, m, y in (d[0], d[-1]))
    return (b - a).days + 1

courses = []
for i, (title, provider, place, term, ue, ects, fmt, comps, text, contents, has_provider_text) in enumerate(COURSES):
    cid = str(990101 + i)
    if title in UNCLEAR_FORMAT:
        fmt = 'unklar'
    # Typ wie in der wba-Suche: mehrteilige, längere Angebote sind Lehrgänge.
    kind = 'Lehrgang' if re.search(r'lehrgang|ausbildung|diplom', title, re.I) or ue >= 20 else 'Kurs/Seminar'
    url = f'https://example.org/wba-demo/angebot/{cid}'
    link = f'https://example.org/{slug(provider)}/kurse/{slug(title)}'
    comps = sorted(comps, key=lambda c: PROFILE_ORDER.index(c[0]))
    credit = '; '.join(f'{p}: {n} ({e:.1f} ECTS)' for p, n, e in comps) or 'keine'
    wba_text = (f'Bildungsangebot (Beispieldaten) {title} {provider} Umfang: {ue} UE / {str(ects).replace(".", ",")} ECTS (wba) '
                f'Termin: {term} Veranstaltungsort: {place} '
                + (f'Zusatzinformationen: {EXTRA_INFO[title]} ' if title in EXTRA_INFO else '')
                + f'Anrechnung: {credit}. {text}')
    sources = [{'label': 'wba · Angebot und Anerkennung (Beispiel)', 'url': url, 'text': wba_text}]
    if has_provider_text:
        sources.append({'label': 'Anbieterseite · Beispieltext', 'url': link,
                        'text': f'{title} – {provider}. {text} Inhalte: ' + ' · '.join(contents) +
                                '. Anmeldung und weitere Termine auf unserer Website. (Alle Angaben sind erfunden.)'})
    conf, reason = REASONS[fmt]
    courses.append({
        'id': cid, 'title': title, 'type': kind, 'provider': provider, 'location': place,
        'states': [s for s in STATES if s in place], 'online': 'online' in place.lower(),
        'nationwide': 'österreichweit' in place.lower(), 'term': term, 'ue': ue, 'ects': ects,
        'span': span(term), 'format': fmt, 'confidence': conf, 'reason': reason, 'url': url,
        'links': [link], 'competencies': [{'profile': p, 'name': n, 'ects': f'{e:.1f} ECTS'} for p, n, e in comps],
        'sources': sources, 'missingProviderText': not has_provider_text})

data = {'date': 'Beispieldaten', 'demo': True, 'count': len(courses), 'courses': courses}
OUT.write_text('window.WBA_DATA = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';\n', encoding='utf-8')
print(f'{len(courses)} Beispielkurse geschrieben.')
