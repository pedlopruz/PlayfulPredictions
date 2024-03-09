
from .models import PartidosEntrenamiento
import csv
path = "data/futbolDatabase.csv"

def populateDatabase():
    PartidosEntrenamiento.objects.all().delete()
    pe = cargarPartidoEntrenamiento()
    return pe

def cargarPartidoEntrenamiento():
    pe = None
    i = 0
    with open(path, newline='', encoding='utf-8') as csvfile:
        lector_csv = csv.DictReader(csvfile, delimiter=';')
        for numero_fila, fila in enumerate(lector_csv, start=1):
            try:
                id = i+1
                league = fila['\ufeffLeague'].lstrip('\ufeff')
                season = fila['Season']
                home_team = fila['Home Team']
                away_team = fila['Away Team']
                home_goals = fila['Home Goals']
                away_goals = fila['Away Goals']
                winner = fila['Winner']
                home_points = fila['Home Points']
                away_points = fila['Away Points']
                i = i+1
                pe = PartidosEntrenamiento.objects.create(id = id, liga=league, temporada=season, equipo_local=home_team, equipo_visitante=away_team, goles_local=home_goals, goles_visitante=away_goals, puntos_local=home_points, puntos_visitante=away_points, winner=winner)
            except Exception as e:
                print(f"Error en la fila {numero_fila}: {e}")
                # Opcional: Puedes añadir más información de la fila si es necesario
                print(f"Contenido de la fila {numero_fila}: {fila}")

    return pe
