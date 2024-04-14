from bs4 import BeautifulSoup
import urllib.request
from .models import PartidosEntrenamiento, PartidoReal, PartidoSinPredecir
import csv
path = "data/Entrenamiento.csv"
path2 = "data/Temporada19-23.csv"
path3 = "data/Partido_Entrenamiento.csv"


def populateDatabaseEntrenamiento():
    PartidosEntrenamiento.objects.all().delete()
    r = cargarPartidoEntrenamiento()
    r18_19 = cargarPartidoEntrenamientoLigaEsp18_19()
    r218_19 = cargarPartidoEntrenamientoLigaEsp2_18_19()
    r19_23 = cargarPartidoEntrenamientoTemporada19_23()
    ad = cargarDatosEntrenamientoAdicionales_Ultimos_5_Partidos()
    ad2 = cargarDatosEntrenamientoAdicionales_Ultimos_3_Partidos()
    return (r,r18_19,r218_19,r19_23,ad,ad2)


def populateDatabaseSinPredecir():
    PartidoSinPredecir.objects.all().delete()
    PartidoReal.objects.all().delete()
    le = cargarPartidoRealLigaEsp()
    esp2 = cargarPartidoRealEsp2()
    pr = cargarPartidoSinPredecir_Ultimos_5_Partidos()
    pr2 = cargarPartidoSinPredecir_Ultimos_3_Partidos()
    el = PartidoSinPredecir.objects.last().delete()
    return (le,esp2,pr,pr2, el)

def cargarPartidoEntrenamiento():
    pe = None
    with open(path, newline='', encoding='utf-8') as csvfile:
        lector_csv = csv.DictReader(csvfile, delimiter=';')
        for numero_fila, fila in enumerate(lector_csv, start=1):
            try:
                id = fila['\ufeffid'].lstrip('\ufeff')
                season = fila['Season']
                league = fila['League']
                jornada = fila['Jornada']
                home_team = fila['Home Team']
                away_team = fila['Away Team']
                home_goals = fila['Home Goals']
                away_goals = fila['Away Goals']
                winner = fila['Winner']
                home_points = fila['Home Points']
                away_points = fila['Away Points']
                pe = PartidosEntrenamiento.objects.create(id = id, liga=league, temporada=season, jornada=jornada,
                                                          equipo_local=home_team, equipo_visitante=away_team, goles_local=home_goals, 
                                                          goles_visitante=away_goals, puntos_local=home_points, puntos_visitante=away_points, 
                                                          winner=winner)
            except Exception as e:
                print(f"Error en la fila {numero_fila}: {e}")
                # Opcional: Puedes añadir más información de la fila si es necesario
                print(f"Contenido de la fila {numero_fila}: {fila}")
    return pe



def cargarPartidoEntrenamientoLigaEsp18_19():
    id = 37148
    temporada = "2018-19"
    for p in range(1,39):
        url = "https://resultados.as.com/resultados/futbol/primera/2018_2019/jornada/regular_a_"+ str(p) +"/"
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        request = urllib.request.Request(url, headers=headers)
        liga = "LaLiga EA Sports"
        jornada = p
        try:
            with urllib.request.urlopen(request) as f:
                s = BeautifulSoup(f, "lxml")
                encuentros = s.find("div", class_="container content").find("div", class_="row").find_next_sibling().find("div", class_="col-md-12").find("div", class_="row").find("div", class_="cont-resultados cf").find("ul").find_all("li", class_="list-resultado")
                for encuentro in encuentros:
                    equipo_local = encuentro.find("div", class_="equipo-local").find("a", itemprop="url").find("span", class_="nombre-equipo").string.strip()
                    equipo_visitante = encuentro.find("div", class_="equipo-visitante").find("a", itemprop="url").find("span", class_="nombre-equipo").string.strip()
                    resultado = encuentro.find("div", class_="cont-resultado finalizado").find("a", class_="resultado").string.strip()
                    goles = resultado.split("-")
                    goles_local = int(goles[0].strip())
                    goles_visitante = int(goles[1].strip())
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1
                    
                    PartidosEntrenamiento.objects.create(id = id, liga = liga, temporada=temporada, jornada = jornada,
                                                          equipo_local=equipo_local, equipo_visitante=equipo_visitante, 
                                                          goles_local=goles_local, goles_visitante=goles_visitante, puntos_local=puntos_local, 
                                                          puntos_visitante=puntos_visitante, winner=winner)
                    id = id+1
                    
        except Exception as e:
            print(f"Ocurrió un error al procesar la jornada {1}: {e}")
    return "Carga Completada"  

def cargarPartidoEntrenamientoLigaEsp2_18_19():
    id = 37529
    temporada = "2018-19"
    for p in range(1, 43):
        url = "https://resultados.as.com/resultados/futbol/segunda/2018_2019/jornada/regular_a_" + str(p) + "/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        request = urllib.request.Request(url, headers=headers)
        liga = "LaLiga Hypermotion"
        jornada = p
        try:
            with urllib.request.urlopen(request) as f:
                s = BeautifulSoup(f, "lxml")
                encuentros = s.find("div", class_="container content").find("div", class_="row").find_next_sibling().find_next_sibling().find("div", class_="col-md-12").find("div", class_="row").find("div", class_="cont-resultados cf").find("ul").find_all("li", class_="list-resultado")
                for encuentro in encuentros:
                    try:
                        equipo_local = encuentro.find("div", class_="equipo-local").find("a", itemprop="url").find("span", class_="nombre-equipo").string.strip()
                        equipo_visitante = encuentro.find("div", class_="equipo-visitante").find("a", itemprop="url").find("span", class_="nombre-equipo").string.strip()
                        resultado = encuentro.find("div", class_="cont-resultado finalizado")
                        if resultado.find("a", class_="resultado"):
                            resultado = resultado.find("a", class_="resultado").string.strip()
                            goles = resultado.split("-")
                            goles_local = int(goles[0].strip())
                            goles_visitante = int(goles[1].strip())
                        else:
                            resultado = resultado.find("span", class_="resultado").string.strip()
                            goles = resultado.split("-")
                            goles_local = int(goles[0].strip())
                            goles_visitante = int(goles[1].strip())
                        if goles_local > goles_visitante:
                            winner = "1"
                            puntos_local = 3
                            puntos_visitante = 0
                        elif goles_visitante > goles_local:
                            winner = "2"
                            puntos_local = 0
                            puntos_visitante = 3
                        else:
                            winner = "X"
                            puntos_local = 1
                            puntos_visitante = 1

                        PartidosEntrenamiento.objects.create(id=id, liga=liga, temporada=temporada, jornada=jornada,
                                                              equipo_local=equipo_local, equipo_visitante=equipo_visitante,
                                                              goles_local=goles_local, goles_visitante=goles_visitante,
                                                              puntos_local=puntos_local, puntos_visitante=puntos_visitante,
                                                              winner=winner)
                        id = id + 1
                    except Exception as e:
                        print(f"Ocurrió un error al procesar el partido {equipo_local} vs {equipo_visitante} en la jornada {jornada} y resultado {resultado}: {e}")
        except Exception as e:
            print(f"Ocurrió un error al procesar la jornada {p}: {e}")
    return "Carga Completada"
  
def cargarPartidoEntrenamientoTemporada19_23():
    id = 37991
    pe = None
    with open(path2, newline='', encoding='utf-8') as csvfile:
        lector_csv = csv.DictReader(csvfile, delimiter=';')
        for numero_fila, fila in enumerate(lector_csv, start=1):
            try:
                league = fila['\ufeffLeague'].lstrip('\ufeff')
                season = fila['Season']
                home_team = fila['Home Team']
                away_team = fila['Away Team']
                home_goals = fila['Home Goals']
                away_goals = fila['Away Goals']
                winner = fila['Winner']
                home_points = fila['Home Points']
                away_points = fila['Away Points']
                jornada = fila['Jornada']
                pe = PartidosEntrenamiento.objects.create(id = id, liga=league, temporada=season, jornada=jornada,
                                                          equipo_local=home_team, equipo_visitante=away_team, 
                                                          goles_local=home_goals, goles_visitante=away_goals, 
                                                          puntos_local=home_points, puntos_visitante=away_points, winner=winner)
                id = id+1
            except Exception as e:
                print(f"Error en la fila {numero_fila}: {e}")
                print(f"Contenido de la fila {numero_fila}: {fila}")
    return pe

def cargarDatosEntrenamientoAdicionales_Ultimos_5_Partidos():
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
        goles_en_contra_ultimos_5_partidos_equipo_local = 0
        goles_en_contra_ultimos_5_partidos_equipo_visitante = 0

        for p in reversed(partidos_en_rango_ordenados):

            if goles_puntos_equipo_local >= 5 and goles_puntos_equipo_visitante >=5 and goles_puntos_local_siendo_local >=5 and goles_puntos_visitante_siendo_visitante >=5:
                continue
            else:
                if p.equipo_local == local and p.equipo_visitante == visitante:
                    pass

                elif p.equipo_local == local and p.equipo_visitante != visitante:
                    if goles_puntos_local_siendo_local <5  and goles_puntos_equipo_local <5:
                        goles_ultimos_5_partidos_local_siendo_local = goles_ultimos_5_partidos_local_siendo_local + p.goles_local
                        puntos_ultimos_5_partidos_local_siendo_local = puntos_ultimos_5_partidos_local_siendo_local + p.puntos_local
                        goles_en_contra_ultimos_5_partidos_local_siendo_local = goles_en_contra_ultimos_5_partidos_local_siendo_local + p.goles_visitante

                        goles_ultimos_5_partidos_equipo_local = goles_ultimos_5_partidos_equipo_local + p.goles_local
                        puntos_ultimos_5_partidos_equipo_local = puntos_ultimos_5_partidos_equipo_local + p.puntos_local
                        goles_en_contra_ultimos_5_partidos_equipo_local = goles_en_contra_ultimos_5_partidos_equipo_local + p.goles_visitante

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
                        goles_en_contra_ultimos_5_partidos_equipo_visitante = goles_en_contra_ultimos_5_partidos_equipo_visitante + p.goles_local
                                
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
                        goles_en_contra_ultimos_5_partidos_equipo_visitante = goles_en_contra_ultimos_5_partidos_equipo_visitante + p.goles_local
                            
                        goles_puntos_equipo_visitante = goles_puntos_equipo_visitante + 1
                    else:
                        continue

                elif local == p.equipo_visitante:
                    if goles_puntos_equipo_local < 5:
                        goles_ultimos_5_partidos_equipo_local = goles_ultimos_5_partidos_equipo_local + p.goles_visitante
                        puntos_ultimos_5_partidos_equipo_local = puntos_ultimos_5_partidos_equipo_local + p.puntos_visitante
                        goles_en_contra_ultimos_5_partidos_equipo_local = goles_en_contra_ultimos_5_partidos_equipo_local + p.goles_local

                        goles_puntos_equipo_local = goles_puntos_equipo_local +1
                    else:
                        continue
                elif visitante == p.equipo_local:
                    if goles_puntos_equipo_visitante < 5:
                        goles_ultimos_5_partidos_equipo_visitante = goles_ultimos_5_partidos_equipo_visitante + p.goles_local
                        puntos_ultimos_5_partidos_equipo_visitante = puntos_ultimos_5_partidos_equipo_visitante + p.puntos_local
                        goles_en_contra_ultimos_5_partidos_equipo_visitante = goles_en_contra_ultimos_5_partidos_equipo_visitante + p.goles_visitante
                            
                        goles_puntos_equipo_visitante = goles_puntos_equipo_visitante + 1
                    else:
                        continue
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
            partido.goles_en_contra_ultimos_5_partidos_equipo_local = goles_en_contra_ultimos_5_partidos_equipo_local
            partido.goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante = goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante
            partido.goles_en_contra_ultimos_5_partidos_equipo_visitante = goles_en_contra_ultimos_5_partidos_equipo_visitante
            partido.save()
                
def cargarDatosEntrenamientoAdicionales_Ultimos_3_Partidos():
    numero_partidos = PartidosEntrenamiento.objects.all().count()
    for i in range(1,numero_partidos+1):
        partidos_en_rango_ordenados = PartidosEntrenamiento.objects.filter(id__range=(1, i+1)).order_by('id')
        partido = partidos_en_rango_ordenados.last()
        local = partido.equipo_local
        visitante = partido.equipo_visitante
            
        goles_ultimos_3_partidos_local_siendo_local = 0
        goles_ultimos_3_partidos_visitante_siendo_visitante = 0
        goles_ultimos_3_partidos_equipo_local = 0
        goles_ultimos_3_partidos_equipo_visitante = 0

        puntos_ultimos_3_partidos_local_siendo_local = 0
        puntos_ultimos_3_partidos_visitante_siendo_visitante = 0
        puntos_ultimos_3_partidos_equipo_local = 0
        puntos_ultimos_3_partidos_equipo_visitante = 0

        goles_puntos_local_siendo_local = 0
        goles_puntos_visitante_siendo_visitante=0
        goles_puntos_equipo_local = 0
        goles_puntos_equipo_visitante=0

        goles_en_contra_ultimos_3_partidos_local_siendo_local = 0
        goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = 0
        goles_en_contra_ultimos_3_partidos_equipo_local = 0
        goles_en_contra_ultimos_3_partidos_equipo_visitante = 0

        for p in reversed(partidos_en_rango_ordenados):

            if goles_puntos_equipo_local >= 3 and goles_puntos_equipo_visitante >=3 and goles_puntos_local_siendo_local >=3 and goles_puntos_visitante_siendo_visitante >=3:
                continue
            else:
                if p.equipo_local == local and p.equipo_visitante == visitante:
                    pass

                elif p.equipo_local == local and p.equipo_visitante != visitante:
                    if goles_puntos_local_siendo_local <3  and goles_puntos_equipo_local <3:
                        goles_ultimos_3_partidos_local_siendo_local = goles_ultimos_3_partidos_local_siendo_local + p.goles_local
                        puntos_ultimos_3_partidos_local_siendo_local = puntos_ultimos_3_partidos_local_siendo_local + p.puntos_local
                        goles_en_contra_ultimos_3_partidos_local_siendo_local = goles_en_contra_ultimos_3_partidos_local_siendo_local + p.goles_visitante

                        goles_ultimos_3_partidos_equipo_local = goles_ultimos_3_partidos_equipo_local + p.goles_local
                        puntos_ultimos_3_partidos_equipo_local = puntos_ultimos_3_partidos_equipo_local + p.puntos_local
                        goles_en_contra_ultimos_3_partidos_equipo_local = goles_en_contra_ultimos_3_partidos_equipo_local + p.goles_visitante

                        goles_puntos_local_siendo_local = goles_puntos_local_siendo_local+1
                        goles_puntos_equipo_local = goles_puntos_equipo_local +1

                    elif goles_puntos_local_siendo_local <3  and goles_puntos_equipo_local >=3:
                        goles_ultimos_3_partidos_local_siendo_local = goles_ultimos_3_partidos_local_siendo_local + p.goles_local
                        puntos_ultimos_3_partidos_local_siendo_local = puntos_ultimos_3_partidos_local_siendo_local + p.puntos_local
                        goles_en_contra_ultimos_3_partidos_local_siendo_local = goles_en_contra_ultimos_3_partidos_local_siendo_local + p.goles_visitante
                        goles_puntos_local_siendo_local = goles_puntos_local_siendo_local+1

                    elif goles_puntos_local_siendo_local >=3  and goles_puntos_equipo_local <3:
                        goles_ultimos_3_partidos_equipo_local = goles_ultimos_3_partidos_equipo_local + p.goles_local
                        puntos_ultimos_3_partidos_equipo_local = puntos_ultimos_3_partidos_equipo_local + p.puntos_local
                        goles_en_contra__ultimos_3_partidos_equipo_local = goles_en_contra__ultimos_3_partidos_equipo_local + p.goles_visitante

                        goles_puntos_equipo_local = goles_puntos_equipo_local +1
                    else:
                        continue

                elif p.equipo_local != local and p.equipo_visitante == visitante:
                    if goles_puntos_visitante_siendo_visitante <3 and goles_puntos_equipo_visitante <3:
                        goles_ultimos_3_partidos_visitante_siendo_visitante = goles_ultimos_3_partidos_visitante_siendo_visitante + p.goles_visitante
                        puntos_ultimos_3_partidos_visitante_siendo_visitante = puntos_ultimos_3_partidos_visitante_siendo_visitante + p.puntos_visitante
                        goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante + p.goles_local

                        goles_ultimos_3_partidos_equipo_visitante = goles_ultimos_3_partidos_equipo_visitante + p.goles_visitante
                        puntos_ultimos_3_partidos_equipo_visitante = puntos_ultimos_3_partidos_equipo_visitante + p.puntos_visitante
                        goles_en_contra_ultimos_3_partidos_equipo_visitante = goles_en_contra_ultimos_3_partidos_equipo_visitante + p.goles_local
                                
                        goles_puntos_visitante_siendo_visitante = goles_puntos_visitante_siendo_visitante+1
                        goles_puntos_equipo_visitante = goles_puntos_equipo_visitante+1

                    elif goles_puntos_visitante_siendo_visitante <3 and goles_puntos_equipo_visitante >=3:
                        goles_ultimos_3_partidos_visitante_siendo_visitante = goles_ultimos_3_partidos_visitante_siendo_visitante + p.goles_visitante
                        puntos_ultimos_3_partidos_visitante_siendo_visitante = puntos_ultimos_3_partidos_visitante_siendo_visitante + p.puntos_visitante
                        goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante + p.goles_local
                        goles_puntos_visitante_siendo_visitante = goles_puntos_visitante_siendo_visitante+1
                            
                    elif goles_puntos_visitante_siendo_visitante >=3 and goles_puntos_equipo_visitante <3:
                        goles_ultimos_3_partidos_equipo_visitante = goles_ultimos_3_partidos_equipo_visitante + p.goles_visitante
                        puntos_ultimos_3_partidos_equipo_visitante = puntos_ultimos_3_partidos_equipo_visitante + p.puntos_visitante
                        goles_en_contra_ultimos_3_partidos_equipo_visitante = goles_en_contra_ultimos_3_partidos_equipo_visitante + p.goles_local
                            
                        goles_puntos_equipo_visitante = goles_puntos_equipo_visitante + 1
                    else:
                        continue

                elif local == p.equipo_visitante:
                    if goles_puntos_equipo_local < 3:
                        goles_ultimos_3_partidos_equipo_local = goles_ultimos_3_partidos_equipo_local + p.goles_visitante
                        puntos_ultimos_3_partidos_equipo_local = puntos_ultimos_3_partidos_equipo_local + p.puntos_visitante
                        goles_en_contra_ultimos_3_partidos_equipo_local = goles_en_contra_ultimos_3_partidos_equipo_local + p.goles_local

                        goles_puntos_equipo_local = goles_puntos_equipo_local +1
                    else:
                        continue
                elif visitante == p.equipo_local:
                    if goles_puntos_equipo_visitante < 3:
                        goles_ultimos_3_partidos_equipo_visitante = goles_ultimos_3_partidos_equipo_visitante + p.goles_local
                        puntos_ultimos_3_partidos_equipo_visitante = puntos_ultimos_3_partidos_equipo_visitante + p.puntos_local
                        goles_en_contra_ultimos_3_partidos_equipo_visitante = goles_en_contra_ultimos_3_partidos_equipo_visitante + p.goles_visitante
                            
                        goles_puntos_equipo_visitante = goles_puntos_equipo_visitante + 1
                    else:
                        continue
                else:
                    continue
                

        if goles_puntos_equipo_local < 3 and goles_puntos_equipo_visitante <3 and goles_puntos_local_siendo_local <3 and goles_puntos_visitante_siendo_visitante <3:
                partido.falta = True
                partido.save()
        else:
            partido.goles_ultimos_3_partidos_local_siendo_local = goles_ultimos_3_partidos_local_siendo_local
            partido.goles_ultimos_3_partidos_equipo_local = goles_ultimos_3_partidos_equipo_local
            partido.goles_ultimos_3_partidos_visitante_siendo_visitante = goles_ultimos_3_partidos_visitante_siendo_visitante
            partido.goles_ultimos_3_partidos_equipo_visitante = goles_ultimos_3_partidos_equipo_visitante

            partido.puntos_ultimos_3_partidos_local_siendo_local = puntos_ultimos_3_partidos_local_siendo_local
            partido.puntos_ultimos_3_partidos_equipo_local = puntos_ultimos_3_partidos_equipo_local
            partido.puntos_ultimos_3_partidos_visitante_siendo_visitante = puntos_ultimos_3_partidos_visitante_siendo_visitante
            partido.puntos_ultimos_3_partidos_equipo_visitante = puntos_ultimos_3_partidos_equipo_visitante

            partido.goles_en_contra_ultimos_3_partidos_local_siendo_local = goles_en_contra_ultimos_3_partidos_local_siendo_local
            partido.goles_en_contra_ultimos_3_partidos_equipo_local = goles_en_contra_ultimos_3_partidos_equipo_local
            partido.goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante
            partido.goles_en_contra_ultimos_3_partidos_equipo_visitante = goles_en_contra_ultimos_3_partidos_equipo_visitante
            partido.save()
    return "Carga Completada"

def cargarPartidoRealLigaEsp():
    id = 1
    temporada = "2023-24"
    url = "https://www.marca.com/futbol/primera-division/calendario.html?intcmp=MENUMIGA&s_kw=calendario"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    jornada = 1
    liga = "LaLiga EA Sports"
    with urllib.request.urlopen(request) as f:
        s = BeautifulSoup(f, "lxml")
        encuentros = s.find("div", class_="recursos-deportivos").find("div", class_= "contenedorCalendarioInt").find_all("div", class_="jornada calendarioInternacional")
        for encuentro in encuentros:
            jornada = encuentro.find("table", class_="jor agendas").find("caption").string.strip()
            jornada = int(jornada.replace("Jornada", ""))
            partidos = encuentro.find("table", class_="jor agendas").find("tbody").find_all("tr")
            for partido in partidos:
                equipo_local = partido.find("td", class_="local").find("span").string.strip()
                equipo_visitante = partido.find("td", class_="visitante").find("span").string.strip()
                dat = partido.find("td", class_="resultado")
                if dat.find("span", class_="resultado-partido"):
                    resultado = dat.find("span", class_="resultado-partido").string.strip()
                    resultado2 = resultado.split("-")
                    goles_local = int(resultado2[0])
                    goles_visitante = int(resultado2[1])
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1

                else:
                    winner = "X"
                    goles_local = 0
                    goles_visitante = 0
                    puntos_local = 1
                    puntos_visitante = 1
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, 
                                                equipo_local=equipo_local, equipo_visitante=equipo_visitante, 
                                                goles_local=goles_local, goles_visitante = goles_visitante, 
                                                winner=winner, puntos_local=puntos_local, puntos_visitante=puntos_visitante)
                id = id+1

    return pr

def cargarPartidoRealPremier():
    id = 381
    temporada = "2023-24"
    url = "https://www.marca.com/futbol/premier-league/calendario.html?intcmp=MENUPROD&s_kw=premier-league-calendario"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    jornada = 1
    liga = "Premier League"
    with urllib.request.urlopen(request) as f:
        s = BeautifulSoup(f, "lxml")
        encuentros = s.find("div", class_="recursos-deportivos").find("div", class_= "contenedorCalendarioInt").find_all("div", class_="jornada calendarioInternacional")
        for encuentro in encuentros:
            jornada = encuentro.find("table", class_="jor agendas").find("caption").string.strip()
            partidos = encuentro.find("table", class_="jor agendas").find("tbody").find_all("tr")
            for partido in partidos:
                equipo_local = partido.find("td", class_="local").find("span").string.strip()
                equipo_visitante = partido.find("td", class_="visitante").find("span").string.strip()
                dat = partido.find("td", class_="resultado")
                if dat.find("span", class_="resultado-partido"):
                    resultado = dat.find("span", class_="resultado-partido").string.strip()
                    resultado2 = resultado.split("-")
                    goles_local = int(resultado2[0])
                    goles_visitante = int(resultado2[1])
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1

                else:
                    winner = "X"
                    goles_local = 0
                    goles_visitante = 0
                    puntos_local = 1
                    puntos_visitante = 1
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner, puntos_local=puntos_local, puntos_visitante=puntos_visitante)
                id = id+1

    return pr

def cargarPartidoRealBundesliga():
    id = 761
    temporada = "2023/2024"
    url = "https://www.marca.com/futbol/bundesliga/calendario.html?intcmp=MENUMIGA&s_kw=calendario"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    jornada = 1
    liga = "Bundesliga"
    with urllib.request.urlopen(request) as f:
        s = BeautifulSoup(f, "lxml")
        encuentros = s.find("div", class_="recursos-deportivos").find("div", class_= "contenedorCalendarioInt").find_all("div", class_="jornada calendarioInternacional")
        for encuentro in encuentros:
            jornada = encuentro.find("table", class_="jor agendas").find("caption").string.strip()
            partidos = encuentro.find("table", class_="jor agendas").find("tbody").find_all("tr")
            for partido in partidos:
                equipo_local = partido.find("td", class_="local").find("span").string.strip()
                equipo_visitante = partido.find("td", class_="visitante").find("span").string.strip()
                dat = partido.find("td", class_="resultado")
                if dat.find("span", class_="resultado-partido"):
                    resultado = dat.find("span", class_="resultado-partido").string.strip()
                    resultado2 = resultado.split("-")
                    goles_local = int(resultado2[0])
                    goles_visitante = int(resultado2[1])
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1

                else:
                    winner = "X"
                    goles_local = 0
                    goles_visitante = 0
                    puntos_local = 1
                    puntos_visitante = 1
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner, puntos_local=puntos_local, puntos_visitante=puntos_visitante)
                id = id+1

    return pr

def cargarPartidoRealSerieA():
    id = 1067
    temporada = "2023/2024"
    url = "https://www.marca.com/futbol/liga-italiana/calendario.html?intcmp=MENUPROD&s_kw=serie-a-calendario"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    jornada = 1
    liga = "Serie A"
    with urllib.request.urlopen(request) as f:
        s = BeautifulSoup(f, "lxml")
        encuentros = s.find("div", class_="recursos-deportivos").find("div", class_= "contenedorCalendarioInt").find_all("div", class_="jornada calendarioInternacional")
        for encuentro in encuentros:
            jornada = encuentro.find("table", class_="jor agendas").find("caption").string.strip()
            partidos = encuentro.find("table", class_="jor agendas").find("tbody").find_all("tr")
            for partido in partidos:
                equipo_local = partido.find("td", class_="local").find("span").string.strip()
                equipo_visitante = partido.find("td", class_="visitante").find("span").string.strip()
                dat = partido.find("td", class_="resultado")
                if dat.find("span", class_="resultado-partido"):
                    resultado = dat.find("span", class_="resultado-partido").string.strip()
                    resultado2 = resultado.split("-")
                    goles_local = int(resultado2[0])
                    goles_visitante = int(resultado2[1])
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1

                else:
                    winner = "X"
                    goles_local = 0
                    goles_visitante = 0
                    puntos_local = 1
                    puntos_visitante = 1
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner, puntos_local=puntos_local, puntos_visitante=puntos_visitante)
                id = id+1

    return pr

def cargarPartidoRealLigue1():
    id = 1447
    temporada = "2023/2024"
    url = "https://www.marca.com/futbol/liga-francesa/calendario.html?intcmp=MENUMIGA&s_kw=calendario"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    jornada = 1
    liga = "Ligue 1"
    with urllib.request.urlopen(request) as f:
        s = BeautifulSoup(f, "lxml")
        encuentros = s.find("div", class_="recursos-deportivos").find("div", class_= "contenedorCalendarioInt").find_all("div", class_="jornada calendarioInternacional")
        for encuentro in encuentros:
            jornada = encuentro.find("table", class_="jor agendas").find("caption").string.strip()
            partidos = encuentro.find("table", class_="jor agendas").find("tbody").find_all("tr")
            for partido in partidos:
                equipo_local = partido.find("td", class_="local").find("span").string.strip()
                equipo_visitante = partido.find("td", class_="visitante").find("span").string.strip()
                dat = partido.find("td", class_="resultado")
                if dat.find("span", class_="resultado-partido"):
                    resultado = dat.find("span", class_="resultado-partido").string.strip()
                    resultado2 = resultado.split("-")
                    goles_local = int(resultado2[0])
                    goles_visitante = int(resultado2[1])
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1

                else:
                    winner = "X"
                    goles_local = 0
                    goles_visitante = 0
                    puntos_local = 1
                    puntos_visitante = 1
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner, puntos_local=puntos_local, puntos_visitante=puntos_visitante)
                id = id+1

    return pr

def cargarPartidoRealLigaPortuguesa():
    id = 1753
    temporada = "2023/2024"
    url = "https://www.marca.com/futbol/liga-portuguesa/calendario.html?intcmp=MENUPROD&s_kw=primeira-liga-portugal-calendario"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    jornada = 1
    liga = "Liga Portuguesa"
    with urllib.request.urlopen(request) as f:
        s = BeautifulSoup(f, "lxml")
        encuentros = s.find("div", class_="recursos-deportivos").find("div", class_= "contenedorCalendarioInt").find_all("div", class_="jornada calendarioInternacional")
        for encuentro in encuentros:
            jornada = encuentro.find("table", class_="jor agendas").find("caption").string.strip()
            partidos = encuentro.find("table", class_="jor agendas").find("tbody").find_all("tr")
            for partido in partidos:
                equipo_local = partido.find("td", class_="local").find("span").string.strip()
                equipo_visitante = partido.find("td", class_="visitante").find("span").string.strip()
                dat = partido.find("td", class_="resultado")
                if dat.find("span", class_="resultado-partido"):
                    resultado = dat.find("span", class_="resultado-partido").string.strip()
                    resultado2 = resultado.split("-")
                    goles_local = int(resultado2[0])
                    goles_visitante = int(resultado2[1])
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1

                else:
                    winner = "X"
                    goles_local = 0
                    goles_visitante = 0
                    puntos_local = 1
                    puntos_visitante = 1
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner, puntos_local=puntos_local, puntos_visitante=puntos_visitante)
                id = id+1

    return pr

def cargarPartidoRealEredivise():
    id = 2059
    temporada = "2023/2024"
    url = "https://www.marca.com/futbol/liga-holandesa/calendario.html"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    jornada = 1
    liga = "Eredivise"
    with urllib.request.urlopen(request) as f:
        s = BeautifulSoup(f, "lxml")
        encuentros = s.find("div", class_="recursos-deportivos").find("div", class_= "contenedorCalendarioInt").find_all("div", class_="jornada calendarioInternacional")
        for encuentro in encuentros:
            jornada = encuentro.find("table", class_="jor agendas").find("caption").string.strip()
            partidos = encuentro.find("table", class_="jor agendas").find("tbody").find_all("tr")
            for partido in partidos:
                equipo_local = partido.find("td", class_="local").find("span").string.strip()
                equipo_visitante = partido.find("td", class_="visitante").find("span").string.strip()
                dat = partido.find("td", class_="resultado")
                if dat.find("span", class_="resultado-partido"):
                    resultado = dat.find("span", class_="resultado-partido").string.strip()
                    resultado2 = resultado.split("-")
                    goles_local = int(resultado2[0])
                    goles_visitante = int(resultado2[1])
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1

                else:
                    winner = "X"
                    goles_local = 0
                    goles_visitante = 0
                    puntos_local = 1
                    puntos_visitante = 1
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner, puntos_local=puntos_local, puntos_visitante=puntos_visitante)
                id = id+1

    return pr

def cargarPartidoRealEsp2():
    id = 381
    temporada = "2023/2024"
    url = "https://www.marca.com/futbol/segunda-division/calendario.html?intcmp=MENUPROD&s_kw=segunda-division-calendario"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    jornada = 1
    liga = "LaLiga Hypermotion"
    with urllib.request.urlopen(request) as f:
        s = BeautifulSoup(f, "lxml")
        encuentros = s.find("div", class_="recursos-deportivos").find("div", class_= "contenedorCalendarioInt").find_all("div", class_="jornada calendarioInternacional")
        for encuentro in encuentros:
            jornada = encuentro.find("table", class_="jor agendas").find("caption").string.strip()
            jornada = int(jornada.replace("Jornada", ""))
            partidos = encuentro.find("table", class_="jor agendas").find("tbody").find_all("tr")
            for partido in partidos:
                equipo_local = partido.find("td", class_="local").find("span").string.strip()
                equipo_visitante = partido.find("td", class_="visitante").find("span").string.strip()
                dat = partido.find("td", class_="resultado")
                if dat.find("span", class_="resultado-partido"):
                    resultado = dat.find("span", class_="resultado-partido").string.strip()
                    resultado2 = resultado.split("-")
                    goles_local = int(resultado2[0])
                    goles_visitante = int(resultado2[1])
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1

                else:
                    winner = "X"
                    goles_local = 0
                    goles_visitante = 0
                    puntos_local = 1
                    puntos_visitante = 1
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner, puntos_local=puntos_local, puntos_visitante=puntos_visitante)
                id = id+1

    return pr

def cargarPartidoRealMLS():
    id = 2827
    temporada = "2023/2024"
    url = "https://www.marca.com/futbol/estados-unidos/calendario.html?intcmp=MENUMIGA&s_kw=calendario"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    jornada = 1
    liga = "Mayor League Soccer"
    with urllib.request.urlopen(request) as f:
        s = BeautifulSoup(f, "lxml")
        encuentros = s.find("div", class_="recursos-deportivos").find("div", class_= "contenedorCalendarioInt").find_all("div", class_="jornada calendarioInternacional")
        for encuentro in encuentros:
            jornada = encuentro.find("table", class_="jor agendas").find("caption").string.strip()
            partidos = encuentro.find("table", class_="jor agendas").find("tbody").find_all("tr")
            for partido in partidos:
                equipo_local = partido.find("td", class_="local").find("span").string.strip()
                equipo_visitante = partido.find("td", class_="visitante").find("span").string.strip()
                dat = partido.find("td", class_="resultado")
                if dat.find("span", class_="resultado-partido"):
                    resultado = dat.find("span", class_="resultado-partido").string.strip()
                    resultado2 = resultado.split("-")
                    goles_local = int(resultado2[0])
                    goles_visitante = int(resultado2[1])
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1

                else:
                    winner = "X"
                    goles_local = 0
                    goles_visitante = 0
                    puntos_local = 1
                    puntos_visitante = 1
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner, puntos_local=puntos_local, puntos_visitante=puntos_visitante)
                id = id+1

    return pr

def cargarPartidoRealBelga():
    id = 3320
    temporada = "2023/2024"
    url = "https://www.marca.com/futbol/liga-belga/calendario.html?intcmp=MENUMIGA&s_kw=calendario"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    jornada = 1
    liga = "Jupiter Pro League"
    with urllib.request.urlopen(request) as f:
        s = BeautifulSoup(f, "lxml")
        encuentros = s.find("div", class_="recursos-deportivos").find("div", class_= "contenedorCalendarioInt").find_all("div", class_="jornada calendarioInternacional")
        for encuentro in encuentros:
            jornada = encuentro.find("table", class_="jor agendas").find("caption").string.strip()
            partidos = encuentro.find("table", class_="jor agendas").find("tbody").find_all("tr")
            for partido in partidos:
                equipo_local = partido.find("td", class_="local").find("span").string.strip()
                equipo_visitante = partido.find("td", class_="visitante").find("span").string.strip()
                dat = partido.find("td", class_="resultado")
                if dat.find("span", class_="resultado-partido"):
                    resultado = dat.find("span", class_="resultado-partido").string.strip()
                    resultado2 = resultado.split("-")
                    goles_local = int(resultado2[0])
                    goles_visitante = int(resultado2[1])
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1

                else:
                    winner = "X"
                    goles_local = 0
                    goles_visitante = 0
                    puntos_local = 1
                    puntos_visitante = 1
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner, puntos_local=puntos_local, puntos_visitante=puntos_visitante)
                id = id+1

    return pr

def cargarPartidoRealRusia():
    id = 3560
    temporada = "2023/2024"
    url = "https://www.marca.com/futbol/liga-rusa/calendario.html?intcmp=MENUMIGA&s_kw=calendario"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    jornada = 1
    liga = "Primera Liga de Rusia"
    with urllib.request.urlopen(request) as f:
        s = BeautifulSoup(f, "lxml")
        encuentros = s.find("div", class_="recursos-deportivos").find("div", class_= "contenedorCalendarioInt").find_all("div", class_="jornada calendarioInternacional")
        for encuentro in encuentros:
            jornada = encuentro.find("table", class_="jor agendas").find("caption").string.strip()
            partidos = encuentro.find("table", class_="jor agendas").find("tbody").find_all("tr")
            for partido in partidos:
                equipo_local = partido.find("td", class_="local").find("span").string.strip()
                equipo_visitante = partido.find("td", class_="visitante").find("span").string.strip()
                dat = partido.find("td", class_="resultado")
                if dat.find("span", class_="resultado-partido"):
                    resultado = dat.find("span", class_="resultado-partido").string.strip()
                    resultado2 = resultado.split("-")
                    goles_local = int(resultado2[0])
                    goles_visitante = int(resultado2[1])
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1

                else:
                    winner = "X"
                    goles_local = 0
                    goles_visitante = 0
                    puntos_local = 1
                    puntos_visitante = 1
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner, puntos_local=puntos_local, puntos_visitante=puntos_visitante)
                id = id+1

    return pr

def cargarPartidoRealTurca():
    id = 3800
    temporada = "2023/2024"
    url = "https://www.marca.com/futbol/liga-turca/calendario.html?intcmp=MENUMIGA&s_kw=calendario"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    jornada = 1
    liga = "Primera Liga de Turquia"
    with urllib.request.urlopen(request) as f:
        s = BeautifulSoup(f, "lxml")
        encuentros = s.find("div", class_="recursos-deportivos").find("div", class_= "contenedorCalendarioInt").find_all("div", class_="jornada calendarioInternacional")
        for encuentro in encuentros:
            jornada = encuentro.find("table", class_="jor agendas").find("caption").string.strip()
            partidos = encuentro.find("table", class_="jor agendas").find("tbody").find_all("tr")
            for partido in partidos:
                equipo_local = partido.find("td", class_="local").find("span").string.strip()
                equipo_visitante = partido.find("td", class_="visitante").find("span").string.strip()
                dat = partido.find("td", class_="resultado")
                if dat.find("span", class_="resultado-partido"):
                    resultado = dat.find("span", class_="resultado-partido").string.strip()
                    resultado2 = resultado.split("-")
                    goles_local = int(resultado2[0])
                    goles_visitante = int(resultado2[1])
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1

                else:
                    winner = "X"
                    goles_local = 0
                    goles_visitante = 0
                    puntos_local = 1
                    puntos_visitante = 1
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner, puntos_local=puntos_local, puntos_visitante=puntos_visitante)
                id = id+1

    return pr

def cargarPartidoRealBrasil():
    id = 4180
    temporada = "2023/2024"
    url = "https://www.marca.com/futbol/brasil/calendario.html?intcmp=MENUMIGA&s_kw=calendario"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    jornada = 1
    liga = "Primera Liga de Brasil"
    with urllib.request.urlopen(request) as f:
        s = BeautifulSoup(f, "lxml")
        encuentros = s.find("div", class_="recursos-deportivos").find("div", class_= "contenedorCalendarioInt").find_all("div", class_="jornada calendarioInternacional")
        for encuentro in encuentros:
            jornada = encuentro.find("table", class_="jor agendas").find("caption").string.strip()
            partidos = encuentro.find("table", class_="jor agendas").find("tbody").find_all("tr")
            for partido in partidos:
                equipo_local = partido.find("td", class_="local").find("span").string.strip()
                equipo_visitante = partido.find("td", class_="visitante").find("span").string.strip()
                dat = partido.find("td", class_="resultado")
                if dat.find("span", class_="resultado-partido"):
                    resultado = dat.find("span", class_="resultado-partido").string.strip()
                    resultado2 = resultado.split("-")
                    goles_local = int(resultado2[0])
                    goles_visitante = int(resultado2[1])
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1

                else:
                    winner = "X"
                    goles_local = 0
                    goles_visitante = 0
                    puntos_local = 1
                    puntos_visitante = 1
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner, puntos_local=puntos_local, puntos_visitante=puntos_visitante)
                id = id+1

    return pr


def cargarPartidoRealArgentina():
    id = 4560
    temporada = "2023/2024"
    url = "https://www.marca.com/futbol/argentina/liga-profesional/calendario.html?intcmp=MENUMIGA&s_kw=calendario"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    jornada = 1
    liga = "Primera Liga de Argentina"
    with urllib.request.urlopen(request) as f:
        s = BeautifulSoup(f, "lxml")
        encuentros = s.find("div", class_="recursos-deportivos").find("div", class_= "contenedorCalendarioInt").find_all("div", class_="jornada calendarioInternacional")
        for encuentro in encuentros:
            jornada = encuentro.find("table", class_="jor agendas").find("caption").string.strip()
            partidos = encuentro.find("table", class_="jor agendas").find("tbody").find_all("tr")
            for partido in partidos:
                equipo_local = partido.find("td", class_="local").find("span").string.strip()
                equipo_visitante = partido.find("td", class_="visitante").find("span").string.strip()
                dat = partido.find("td", class_="resultado")
                if dat.find("span", class_="resultado-partido"):
                    resultado = dat.find("span", class_="resultado-partido").string.strip()
                    resultado2 = resultado.split("-")
                    goles_local = int(resultado2[0])
                    goles_visitante = int(resultado2[1])
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1

                else:
                    winner = "X"
                    goles_local = 0
                    goles_visitante = 0
                    puntos_local = 1
                    puntos_visitante = 1
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner, puntos_local=puntos_local, puntos_visitante=puntos_visitante)
                id = id+1

    return pr

def cargarPartidoRealJaponesa():
    id = 4938
    temporada = "2023/2024"
    url = "https://www.marca.com/futbol/liga-japonesa/calendario.html?intcmp=MENUMIGA&s_kw=calendario"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    jornada = 1
    liga = "Primera Liga de Japón"
    with urllib.request.urlopen(request) as f:
        s = BeautifulSoup(f, "lxml")
        encuentros = s.find("div", class_="recursos-deportivos").find("div", class_= "contenedorCalendarioInt").find_all("div", class_="jornada calendarioInternacional")
        for encuentro in encuentros:
            jornada = encuentro.find("table", class_="jor agendas").find("caption").string.strip()
            partidos = encuentro.find("table", class_="jor agendas").find("tbody").find_all("tr")
            for partido in partidos:
                equipo_local = partido.find("td", class_="local").find("span").string.strip()
                equipo_visitante = partido.find("td", class_="visitante").find("span").string.strip()
                dat = partido.find("td", class_="resultado")
                if dat.find("span", class_="resultado-partido"):
                    resultado = dat.find("span", class_="resultado-partido").string.strip()
                    resultado2 = resultado.split("-")
                    goles_local = int(resultado2[0])
                    goles_visitante = int(resultado2[1])
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1

                else:
                    winner = "X"
                    goles_local = 0
                    goles_visitante = 0
                    puntos_local = 1
                    puntos_visitante = 1
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner, puntos_local=puntos_local, puntos_visitante=puntos_visitante)
                id = id+1

    return pr

def cargarPartidoRealChina():
    id = 5318
    temporada = "2023/2024"
    url = "https://www.marca.com/futbol/liga-china/calendario.html?intcmp=MENUMIGA&s_kw=calendario"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    jornada = 1
    liga = "Primera Liga de China"
    with urllib.request.urlopen(request) as f:
        s = BeautifulSoup(f, "lxml")
        encuentros = s.find("div", class_="recursos-deportivos").find("div", class_= "contenedorCalendarioInt").find_all("div", class_="jornada calendarioInternacional")
        for encuentro in encuentros:
            jornada = encuentro.find("table", class_="jor agendas").find("caption").string.strip()
            partidos = encuentro.find("table", class_="jor agendas").find("tbody").find_all("tr")
            for partido in partidos:
                equipo_local = partido.find("td", class_="local").find("span").string.strip()
                equipo_visitante = partido.find("td", class_="visitante").find("span").string.strip()
                dat = partido.find("td", class_="resultado")
                if dat.find("span", class_="resultado-partido"):
                    resultado = dat.find("span", class_="resultado-partido").string.strip()
                    resultado2 = resultado.split("-")
                    goles_local = int(resultado2[0])
                    goles_visitante = int(resultado2[1])
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1

                else:
                    winner = "X"
                    goles_local = 0
                    goles_visitante = 0
                    puntos_local = 1
                    puntos_visitante = 1
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner, puntos_local=puntos_local, puntos_visitante=puntos_visitante)
                id = id+1

    return pr

def cargarPartidoRealMexico():
    id = 5558
    temporada = "2023/2024"
    url = "https://www.marca.com/futbol/liga-mx/clausura/calendario.html"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    request = urllib.request.Request(url, headers=headers)
    jornada = 1
    liga = "Liga MX"
    with urllib.request.urlopen(request) as f:
        s = BeautifulSoup(f, "lxml")
        encuentros = s.find("div", class_="recursos-deportivos").find("div", class_= "contenedorCalendarioInt").find_all("div", class_="jornada calendarioInternacional")
        for encuentro in encuentros:
            jornada = encuentro.find("table", class_="jor agendas").find("caption").string.strip()
            partidos = encuentro.find("table", class_="jor agendas").find("tbody").find_all("tr")
            for partido in partidos:
                equipo_local = partido.find("td", class_="local").find("span").string.strip()
                equipo_visitante = partido.find("td", class_="visitante").find("span").string.strip()
                dat = partido.find("td", class_="resultado")
                if dat.find("span", class_="resultado-partido"):
                    resultado = dat.find("span", class_="resultado-partido").string.strip()
                    resultado2 = resultado.split("-")
                    goles_local = int(resultado2[0])
                    goles_visitante = int(resultado2[1])
                    if goles_local > goles_visitante:
                        winner = "1"
                        puntos_local = 3
                        puntos_visitante = 0
                    elif goles_visitante > goles_local:
                        winner = "2"
                        puntos_local = 0
                        puntos_visitante = 3
                    else:
                        winner = "X"
                        puntos_local = 1
                        puntos_visitante = 1

                else:
                    winner = "X"
                    goles_local = 0
                    goles_visitante = 0
                    puntos_local = 1
                    puntos_visitante = 1
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner, puntos_local=puntos_local, puntos_visitante=puntos_visitante)
                id = id+1

    return pr


def cargarPartidoSinPredecir_Ultimos_5_Partidos():
    id = 0
    numero_partidos = PartidoReal.objects.all().count()
    for i in range(1,numero_partidos+1):
        partidos_en_rango_ordenados = PartidoReal.objects.filter(id__range=(1, i+1)).order_by('id')
        partido = partidos_en_rango_ordenados.last()
        id = id+1
        local = partido.equipo_local
        visitante = partido.equipo_visitante
        liga = partido.liga
        jornada = partido.jornada
        temporada = partido.temporada
            
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
        goles_en_contra_ultimos_5_partidos_equipo_local = 0
        goles_en_contra_ultimos_5_partidos_equipo_visitante = 0

        for p in reversed(partidos_en_rango_ordenados):

            if goles_puntos_equipo_local >= 5 and goles_puntos_equipo_visitante >=5 and goles_puntos_local_siendo_local >=5 and goles_puntos_visitante_siendo_visitante >=5:
                    continue
            else:
                if p.equipo_local == local and p.equipo_visitante == visitante:
                    pass

                elif p.equipo_local == local and p.equipo_visitante != visitante:
                    if goles_puntos_local_siendo_local <5  and goles_puntos_equipo_local <5:
                        goles_ultimos_5_partidos_local_siendo_local = goles_ultimos_5_partidos_local_siendo_local + p.goles_local
                        puntos_ultimos_5_partidos_local_siendo_local = puntos_ultimos_5_partidos_local_siendo_local + p.puntos_local
                        goles_en_contra_ultimos_5_partidos_local_siendo_local = goles_en_contra_ultimos_5_partidos_local_siendo_local + p.goles_visitante

                        goles_ultimos_5_partidos_equipo_local = goles_ultimos_5_partidos_equipo_local + p.goles_local
                        puntos_ultimos_5_partidos_equipo_local = puntos_ultimos_5_partidos_equipo_local + p.puntos_local
                        goles_en_contra_ultimos_5_partidos_equipo_local = goles_en_contra_ultimos_5_partidos_equipo_local + p.goles_visitante

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
                        goles_en_contra_ultimos_5_partidos_equipo_visitante = goles_en_contra_ultimos_5_partidos_equipo_visitante + p.goles_local
                                
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
                        goles_en_contra_ultimos_5_partidos_equipo_visitante = goles_en_contra_ultimos_5_partidos_equipo_visitante + p.goles_local
                            
                        goles_puntos_equipo_visitante = goles_puntos_equipo_visitante + 1
                    else:
                        continue

                elif local == p.equipo_visitante:
                    if goles_puntos_equipo_local < 5:
                        goles_ultimos_5_partidos_equipo_local = goles_ultimos_5_partidos_equipo_local + p.goles_visitante
                        puntos_ultimos_5_partidos_equipo_local = puntos_ultimos_5_partidos_equipo_local + p.puntos_visitante
                        goles_en_contra_ultimos_5_partidos_equipo_local = goles_en_contra_ultimos_5_partidos_equipo_local + p.goles_local

                        goles_puntos_equipo_local = goles_puntos_equipo_local +1
                    else:
                        continue
                elif visitante == p.equipo_local:
                    if goles_puntos_equipo_visitante < 5:
                        goles_ultimos_5_partidos_equipo_visitante = goles_ultimos_5_partidos_equipo_visitante + p.goles_local
                        puntos_ultimos_5_partidos_equipo_visitante = puntos_ultimos_5_partidos_equipo_visitante + p.puntos_local
                        goles_en_contra_ultimos_5_partidos_equipo_visitante = goles_en_contra_ultimos_5_partidos_equipo_visitante + p.goles_visitante
                            
                        goles_puntos_equipo_visitante = goles_puntos_equipo_visitante + 1
                    else:
                        continue
                else:
                    continue
                

        if goles_puntos_equipo_local < 5 and goles_puntos_equipo_visitante <5 and goles_puntos_local_siendo_local <5 and goles_puntos_visitante_siendo_visitante <5:
            pe = PartidoSinPredecir.objects.create(id=id,
                                                        liga=liga,
                                                        jornada=jornada,
                                                        temporada=temporada, 
                                                        equipo_local = local, 
                                                        equipo_visitante=visitante,
                                                        falta = True)
                    
        else:
            pe = PartidoSinPredecir.objects.create(id=id,
                                                    liga=liga,
                                                    jornada=jornada,
                                                    temporada=temporada, 
                                                    equipo_local = local, 
                                                    equipo_visitante=visitante,
                                                    goles_ultimos_5_partidos_equipo_local =  goles_ultimos_5_partidos_equipo_local,
                                                    goles_ultimos_5_partidos_equipo_visitante = goles_ultimos_5_partidos_equipo_visitante, 
                                                    puntos_ultimos_5_partidos_equipo_local = puntos_ultimos_5_partidos_equipo_local, 
                                                    puntos_ultimos_5_partidos_equipo_visitante=puntos_ultimos_5_partidos_equipo_visitante, 
                                                    goles_ultimos_5_partidos_local_siendo_local=goles_ultimos_5_partidos_local_siendo_local, 
                                                    goles_ultimos_5_partidos_visitante_siendo_visitante = goles_ultimos_5_partidos_visitante_siendo_visitante,
                                                    puntos_ultimos_5_partidos_local_siendo_local = puntos_ultimos_5_partidos_local_siendo_local,
                                                    puntos_ultimos_5_partidos_visitante_siendo_visitante = puntos_ultimos_5_partidos_visitante_siendo_visitante,
                                                    goles_en_contra_ultimos_5_partidos_equipo_local = goles_en_contra_ultimos_5_partidos_equipo_local,
                                                    goles_en_contra_ultimos_5_partidos_equipo_visitante = goles_en_contra_ultimos_5_partidos_equipo_visitante,
                                                    goles_en_contra_ultimos_5_partidos_local_siendo_local = goles_en_contra_ultimos_5_partidos_local_siendo_local,
                                                    goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante = goles_en_contra_ultimos_5_partidos_visitante_siendo_visitante)
                


    return pe

def cargarPartidoSinPredecir_Ultimos_3_Partidos():
    numero_partidos = PartidoReal.objects.all().count()
    for i in range(1,numero_partidos+1):
        
        partidos_en_rango_ordenados = PartidoReal.objects.filter(id__range=(1, i+1)).order_by('id')
        partido = partidos_en_rango_ordenados.last()
        local = partido.equipo_local
        visitante = partido.equipo_visitante
        partido_actualizar = PartidoSinPredecir.objects.get(id=i)
            
        goles_ultimos_3_partidos_local_siendo_local = 0
        goles_ultimos_3_partidos_visitante_siendo_visitante = 0
        goles_ultimos_3_partidos_equipo_local = 0
        goles_ultimos_3_partidos_equipo_visitante = 0

        puntos_ultimos_3_partidos_local_siendo_local = 0
        puntos_ultimos_3_partidos_visitante_siendo_visitante = 0
        puntos_ultimos_3_partidos_equipo_local = 0
        puntos_ultimos_3_partidos_equipo_visitante = 0

        goles_puntos_local_siendo_local_ultimos_3 = 0
        goles_puntos_visitante_siendo_visitante_ultimos_3=0
        goles_puntos_equipo_local_ultimos_3 = 0
        goles_puntos_equipo_visitante_ultimos_3=0

        goles_en_contra_ultimos_3_partidos_local_siendo_local = 0
        goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = 0
        goles_en_contra_ultimos_3_partidos_equipo_local = 0
        goles_en_contra_ultimos_3_partidos_equipo_visitante = 0

        for p in reversed(partidos_en_rango_ordenados):

            if goles_puntos_equipo_local_ultimos_3 >= 3 and goles_puntos_equipo_visitante_ultimos_3 >=3 and goles_puntos_local_siendo_local_ultimos_3 >=3 and goles_puntos_visitante_siendo_visitante_ultimos_3 >=3:
                    continue
            else:
                if p.equipo_local == local and p.equipo_visitante == visitante:
                    pass

                elif p.equipo_local == local and p.equipo_visitante != visitante:
                    if goles_puntos_local_siendo_local_ultimos_3 <3  and goles_puntos_equipo_local_ultimos_3 <3:
                        goles_ultimos_3_partidos_local_siendo_local = goles_ultimos_3_partidos_local_siendo_local + p.goles_local
                        puntos_ultimos_3_partidos_local_siendo_local = puntos_ultimos_3_partidos_local_siendo_local + p.puntos_local
                        goles_en_contra_ultimos_3_partidos_local_siendo_local = goles_en_contra_ultimos_3_partidos_local_siendo_local + p.goles_visitante

                        goles_ultimos_3_partidos_equipo_local = goles_ultimos_3_partidos_equipo_local + p.goles_local
                        puntos_ultimos_3_partidos_equipo_local = puntos_ultimos_3_partidos_equipo_local + p.puntos_local
                        goles_en_contra_ultimos_3_partidos_equipo_local = goles_en_contra_ultimos_3_partidos_equipo_local + p.goles_visitante

                        goles_puntos_local_siendo_local_ultimos_3 = goles_puntos_local_siendo_local_ultimos_3+1
                        goles_puntos_equipo_local_ultimos_3 = goles_puntos_equipo_local_ultimos_3 +1

                    elif goles_puntos_local_siendo_local_ultimos_3 <3  and goles_puntos_equipo_local_ultimos_3 >=3:
                        goles_ultimos_3_partidos_local_siendo_local = goles_ultimos_3_partidos_local_siendo_local + p.goles_local
                        puntos_ultimos_3_partidos_local_siendo_local = puntos_ultimos_3_partidos_local_siendo_local + p.puntos_local
                        goles_en_contra_ultimos_3_partidos_local_siendo_local = goles_en_contra_ultimos_3_partidos_local_siendo_local + p.goles_visitante
                        goles_puntos_local_siendo_local_ultimos_3 = goles_puntos_local_siendo_local_ultimos_3+1

                    elif goles_puntos_local_siendo_local_ultimos_3 >=3  and goles_puntos_equipo_local_ultimos_3 <3:
                        goles_ultimos_3_partidos_equipo_local = goles_ultimos_3_partidos_equipo_local + p.goles_local
                        puntos_ultimos_3_partidos_equipo_local = puntos_ultimos_3_partidos_equipo_local + p.puntos_local
                        goles_en_contra__ultimos_3_partidos_equipo_local = goles_en_contra__ultimos_3_partidos_equipo_local + p.goles_visitante

                        goles_puntos_equipo_local_ultimos_3 = goles_puntos_equipo_local_ultimos_3 +1
                    else:
                        continue

                elif p.equipo_local != local and p.equipo_visitante == visitante:
                    if goles_puntos_visitante_siendo_visitante_ultimos_3 <3 and goles_puntos_equipo_visitante_ultimos_3 <3:
                        goles_ultimos_3_partidos_visitante_siendo_visitante = goles_ultimos_3_partidos_visitante_siendo_visitante + p.goles_visitante
                        puntos_ultimos_3_partidos_visitante_siendo_visitante = puntos_ultimos_3_partidos_visitante_siendo_visitante + p.puntos_visitante
                        goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante + p.goles_local

                        goles_ultimos_3_partidos_equipo_visitante = goles_ultimos_3_partidos_equipo_visitante + p.goles_visitante
                        puntos_ultimos_3_partidos_equipo_visitante = puntos_ultimos_3_partidos_equipo_visitante + p.puntos_visitante
                        goles_en_contra_ultimos_3_partidos_equipo_visitante = goles_en_contra_ultimos_3_partidos_equipo_visitante + p.goles_local
                                
                        goles_puntos_visitante_siendo_visitante_ultimos_3 = goles_puntos_visitante_siendo_visitante_ultimos_3+1
                        goles_puntos_equipo_visitante_ultimos_3 = goles_puntos_equipo_visitante_ultimos_3+1

                    elif goles_puntos_visitante_siendo_visitante_ultimos_3 <3 and goles_puntos_equipo_visitante_ultimos_3 >=3:
                        goles_ultimos_3_partidos_visitante_siendo_visitante = goles_ultimos_3_partidos_visitante_siendo_visitante + p.goles_visitante
                        puntos_ultimos_3_partidos_visitante_siendo_visitante = puntos_ultimos_3_partidos_visitante_siendo_visitante + p.puntos_visitante
                        goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante + p.goles_local
                        goles_puntos_visitante_siendo_visitante_ultimos_3 = goles_puntos_visitante_siendo_visitante_ultimos_3+1
                            
                    elif goles_puntos_visitante_siendo_visitante_ultimos_3 >=3 and goles_puntos_equipo_visitante_ultimos_3 <3:
                        goles_ultimos_3_partidos_equipo_visitante = goles_ultimos_3_partidos_equipo_visitante + p.goles_visitante
                        puntos_ultimos_3_partidos_equipo_visitante = puntos_ultimos_3_partidos_equipo_visitante + p.puntos_visitante
                        goles_en_contra_ultimos_3_partidos_equipo_visitante = goles_en_contra_ultimos_3_partidos_equipo_visitante + p.goles_local
                            
                        goles_puntos_equipo_visitante_ultimos_3 = goles_puntos_equipo_visitante_ultimos_3 + 1
                    else:
                        continue

                elif local == p.equipo_visitante:
                    if goles_puntos_equipo_local_ultimos_3 < 3:
                        goles_ultimos_3_partidos_equipo_local = goles_ultimos_3_partidos_equipo_local + p.goles_visitante
                        puntos_ultimos_3_partidos_equipo_local = puntos_ultimos_3_partidos_equipo_local + p.puntos_visitante
                        goles_en_contra_ultimos_3_partidos_equipo_local = goles_en_contra_ultimos_3_partidos_equipo_local + p.goles_local

                        goles_puntos_equipo_local_ultimos_3 = goles_puntos_equipo_local_ultimos_3 +1
                    else:
                        continue
                elif visitante == p.equipo_local:
                    if goles_puntos_equipo_visitante_ultimos_3 < 3:
                        goles_ultimos_3_partidos_equipo_visitante = goles_ultimos_3_partidos_equipo_visitante + p.goles_local
                        puntos_ultimos_3_partidos_equipo_visitante = puntos_ultimos_3_partidos_equipo_visitante + p.puntos_local
                        goles_en_contra_ultimos_3_partidos_equipo_visitante = goles_en_contra_ultimos_3_partidos_equipo_visitante + p.goles_visitante
                            
                        goles_puntos_equipo_visitante_ultimos_3 = goles_puntos_equipo_visitante_ultimos_3 + 1
                    else:
                        continue
                else:
                    continue
                

        if goles_puntos_equipo_local_ultimos_3 < 3 and goles_puntos_equipo_visitante_ultimos_3 <3 and goles_puntos_local_siendo_local_ultimos_3 <3 and goles_puntos_visitante_siendo_visitante_ultimos_3 <3:
            partido_actualizar.falta = True
            partido_actualizar.save()
        else:
            partido_actualizar.goles_ultimos_3_partidos_local_siendo_local = goles_ultimos_3_partidos_local_siendo_local
            partido_actualizar.goles_ultimos_3_partidos_equipo_local = goles_ultimos_3_partidos_equipo_local
            partido_actualizar.goles_ultimos_3_partidos_visitante_siendo_visitante = goles_ultimos_3_partidos_visitante_siendo_visitante
            partido_actualizar.goles_ultimos_3_partidos_equipo_visitante = goles_ultimos_3_partidos_equipo_visitante

            partido_actualizar.puntos_ultimos_3_partidos_local_siendo_local = puntos_ultimos_3_partidos_local_siendo_local
            partido_actualizar.puntos_ultimos_3_partidos_equipo_local = puntos_ultimos_3_partidos_equipo_local
            partido_actualizar.puntos_ultimos_3_partidos_visitante_siendo_visitante = puntos_ultimos_3_partidos_visitante_siendo_visitante
            partido_actualizar.puntos_ultimos_3_partidos_equipo_visitante = puntos_ultimos_3_partidos_equipo_visitante

            partido_actualizar.goles_en_contra_ultimos_3_partidos_local_siendo_local = goles_en_contra_ultimos_3_partidos_local_siendo_local
            partido_actualizar.goles_en_contra_ultimos_3_partidos_equipo_local = goles_en_contra_ultimos_3_partidos_equipo_local
            partido_actualizar.goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante = goles_en_contra_ultimos_3_partidos_visitante_siendo_visitante
            partido_actualizar.goles_en_contra_ultimos_3_partidos_equipo_visitante = goles_en_contra_ultimos_3_partidos_equipo_visitante
            partido_actualizar.save()
                


    
        