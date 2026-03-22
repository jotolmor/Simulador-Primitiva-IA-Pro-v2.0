import os
import sys
import subprocess

# --- AUTO-INSTALACIÓN ---
def instalar_dependencias():
    librerias = ["pandas", "openpyxl", "scikit-learn"]
    for lib in librerias:
        try:
            __import__(lib)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

instalar_dependencias()

import pandas as pd
import random
import tkinter as tk
from sklearn.cluster import KMeans

ARCHIVO_CSV = 'historico_limpio.csv'

def cargar_y_analizar():
    if not os.path.exists(ARCHIVO_CSV): return None, None, None
    try:
        df = pd.read_csv(ARCHIVO_CSV)
        cols = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6']
        for c in cols: df[c] = pd.to_numeric(df[c], errors='coerce')
        df = df.dropna(subset=cols)
        todas = pd.concat([df[c] for c in cols]).astype(float)
        frec = todas.value_counts().sort_index()
        datos_ia = pd.DataFrame({'Numero': frec.index.astype(int), 'Frecuencia': frec.values.astype(float)})
        return df, datos_ia, {"calientes": frec.nlargest(5).index.tolist(), "frios": frec.nsmallest(5).index.tolist()}
    except: return None, None, None

def generar_ia_inteligente(df, d_ia):
    # 1. Calculamos la probabilidad de cada reintegro (0-9) basado en el histórico
    frec_reintegro = df['Reintegro'].value_counts(normalize=True).sort_index()
    opciones_reintegro = frec_reintegro.index.tolist()
    pesos_reintegro = frec_reintegro.values.tolist()

    for _ in range(200):
        # Lógica de Clustering para los números principales
        km = KMeans(n_clusters=6, n_init=5)
        d_ia['Cluster'] = km.fit_predict(d_ia[['Frecuencia']].values)
        
        apuesta = sorted(list(set([int(random.choice(d_ia[d_ia['Cluster'] == i]['Numero'].tolist())) for i in range(6)])))
        
        while len(apuesta) < 6:
            n = random.randint(1, 49)
            if n not in apuesta: apuesta.append(n); apuesta.sort()
        
        suma = sum(apuesta)
        pares = len([x for x in apuesta if x % 2 == 0])
        impares = 6 - pares
        
        # Filtros de Suma y Paridad
        if (130 <= suma <= 210) and (1 <= pares <= 5):
            # ELEGIMOS REINTEGRO DINÁMICO:
            # Usamos random.choices con pesos para que los que más salen tengan más probabilidad,
            # pero que pueda salir cualquiera del 0 al 9.
            r_elegido = random.choices(opciones_reintegro, weights=pesos_reintegro, k=1)[0]
            
            return apuesta, int(r_elegido), suma, f"{pares}P/{impares}I"
            
    # Fallback por si no encuentra combinación en 200 intentos
    r_random = random.choices(opciones_reintegro, weights=pesos_reintegro, k=1)[0]
    return apuesta, int(r_random), sum(apuesta), f"{pares}P/{impares}I"

class AppPro:
    def __init__(self, root):
        self.root = root
        root.title("Primitiva IA Pro - v2.0")
        root.geometry("800x850")
        root.configure(bg="#0F0F0F")
        
        # Título Superior
        tk.Label(root, text="SISTEMA DE PREDICCIÓN IA", font=("Consolas", 22, "bold"), 
                 bg="#0F0F0F", fg="#00FF41").pack(pady=25)

        # Configuración del área de texto (Textbox)
        # Ajustamos el ancho (width) y el espaciado interno (padx)
        self.txt = tk.Text(root, height=25, width=80, font=("Consolas", 11), 
                           bg="#1A1A1A", fg="#00FF41", borderwidth=0, 
                           padx=20, pady=20, highlightthickness=1, highlightbackground="#333")
        
        # DEFINICIÓN DEL TAG DE CENTRADO (Esto es la clave)
        self.txt.tag_configure("center", justify='center')
        self.txt.pack(pady=10)
        
        self.df, self.d_ia, self.stats = cargar_y_analizar()
        self.mostrar_inicio()

        # Panel de Controles
        ctrl = tk.Frame(root, bg="#0F0F0F")
        ctrl.pack(pady=20)
        
        tk.Label(ctrl, text="Nº DE JUGADAS:", bg="#0F0F0F", fg="white", 
                 font=("Consolas", 11)).grid(row=0, column=0, padx=10)
        
        self.ent = tk.Entry(ctrl, width=6, justify="center", font=("Consolas", 16), 
                            bg="#333", fg="white", borderwidth=0)
        self.ent.insert(0, "5")
        self.ent.grid(row=0, column=1)
        
        tk.Button(root, text="[ GENERAR APUESTAS OPTIMIZADAS ]", font=("Consolas", 12, "bold"), 
                  bg="#00FF41", fg="black", command=self.go, activebackground="#00CC33", 
                  cursor="hand2", padx=25, pady=10).pack(pady=15)

    def mostrar_inicio(self):
        """Dibuja la cabecera de estadísticas de forma centrada."""
        self.txt.delete(1.0, tk.END)
        if self.df is not None:
            cabecera = (
                f"ESTADO: BASE DE DATOS CONECTADA\n"
                f"REGISTROS ANALIZADOS: {len(self.df)} SORTEOS\n"
                f"{'-'*60}\n"
                f"NÚMEROS CALIENTES: {self.stats['calientes']}\n"
                f"NÚMEROS FRÍOS: {self.stats['frios']}\n"
                f"{'='*60}\n\n"
            )
            self.txt.insert(tk.END, cabecera, "center")
        else:
            self.txt.insert(tk.END, "❌ ERROR: No se detecta el histórico.", "center")

    def go(self):
        if self.df is None: return
        try:
            # 1. Obtenemos la cantidad de jugadas
            n_input = self.ent.get()
            if not n_input.isdigit(): return
            n = int(n_input)

            # 2. Limpiamos TODO y redibujamos la cabecera para que la Jugada 01 baje
            self.mostrar_inicio() 
            
            # 3. Forzamos un pequeño espacio después de los ====
            self.txt.insert(tk.END, "\n")

            # 4. Generamos e insertamos las apuestas una a una
            for i in range(n):
                c, r, s, p = generar_ia_inteligente(self.df, self.d_ia)
                
                # Formateo ultra-preciso para que no se mueva el centrado
                s_nums = "  ".join([f"{x:02d}" for x in c])
                linea_apuesta = f"JUGADA {i+1:02d} |  {s_nums}  | R:{r} | Σ:{s} | {p}\n"
                
                # Insertamos con el tag 'center'
                self.txt.insert(tk.END, linea_apuesta, "center")
            
            # 5. Mensaje de cierre
            self.txt.insert(tk.END, f"\n{'*'*20} ANÁLISIS FINALIZADO {'*'*20}\n", "center")
            
            # 6. Scroll automático al final
            self.txt.see(tk.END)
            
        except Exception as e:
            print(f"Error en ejecución: {e}")
if __name__ == "__main__":
    root = tk.Tk()
    app = AppPro(root)
    root.mainloop()