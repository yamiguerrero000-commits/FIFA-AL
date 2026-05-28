from clases import torneo, equipo, partido

# Definicion del torneo
torneo_actual = torneo("Copa Mundial 2026", "2026-06-11", "2026-07-19")

# Validaciones
def es_numero(valor):
    return valor.isdigit()

def existe_equipo(identificador):
    for e in torneo_actual.equipos:
        if e.identificador == identificador:
            return True
    return False

def pedir_no_vacio(mensaje):
    while True:
        dato = input(mensaje).strip()
        if dato:
            return dato
        print("Error: este campo no puede estar vacío.")

def pedir_abreviatura():
    while True:
        abrev = input("Abreviatura (3 letras): ").upper().strip()
        if len(abrev) == 3 and abrev.isalpha():
            return abrev
        print("Error: la abreviatura debe tener exactamente 3 letras.")

def pedir_prefijo():
    while True:
        prefijo = input("Prefijo telefónico: ").strip()
        if es_numero(prefijo):
            return int(prefijo)
        print("Error: el prefijo debe ser un número.")

def pedir_grupo():
    while True:
        grupo = input("Grupo (A-F): ").upper().strip()
        if grupo in ["A","B","C","D","E","F"]:
            return grupo
        print("Error: el grupo debe estar entre A-F.")

def pedir_confederacion():
    while True:
        conf = input("Confederación (UEFA, CONMEBOL, AFC, CAF, CONCACAF, OFC): ").upper().strip()
        if conf in ["UEFA","CONMEBOL","AFC","CAF","CONCACAF","OFC"]:
            return conf
        print("Error: confederación inválida.")

# MENÚ PRINCIPAL
def configurar_torneo():
    while True:
        print("\n CONFIGURACIÓN DEL TORNEO ")
        print("1. Registrar equipo")
        print("2. Registrar partido")
        print("3. Listar equipos")
        print("4. Listar partidos")
        print("5. Cerrar configuración")
        print("0. Volver")

        opcion = input("Opción: ")

        if opcion == "1":
            ident = pedir_no_vacio("Identificador: ")
            if existe_equipo(ident):
                print("Error: ya existe un equipo con ese identificador.")
                continue

            pais = pedir_no_vacio("País: ")
            abrev = pedir_abreviatura()
            prefijo = pedir_prefijo()
            conf = pedir_confederacion()
            grupo = pedir_grupo()

            e = equipo(ident, pais, abrev, prefijo, conf, grupo)
            torneo_actual.registro_e(e)
            print(f"Equipo {pais} registrado en grupo {grupo}.")

        elif opcion == "2":
            fecha = pedir_no_vacio("Fecha (YYYY-MM-DD): ")
            hora = pedir_no_vacio("Hora (HH:MM): ")
            lugar = pedir_no_vacio("Lugar: ")
            id1 = pedir_no_vacio("Identificador equipo 1: ")
            id2 = pedir_no_vacio("Identificador equipo 2: ")

            if id1 == id2:
                print("Error: un partido no puede tener el mismo equipo dos veces.")
                continue
            if not existe_equipo(id1):
                print("Error: equipo 1 no registrado.")
                continue
            if not existe_equipo(id2):
                print("Error: equipo 2 no registrado.")
                continue

            p = partido(fecha, hora, lugar, id1, id2)
            torneo_actual.registro_p(p)
            print(f"Partido registrado: {id1} vs {id2} en {lugar}.")

        elif opcion == "3":
            print("\n LISTA DE EQUIPOS ")
            if not torneo_actual.equipos:
                print("No hay equipos registrados.")
            else:
                for e in torneo_actual.equipos:
                    print(f"{e.identificador} - {e.pais} ({e.abreviatura}) Grupo {e.grupo}")

        elif opcion == "4":
            print("\n LISTA DE PARTIDOS ")
            if not torneo_actual.partidos:
                print("No hay partidos registrados.")
            else:
                for p in torneo_actual.partidos:
                    print(f"{p.fecha} {p.hora} - {p.identificador1} vs {p.identificador2} en {p.lugar}")

        elif opcion == "5":
            torneo_actual.configuracion()
            print("Configuración cerrada. No se podrán modificar los datos.")
            break

        elif opcion == "0":
            break

        else:
            print("Opción inválida.")

if __name__ == "__main__":
    configurar_torneo()

