import tkinter as tk                  # libreria para crear ventanas y botones
from tkinter import messagebox        # para mostrar carteles emergentes de alerta
from tkinter import ttk               # para tablas avanzadas (Treeview)
import os                             # para verificar si existe un archivo
import time                           # para obtener la hora actual
from PIL import Image, ImageTk       # para manejar imagenes y usarlas como fondo
import os
from conf_torneo import torneo_actual
from clases import equipo, partido

# PERSISTENCIA: GUARDAR Y CARGAR DATOS EN ARCHIVO DE TEXTO
def guardar_datos():
    # Abrimos el archivo en modo escritura. Si no existe, lo crea automaticamente
    archivo = open("datos_torneo.txt", "w", encoding="utf-8")

    # Primera linea: guardamos si la configuracion esta cerrada (True o False)
    archivo.write(str(torneo_actual.datos) + "\n")

    # Guardamos cada equipo en una linea con sus atributos separados por comas
    for eq in torneo_actual.equipos:
        linea = ("EQUIPO," +
                 str(eq.identificador) + "," +
                 str(eq.pais) + "," +
                 str(eq.abreviatura) + "," +
                 str(eq.prefijo) + "," +
                 str(eq.confederacion) + "," +
                 str(eq.grupo) + "," +
                 str(eq.total_p) + "," +
                 str(eq.ganados) + "," +
                 str(eq.empate) + "," +        # empate (no empatados)
                 str(eq.perdidos) + "," +
                 str(eq.goles_a) + "," +       # goles_a (no goles_f)
                 str(eq.goles_c) + "," +
                 str(eq.puntos) + "," +
                 str(eq.avance) + "," +
                 str(eq.tarjetas_amarillas) + "," +
                 str(eq.tarjetas_rojas) + "," +
                 str(eq.suspendido) + "\n")
        archivo.write(linea)

    # Guardamos cada partido en una linea con sus atributos
    for p in torneo_actual.partidos:
        linea = ("PARTIDO," +
                 str(p.fecha) + "," +
                 str(p.hora) + "," +
                 str(p.lugar) + "," +
                 str(p.identificador1) + "," +   # identificador1 (no equipo1)
                 str(p.identificador2) + "," +   # identificador2 (no equipo2)
                 str(p.goles1) + "," +
                 str(p.goles2) + "," +
                 str(p.penales1) + "," +
                 str(p.penales2) + "," +
                 str(p.terminado) + "," +
                 str(p.estado) + "\n")
        archivo.write(linea)

    archivo.close()


def cargar_datos():
    # Verificamos si el archivo existe antes de intentar abrirlo 
    if not os.path.exists("datos_torneo.txt"):
        return   # si no existe, salimos sin hacer nada 
    archivo = open("datos_torneo.txt", "r", encoding="utf-8")
    lineas = archivo.readlines()   # leemos todas las lineas de una vez en una lista
    archivo.close()

    # Si el archivo esta vacio, salimos
    if len(lineas) == 0:
        return

    # Primera linea: recuperamos si la configuracion estaba cerrada
    primera_linea = lineas[0].strip()
    if primera_linea == "True":
        torneo_actual.datos = True
    else:
        torneo_actual.datos = False

    # Recorremos el resto de las lineas a partir de la posicion 1
    for i in range(1, len(lineas)):
        linea_limpia = lineas[i].strip()

        # Si la linea esta vacia la saltamos
        if linea_limpia == "":
            continue

        # Separamos la linea por comas para obtener cada atributo
        partes = linea_limpia.split(",")

        # Segun el prefijo, reconstruimos el objeto correspondiente
        if partes[0] == "EQUIPO":
            # Creamos el equipo con los datos basicos
            eq = equipo(partes[1], partes[2], partes[3],
                        int(partes[4]), partes[5], partes[6])
            # Restauramos las estadisticas 
            eq.total_p            = int(partes[7])
            eq.ganados            = int(partes[8])
            eq.empate             = int(partes[9])    # empate, no empatados
            eq.perdidos           = int(partes[10])
            eq.goles_a            = int(partes[11])   # goles_a, no goles_f
            eq.goles_c            = int(partes[12])
            eq.puntos             = int(partes[13])
            eq.avance             = partes[14]
            eq.tarjetas_amarillas = int(partes[15])
            eq.tarjetas_rojas     = int(partes[16])
            eq.suspendido         = (partes[17] == "True")
            # Agregamos el equipo reconstruido al torneo
            torneo_actual.equipos.append(eq)

        elif partes[0] == "PARTIDO":
            # Creamos el partido con los datos basicos usando los parametros correctos
            p = partido(partes[1], partes[2], partes[3], partes[4], partes[5])
            # Restauramos el resultado y estado
            p.goles1    = int(partes[6])
            p.goles2    = int(partes[7])
            p.penales1  = int(partes[8])
            p.penales2  = int(partes[9])
            p.terminado = (partes[10] == "True")
            p.estado    = partes[11]
            # Agregamos el partido reconstruido al torneo
            torneo_actual.partidos.append(p)

# ESTRUCTURAS DE DATOS: PILA Y COLA
historial_pantallas = []
cola_partidos = []

def inicializar_cola_partidos():
    # Vaciamos la cola y la llenamos con los partidos que aun no tienen resultado
    global cola_partidos
    cola_partidos = []
    for p in torneo_actual.partidos:
        if not p.terminado:
            cola_partidos.append(p)   # enqueue: agregamos al final de la cola


# CLASE PRINCIPAL: APLICACION 

class Aplicacion:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("⚽ FIFA 2026 – Panel de Control Oficial")
        self.raiz.geometry("950x700")
        self.raiz.configure(bg="#1a1a2e")

        # Centramos la ventana en la pantalla
        self.raiz.update_idletasks()
        x = (self.raiz.winfo_screenwidth() // 2) - (950 // 2)
        y = (self.raiz.winfo_screenheight() // 2) - (700 // 2)
        self.raiz.geometry("950x700+" + str(x) + "+" + str(y))

        # Configuramos el estilo visual de los Treeview (tablas)
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Treeview",
                         background="#600f45",
                         fieldbackground="#600b45",
                         foreground="white",
                         font=("Arial", 10))
        estilo.configure("Treeview.Heading",
                         background="#600f45",
                         foreground="#f5a623",
                         font=("Arial", 10, "bold"))
        estilo.map("Treeview", background=[("selected", "#e94560")])

        # Contenedor principal donde se van a pintar todas las pantallas
        self.contenedor = tk.Frame(self.raiz, bg="#1a1a2e")
        self.contenedor.pack(fill="both", expand=True)

        # Cargar imagen de fondo de forma segura
        try:
            self.imagen_original = Image.open("fondo.png") 
            self.foto_fondo = None
        except Exception as e:
            print(f"No se pudo cargar la imagen de fondo: {e}")
            self.imagen_original = None
            self.foto_fondo = None

        # Vinculamos el contenedor al evento de cambio de tamaño dinámico
        self.contenedor.bind("<Configure>", self.redimensionar_fondo)

        # Cuando el usuario cierra con la X, guardamos datos primero
        self.raiz.protocol("WM_DELETE_WINDOW", self.salir_aplicacion)

        # Mostramos el menu principal al iniciar
        self.mostrar_menu_principal()

    def redimensionar_fondo(self, evento=None):
        if not self.imagen_original or not self.contenedor.winfo_exists():
            return

        ancho = self.contenedor.winfo_width()
        alto = self.contenedor.winfo_height()

        if ancho <= 1 or alto <= 1:
            return

        imagen_rediseñada = self.imagen_original.resize((ancho, alto), Image.Resampling.LANCZOS)
        self.foto_fondo = ImageTk.PhotoImage(imagen_rediseñada)

        for widget in self.contenedor.winfo_children():
            if isinstance(widget, tk.Label) and widget.winfo_manager() == "place":
                widget.config(image=self.foto_fondo)
                break

    def crear_encabezado(self, frame_destino):
        f_header = tk.Frame(frame_destino, bg="#de8ebf", pady=8)
        f_header.pack(fill="x", side="top")

        tk.Label(f_header,
                 text="Algoritmos y Estructuras de Datos II  –  Facultad Politecnica  –  UNA",
                 bg="#de8ebf", fg="#16213e",
                 font=("Arial", 10, "bold")).pack()

        tk.Label(f_header,
                 text="⚽  Sistema de Gestion  –  Copa Mundial FIFA 2026",
                 bg="#de8ebf", fg="white",
                 font=("Arial", 14, "bold")).pack(pady=2)

        lbl_reloj = tk.Label(f_header, text="", bg="#de8ebf", fg="#222222",
                             font=("Arial", 10))
        lbl_reloj.pack()

        def actualizar_reloj():
            lbl_reloj.config(text=time.strftime("%d/%m/%Y   %H:%M:%S"))
            self.raiz.after(1000, actualizar_reloj)

        actualizar_reloj()

    def limpiar_contenedor(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()

        if self.imagen_original:
            lbl_fondo = tk.Label(self.contenedor)
            lbl_fondo.place(x=0, y=0, relwidth=1, relheight=1)
            self.redimensionar_fondo()

    def mostrar_menu_principal(self):
        self.limpiar_contenedor()
        historial_pantallas.append("MENU")
        self.crear_encabezado(self.contenedor)
        panel = tk.Frame(self.contenedor, bg="#ec7bc0", padx=60, pady=30)
        panel.pack(pady=50)
        tk.Label(panel, text="MENU PRINCIPAL",
                 bg="#ec7bc0", fg="white",
                 font=("Arial", 18, "bold")).pack(pady=20)

        # Boton 1
        btn1 = tk.Button(panel,
                         text="1.  Configuracion del Torneo",
                         width=38, height=2,
                         bg="#b3428d", fg="white",
                         font=("Arial", 11, "bold"),
                         activebackground="#e94560",
                         command=self.abrir_configuracion)
        btn1.pack(pady=8)

        # Boton 2
        btn2 = tk.Button(panel,
                         text="2.  Registro de Resultados",
                         width=38, height=2,
                         bg="#b3428d", fg="white",
                         font=("Arial", 11, "bold"),
                         activebackground="#e94560",
                         command=self.abrir_resultados)
        btn2.pack(pady=8)

        # Boton 3
        btn3 = tk.Button(panel,
                         text="3.  Emision de Informes",
                         width=38, height=2,
                         bg="#b3428d", fg="white",
                         font=("Arial", 11, "bold"),
                         activebackground="#e94560",
                         command=self.abrir_informes)
        btn3.pack(pady=8)

        if not torneo_actual.datos:
            btn2.config(state="disabled", bg="#333333", fg="#777777")
            btn3.config(state="disabled", bg="#333333", fg="#777777")

        # Boton 4: Salir
        btn4 = tk.Button(panel,
                         text="4.  Salir",
                         width=38, height=2,
                         bg="#b3428d", fg="white",
                         font=("Arial", 11, "bold"),
                         activebackground="#e94560",
                         command=self.salir_aplicacion)
        btn4.pack(pady=8)

    def volver_atras(self):
        if len(historial_pantallas) > 0:
            historial_pantallas.pop()

        if len(historial_pantallas) > 0:
            anterior = historial_pantallas[len(historial_pantallas) - 1]
            if anterior == "MENU":
                self.mostrar_menu_principal()
            elif anterior == "INFORMES":
                self.abrir_informes()
        else:
            self.mostrar_menu_principal()

    def abrir_configuracion(self):
        self.limpiar_contenedor()
        PantallaConfiguracion(self.contenedor, self)

    def abrir_resultados(self):
        self.limpiar_contenedor()
        PantallaResultados(self.contenedor, self)

    def abrir_informes(self):
        self.limpiar_contenedor()
        PantallaInformes(self.contenedor, self)

    def salir_aplicacion(self):
        confirmar = messagebox.askyesno("Salir",
                                        "Desea guardar los datos y cerrar el sistema?")
        if confirmar:
            guardar_datos()
            self.raiz.destroy()


# PANTALLA 1: CONFIGURACION DEL TORNEO

class PantallaConfiguracion:
    def __init__(self, contenedor, app):
        self.contenedor = contenedor
        self.app = app

        # Apilamos esta pantalla en el historial (push)
        historial_pantallas.append("CONFIGURACION")

        self.app.crear_encabezado(self.contenedor)

        # 1. El cuerpo principal ocupa todo el espacio disponible
        f_cuerpo = tk.Frame(self.contenedor, bg="#ea008f")
        f_cuerpo.pack(fill="both", expand=True)

        # 2. El Canvas ahora se expande al 100% cubriendo todo el fondo
        self.canvas = tk.Canvas(f_cuerpo, bg="#ea008f", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        try:
            self.imagen_original = Image.open("fondo2.png")
            self.foto_fondo = None
            # Evento de redimensión asignado directamente al Canvas
            self.canvas.bind("<Configure>", self.redimensionar_fondo_canvas)
        except Exception as e:
            print(f"⚠️ Alerta: No se pudo cargar la imagen: {e}")
            self.imagen_original = None
        COLOR_CAJA = "#edcbf6" 
        COLOR_TEXTO_TITULO = "#66156c" 
        COLOR_TEXTO_LABELS = "#000000" 
        estilo = ttk.Style()
        estilo.theme_use("clam") 
        
        estilo.configure("Treeview", 
                         background="#ffffff", 
                         fieldbackground="#ffffff", 
                         foreground="black", 
                         bordercolor=COLOR_CAJA, 
                         borderwidth=1)
        
        estilo.configure("Treeview.Heading", 
                         background=COLOR_CAJA, 
                         foreground=COLOR_TEXTO_TITULO, 
                         font=("Arial", 10, "bold"),
                         relief="flat")
        
        estilo.map("Treeview.Heading", 
                   background=[('active', COLOR_CAJA)], 
                   foreground=[('active', COLOR_TEXTO_TITULO)])

        self.f_componentes = tk.Frame(self.canvas, bg="#d3459c", width=935, height=540)
        
        # En lugar de usar place o pack, metemos el frame "DENTRO" del flujo del Canvas
        self.canvas_window = self.canvas.create_window(0, 0, anchor="nw", window=self.f_componentes)

        f_equipo = tk.LabelFrame(self.f_componentes,
                                  text="   Registrar Equipo   ",
                                  bg=COLOR_CAJA, fg=COLOR_TEXTO_TITULO,
                                  font=("Arial", 11, "bold"), bd=1, relief="solid")
        f_equipo.place(x=15, y=15, width=440, height=230)

        tk.Label(f_equipo, text="ID:", bg=COLOR_CAJA, fg=COLOR_TEXTO_LABELS).grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.ent_id = tk.Entry(f_equipo, width=12, bg="white", fg="black", insertbackground="black", bd=1)
        self.ent_id.grid(row=0, column=1, padx=8, pady=8, sticky="w")

        tk.Label(f_equipo, text="Pais:", bg=COLOR_CAJA, fg=COLOR_TEXTO_LABELS).grid(row=0, column=2, padx=8, pady=8, sticky="w")
        self.ent_pais = tk.Entry(f_equipo, width=18, bg="white", fg="black", insertbackground="black", bd=1)
        self.ent_pais.grid(row=0, column=3, padx=8, pady=8, sticky="w")

        tk.Label(f_equipo, text="Abreviatura:", bg=COLOR_CAJA, fg=COLOR_TEXTO_LABELS).grid(row=1, column=0, padx=8, pady=8, sticky="w")
        self.ent_abrev = tk.Entry(f_equipo, width=12, bg="white", fg="black", insertbackground="black", bd=1)
        self.ent_abrev.grid(row=1, column=1, padx=8, pady=8, sticky="w")

        tk.Label(f_equipo, text="Prefijo Tel:", bg=COLOR_CAJA, fg=COLOR_TEXTO_LABELS).grid(row=1, column=2, padx=8, pady=8, sticky="w")
        self.ent_pref = tk.Entry(f_equipo, width=18, bg="white", fg="black", insertbackground="black", bd=1)
        self.ent_pref.grid(row=1, column=3, padx=8, pady=8, sticky="w")

        tk.Label(f_equipo, text="Confederacion:", bg=COLOR_CAJA, fg=COLOR_TEXTO_LABELS).grid(row=2, column=0, padx=8, pady=8, sticky="w")
        self.var_conf = tk.StringVar(f_equipo)
        self.var_conf.set("UEFA")
        opciones_conf = ["UEFA", "CONMEBOL", "AFC", "CAF", "CONCACAF", "OFC"]
        menu_c = tk.OptionMenu(f_equipo, self.var_conf, *opciones_conf)
        menu_c.config(bg="white", fg="black", activebackground="#f0f0f0", activeforeground="black", bd=1,
                      highlightbackground=COLOR_CAJA, highlightthickness=0)
        menu_c.grid(row=2, column=1, padx=8, pady=8, sticky="w")

        tk.Label(f_equipo, text="Grupo:", bg=COLOR_CAJA, fg=COLOR_TEXTO_LABELS).grid(row=2, column=2, padx=8, pady=8, sticky="w")
        self.var_grupo = tk.StringVar(f_equipo)
        self.var_grupo.set("A")
        opciones_grupo = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
        menu_g = tk.OptionMenu(f_equipo, self.var_grupo, *opciones_grupo)
        menu_g.config(bg="white", fg="black", activebackground="#f0f0f0", activeforeground="black", bd=1,
                      highlightbackground=COLOR_CAJA, highlightthickness=0)
        menu_g.grid(row=2, column=3, padx=8, pady=8, sticky="w")

        tk.Button(f_equipo, text="Guardar Equipo",
                  bg="#e18ddd", fg="white", font=("Arial", 10, "bold"), activebackground="#e18ddd",
                  command=self.guardar_equipo).grid(row=3, column=0, columnspan=4, pady=10)

        f_partido = tk.LabelFrame(self.f_componentes,
                                   text="   Registrar Partido   ",
                                   bg=COLOR_CAJA, fg=COLOR_TEXTO_TITULO,
                                   font=("Arial", 11, "bold"), bd=1, relief="solid")
        f_partido.place(x=480, y=15, width=440, height=230)

        tk.Label(f_partido, text="Fecha (AAAA-MM-DD):", bg=COLOR_CAJA, fg=COLOR_TEXTO_LABELS).grid(row=0, column=0, padx=5, pady=8, sticky="w")
        self.ent_fec = tk.Entry(f_partido, width=13, bg="white", fg="black", insertbackground="black", bd=1)
        self.ent_fec.grid(row=0, column=1, padx=5, pady=8, sticky="w")

        tk.Label(f_partido, text="Hora (HH:MM):", bg=COLOR_CAJA, fg=COLOR_TEXTO_LABELS).grid(row=0, column=2, padx=5, pady=8, sticky="w")
        self.ent_hor = tk.Entry(f_partido, width=10, bg="white", fg="black", insertbackground="black", bd=1)
        self.ent_hor.grid(row=0, column=3, padx=5, pady=8, sticky="w")

        tk.Label(f_partido, text="Lugar:", bg=COLOR_CAJA, fg=COLOR_TEXTO_LABELS).grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.ent_lug = tk.Entry(f_partido, width=38, bg="white", fg="black", insertbackground="black", bd=1)
        self.ent_lug.grid(row=1, column=1, columnspan=3, padx=5, pady=8, sticky="w")

        tk.Label(f_partido, text="Equipo 1:", bg=COLOR_CAJA, fg=COLOR_TEXTO_LABELS).grid(row=2, column=0, padx=5, pady=8, sticky="w")
        self.var_e1 = tk.StringVar(f_partido)
        self.menu_e1 = tk.OptionMenu(f_partido, self.var_e1, "")
        self.menu_e1.config(bg="white", fg="black", activebackground="#f0f0f0", activeforeground="black", bd=1,
                            highlightbackground=COLOR_CAJA, highlightthickness=0)
        self.menu_e1.grid(row=2, column=1, padx=5, pady=8, sticky="w")

        tk.Label(f_partido, text="Equipo 2:", bg=COLOR_CAJA, fg=COLOR_TEXTO_LABELS).grid(row=2, column=2, padx=5, pady=8, sticky="w")
        self.var_e2 = tk.StringVar(f_partido)
        self.menu_e2 = tk.OptionMenu(f_partido, self.var_e2, "")
        self.menu_e2.config(bg="white", fg="black", activebackground="#f0f0f0", activeforeground="black", bd=1,
                            highlightbackground=COLOR_CAJA, highlightthickness=0)
        self.menu_e2.grid(row=2, column=3, padx=5, pady=8, sticky="w")

        tk.Button(f_partido, text="Guardar Partido",
                  bg="#e18ddd", fg="white", font=("Arial", 10, "bold"), activebackground="#e18ddd",
                  command=self.guardar_partido).grid(row=3, column=0, columnspan=4, pady=10)

        tk.Label(self.f_componentes, text=" Equipos Registrados ", bg=COLOR_CAJA, fg=COLOR_TEXTO_TITULO, font=("Arial", 10, "bold")).place(x=15, y=255)

        self.tabla_e = ttk.Treeview(self.f_componentes,
                                     columns=("ID", "Pais", "Abrev", "Grupo", "Conf"),
                                     show="headings", height=5)
        for col, ancho in [("ID", 60), ("Pais", 150), ("Abrev", 70), ("Grupo", 60), ("Conf", 100)]:
            self.tabla_e.heading(col, text=col)
            self.tabla_e.column(col, width=ancho, anchor="center")
        self.tabla_e.place(x=15, y=280, width=440, height=140)

        tk.Label(self.f_componentes, text=" Partidos Programados ", bg=COLOR_CAJA, fg=COLOR_TEXTO_TITULO, font=("Arial", 10, "bold")).place(x=480, y=255)

        self.tabla_p = ttk.Treeview(self.f_componentes,
                                     columns=("Fecha", "Hora", "Lugar", "Eq1", "Eq2"),
                                     show="headings", height=5)
        for col, ancho in [("Fecha", 90), ("Hora", 55), ("Lugar", 125), ("Eq1", 85), ("Eq2", 85)]:
            self.tabla_p.heading(col, text=col)
            self.tabla_p.column(col, width=ancho, anchor="center")
        self.tabla_p.place(x=480, y=280, width=440, height=140)

        # BOTONES INFERIORES

        self.btn_cerrar = tk.Button(self.f_componentes,
                                     text="🔒   Cerrar Configuracion del Torneo",
                                     bg="#6c0e59", fg="white",
                                     font=("Arial", 11, "bold"),
                                     command=self.cerrar_configuracion)
        self.btn_cerrar.place(x=292, y=440, width=350, height=38)

        tk.Button(self.f_componentes,
                  text="⬅   Volver al Menu",
                  bg="#5e1e47", fg="white", activebackground="#5e1e47",
                  font=("Arial", 10),
                  command=self.app.volver_atras).place(x=387, y=492, width=160, height=30)

        self.actualizar_tablas()
        self.actualizar_desplegables()

        if torneo_actual.datos:
            self.bloquear_formularios()

        self.canvas.update_idletasks()
        self.redimensionar_fondo_canvas()

    def redimensionar_fondo_canvas(self, evento=None):
        if not self.imagen_original or not self.canvas.winfo_exists():
            return

        # Obtenemos el ancho y alto en tiempo real de la ventana de la App
        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()

        if ancho <= 1 or alto <= 1:
            return


        imagen_rediseñada = self.imagen_original.resize((ancho, alto), Image.Resampling.LANCZOS)
        self.foto_fondo = ImageTk.PhotoImage(imagen_rediseñada)
        
        # Limpiamos y dibujamos el fondo
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.foto_fondo)

        pos_x = (ancho - 935) // 2
        pos_y = (alto - 540) // 2
        

        self.canvas.create_window(max(0, pos_x), max(0, pos_y), anchor="nw", window=self.f_componentes)

    def bloquear_formularios(self):
        self.btn_cerrar.config(state="disabled", text="Configuracion Cerrada", bg="#FFFFFF")

    def actualizar_desplegables(self):
        lista_ids = []
        for eq in torneo_actual.equipos:
            lista_ids.append(eq.identificador)

        if len(lista_ids) > 0:
            self.var_e1.set(lista_ids[0])
            self.var_e2.set(lista_ids[0])

            menu = self.menu_e1["menu"]
            menu.delete(0, "end")
            self.menu_e1.config(highlightbackground="#edcbf6", highlightthickness=0)
            for item in lista_ids:
                menu.add_command(label=item, command=tk._setit(self.var_e1, item))

            menu2 = self.menu_e2["menu"]
            menu2.delete(0, "end")
            self.menu_e2.config(highlightbackground="#edcbf6", highlightthickness=0)
            for item in lista_ids:
                menu2.add_command(label=item, command=tk._setit(self.var_e2, item))

    def actualizar_tablas(self):
        for item in self.tabla_e.get_children():
            self.tabla_e.delete(item)
        for item in self.tabla_p.get_children():
            self.tabla_p.delete(item)

        for eq in torneo_actual.equipos:
            self.tabla_e.insert("", "end",
                                 values=(eq.identificador, eq.pais,
                                         eq.abreviatura, eq.grupo, eq.confederacion))

        for p in torneo_actual.partidos:
            self.tabla_p.insert("", "end",
                                 values=(p.fecha, p.hora, p.lugar,
                                         p.identificador1, p.identificador2))

    def guardar_equipo(self):
        if torneo_actual.datos:
            messagebox.showerror("Error", "La configuracion ya esta cerrada.")
            return

        v_id    = self.ent_id.get().strip()
        v_pais  = self.ent_pais.get().strip()
        v_abrev = self.ent_abrev.get().strip().upper()
        v_pref  = self.ent_pref.get().strip()

        if v_id == "" or v_pais == "" or v_abrev == "" or v_pref == "":
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not v_pref.isdigit():
            messagebox.showerror("Error", "El prefijo telefonico debe ser un numero.")
            return

        if len(v_abrev) != 3 or not v_abrev.isalpha():
            messagebox.showerror("Error", "La abreviatura debe tener exactamente 3 letras.")
            return

        for eq in torneo_actual.equipos:
            if eq.identificador == v_id:
                messagebox.showerror("Error", "Ya existe un equipo con ese identificador.")
                return

        nuevo = equipo(v_id, v_pais, v_abrev, int(v_pref),
                       self.var_conf.get(), self.var_grupo.get())
        torneo_actual.registro_e(nuevo)

        self.ent_id.delete(0, "end")
        self.ent_pais.delete(0, "end")
        self.ent_abrev.delete(0, "end")
        self.ent_pref.delete(0, "end")

        self.actualizar_tablas()
        self.actualizar_desplegables()
        messagebox.showinfo("Exito", "Equipo " + v_pais + " registrado correctamente.")

    def guardar_partido(self):
        if torneo_actual.datos:
            messagebox.showerror("Error", "La configuracion ya esta cerrada.")
            return

        v_fec = self.ent_fec.get().strip()
        v_hor = self.ent_hor.get().strip()
        v_lug = self.ent_lug.get().strip()
        v_e1  = self.var_e1.get()
        v_e2  = self.var_e2.get()

        if v_fec == "" or v_hor == "" or v_lug == "" or v_e1 == "" or v_e2 == "":
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if v_e1 == v_e2:
            messagebox.showerror("Error", "Los dos equipos deben ser distintos.")
            return

        nuevo_p = partido(v_fec, v_hor, v_lug, v_e1, v_e2)
        torneo_actual.registro_p(nuevo_p)

        self.ent_fec.delete(0, "end")
        self.ent_hor.delete(0, "end")
        self.ent_lug.delete(0, "end")

        self.actualizar_tablas()
        messagebox.showinfo("Exito", "Partido registrado correctamente.")

    def cerrar_configuracion(self):
        if len(torneo_actual.equipos) < 2:
            messagebox.showerror("Error", "Debe registrar al menos 2 equipos antes de cerrar.")
            return

        confirmar = messagebox.askyesno("Confirmacion",
                                         "Esta seguro de cerrar la configuracion? Esta accion no se puede revertir.")
        if confirmar:
            torneo_actual.configuracion()
            self.bloquear_formularios()
            messagebox.showinfo("Exito", "Configuracion cerrada. Ya puede registrar resultados e informes.")

# PANTALLA 2: REGISTRO DE RESULTADOS
class PantallaResultados:
    def __init__(self, contenedor, app):
        self.contenedor = contenedor
        self.app = app

        # Apilamos esta pantalla en el historial (push)
        historial_pantallas.append("RESULTADOS")

        self.app.crear_encabezado(self.contenedor)

        # Inicializamos la cola con los partidos pendientes
        inicializar_cola_partidos()

        f_cuerpo = tk.Frame(self.contenedor, bg="#edcbf6")
        f_cuerpo.pack(fill="both", expand=True, padx=15, pady=10)

        # Titulo de la cola
        tk.Label(f_cuerpo,
                 text="COLA DE PARTIDOS PENDIENTES  (se procesan en orden de registro)",
                 bg="#bc83b6", fg="#ffffff",
                 font=("Arial", 11, "bold")).pack(anchor="w", pady=5)

        # Tabla que muestra la cola de partidos
        self.tabla_cola = ttk.Treeview(f_cuerpo,
                                        columns=("Fecha", "Hora", "Lugar", "Local", "Visitante", "Estado"),
                                        show="headings", height=5)
        for col, ancho in [("Fecha", 95), ("Hora", 60), ("Lugar", 160), ("Local", 100), ("Visitante", 100), ("Estado", 110)]:
            self.tabla_cola.heading(col, text=col)
            self.tabla_cola.column(col, width=ancho, anchor="center")
        self.tabla_cola.pack(fill="x", pady=5)

        # Al hacer clic en una fila de la cola, se activan los campos de goles
        self.tabla_cola.bind("<<TreeviewSelect>>", self.seleccionar_partido)

        # Frame del formulario de marcador
        f_marcador = tk.LabelFrame(f_cuerpo,
                                    text="  Ingresar Marcador del Partido Seleccionado  ",
                                    bg="#943976", fg="white",
                                    font=("Arial", 10, "bold"))
        f_marcador.pack(fill="x", pady=12, ipady=8)

        # Label que muestra que partido esta seleccionado
        self.lbl_vs = tk.Label(f_marcador,
                                text="Seleccione un partido de la cola de arriba",
                                bg="#943976", fg="#ffffff",
                                font=("Arial", 12, "bold"))
        self.lbl_vs.pack(pady=8)

        # Frame para los campos de goles, penales y tarjetas
        f_goles = tk.Frame(f_marcador, bg="#6f0c50")
        f_goles.pack()

        # Fila 0: Goles
        tk.Label(f_goles, text="Goles Local:", bg="#6f0c50", fg="white").grid(row=0, column=0, padx=10, pady=5)
        self.ent_gl = tk.Entry(f_goles, width=8, state="disabled")
        self.ent_gl.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(f_goles, text="Goles Visitante:", bg="#6f0c50", fg="white").grid(row=0, column=2, padx=10, pady=5)
        self.ent_gv = tk.Entry(f_goles, width=8, state="disabled")
        self.ent_gv.grid(row=0, column=3, padx=10, pady=5)

        # Fila 1: Penales
        tk.Label(f_goles, text="Penales Local:", bg="#6f0c50", fg="white").grid(row=1, column=0, padx=10, pady=5)
        self.ent_pl = tk.Entry(f_goles, width=8, state="disabled")
        self.ent_pl.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(f_goles, text="Penales Visitante:", bg="#6f0c50", fg="white").grid(row=1, column=2, padx=10, pady=5)
        self.ent_pv = tk.Entry(f_goles, width=8, state="disabled")
        self.ent_pv.grid(row=1, column=3, padx=10, pady=5)

        # Fila 2: Tarjetas Amarillas
        tk.Label(f_goles, text="Amarillas Local:", bg="#6f0c50", fg="white").grid(row=2, column=0, padx=10, pady=5)
        self.ent_al = tk.Entry(f_goles, width=8, state="disabled")
        self.ent_al.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(f_goles, text="Amarillas Visitante:", bg="#6f0c50", fg="white").grid(row=2, column=2, padx=10, pady=5)
        self.ent_av = tk.Entry(f_goles, width=8, state="disabled")
        self.ent_av.grid(row=2, column=3, padx=10, pady=5)

        # Fila 3: Tarjetas Rojas
        tk.Label(f_goles, text="Rojas Local:", bg="#6f0c50", fg="white").grid(row=3, column=0, padx=10, pady=5)
        self.ent_rl = tk.Entry(f_goles, width=8, state="disabled")
        self.ent_rl.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(f_goles, text="Rojas Visitante:", bg="#6f0c50", fg="white").grid(row=3, column=2, padx=10, pady=5)
        self.ent_rv = tk.Entry(f_goles, width=8, state="disabled")
        self.ent_rv.grid(row=3, column=3, padx=10, pady=5)

        # Frame para los botones de accion
        f_botones = tk.Frame(f_cuerpo, bg="#5e1e47")
        f_botones.pack(pady=10)

        self.btn_registrar = tk.Button(f_botones,
                                        text="⚽  Registrar Resultado",
                                        bg="#9c3978", fg="white",
                                        font=("Arial", 10, "bold"),
                                        state="disabled",
                                        command=self.registrar_marcador)
        self.btn_registrar.grid(row=0, column=0, padx=10)

        self.btn_suspender = tk.Button(f_botones,
                                        text="⛔  Suspender Partido",
                                        bg="#9c3978", fg="white",
                                        state="disabled",
                                        command=self.suspender_partido)
        self.btn_suspender.grid(row=0, column=1, padx=10)

        self.btn_reanudar = tk.Button(f_botones,
                                       text="🔄  Reanudar Partido",
                                       bg="#9c3978", fg="white",
                                       state="disabled",
                                       command=self.reanudar_partido)
        self.btn_reanudar.grid(row=0, column=2, padx=10)

        tk.Button(f_cuerpo,
                  text="⬅  Volver al Menu",
                  bg="#9c3978", fg="white",
                  command=self.app.volver_atras).pack(pady=12)

        # Variable que guarda el partido actualmente seleccionado
        self.partido_seleccionado = None

        # Cargamos la tabla con la cola actual
        self.actualizar_tabla_cola()

    def actualizar_tabla_cola(self):
        # Borramos las filas actuales de la tabla
        for item in self.tabla_cola.get_children():
            self.tabla_cola.delete(item)
        # Insertamos cada partido de la cola
        for p in cola_partidos:
            self.tabla_cola.insert("", "end",
                                    values=(p.fecha, p.hora, p.lugar,
                                            p.identificador1, p.identificador2,
                                            p.estado))

    def seleccionar_partido(self, evento):
        # Obtenemos la fila seleccionada en la tabla
        seleccion = self.tabla_cola.selection()
        if not seleccion:
            return

        valores = self.tabla_cola.item(seleccion[0], "values")
        v_fec = valores[0]
        v_hor = valores[1]
        v_id1 = valores[3]
        v_id2 = valores[4]

        # Buscamos el objeto partido real que coincide con esos datos
        self.partido_seleccionado = None
        for p in torneo_actual.partidos:
            if (p.fecha == v_fec and p.hora == v_hor and
                    p.identificador1 == v_id1 and p.identificador2 == v_id2):
                self.partido_seleccionado = p

        # Si lo encontramos, mostramos su nombre y habilitamos los campos
        if self.partido_seleccionado:
            self.lbl_vs.config(text=self.partido_seleccionado.identificador1 +
                                    "  VS  " +
                                    self.partido_seleccionado.identificador2)
            self.ent_gl.config(state="normal")
            self.ent_gv.config(state="normal")
            self.ent_pl.config(state="normal")
            self.ent_pv.config(state="normal")
            self.ent_al.config(state="normal")
            self.ent_av.config(state="normal")
            self.ent_rl.config(state="normal")
            self.ent_rv.config(state="normal")
            self.btn_registrar.config(state="normal")
            self.btn_suspender.config(state="normal")
            self.btn_reanudar.config(state="normal")

    def registrar_marcador(self):
        if not self.partido_seleccionado:
            return

        # Verificamos que el partido seleccionado sea el primero de la cola (orden FIFO)
        if len(cola_partidos) == 0 or self.partido_seleccionado != cola_partidos[0]:
            messagebox.showwarning("Atencion",
                                   "Debe registrar los resultados en orden. Seleccione el primero de la cola.")
            return

        # Obtenemos los goles, penales y tarjetas ingresados
        gl_str = self.ent_gl.get().strip()
        gv_str = self.ent_gv.get().strip()
        pl_str = self.ent_pl.get().strip()
        pv_str = self.ent_pv.get().strip()
        al_str = self.ent_al.get().strip()
        av_str = self.ent_av.get().strip()
        rl_str = self.ent_rl.get().strip()
        rv_str = self.ent_rv.get().strip()

        # Validacion: todos los campos son obligatorios
        if gl_str == "" or gv_str == "" or pl_str == "" or pv_str == "" or al_str == "" or av_str == "" or rl_str == "" or rv_str == "":
            messagebox.showerror("Error", "Complete todos los campos de goles, penales y tarjetas.")
            return

        # Validacion: deben ser numeros enteros
        if not gl_str.isdigit() or not gv_str.isdigit() or not pl_str.isdigit() or not pv_str.isdigit() or not al_str.isdigit() or not av_str.isdigit() or not rl_str.isdigit() or not rv_str.isdigit():
            messagebox.showerror("Error", "Todos los valores ingresados deben ser numeros enteros.")
            return

        gl = int(gl_str)
        gv = int(gv_str)
        pl = int(pl_str)
        pv = int(pv_str)
        al = int(al_str)
        av = int(av_str)
        rl = int(rl_str)
        rv = int(rv_str)

        # Llamamos al metodo resultado() de la clase torneo (compañero 1)
        mensaje = torneo_actual.resultado(
            self.partido_seleccionado.identificador1,
            self.partido_seleccionado.identificador2,
            self.partido_seleccionado.fecha,
            gl, gv, pl, pv
        )

        if mensaje == "Datos dos guardados con exito" or mensaje == "Datos guardados con exito":
            # Buscamos los objetos equipo para actualizar sus estadisticas
            eq_local     = torneo_actual.busqueda(self.partido_seleccionado.identificador1)
            eq_visitante = torneo_actual.busqueda(self.partido_seleccionado.identificador2)

            # Sumamos partidos jugados a ambos
            eq_local.total_p     += 1
            eq_visitante.total_p += 1

            # Actualizamos goles a favor y en contra
            eq_local.goles_a     += gl
            eq_local.goles_c     += gv
            eq_visitante.goles_a += gv
            eq_visitante.goles_c += gl

            # Segun el resultado actualizamos ganados, perdidos, empates y puntos
            if gl > gv:
                eq_local.ganados     += 1
                eq_visitante.perdidos += 1
                eq_local.puntos      += 3
            elif gv > gl:
                eq_visitante.ganados  += 1
                eq_local.perdidos    += 1
                eq_visitante.puntos  += 3
            else:
                eq_local.empate      += 1
                eq_visitante.empate  += 1
                eq_local.puntos      += 1
                eq_visitante.puntos  += 1

            # Actualizamos contadores de tarjetas en los objetos de los equipos
            eq_local.tarjetas_amarillas += al
            eq_local.tarjetas_rojas     += rl
            eq_visitante.tarjetas_amarillas += av
            eq_visitante.tarjetas_rojas     += rv

            # Verificacion de suspensiones por tarjetas corrigiendo el bug del cero (0)
            if eq_local.tarjetas_rojas > 0 or (eq_local.tarjetas_amarillas > 0 and eq_local.tarjetas_amarillas % 2 == 0):
                eq_local.suspendido = True
            if eq_visitante.tarjetas_rojas > 0 or (eq_visitante.tarjetas_amarillas > 0 and eq_visitante.tarjetas_amarillas % 2 == 0):
                eq_visitante.suspendido = True

            # OPERACION DE COLA: sacamos el partido del frente (dequeue)
            cola_partidos.pop(0)

            # Limpiamos y deshabilitamos los campos
            self.ent_gl.delete(0, "end")
            self.ent_gv.delete(0, "end")
            self.ent_pl.delete(0, "end")
            self.ent_pv.delete(0, "end")
            self.ent_al.delete(0, "end")
            self.ent_av.delete(0, "end")
            self.ent_rl.delete(0, "end")
            self.ent_rv.delete(0, "end")
            
            self.ent_gl.config(state="disabled")
            self.ent_gv.config(state="disabled")
            self.ent_pl.config(state="disabled")
            self.ent_pv.config(state="disabled")
            self.ent_al.config(state="disabled")
            self.ent_av.config(state="disabled")
            self.ent_rl.config(state="disabled")
            self.ent_rv.config(state="disabled")
            
            self.btn_registrar.config(state="disabled")
            self.btn_suspender.config(state="disabled")
            self.btn_reanudar.config(state="disabled")
            self.lbl_vs.config(text="Seleccione un partido de la cola de arriba")
            self.partido_seleccionado = None

            self.actualizar_tabla_cola()
            messagebox.showinfo("Exito", "Resultado registrado y partido removido de la cola.")
            guardar_datos()  # guardamos cambios en el torneo
        else:
            messagebox.showerror("Error", mensaje)

    def suspender_partido(self):
        if self.partido_seleccionado:
            self.partido_seleccionado.suspender()   # metodo de la clase partido
            self.actualizar_tabla_cola()
            messagebox.showinfo("Estado", "Partido marcado como SUSPENDIDO.")
            guardar_datos()  # guardamos cambios en el torneo

    def reanudar_partido(self):
        if self.partido_seleccionado:
            self.partido_seleccionado.reanudar()    # metodo de la clase partido
            self.actualizar_tabla_cola()
            messagebox.showinfo("Estado", "Partido marcado como REPROGRAMADO.")
            guardar_datos()  # guardamos cambios en el torneo


# PANTALLA 3: EMISION DE INFORMES (5 informes)

class PantallaInformes:
    def __init__(self, contenedor, app):
        self.contenedor = contenedor
        self.app = app

        # Apilamos solo si no estamos ya en INFORMES
        if len(historial_pantallas) == 0 or historial_pantallas[len(historial_pantallas) - 1] != "INFORMES":
            historial_pantallas.append("INFORMES")

        self.app.crear_encabezado(self.contenedor)

        # Barra de botones para elegir el informe
        f_barra = tk.Frame(self.contenedor, bg="#651765", pady=6)
        f_barra.pack(fill="x")

        tk.Button(f_barra, text="INF 1\nPartidos x Fecha",
                  width=14, bg="#cb3ba9", fg="white",
                  command=self.mostrar_informe1).grid(row=0, column=0, padx=4)

        tk.Button(f_barra, text="INF 2\nPosiciones Grupo",
                  width=14, bg="#cb3ba9", fg="white",
                  command=self.mostrar_informe2).grid(row=0, column=1, padx=4)

        tk.Button(f_barra, text="INF 3\nHistorial Equipo",
                  width=14, bg="#cb3ba9", fg="white",
                  command=self.mostrar_informe3).grid(row=0, column=2, padx=4)

        tk.Button(f_barra, text="INF 4\nProximo Partido",
                  width=14, bg="#cb3ba9", fg="white",
                  command=self.mostrar_informe4).grid(row=0, column=3, padx=4)

        tk.Button(f_barra, text="INF 5\nClasif. General",
                  width=14, bg="#cb3ba9", fg="white",
                  command=self.mostrar_informe5).grid(row=0, column=4, padx=4)

        tk.Button(f_barra, text="⬅ Volver",
                  width=10, bg="#6a0c43", fg="white",
                  font=("Arial", 10, "bold"),
                  command=self.app.volver_atras).grid(row=0, column=5, padx=20)

        # Zona donde se renderiza el informe seleccionado
        self.f_zona = tk.Frame(self.contenedor, bg="#681345")
        self.f_zona.pack(fill="both", expand=True, padx=10, pady=10)

        # Mostramos el informe 1 por defecto
        self.mostrar_informe1()

    def limpiar_zona(self):
        # Borramos el contenido anterior del area de informes
        for widget in self.f_zona.winfo_children():
            widget.destroy()

    # INFORME 1: partidos de una fecha especifica
    def mostrar_informe1(self):
        self.limpiar_zona()

        tk.Label(self.f_zona,
                 text="INFORME 1 – PARTIDOS POR FECHA",
                 bg="#700a3f", fg="#ffffff",
                 font=("Arial", 12, "bold")).pack(anchor="w", pady=5)

        # Fila de busqueda
        f_busq = tk.Frame(self.f_zona, bg="#700a3f")
        f_busq.pack(anchor="w", pady=5)

        tk.Label(f_busq, text="Fecha (AAAA-MM-DD):", bg="#700a3f", fg="white").pack(side="left", padx=5)
        ent_fecha = tk.Entry(f_busq, width=14)
        ent_fecha.pack(side="left", padx=5)

        # Tabla de resultados
        tabla = ttk.Treeview(self.f_zona,
                              columns=("Hora", "Local", "Visitante", "Lugar", "Estado", "Resultado"),
                              show="headings")
        for col, ancho in [("Hora", 60), ("Local", 110), ("Visitante", 110), ("Lugar", 180), ("Estado", 100), ("Resultado", 120)]:
            tabla.heading(col, text=col)
            tabla.column(col, width=ancho, anchor="center")

        # Scrollbar vertical para la tabla
        scroll = tk.Scrollbar(self.f_zona, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll.set)
        tabla.pack(side="left", fill="both", expand=True, pady=10)
        scroll.pack(side="right", fill="y", pady=10)

        def buscar():
            # Limpiamos la tabla antes de buscar
            for item in tabla.get_children():
                tabla.delete(item)
            fecha_b = ent_fecha.get().strip()
            encontrados = 0
            for p in torneo_actual.partidos:
                if p.fecha == fecha_b:
                    encontrados += 1
                    resultado = str(p.goles1) + " - " + str(p.goles2)
                    if p.penales1 > 0 or p.penales2 > 0:
                        resultado += " (Pen: " + str(p.penales1) + "-" + str(p.penales2) + ")"
                    tabla.insert("", "end",
                                  values=(p.hora, p.identificador1, p.identificador2,
                                          p.lugar, p.estado, resultado))
            if encontrados == 0:
                messagebox.showinfo("Sin resultados", "No hay partidos para la fecha ingresada.")

        tk.Button(f_busq, text="Buscar",
                  bg="#cb3ba9", fg="white",
                  command=buscar).pack(side="left", padx=8)

    # INFORME 2: tabla de posiciones de un grupo
    def mostrar_informe2(self):
        self.limpiar_zona()

        tk.Label(self.f_zona,
                 text="INFORME 2 – TABLA DE POSICIONES DE UN GRUPO",
                 bg="#681345", fg="#ffffff",
                 font=("Arial", 12, "bold")).pack(anchor="w", pady=5)

        f_ctrl = tk.Frame(self.f_zona, bg="#A43C79")
        f_ctrl.pack(anchor="w", pady=5)

        tk.Label(f_ctrl, text="Grupo:", bg="#891D5C", fg="white").pack(side="left", padx=5)
        var_g = tk.StringVar(f_ctrl)
        var_g.set("A")
        opciones = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
        tk.OptionMenu(f_ctrl, var_g, *opciones).pack(side="left", padx=5)

        # Tabla con columnas de estadisticas
        tabla = ttk.Treeview(self.f_zona,
                              columns=("Pos", "Pais", "PJ", "G", "E", "P", "GF", "GC", "DG", "Pts"),
                              show="headings")
        for col, ancho in [("Pos", 40), ("Pais", 150), ("PJ", 45), ("G", 40),
                            ("E", 40), ("P", 40), ("GF", 45), ("GC", 45), ("DG", 50), ("Pts", 50)]:
            tabla.heading(col, text=col)
            tabla.column(col, width=ancho, anchor="center")
        tabla.column("Pais", anchor="w")
        tabla.pack(fill="both", expand=True, pady=10)

        def consultar():
            for item in tabla.get_children():
                tabla.delete(item)
            # Llamamos al metodo tabla_posiciones del compañero 1 (usa bubble sort)
            lista = torneo_actual.tabla_posiciones(var_g.get())
            pos = 1
            for eq in lista:
                dg = eq.goles_a - eq.goles_c
                tabla.insert("", "end",
                              values=(pos, eq.pais, eq.total_p, eq.ganados,
                                      eq.empate, eq.perdidos,
                                      eq.goles_a, eq.goles_c, dg, eq.puntos))
                pos += 1

        tk.Button(f_ctrl, text="Consultar",
                  bg="#cb3ba9", fg="white",
                  command=consultar).pack(side="left", padx=8)
        consultar()   # cargamos el grupo A por defecto al abrir

    # INFORME 3: historial de partidos de un equipo
    def mostrar_informe3(self):
        self.limpiar_zona()

        tk.Label(self.f_zona,
                 text="INFORME 3 – HISTORIAL Y AVANCE DE UN EQUIPO",
                 bg="#891D5C", fg="#ffffff",
                 font=("Arial", 12, "bold")).pack(anchor="w", pady=5)

        # Armamos la lista de paises para el desplegable
        lista_paises = []
        for eq in torneo_actual.equipos:
            lista_paises.append(eq.pais)

        if len(lista_paises) == 0:
            tk.Label(self.f_zona,
                     text="No hay equipos registrados en el sistema.",
                     fg="red", bg="#891D5C").pack()
            return

        f_ctrl = tk.Frame(self.f_zona, bg="#681345")
        f_ctrl.pack(anchor="w", pady=5)

        tk.Label(f_ctrl, text="Equipo:", bg="#681345", fg="black").pack(side="left", padx=5)
        var_e = tk.StringVar(f_ctrl)
        var_e.set(lista_paises[0])
        tk.OptionMenu(f_ctrl, var_e, *lista_paises).pack(side="left", padx=5)

        # Caja de texto para mostrar el historial
        txt = tk.Text(self.f_zona, bg="#681345", fg="white",
                       font=("Courier", 10), state="disabled")
        scroll = tk.Scrollbar(self.f_zona, orient="vertical", command=txt.yview)
        txt.configure(yscrollcommand=scroll.set)
        txt.pack(side="left", fill="both", expand=True, pady=10)
        scroll.pack(side="right", fill="y", pady=10)

        def ver_historial():
            # Habilitamos para escribir, borramos el contenido anterior
            txt.config(state="normal")
            txt.delete("1.0", "end")

            nombre = var_e.get()
            eq_obj = None
            for eq in torneo_actual.equipos:
                if eq.pais == nombre:
                    eq_obj = eq

            if eq_obj:
                txt.insert("end", "HISTORIAL: " + eq_obj.pais.upper() +
                            "  (" + eq_obj.abreviatura + ")\n")
                txt.insert("end", "=" * 55 + "\n\n")

                hay_partidos = False
                for p in torneo_actual.partidos:
                    if (p.identificador1 == eq_obj.identificador or
                            p.identificador2 == eq_obj.identificador):
                        if p.terminado:
                            hay_partidos = True
                            marcador = str(p.goles1) + " - " + str(p.goles2)
                            txt.insert("end",
                                        "Fecha: " + p.fecha +
                                        "  |  " + p.identificador1 +
                                        "  " + marcador + "  " +
                                        p.identificador2 +
                                        "  |  " + p.lugar + "\n")

                if not hay_partidos:
                    txt.insert("end", "Sin partidos jugados registrados.\n")
                
                txt.insert("end", "\n" + "-" * 55 + "\n")
                txt.insert("end", f"Tarjetas Amarillas: {eq_obj.tarjetas_amarillas}\n")
                txt.insert("end", f"Tarjetas Rojas: {eq_obj.tarjetas_rojas}\n")
                estado = "Suspendido" if eq_obj.suspendido else "Activo"
                txt.insert("end", f"Estado del Equipo: {estado}\n")

                txt.insert("end", "\n" + "=" * 55 + "\n")
                txt.insert("end", "ESTADO DE AVANCE: " + eq_obj.avance + "\n")

            # Deshabilitamos para que no se pueda editar
            txt.config(state="disabled")

        tk.Button(f_ctrl, text="Ver Historial",
                  bg="#cb3ba9", fg="white",
                  command=ver_historial).pack(side="left", padx=8)
        ver_historial()   # cargamos el primer equipo por defecto

# #INFORME 4: proximo partido de un equipo desde una fecha
    def mostrar_informe4(self):
        self.limpiar_zona()

        tk.Label(self.f_zona,
                 text="INFORME 4 – PROXIMO PARTIDO DE UN EQUIPO",
                 bg="#A43C79", fg="#ffffff",
                 font=("Arial", 12, "bold")).pack(anchor="w", pady=5)

        lista_paises = []
        for eq in torneo_actual.equipos:
            lista_paises.append(eq.pais)

        if len(lista_paises) == 0:
            tk.Label(self.f_zona,
                     text="No hay equipos registrados.",
                     fg="red", bg="#A43C79").pack()
            return

        f_ctrl = tk.Frame(self.f_zona, bg="#A43C79")
        f_ctrl.pack(anchor="w", pady=5)

        tk.Label(f_ctrl, text="Equipo:", bg="#A43C79", fg="white").grid(row=0, column=0, padx=5)
        var_e = tk.StringVar(f_ctrl)
        var_e.set(lista_paises[0])
        tk.OptionMenu(f_ctrl, var_e, *lista_paises).grid(row=0, column=1, padx=5)

        tk.Label(f_ctrl, text="Desde fecha (AAAA-MM-DD):", bg="#A43C79", fg="white").grid(row=0, column=2, padx=5)
        ent_fecha = tk.Entry(f_ctrl, width=14)
        ent_fecha.insert(0, "2026-06-11")   # fecha de inicio del mundial como default
        ent_fecha.grid(row=0, column=3, padx=5)

        # CONTENEDOR PRINCIPAL DEL RESULTADO: Cambiamos el Label único por un Frame contenedor
        f_resultado = tk.Frame(self.f_zona, bg="#A43C79", relief="solid", bd=1)
        f_resultado.pack(fill="x", pady=20, padx=10)

        # Creamos los 3 sub-componentes internos (Banderas + Texto)
        lbl_bandera_izq = tk.Label(f_resultado, bg="#A43C79")
        lbl_bandera_izq.pack(side="left", padx=30)

        lbl_res = tk.Label(f_resultado, text="", bg="#A43C79", fg="white",
                           font=("Arial", 11), justify="left", padx=10, pady=20)
        lbl_res.pack(side="left", expand=True, fill="both")

        lbl_bandera_der = tk.Label(f_resultado, bg="#A43C79")
        lbl_bandera_der.pack(side="right", padx=30)

        # Diccionario auxiliar para no perder la referencia de las 2 imágenes actuales de la pantalla
        self.img_cache_inf4 = {}

        def buscar_proximo():
            nombre  = var_e.get()
            fecha_b = ent_fecha.get().strip()

            # Buscamos el objeto equipo por pais
            eq_obj = None
            for eq in torneo_actual.equipos:
                if eq.pais == nombre:
                    eq_obj = eq

            if not eq_obj:
                return

            # Buscamos el partido mas cercano a la fecha ingresada que no este terminado
            proximo = None
            for p in torneo_actual.partidos:
                es_del_equipo = (p.identificador1 == eq_obj.identificador or
                                 p.identificador2 == eq_obj.identificador)
                es_futuro     = (not p.terminado and p.fecha >= fecha_b)

                if es_del_equipo and es_futuro:
                    if proximo is None or p.fecha < proximo.fecha:
                        proximo = p

            # Limpiamos imágenes anteriores del caché de este informe
            lbl_bandera_izq.config(image="")
            lbl_bandera_der.config(image="")
            self.img_cache_inf4.clear()

            if proximo:
                texto = ("PROXIMO PARTIDO ENCONTRADO\n\n" +
                         "Fecha:  " + proximo.fecha + "    Hora: " + proximo.hora + "\n" +
                         "Lugar:  " + proximo.lugar + "\n" +
                         "Partido: " + proximo.identificador1 + "  vs  " + proximo.identificador2 + "\n" +
                         "Estado: " + proximo.estado.upper())
                lbl_res.config(text=texto, fg="#ffffff")

                # Buscamos los objetos de ambos equipos usando sus identificadores para conocer sus nombres de país
                eq1 = torneo_actual.busqueda(proximo.identificador1)
                eq2 = torneo_actual.busqueda(proximo.identificador2)

                # --- CARGA DE BANDERA IZQUIERDA (Equipo 1) ---
                if isinstance(eq1, equipo):
                    ruta_izq = os.path.join("banderas", eq1.pais.upper() + ".png")
                    if os.path.exists(ruta_izq):
                        try:
                            img_i = Image.open(ruta_izq).resize((80, 50), Image.Resampling.LANCZOS)
                            foto_i = ImageTk.PhotoImage(img_i)
                            self.img_cache_inf4["izq"] = foto_i
                            lbl_bandera_izq.config(image=foto_i)
                        except Exception:
                            pass

                # --- CARGA DE BANDERA DERECHA (Equipo 2) ---
                if isinstance(eq2, equipo):
                    ruta_der = os.path.join("banderas", eq2.pais.upper() + ".png")
                    if os.path.exists(ruta_der):
                        try:
                            img_d = Image.open(ruta_der).resize((80, 50), Image.Resampling.LANCZOS)
                            foto_d = ImageTk.PhotoImage(img_d)
                            self.img_cache_inf4["der"] = foto_d
                            lbl_bandera_der.config(image=foto_d)
                        except Exception:
                            pass
            else:
                lbl_res.config(text="Sin partidos programados desde la fecha indicada.", fg="#ffffff")

        tk.Button(f_ctrl, text="Buscar Proximo",
                  bg="#b9369a", fg="white",
                  command=buscar_proximo).grid(row=0, column=4, padx=12)
        
        buscar_proximo()   # Carga el resultado por defecto al iniciar la pantalla

    # INFORME 5: clasificacion general de todos los grupos

    def mostrar_informe5(self):
        self.limpiar_zona()

        tk.Label(self.f_zona,
                text="INFORME 5 – CLASIFICACION GENERAL (todos los grupos)",
                bg="#7D1351", fg="#ffffff",
                font=("Arial", 12, "bold")).pack(anchor="w", pady=5)

        f_scroll = tk.Frame(self.f_zona, bg="#681345")
        f_scroll.pack(fill="both", expand=True)

        canvas = tk.Canvas(f_scroll, bg="#681345", highlightthickness=0)
        scrollbar = tk.Scrollbar(f_scroll, orient="vertical", command=canvas.yview)

        f_interno = tk.Frame(canvas, bg="#AA407E")
        f_interno.bind("<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=f_interno, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        grupos = ["A","B","C","D","E","F","G","H","I","J","K","L"]

        # Mantener referencias de imágenes
        self.img_refs = {}

        for g in grupos:
            lista_grupo = torneo_actual.tabla_posiciones(g)
            if len(lista_grupo) > 0:
                f_caja = tk.LabelFrame(f_interno,
                                    text="  GRUPO " + g + "  ",
                                    bg="#FFA9EC", fg="#ffffff",
                                    font=("Arial", 11, "bold"),
                                    padx=10, pady=5)
                f_caja.pack(fill="x", pady=8, padx=5)

                columnas = [("Pos",5),("Pais",22),("PJ",5),("G",5),
                            ("E",5),("P",5),("GF",5),("GC",5),("DG",6),("Pts",6)]
                for col_i,(texto,ancho) in enumerate(columnas):
                    tk.Label(f_caja,text=texto,
                            bg="#EE7FC0",fg="#ffffff",
                            font=("Arial",9,"bold"),
                            width=ancho).grid(row=0,column=col_i)

                pos = 1
                for eq in lista_grupo:
                    dg = eq.goles_a - eq.goles_c
                    datos_fila = [str(pos), eq.pais, str(eq.total_p), str(eq.ganados),
                                str(eq.empate), str(eq.perdidos),
                                str(eq.goles_a), str(eq.goles_c), str(dg), str(eq.puntos)]
                    anchos_fila = [5,22,5,5,5,5,5,5,6,6]

                    for col_i,(dato,ancho) in enumerate(zip(datos_fila,anchos_fila)):
                        color = "#ffffff" if col_i == 9 else "white"
                        negrita = "bold" if col_i == 9 else "normal"

                        if col_i == 1:  # columna País → bandera + texto
                            # Creamos un contenedor del tamaño exacto de la columna para alinear adentro
                            f_pais = tk.Frame(f_caja, bg="#994E7A", width=158, height=22)
                            f_pais.grid_propagate(False) # Evita que el frame se encoja
                            f_pais.grid(row=pos, column=col_i, sticky="nsew")

                            try:
                                # Forzamos la búsqueda de la imagen en mayúsculas (.upper())
                                ruta = os.path.join("banderas", eq.pais.upper() + ".png")
                                img = Image.open(ruta).resize((25,15), Image.Resampling.LANCZOS)
                                foto = ImageTk.PhotoImage(img)
                                self.img_refs[eq.pais] = foto
                                
                                # Colocamos la bandera alineada a la izquierda dentro del sub-frame
                                lbl_bandera = tk.Label(f_pais, image=foto, bg="#994E7A")
                                lbl_bandera.pack(side="left", padx=(15, 5))
                                
                                # Colocamos el texto del País al lado de la bandera
                                lbl_texto = tk.Label(f_pais, text=dato, bg="#994E7A", fg=color,
                                                     font=("Arial", 9, negrita))
                                lbl_texto.pack(side="left")
                            except Exception:
                                # Si la imagen falla o no existe, solo muestra el texto centrado/alineado
                                lbl_texto = tk.Label(f_pais, text=dato, bg="#994E7A", fg=color,
                                                     font=("Arial", 9, negrita))
                                lbl_texto.pack(expand=True)
                        else:
                            tk.Label(f_caja,text=dato,
                                    bg="#994E7A",fg=color,
                                    font=("Arial",9,negrita),
                                    width=ancho).grid(row=pos,column=col_i)
                    pos += 1

# ARRANQUE DE LA APLICACION
if __name__ == "__main__":
    cargar_datos() # Cargamos los datos guardados ANTES de construir la interfaz

    raiz_tk = tk.Tk() # Se crea la ventana raiz de Tkinter
    app_sistema = Aplicacion(raiz_tk) # Creamos la aplicacion pasandole la ventana raiz

    raiz_tk.mainloop() # Iniciamos el bucle principal que mantiene la ventana abierta