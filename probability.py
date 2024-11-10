import pandas as pd


# Funktion zur Berechnung der Häufigkeiten und Wahrscheinlichkeiten für jede Zutat in einer CSV-Datei
# Diese Funktion lädt eine CSV-Datei mit Burger-Bestelldaten und berechnet die Häufigkeit und Wahrscheinlichkeit,
# mit der jede Menge einer Zutat verwendet wird. Für jede Zutat wird eine separate Tabelle erstellt.
# Am Ende werden alle Tabellen in eine Textdatei geschrieben, um eine Übersicht der Wahrscheinlichkeiten zu haben.

def berechne_zutaten_wahrscheinlichkeiten(datei_pfad):

    burger_data = pd.read_csv(datei_pfad)

    # Zutaten-Spalten, die analysiert werden sollen
    zutaten_spalten = ["Bun", "Patty", "Gewuerz", "Kaese", "Bacon", "Salat", "Gemuese", "Sauce"]

    # Eine leere Liste, um die Ergebnisse für jede Zutat zu speichern
    ergebnisse_gesamt = []

    # Schleife über jede Zutat, um Häufigkeiten und Wahrscheinlichkeiten zu berechnen
    for zutat in zutaten_spalten:
        # Zählt, wie oft jede Menge der Zutat verwendet wurde und sortiert die Ergebnisse
        haeufigkeit = burger_data[zutat].value_counts().sort_index()

        # Berechnet die Gesamtzahl der Bestellungen, die eine Menge der Zutat enthalten
        gesamt = haeufigkeit.sum()

        # Die Wahrscheinlichkeit für jede Menge der Zutat, indem die Häufigkeit durch die Gesamtzahl geteilt wird
        wahrscheinlichkeit = haeufigkeit / gesamt

        # Erstellt ein DataFrame, um die Ergebnisse für die aktuelle Zutat zu speichern
        ergebnisse_df = pd.DataFrame({
            zutat: haeufigkeit.index,
            'Häufigkeit': haeufigkeit.values,
            'Wahrscheinlichkeit': wahrscheinlichkeit.values
        })

        # Speichert die Ergebnisse als Text für die Ausgabe und zur Speicherung in der Datei
        ergebnisse_text = f"Ergebnisse für {zutat}:\n" + ergebnisse_df.to_string(index=False) + "\n" + "-" * 50 + "\n"
        ergebnisse_gesamt.append(ergebnisse_text)

        # Ausgabe der Ergebnisse im Terminal
        print(ergebnisse_text)

    # Speichert alle Ergebnisse in einer Textdatei
    with open("zutaten_wahrscheinlichkeiten.txt", "w") as datei:
        datei.writelines(ergebnisse_gesamt)


# Beispielnutzung
datei_pfad = "/Users/Narek/Desktop/Uni/Master of Science/p&k1/PuK_-_Aufgabe_1_Burgerbestellungen.csv"
berechne_zutaten_wahrscheinlichkeiten(datei_pfad)
