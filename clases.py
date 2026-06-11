class equipo:
    def __init__(self,identificador,pais,abreviatura,prefijo,confederacion,grupo):
        self.identificador=identificador
        self.pais=pais
        self.abreviatura=abreviatura
        self.prefijo=int(prefijo) # prefijo telefonico 
        self.confederacion=confederacion
        self.grupo=grupo
        self.total_p=0 #partidos jugados
        self.ganados=0 #partidos ganados
        self.perdidos=0 #partidos perdidos
        self.empate=0 #partidos empatados
        self.goles_c=0 #goles en contra
        self.goles_a=0 #goles a favor
        self.puntos=0 #total de puntos
        self.avance="Fase de Grupos" #lugar del equipo 

        #atributos disciplina
        self.tarjetas_amarillas = 0
        self.tarjetas_rojas = 0
        self.suspendido = False

    #registrar tarjetas
    def registrar_tarjeta(self, tipo):
        if tipo == "amarilla":
            self.tarjetas_amarillas += 1
            if self.tarjetas_amarillas % 2 == 0:
                self.suspendido = True
        elif tipo == "roja":
            self.tarjetas_rojas += 1
            self.suspendido = True

    #fair play
    def fair_play_score(self):
        return -(self.tarjetas_amarillas + 4 * self.tarjetas_rojas)


class partido:
    def __init__(self, fecha, hora, lugar, id1,id2, fase="Grupos"):
        self.fecha=fecha
        self.hora=hora
        self.lugar=lugar
        self.identificador1=id1
        self.identificador2=id2
        self.goles1=0 #goles del primer equipo
        self.goles2=0 #goles del segundo equipo
        self.penales1=0 #penales del primer equipo
        self.penales2=0 #penales del segundo equipo
        self.terminado=False
        self.fase=fase # "Grupos", "Dieciseisavos", "Octavos", "Cuartos", "Semifinal", "Final" 

        #estado del partido
        self.estado = "programado"

    #registrar resultado
    def registrar_resultado(self, gl, gv, penales1=0, penales2=0):
        self.goles1 = gl
        self.goles2 = gv
        self.penales1 = penales1
        self.penales2 = penales2
        self.terminado = True
        self.estado = "jugado"

#suspender y reanudar
    def suspender(self):
        self.estado = "suspendido"

    def reanudar(self):
        self.estado = "reprogramado"


class torneo:
    def __init__(self, nombre,inicio,fin):
        self.nombre=nombre #nombre del torneo
        self.inicio=inicio #fecha de inicio
        self.fin=fin #fecha de fin
        self.equipos=[]
        self.partidos=[]
        self.datos=False #termino de carga de datos

    def registro_e(self,equipo): #registro de equipo
        if not self.datos:
            self.equipos.append(equipo)

    def registro_p(self,partido): #registro de partido
        if not self.datos:
            self.partidos.append(partido)

    def resultado(self, local, visitante, fecha, gl, gv, penales1, penales2):
        for X in self.partidos:
            # Verificamos coincidencia exacta del partido
            if (X.identificador1 == local and X.identificador2 == visitante and X.fecha == fecha):

                if X.terminado:
                    return "Este partido ya fue registrado anteriormente."

                # Guardamos los datos del resultado
                X.goles1 = gl
                X.goles2 = gv
                X.penales1 = penales1
                X.penales2 = penales2
                X.terminado = True
                X.estado = "jugado"

                # Actualizamos estadísticas solo una vez
                self.actualizar_estadisticas(local, visitante, gl, gv)

                # Control automático del avance para fases eliminatorias
                if hasattr(X, "fase") and X.fase != "Grupos":
                    eq_l = self.busqueda(local)
                    eq_v = self.busqueda(visitante)

                    if gl > gv:
                        ganador, perdedor = eq_l, eq_v
                    elif gv > gl:
                        ganador, perdedor = eq_v, eq_l
                    else:
                        # En caso de empate, se define por penales
                        if penales1 >= penales2:
                            ganador, perdedor = eq_l, eq_v
                        else:
                            ganador, perdedor = eq_v, eq_l

                    fases = ["Dieciseisavos", "Octavos", "Cuartos", "Semifinal", "Final", "Campeón"]
                    if X.fase in fases:
                        idx = fases.index(X.fase)
                        ganador.avance = fases[idx + 1]
                        if ganador.avance == "Campeón":
                            perdedor.avance = "Vicecampeón"

                return "Datos guardados con exito"

        return "Partido no encontrado o ya jugado"


    def configuracion(self):
        self.datos=True #cierre de carga de datos

    def busqueda(self,identificador):
        for X in self.equipos:
            if X.identificador==identificador:
                return X #retorno del equipo buscado
        return "Sin coincidencias"
    
    def actualizar_estadisticas(self, local, visitante, gl, gv):
        eq_l = self.busqueda(local)
        eq_v = self.busqueda(visitante)


        partido_existente = None
        for p in self.partidos:
            if p.identificador1 == local and p.identificador2 == visitante and p.terminado:
                partido_existente = p
                break

        if partido_existente:
            # Si el partido ya está terminado, no volver a sumar estadísticas
            return

        # Partidos jugados
        eq_l.total_p += 1
        eq_v.total_p += 1

        # Goles
        eq_l.goles_a += gl
        eq_l.goles_c += gv
        eq_v.goles_a += gv
        eq_v.goles_c += gl

        # Resultado
        if gl > gv:
            eq_l.ganados += 1
            eq_v.perdidos += 1
            eq_l.puntos += 3
        elif gv > gl:
            eq_v.ganados += 1
            eq_l.perdidos += 1
            eq_v.puntos += 3
        else:
            eq_l.empate += 1
            eq_v.empate += 1
            eq_l.puntos += 1
            eq_v.puntos += 1


    def tabla_posiciones(self, grupo):
        equipos_grupo = [e for e in self.equipos if e.grupo == grupo]
        n = len(equipos_grupo)
        for i in range(n - 1):
            for j in range(n - i - 1):
                e1 = equipos_grupo[j]
                e2 = equipos_grupo[j + 1]
                
                dg1 = e1.goles_a - e1.goles_c
                dg2 = e2.goles_a - e2.goles_c
                
                intercambiar = False
                if e1.puntos < e2.puntos:
                    intercambiar = True
                elif e1.puntos == e2.puntos:
                    if dg1 < dg2:
                        intercambiar = True
                    elif dg1 == dg2:
                        if e1.goles_a < e2.goles_a:
                            intercambiar = True
                        elif e1.goles_a == e2.goles_a:
                            if e1.prefijo < e2.prefijo: 
                                intercambiar = True
                                
                if intercambiar:
                    equipos_grupo[j], equipos_grupo[j + 1] = equipos_grupo[j + 1], equipos_grupo[j]
        return equipos_grupo

    def clasificar_mejores_terceros(self):
        terceros = []
        grupos = []
        for e in self.equipos:
            if e.grupo not in grupos:
                grupos.append(e.grupo)
        for g in grupos:
            tabla = self.tabla_posiciones(g)
            if len(tabla) >= 3:
                terceros.append(tabla[2])
        n = len(terceros)
        for i in range(n - 1):
            for j in range(n - i - 1):
                e1 = terceros[j]
                e2 = terceros[j + 1]
                
                dg1 = e1.goles_a - e1.goles_c
                dg2 = e2.goles_a - e2.goles_c
                
                intercambiar = False
                if e1.puntos < e2.puntos:
                    intercambiar = True
                elif e1.puntos == e2.puntos:
                    if dg1 < dg2:
                        intercambiar = True
                    elif dg1 == dg2:
                        if e1.goles_a < e2.goles_a:
                            intercambiar = True
                        elif e1.goles_a == e2.goles_a:
                            if e1.prefijo < e2.prefijo:
                                intercambiar = True
                                
                if intercambiar:
                    terceros[j], terceros[j + 1] = terceros[j + 1], terceros[j]
        return terceros 

    def avanzar_fase_eliminatoria(self):

        clasificados = []
        grupos = []

        # recolectamos grupos
        for e in self.equipos:
            if e.grupo not in grupos:
                grupos.append(e.grupo)

        # agregamos primeros y segundos
        for g in grupos:
            tabla = self.tabla_posiciones(g)
            if len(tabla) >= 1:
                clasificados.append(tabla[0])
            if len(tabla) >= 2:
                clasificados.append(tabla[1])

        # mejores terceros
        terceros_ordenados = self.clasificar_mejores_terceros()
        mejores_terceros = terceros_ordenados[:8]
        clasificados.extend(mejores_terceros)


        for e in self.equipos:
            if e not in clasificados:
                e.avance = "Eliminado en Fase de Grupos"

        # armamos dieciseisavos
        total = len(clasificados)
        for i in range(total // 2):
            local = clasificados[i]
            visitante = clasificados[total - 1 - i]

            local.avance = "Dieciseisavos"
            visitante.avance = "Dieciseisavos"

            nuevo_p = partido(
                fecha="2026-06-28",
                hora="16:00",
                lugar="Estadio Copa Mundial",
                id1=local.identificador,
                id2=visitante.identificador,
                fase="Dieciseisavos"
            )
            self.partidos.append(nuevo_p)

        return f"¡Fase Eliminatoria Generada! {total} equipos clasificados a Dieciseisavos de Final."
