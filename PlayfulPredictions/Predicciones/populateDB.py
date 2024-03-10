
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
        numero_partidos = PartidosEntrenamiento.objects.all().count()

        for i in range(1,numero_partidos+1):
            partidos_en_rango_ordenados = PartidosEntrenamiento.objects.filter(id__range=(1, i+1)).order_by('id')
            partido = partidos_en_rango_ordenados.last()
            local = partido.equipo_local
            visitante = partido.equipo_visitante
            
            goles_ultimos_5_partidos_local_siendo_local = 0
            goles_ultimos_5_partidos_visitante_siendo_visitante = 0
            goles_ultimos_5_partidos_equipo_local = 0
            goles_ultimos_5_partidos_equipo_visitante = 0

            puntos_ultimos_5_partidos_local_siendo_local = 0
            puntos_ultimos_5_partidos_visitante_siendo_visitante = 0
            puntos_ultimos_5_partidos_equipo_local = 0
            puntos_ultimos_5_partidos_equipo_visitante = 0

            goles_puntos_local_siendo_local = 0
            goles_puntos_visitante_siendo_visitante=0
            goles_puntos_equipo_local = 0
            goles_puntos_equipo_visitante=0

            goles_en_contra_ultimos_5_partidos_local_siendo_local = 0
            goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante = 0
            goles_en_contra__ultimos_5_partidos_equipo_local = 0
            goles_en_contra__ultimos_5_partidos_equipo_visitante = 0

            for p in reversed(partidos_en_rango_ordenados):

                if goles_puntos_equipo_local >= 5 and goles_puntos_equipo_visitante >=5 and goles_puntos_local_siendo_local >=5 and goles_puntos_visitante_siendo_visitante >=5:
                    continue
                else:
                    if p.equipo_local == local and p.equipo_visitante == visitante:
                        pass

                    elif p.equipo_local != local and p.equipo_visitante != visitante:
                        continue

                    elif p.equipo_local == local and p.equipo_visitante != visitante:
                        if goles_puntos_local_siendo_local <5  and goles_puntos_equipo_local <5:
                            goles_ultimos_5_partidos_local_siendo_local = goles_ultimos_5_partidos_local_siendo_local + p.goles_local
                            puntos_ultimos_5_partidos_local_siendo_local = puntos_ultimos_5_partidos_local_siendo_local + p.puntos_local
                            goles_en_contra_ultimos_5_partidos_local_siendo_local = goles_en_contra_ultimos_5_partidos_local_siendo_local + p.goles_visitante

                            goles_ultimos_5_partidos_equipo_local = goles_ultimos_5_partidos_equipo_local + p.goles_local
                            puntos_ultimos_5_partidos_equipo_local = puntos_ultimos_5_partidos_equipo_local + p.puntos_local
                            goles_en_contra__ultimos_5_partidos_equipo_local = goles_en_contra__ultimos_5_partidos_equipo_local + p.goles_visitante

                            goles_puntos_local_siendo_local = goles_puntos_local_siendo_local+1
                            goles_puntos_equipo_local = goles_puntos_equipo_local +1

                        elif goles_puntos_local_siendo_local <5  and goles_puntos_equipo_local >=5:
                            goles_ultimos_5_partidos_local_siendo_local = goles_ultimos_5_partidos_local_siendo_local + p.goles_local
                            puntos_ultimos_5_partidos_local_siendo_local = puntos_ultimos_5_partidos_local_siendo_local + p.puntos_local
                            goles_en_contra_ultimos_5_partidos_local_siendo_local = goles_en_contra_ultimos_5_partidos_local_siendo_local + p.goles_visitante
                            goles_puntos_local_siendo_local = goles_puntos_local_siendo_local+1

                        elif goles_puntos_local_siendo_local >=5  and goles_puntos_equipo_local <5:
                            goles_ultimos_5_partidos_equipo_local = goles_ultimos_5_partidos_equipo_local + p.goles_local
                            puntos_ultimos_5_partidos_equipo_local = puntos_ultimos_5_partidos_equipo_local + p.puntos_local
                            goles_en_contra__ultimos_5_partidos_equipo_local = goles_en_contra__ultimos_5_partidos_equipo_local + p.goles_visitante

                            goles_puntos_equipo_local = goles_puntos_equipo_local +1
                        else:
                            continue

                    elif p.equipo_local != local and p.equipo_visitante == visitante:
                        if goles_puntos_visitante_siendo_visitante <5 and goles_puntos_equipo_visitante <5:
                            goles_ultimos_5_partidos_visitante_siendo_visitante = goles_ultimos_5_partidos_visitante_siendo_visitante + p.goles_visitante
                            puntos_ultimos_5_partidos_visitante_siendo_visitante = puntos_ultimos_5_partidos_visitante_siendo_visitante + p.puntos_visitante
                            goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante = goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante + p.goles_local

                            goles_ultimos_5_partidos_equipo_visitante = goles_ultimos_5_partidos_equipo_visitante + p.goles_visitante
                            puntos_ultimos_5_partidos_equipo_visitante = puntos_ultimos_5_partidos_equipo_visitante + p.puntos_visitante
                            goles_en_contra__ultimos_5_partidos_equipo_visitante = goles_en_contra__ultimos_5_partidos_equipo_visitante + p.goles_local
                                
                            goles_puntos_visitante_siendo_visitante = goles_puntos_visitante_siendo_visitante+1
                            goles_puntos_equipo_visitante = goles_puntos_equipo_visitante+1

                        elif goles_puntos_visitante_siendo_visitante <5 and goles_puntos_equipo_visitante >=5:
                            goles_ultimos_5_partidos_visitante_siendo_visitante = goles_ultimos_5_partidos_visitante_siendo_visitante + p.goles_visitante
                            puntos_ultimos_5_partidos_visitante_siendo_visitante = puntos_ultimos_5_partidos_visitante_siendo_visitante + p.puntos_visitante
                            goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante = goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante + p.goles_local
                            goles_puntos_visitante_siendo_visitante = goles_puntos_visitante_siendo_visitante+1
                            
                        elif goles_puntos_visitante_siendo_visitante >=5 and goles_puntos_equipo_visitante <5:
                            goles_ultimos_5_partidos_equipo_visitante = goles_ultimos_5_partidos_equipo_visitante + p.goles_visitante
                            puntos_ultimos_5_partidos_equipo_visitante = puntos_ultimos_5_partidos_equipo_visitante + p.puntos_visitante
                            goles_en_contra__ultimos_5_partidos_equipo_visitante = goles_en_contra__ultimos_5_partidos_equipo_visitante + p.goles_local
                            
                            goles_puntos_equipo_visitante = goles_puntos_equipo_visitante + 1
                        else:
                            continue

                    elif local == p.equipo_visitante:
                        if goles_puntos_equipo_local < 5:
                            goles_ultimos_5_partidos_equipo_local = goles_ultimos_5_partidos_equipo_local + p.goles_local
                            puntos_ultimos_5_partidos_equipo_local = puntos_ultimos_5_partidos_equipo_local + p.puntos_local
                            goles_en_contra_ultimos_5_partidos_local_siendo_local = goles_en_contra_ultimos_5_partidos_local_siendo_local + p.goles_visitante

                            goles_puntos_equipo_local = goles_puntos_equipo_local +1
                        else:
                            continue
                    elif visitante == p.equipo_local:
                        if goles_puntos_equipo_visitante < 5:
                            goles_ultimos_5_partidos_equipo_visitante = goles_ultimos_5_partidos_equipo_visitante + p.goles_visitante
                            puntos_ultimos_5_partidos_equipo_visitante = puntos_ultimos_5_partidos_equipo_visitante + p.puntos_visitante
                            goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante = goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante + p.goles_local
                            
                            goles_puntos_equipo_visitante = goles_puntos_equipo_visitante + 1
                        else:
                            continue
                

            if goles_puntos_equipo_local < 5 and goles_puntos_equipo_visitante <5 and goles_puntos_local_siendo_local <5 and goles_puntos_visitante_siendo_visitante <5:
                    partido.falta = True
                    partido.save()
            else:
                partido.goles_ultimos_5_partidos_local_siendo_local = goles_ultimos_5_partidos_local_siendo_local
                partido.goles_ultimos_5_partidos_equipo_local = goles_ultimos_5_partidos_equipo_local
                partido.goles_ultimos_5_partidos_visitante_siendo_visitante = goles_ultimos_5_partidos_visitante_siendo_visitante
                partido.goles_ultimos_5_partidos_equipo_visitante = goles_ultimos_5_partidos_equipo_visitante

                partido.puntos_ultimos_5_partidos_local_siendo_local = puntos_ultimos_5_partidos_local_siendo_local
                partido.puntos_ultimos_5_partidos_equipo_local = puntos_ultimos_5_partidos_equipo_local
                partido.puntos_ultimos_5_partidos_visitante_siendo_visitante = puntos_ultimos_5_partidos_visitante_siendo_visitante
                partido.puntos_ultimos_5_partidos_equipo_visitante = puntos_ultimos_5_partidos_equipo_visitante

                partido.goles_en_contra_ultimos_5_partidos_local_siendo_local = goles_en_contra_ultimos_5_partidos_local_siendo_local
                partido.goles_en_contra_ultimos_5_partidos_equipo_local = goles_en_contra__ultimos_5_partidos_equipo_local
                partido.goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante = goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante
                partido.goles_en_contra_ultimos_5_partidos_equipo_visitante = goles_en_contra__ultimos_5_partidos_equipo_visitante
                partido.save()
                


    return pe
