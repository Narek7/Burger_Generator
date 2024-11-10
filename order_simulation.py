from processes import vorarbeitstheke, zubereitungstheke, abholung
import random


def bestellung_prozess(env, bestellung_id, zutaten, resources, bestellzeit):
    """Simuliert den Prozess einer einzelnen Bestellung durch alle Stationen."""
    abholzeit = bestellzeit + 30
    yield env.process(vorarbeitstheke(env, bestellung_id, zutaten, resources, bestellzeit))
    yield env.process(zubereitungstheke(env, bestellung_id, zutaten, resources, abholzeit, bestellzeit))
    yield env.process(abholung(env, bestellung_id, bestellzeit))

def bestellungen_erstellen(env, resources):
    """Generiert Bestellungen zwischen 11:00 und 14:00 Uhr und startet deren Prozesse."""
    aktuelle_zeit = 0  # Startzeitpunkt in Minuten nach 11:00 Uhr (d.h., 11:00 Uhr entspricht 0 Minuten)
    endzeit = 3 * 60  # Endzeitpunkt in Minuten nach 11:00 Uhr (d.h., 14:00 Uhr entspricht 180 Minuten)

    bestellung_id = 0
    while aktuelle_zeit < endzeit:
        bestellzeit = aktuelle_zeit  # Bestellzeit innerhalb des Zeitraums 11:00 bis 14:00 Uhr
        zutaten = {
            'kalte_zutaten': ['Salat', 'Sauce'],
            'patty_typ': random.choice(['Fleisch', 'Geflügel', 'Vegetarisch']),
            'pommes_bestellt': random.random() < 0.5,
        }

        env.process(bestellung_prozess(env, bestellung_id, zutaten, resources, bestellzeit))

        # Berechnen der Wartezeit bis zur nächsten Bestellung
        wartezeit = max(1, abs(int(random.normalvariate(8, 105))))  # mind. 1 Sekunde Intervall
        aktuelle_zeit += wartezeit / 60  # in Minuten umrechnen
        bestellung_id += 1

        # Überprüfen, ob die nächste Bestellung nach 14:00 Uhr wäre
        if aktuelle_zeit >= endzeit:
            break

        yield env.timeout(wartezeit / 60)  # Simpy-Timeout in Minuten



""" 
def bestellungen_erstellen(env, resources):
    #Generiert Bestellungen zwischen 11:00 und 14:00 Uhr und startet deren Prozesse
    aktuelle_zeit = 0  # Startzeitpunkt in Minuten nach 11:00 Uhr (d.h., 11:00 Uhr entspricht 0 Minuten)
    endzeit = 3 * 60  # Endzeitpunkt in Minuten nach 11:00 Uhr (d.h., 14:00 Uhr entspricht 180 Minuten)

    bestellung_id = 0
    while aktuelle_zeit < endzeit:
        bestellzeit = aktuelle_zeit  # Bestellzeit innerhalb des Zeitraums 11:00 bis 14:00 Uhr
        zutaten = {
            'kalte_zutaten': ['Salat', 'Sauce'],
            'patty_typ': random.choice(['Fleisch', 'Geflügel', 'Vegetarisch']),
            'pommes_bestellt': random.random() < 0.5,
        }

        env.process(bestellung_prozess(env, bestellung_id, zutaten, resources, bestellzeit))

        wartezeit = abs(int(random.normalvariate(8, 105)))
        aktuelle_zeit += wartezeit
        bestellung_id += 1
        yield env.timeout(wartezeit)
"""


