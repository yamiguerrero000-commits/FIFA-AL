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

        # Fabri modificacion, atributos disciplina
        self.tarjetas_amarillas = 0
        self.tarjetas_rojas = 0
        self.suspendido = False

    # Fabri modificacion, registrar tarjetas
    def registrar_tarjeta(self, tipo):
        if tipo == "amarilla":
            self.tarjetas_amarillas += 1
            if self.tarjetas_amarillas % 2 == 0:
                self.suspendido = True
        elif tipo == "roja":
            self.tarjetas_rojas += 1
            self.suspendido = True

    # Fabri modificacion, fair play
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

        # Fabri modificacion, estado del partido
        self.estado = "programado"

    # Fabri modificacion, registrar resultado
    def registrar_resultado(self, gl, gv, penales1=0, penales2=0):
        self.goles1 = gl
        self.goles2 = gv
        self.penales1 = penales1
        self.penales2 = penales2
        self.terminado = True
        self.estado = "jugado"

    # Fabri modificacion, suspender y reanudar
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
            if (X.identificador1 == local) and (X.identificador2 == visitante) and (X.fecha == fecha) and not X.terminado:
                X.goles1 = gl
                X.goles2 = gv
                X.penales1 = penales1
                X.penales2 = penales2
                X.terminado = True
                X.estado = "jugado"

                if X.fase != "Grupos":
                    eq_l = self.busqueda(local)
                    eq_v = self.busqueda(visitante)

                    if not isinstance(eq_l, str) and not isinstance(eq_v, str):
                        if gl > gv or (gl == gv and penales1 > penales2):
                            ganador = eq_l
                            perdedor = eq_v
                        elif gv > gl or (gl == gv and penales2 > penales1):
                            ganador = eq_v
                            perdedor = eq_l
                        else:
                            ganador = eq_l
                            perdedor = eq_v

                        fases = ["Dieciseisavos", "Octavos", "Cuartos", "Semifinal", "Final", "Campeón"]
                        if X.fase in fases:
                            idx = fases.index(X.fase)
                            if idx < len(fases) - 1:
                                ganador.avance = fases[idx + 1]
                                perdedor.avance = "Eliminado"

                return "Datos guardados con exito"

        return "Partido no encontrado o ya jugado"


    def configuracion(self):
        self.datos=True #cierre de carga de datos

    def busqueda(self,identificador):
        for X in self.equipos:
            if X.identificador==identificador:
                return X #retorno del equipo buscado
        return "Sin coincidencias"

    # Fabri modificacion, tabla de posiciones por grupo 
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

    # Fabri modificacion, clasificación de mejores terceros
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
        """
        Agrupa los 2 primeros de cada grupo, calcula los 8 mejores terceros,
        y arma de forma directa las llaves de Dieciseisavos dentro de self.partidos.
        """
        clasificados = []
        grupos = []

        
        for e in self.equipos:
            if e.grupo not in grupos:
                grupos.append(e.grupo)

        
        for g in grupos:
            tabla = self.tabla_posiciones(g)
            if len(tabla) >= 1:
                clasificados.append(tabla[0])
            if len(tabla) >= 2:
                clasificados.append(tabla[1])

        
        terceros_ordenados = self.clasificar_mejores_terceros()
        mejores_terceros = terceros_ordenados[:8]
        clasificados.extend(mejores_terceros) 


        for e in self.equipos:
            if e not in clasificados:
                e.avance = "Fase de Grupos"

        
        total = len(clasificados)
        for i in range(total // 2):
            local = clasificados[i]
            visitante = clasificados[total - 1 - i]

            # Seteamos el estatus inicial en play-offs
            local.avance = "Dieciseisavos"
            visitante.avance = "Dieciseisavos"

            # Creamos el objeto partido registrando que pertenece a la fase "Dieciseisavos"
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