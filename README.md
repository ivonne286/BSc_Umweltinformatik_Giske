# Readme

Dieses Repository wurde im Rahmen der Bachelorarbeit **"Überprüfung der Datenqualität im Citizen-Science-Projekt "Die Herbonauten" am Botanischen Garten Berlin"** von Ivonne Giske (HTW Berlin) erstellt.

## Zweck

Das Repository enthält Daten und Skripte, die zur Erstellung der Projekt-Datenbank sowie weiterer Tabellen und Diagramme zur Auswertung und Fehleranalyse verwendet wurden.

## Zugriff auf die Datenbank (SQLite)

Die Datei **db_20240927.sqlite** im Stammverzeichnis enthält die finale Datenbank. Zur Ansicht eignet sich das freie Tool 'DB Browser for SQLite', erhältlich unter https://sqlitebrowser.org/ oder die Webseite https://inloop.github.io/sqlite-viewer/ mit der die Tabellen und Views direkt im Browser angeschaut werden können.


_Möchten Sie die Datenbank neu generieren, lesen Sie bitte weiter:_

## Installationsvoraussetzungen

**Voraussetzung**\
aktuelles python (getestet mit 3.12, minimum >= 3.9)

**Achtung** Das Hauptscript zur Erstellung der Datenbank funktioniert ohne weitere Voraussetzungen. Es kann wie unter [Erstellen der Datenbank](#erstellen-der-datenbank) beschrieben direkt ausgeführt werden.

Um weitere Skripte (im Unterordner `/scripts`) auszuführen, werden zusätzliche Python-Pakete benötigt (matplotlib, pandas). Diese können wie folgt installiert werden.

1. Erstellen einer virtuellen Umgebung für die Python-Abhängigkeiten:

```sh
python -m venv .venv
```

2. Virtuelle Umgebung aktivieren

**Windows**

```sh
.\.venv\Scripts\activate
```

**Linux / Mac**

```sh
source .venv/bin/activate
```

3. Abhängigkeiten installieren

```sh
python -m pip intall -r .\requirements.txt
```

4. Verlassen der virtuellen Umgebung nach Abschluss

```sh
deactivate
```

## Erstellen der Datenbank

Um die Datenbank von Grund auf neu zu erstellen, führen Sie bitte folgenden Befehl in der Kommandozeile aus:

```sh
python3 ./create_db.py
```
oder

```sh
python create_db.py
```

Danach wird die Datenbank aus den CSV-Dateien der Missionen und Tabellenvorlagen erstellt, die Stichprobe sowie die Auswertung werden importiert.

Die Datei wird als `db_neu.sqlite` erstellt und im Ordner `/output/` abgelegt.

**Achtung** Die für die Abschlussarbeit verwendete Version der Datenbank ist zwecks Reproduzierbarkeit als `db_20240927.sqlite` im Stammverzeichnis abgelegt.

## Ausführen von Hilfsskripten

Der Ordner `/scripts` enthält einige weitere Skripte, die zur Ziehung der Stichprobe oder für die Erstellung von Diagrammen und Tabellen verwendet wurden.

| Dateiname                       | Funktion                                                    | Output                       |
| ------------------------------- | ----------------------------------------------------------- | ---------------------------- |
| create_cross_table.py           | erzeugt Kreuztabelle Kategorie Fehlertyp                    | `/output/kreuztabelle.csv`   |
| create_diagram_Fehlerquoten1.py | erzeugt Diagramm der Fehlerquotenentwicklung                | Fenster mit Diagramm         |
| create_diagram_Fehlerquoten2.py | erzeugt Diagramm der aktuellen und potenzielle Fehlerquoten | Fenster mit Diagramm         |
| draw_sample.py                  | zieht eine Stichprobe der Größe `sample_size`               | `/output/sample_example.csv` |

## ERM

![ERM](./images/ERM_Herbonauten_DB.jpg)
