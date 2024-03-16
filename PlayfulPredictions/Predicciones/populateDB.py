from bs4 import BeautifulSoup
import urllib.request
from .models import PartidosEntrenamiento, PartidoReal
import csv
path = "data/futbolDatabase.csv"

def populateDatabaseEntrenamiento():
    PartidosEntrenamiento.objects.all().delete()
    pe = cargarPartidoEntrenamiento()
    return pe
def populateDatabaseReal():
    PartidoReal.objects.all().delete()
    pr = cargarPartidoReal()
    return pr

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

def cargarPartidoReal():
    le = cargarPartidoRealLigaEsp()
    pre = cargarPartidoRealPremier()
    bu = cargarPartidoRealBundesliga()
    sea = cargarPartidoRealSerieA()
    li = cargarPartidoRealLigue1()
    lpo = cargarPartidoRealLigaPortuguesa()
    erev = cargarPartidoRealEredivise()
    esp2 = cargarPartidoRealEsp2()
    mls = cargarPartidoRealMLS()
    return (le, pre, bu, sea, li, lpo, erev, esp2, mls)


def cargarPartidoRealLigaEsp():
    id = 1
    temporada = "2023/2024"
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
                    elif goles_visitante > goles_local:
                        winner = "2"
                    else:
                        winner = "X"
                else:
                    goles_local = 0
                    goles_visitante = 0
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, fecha = "hola" ,equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner)
                id = id+1

    return pr

def cargarPartidoRealPremier():
    id = 381
    temporada = "2023/2024"
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
                    elif goles_visitante > goles_local:
                        winner = "2"
                    else:
                        winner = "X"

                else:
                    goles_local = 0
                    goles_visitante = 0
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, fecha = "hola" ,equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner)
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
                    elif goles_visitante > goles_local:
                        winner = "2"
                    else:
                        winner = "X"

                else:
                    goles_local = 0
                    goles_visitante = 0
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner)
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
                    elif goles_visitante > goles_local:
                        winner = "2"
                    else:
                        winner = "X"

                else:
                    goles_local = 0
                    goles_visitante = 0
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner)
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
                    elif goles_visitante > goles_local:
                        winner = "2"
                    else:
                        winner = "X"

                else:
                    goles_local = 0
                    goles_visitante = 0
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner)
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
                    elif goles_visitante > goles_local:
                        winner = "2"
                    else:
                        winner = "X"

                else:
                    goles_local = 0
                    goles_visitante = 0
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner)
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
                    elif goles_visitante > goles_local:
                        winner = "2"
                    else:
                        winner = "X"

                else:
                    goles_local = 0
                    goles_visitante = 0
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner)
                id = id+1

    return pr

def cargarPartidoRealEsp2():
    id = 2365
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
                    elif goles_visitante > goles_local:
                        winner = "2"
                    else:
                        winner = "X"

                else:
                    goles_local = 0
                    goles_visitante = 0
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner)
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
                    elif goles_visitante > goles_local:
                        winner = "2"
                    else:
                        winner = "X"

                else:
                    goles_local = 0
                    goles_visitante = 0
                pr = PartidoReal.objects.create(id = id, liga = liga, jornada=jornada, temporada = temporada, equipo_local=equipo_local, equipo_visitante=equipo_visitante, goles_local=goles_local, goles_visitante = goles_visitante, winner=winner)
                id = id+1

    return pr