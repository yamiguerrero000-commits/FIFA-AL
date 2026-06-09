from clases import torneo
from conf_torneo import torneo_actual 

#funcion para ingresar resultados de partidos
def registrar_resultado():
    print("\n REGISTRO DE RESULTADOS ")
    #Pedimos los datos basicos del partido
    fecha = input("Fecha del partido (AAAA-MM-DD): ").strip()
    id_local = input("Identificador equipo local: ").strip()
    id_visitante = input("Identificador equipo visitante: ").strip()

    #Pedimos los goles y penales de cada equipo
    gl = int(input("Goles equipo local: "))
    gv = int(input("Goles equipo visitante: "))
    penales1 = int(input("Penales equipo local (si aplica, sino 0): "))
    penales2 = int(input("Penales equipo visitante (si aplica, sino 0): "))

    #Guardamos el resultado en el torneo
    mensaje = torneo.resultado(id_local, id_visitante, fecha, gl, gv, penales1, penales2)
    print(mensaje)

    #Buscamos los equipos para actualizar sus estadisticas
    equipo_local = torneo.busqueda(id_local)
    equipo_visitante = torneo.busqueda(id_visitante)

    if mensaje == "Datos guardados con exito":
        #Sumamos un partido jugado a cada equipo
        equipo_local.total_p += 1
        equipo_visitante.total_p += 1
        
        #Actualizamos goles a favor y en contra
        equipo_local.goles_a += gl
        equipo_local.goles_c += gv
        equipo_visitante.goles_a += gv
        equipo_visitante.goles_c += gl

        #Segun el resultado, actualizamos ganados, perdidos, empates y puntos
        if gl > gv:
            equipo_local.ganados += 1
            equipo_visitante.perdidos += 1
            equipo_local.puntos += 3
        elif gv > gl:
            equipo_visitante.ganados += 1
            equipo_local.perdidos += 1
            equipo_visitante.puntos += 3
        else:
            equipo_local.empate += 1
            equipo_visitante.empate += 1
            equipo_local.puntos += 1
            equipo_visitante.puntos += 1

        amarillas_local = int(input("Tarjetas amarillas equipo local: "))
        rojas_local = int(input("Tarjetas rojas equipo local: "))
        amarillas_visitante = int(input("Tarjetas amarillas equipo visitante: "))
        rojas_visitante = int(input("Tarjetas rojas equipo visitante: "))
        for _ in range(amarillas_local):
            equipo_local.registrar_tarjeta("amarilla")
        for _ in range(rojas_local):
            equipo_local.registrar_tarjeta("roja")

        for _ in range(amarillas_visitante):
            equipo_visitante.registrar_tarjeta("amarilla")
        for _ in range(rojas_visitante):
            equipo_visitante.registrar_tarjeta("roja")

#Mostrar tabla de posiciones en fase de grupos 
def mostrar_tabla(grupo):
    print("\n TABLA DE POSICIONES - GRUPO", grupo)
    #Obtenemos la tabla ordenada del grupo
    tabla= torneo.tabla_posiciones(grupo)
    if not tabla:
        print("No hay equipos en este grupo.")
        return 
    pos = 1
    #Recorremos los equipos y mostramos sus estadisticas
    for e in tabla:
        dif = e.goles_a - e.goles_c #diferencia de goles
        print(str(pos) + ". " + e.pais + " - Pts:" + str(e.puntos) +
              " GF:" + str(e.goles_a) + " GC:" + str(e.goles_c) + 
              " Dif:" + str(dif))
        pos +=1

#Clasificacion de los mejores terceros
def mostrar_mejores_terceros():
    print("\n MEJORES TERCEROS CLASIFICADOS ")
    #Obtenemos la lista de mejores terceros
    terceros = torneo.clasificar_mejores_terceros()
    pos = 1
    for e in terceros:
        dif = e.goles_a - e.goles_c
        print(str(pos) + ". " + e.pais + " - Pts:" + str(e.puntos) + 
              " GF:" + str(e.goles_a) + "GC:" + str(e.goles_c) +
              " Dif:" + str(dif))
        pos += 1

#Avance de equipos en fase de eliminacion directa 
def avanzar_eliminacion_directa():
    print("\n FASE DE ELIMINACION DIRECTA ")
    clasificados = []
    grupos = []

    #Armamos lista de grupos sin repetir
    for e in torneo_actual.equipos:
        if e.grupo not in grupos:
            grupos.append(e.grupo)

    #Tomamos los dos primeros de cada grupo y los agregamos a clasificados
    for g in grupos:
        tabla = torneo.tabla_posiciones(g)
        if len(tabla) >= 2:
            clasificados.extend(tabla[:2]) #usamos extend para agregar varios equipos

    #Agregamos tambien los mejores terceros
    clasificados.extend(torneo.clasificar_mejores_terceros())

    #Mostramos todos los equipos que pasan a octavos
    print("Equipos clasificados a octavos de final:")
    for e in clasificados:
        print("- " + e.pais + " (Grupo " + e.grupo + ", Pts:" + str(e.puntos) + ")")
        e.avance = "Octavos de Final" #actualizamos el avance del equipo