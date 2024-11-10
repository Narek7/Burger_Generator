import random
import simpy
import logging
from datetime import timedelta

# Einrichten des Loggings für die Prozesse
logging.basicConfig(filename="burger_zubereitung_logs.txt", level=logging.INFO, format="%(message)s")


def log_event(event):
    """Schreibt das Event in die Logdatei und gibt es in der Konsole aus."""
    logging.info(event)
    print(event)


def format_time(minutes):
    """Formatiert Minuten als Uhrzeit im HH:MM-Format ab 11:00 Uhr."""
    start_time = timedelta(hours=11)  # 11:00 Uhr als Startzeit
    current_time = start_time + timedelta(minutes=minutes)
    hours, remainder = divmod(current_time.total_seconds(), 3600)
    minutes = remainder // 60
    return f"{int(hours):02}:{int(minutes):02}"  # Gibt Zeit im HH:MM-Format zurück


def vorarbeitstheke(env, bestellung_id, zutaten, resources, bestellzeit):
    if env.now > 14.5 * 60:  # 14:30 Uhr in Minuten
        return  # Abbruch des Prozesses, wenn es nach 14:30 Uhr ist

    log_event(
        f"Bestellung {bestellung_id}: Start Vorarbeitstheke um {format_time(env.now)} (Bestellt um {format_time(bestellzeit)})")

    with resources['zuarbeiter'].request() as zuarbeiter_request:
        yield zuarbeiter_request
        log_event(f"Bestellung {bestellung_id}: Zuarbeiter*in zugewiesen um {format_time(env.now)}")

        # Aufwand für das Entnehmen aus dem Gefrierschrank (10-30 Sekunden, Gamma-Verteilung)
        gefrierzeit = random.gammavariate(10, 2) / 60
        yield env.timeout(gefrierzeit)
        log_event(f"Bestellung {bestellung_id}: Zutaten aus Gefrierschrank entnommen nach {gefrierzeit:.2f} Minuten")

        if zutaten['patty_typ'] == 'Fleisch':
            with resources['kontaktgrill'].request() as grill_request:
                yield grill_request
                log_event(
                    f"Bestellung {bestellung_id}: Fleisch-Pattie wird auf dem Grill angebraten um {format_time(env.now)}")
                yield env.timeout(random.uniform(2, 3))

            with resources['garschrank'].request() as garschrank_request:
                yield garschrank_request
                log_event(
                    f"Bestellung {bestellung_id}: Fleisch-Pattie zieht im Garschrank durch um {format_time(env.now)}")
                yield env.timeout(random.uniform(3, 5))
        else:
            with resources['fritteusen'].request() as fritteusen_request:
                yield fritteusen_request
                log_event(
                    f"Bestellung {bestellung_id}: {zutaten['patty_typ']} wird in der Fritteuse zubereitet um {format_time(env.now)}")
                yield env.timeout(random.uniform(6, 10))

    log_event(f"Bestellung {bestellung_id}: Warme Zutaten fertig an der Vorarbeitstheke um {format_time(env.now)}")


"""
def zubereitungstheke(env, bestellung_id, zutaten, resources, abholzeit, bestellzeit):
    #Prozess für den Zusammenbau und die Fertigstellung des Burgers an der Zubereitungstheke durch den Burgermeister
    start_zeitpunkt = max(0, abholzeit - 5)
    yield env.timeout(start_zeitpunkt - env.now)
    log_event(
        f"Bestellung {bestellung_id}: Beginne Zusammenbau frühestens 5 Minuten vor Abholzeit um {format_time(env.now)}")

    with resources['burgermeister'].request() as request:
        yield request
        log_event(
            f"Bestellung {bestellung_id}: Burgermeister beginnt mit dem Zusammenbau des Burgers um {format_time(env.now)}")

        # Toasten des Buns (40 Sekunden)
        yield env.timeout(0.67)
        log_event(f"Bestellung {bestellung_id}: Bun getoastet um {format_time(env.now)}")

        belegzeit = random.normalvariate(5, 1) * len(zutaten['kalte_zutaten'])
        yield env.timeout(belegzeit / 60)
        log_event(f"Bestellung {bestellung_id}: Burger belegt um {format_time(env.now)}")

        if random.random() < 0.05:
            log_event(
                f"Bestellung {bestellung_id}: Fehler bei Zusammenbau, Neustart erforderlich um {format_time(env.now)}")
            yield env.process(zubereitungstheke(env, bestellung_id, zutaten, resources, abholzeit, bestellzeit))
            return

        verpackungszeit = random.uniform(10, 20) / 60
        if zutaten['pommes_bestellt']:
            verpackungszeit += random.uniform(15, 30) / 60
            log_event(f"Bestellung {bestellung_id}: Zusätzliche Zeit für Pommes hinzugefügt")

        yield env.timeout(verpackungszeit)
        log_event(
            f"Bestellung {bestellung_id}: Burger fertiggestellt und verpackt um {format_time(env.now)} (Dauer: {env.now - bestellzeit:.2f} Minuten)")
"""

def zubereitungstheke(env, bestellung_id, zutaten, resources, abholzeit, bestellzeit):
    start_zeitpunkt = abholzeit - 5  # 5 Minuten vor der Abholzeit

    if env.now > 14.5 * 60:  # 14:30 Uhr in Minuten
        return  # Abbruch des Prozesses, wenn es nach 14:30 Uhr ist

    if start_zeitpunkt > env.now:
        yield env.timeout(start_zeitpunkt - env.now)

    log_event(f"Bestellung {bestellung_id}: Beginne Zusammenbau frühestens 5 Minuten vor Abholzeit um {format_time(env.now)}")

    with resources['burgermeister'].request() as request:
        yield request
        log_event(f"Bestellung {bestellung_id}: Burgermeister beginnt mit dem Zusammenbau des Burgers um {format_time(env.now)}")

        # Toasten des Buns (40 Sekunden)
        yield env.timeout(0.67)
        log_event(f"Bestellung {bestellung_id}: Bun getoastet um {format_time(env.now)}")

        belegzeit = random.normalvariate(5, 1) * len(zutaten['kalte_zutaten'])
        yield env.timeout(belegzeit / 60)
        log_event(f"Bestellung {bestellung_id}: Burger belegt um {format_time(env.now)}")

        if random.random() < 0.05:
            log_event(f"Bestellung {bestellung_id}: Fehler bei Zusammenbau, Neustart erforderlich um {format_time(env.now)}")
            yield env.process(zubereitungstheke(env, bestellung_id, zutaten, resources, abholzeit, bestellzeit))
            return

        verpackungszeit = random.uniform(10, 20) / 60
        if zutaten['pommes_bestellt']:
            verpackungszeit += random.uniform(15, 30) / 60
            log_event(f"Bestellung {bestellung_id}: Zusätzliche Zeit für Pommes hinzugefügt")

        yield env.timeout(verpackungszeit)
        log_event(f"Bestellung {bestellung_id}: Burger fertiggestellt und verpackt um {format_time(env.now)} (Dauer: {env.now - bestellzeit:.2f} Minuten)")



def abholung(env, bestellung_id, bestellzeit):
    if env.now > 14.5 * 60:  # 14:30 Uhr in Minuten
        return  # Abbruch des Prozesses, wenn es nach 14:30 Uhr ist

    gesamt_dauer = env.now - bestellzeit
    log_event(
        f"Bestellung {bestellung_id}: Burger zur Abholung bereit um {format_time(env.now)} (Dauer: {gesamt_dauer:.2f} Minuten)")
    yield env.timeout(0)

