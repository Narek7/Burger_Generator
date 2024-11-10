import simpy
import random

# Parameter festlegen
BESTELL_INTERVAL = [8, 105]  # Zeit zwischen Bestellungen in Sekunden [Normal(8,105)]
orderCounter = 0
STARTZEIT = 11 * 3600  # Startzeit in Sekunden (11:00 Uhr)

class BurgerGenerator:
    def __init__(self, env):
        self.env = env
        env.process(self.bestellungen_erhalten())

    def bestellungen_erhalten(self):
        """
        Bestellungen in der Mittagszeit (von 11:00 bis 14:00 Uhr) annehmen.
        """
        while True:
            zeit_bis_naechste_bestellung = abs(random.gauss(BESTELL_INTERVAL[0], BESTELL_INTERVAL[1]))
            yield self.env.timeout(zeit_bis_naechste_bestellung)
            self.bestellung_bearbeiten()

    def bestellung_bearbeiten(self):
        """
        Bearbeiten der Bestellung (Ausgabe der Uhrzeit im Format HH:MM:SS).
        """
        global orderCounter

        orderCounter += 1
        aktuelle_uhrzeit = self.sekunden_zu_uhrzeit(self.env.now)
        print(f"Bestellung {orderCounter} um {aktuelle_uhrzeit} erhalten und bearbeitet.")

    @staticmethod
    def sekunden_zu_uhrzeit(sekunden):
        """
        Wandelt Sekunden in das Format HH:MM:SS um, basierend auf der Startzeit (11:00 Uhr).
        """
        sekunden += STARTZEIT  # Startzeit hinzufügen (11:00 Uhr)
        stunden = sekunden // 3600
        minuten = (sekunden % 3600) // 60
        sekunden = sekunden % 60
        return f"{int(stunden):02d}:{int(minuten):02d}:{int(sekunden):02d}"


# Simulation starten
def run_simulation(zeit_in_stunden=3):
    env = simpy.Environment()
    mensa = BurgerGenerator(env)
    env.run(until=zeit_in_stunden * 3600)  # Simulationszeit in Sekunden


if __name__ == "__main__":
    run_simulation(zeit_in_stunden=3)  # Für eine Simulation von 3 Stunden (11:00 bis 14:00 Uhr)
