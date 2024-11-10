# env_setup.py

import simpy


def setup_environment():
    """Erstellt die SimPy-Umgebung und die Ressourcen für die Stationen."""
    env = simpy.Environment()

    # Ressourcen für die Arbeitsstationen entsprechend der Ausstattung
    resources = {
        'fritteusen': simpy.Resource(env, capacity=4),  # Vier Fritteusen
        'kontaktgrill': simpy.Resource(env, capacity=1),  # Ein Kontaktgrill
        'garschrank': simpy.Resource(env, capacity=1),  # Ein Garschrank
        'burgermeister': simpy.Resource(env, capacity=1),  # Ein Burgermeister
        'zuarbeiter': simpy.Resource(env, capacity=2)  # Zwei Zuarbeiter*innen
    }

    return env, resources
