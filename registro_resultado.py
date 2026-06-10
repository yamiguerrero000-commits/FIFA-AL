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
    mensaje = torneo_actual.resultado(id_local, id_visitante, fecha, gl, gv, penales1, penales2)
    print(mensaje)

    #Buscamos los equipos para actualizar sus estadisticas
    equipo_local = torneo_actual.busqueda(id_local)
    equipo_visitante = torneo_actual.busqueda(id_visitante)

    if mensaje == "Datos guardados con exito":
        #Sumamos un partido jugado a cada equipo
        equipo_local.total_p += 1
        equipo_visitante.total_p += 1
        
        #Actualizamos goles a favor y en contra
        equipo_local.goles_a += gl
        equipo_local.goles_c += gv
        equipo_visitante.goles_a += gv
        equipo_visitante.goles_c += gl

        # Determinamos ganador, perdedor o empate para actualizar estadísticas de fase de grupos
        if gl > gv:
            equipo_local.ganados += 1
            equipo_local.puntos += 3
            equipo_visitante.perdidos += 1
        elif gv > gl:
            equipo_visitante.ganados += 1
            equipo_visitante.puntos += 3
            equipo_local.perdidos += 1
        else:
            # Si es fase de grupos, suma 1 punto a cada uno
            equipo_local.empate += 1
            equipo_visitante.empate += 1
            equipo_local.puntos += 1
            equipo_visitante.puntos += 1

#Mostrar tabla de posiciones de un grupo determinado
def mostrar_tabla_grupo():
    grupo = input("\n Ingrese el grupo a mostrar (A-L): ").strip().upper()
    print(f"\n TABLA DE POSICIONES - GRUPO {grupo} ")
    tabla = torneo_actual.tabla_posiciones(grupo)
    pos = 1
    for e in tabla:
        dif = e.goles_a - e.goles_c
        print(str(pos) + ". " + e.pais + " - Pts:" + str(e.puntos) +
              " GF:" + str(e.goles_a) + " GC:" + str(e.goles_c) + 
              " Dif:" + str(dif))
        pos +=1

#Clasificacion de los mejores terceros
def mostrar_mejores_terceros():
    print("\n MEJORES TERCEROS CLASIFICADOS ")
    #Obtenemos la lista de mejores terceros
    terceros = torneo_actual.clasificar_mejores_terceros()
    pos = 1
    for e in terceros:
        dif = e.goles_a - e.goles_c
        print(str(pos) + ". " + e.pais + " - Pts:" + str(e.puntos) + 
              " GF:" + str(e.goles_a) + " GC:" + str(e.goles_c) +
              " Dif:" + str(dif))
        pos += 1

#Avance de equipos en fase de eliminacion directa 
def avanzar_eliminacion_directa():
    print("\n FASE DE ELIMINACION DIRECTA ")
    
    # Invocamos la función unificada de clases.py que automatiza todo el proceso de corte del PDF
    mensaje_fase = torneo_actual.avanzar_fase_eliminatoria()
    print(mensaje_fase)

    print("\n PARTIDOS PROGRAMADOS PARA DIECISEISAVOS DE FINAL:")
    # Listamos los partidos que acaban de crearse en el árbol de playoffs
    cont = 1
    for p in torneo_actual.partidos:
        if p.fase == "Dieciseisavos":
            eq_l = torneo_actual.busqueda(p.identificador1)
            eq_v = torneo_actual.busqueda(p.identificador2)
            print(f"Llave {cont}: {eq_l.pais} ({eq_l.identificador}) vs {eq_v.pais} ({eq_v.identificador}) - Estado: {p.estado}")
            cont += 1