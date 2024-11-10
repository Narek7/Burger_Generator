from env_setup import setup_environment
from order_simulation import bestellungen_erstellen


def run_simulation():
    """Startet die gesamte Simulation von 11:00 bis 14:30 Uhr."""
    env, resources = setup_environment()

    # Starte die Bestellungserstellung um 11:00 Uhr
    env.process(bestellungen_erstellen(env, resources))

    # Simulation laufen lassen bis 14:30 Uhr
    env.run(until=14.5 * 60)  # 14:30 in Minuten


if __name__ == "__main__":
    run_simulation()
