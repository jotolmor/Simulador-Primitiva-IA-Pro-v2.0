import os
import sys
import subprocess

# --- AUTO-INSTALACIÓN ---
def instalar_dependencias():
    for lib in ["pandas", "openpyxl", "scikit-learn"]:
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
        columnas = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6']
        for col in columnas: df[col] = pd.to_numeric(df[col], errors='coerce')
        df = df.dropna(subset=columnas)
        todas = pd.concat([df[c] for c in columnas]).astype(float)
        frec = todas.value_counts().sort_index()
        datos_ia = pd.DataFrame({'Numero': frec.index.astype(int), 'Frecuencia': frec.values.astype(float)})
        return df, datos_ia, {"calientes": frec.nlargest(5).index.tolist(), "frios": frec.nsmallest(5).index.tolist()}
    except: return None, None, None

def generar_ia_inteligente(df, d_ia):
    for _ in range(100):
        km = KMeans(n_clusters=6, n_init=5)
        d_ia['Cluster'] = km.fit_predict(d_ia[['Frecuencia']].values)
        apuesta = sorted(list(set([int(random.choice(d_ia[d_ia['Cluster'] == i]['Numero'].tolist())) for i in range(6)])))
        while len(apuesta) < 6:
            n = random.randint(1, 49)
            if n not in apuesta: apuesta.append(n); apuesta.sort()
        suma = sum(apuesta)
        if 130 <= suma <= 210: return apuesta, int(df['Reintegro'].mode()[0]), suma
    return apuesta, int(df['Reintegro'].mode()[0]), sum(apuesta)

class AppPro:
    def __init__(self, root):
        self.root = root
        root.title("Primitiva IA Pro")
        root.geometry("750x850")
        root.configure(bg="#0F0F0F")
        
        tk.Label(root, text="SISTEMA DE PREDICCIÓN IA", font=("Consolas", 20, "bold"), bg="#0F0F0F", fg="#00FF41").pack(pady=20)
        
        # Textbox con configuración de centrado
        self.txt = tk.Text(root, height=25, width=75, font=("Consolas", 11), bg="#1A1A1A", fg="#00FF41", borderwidth=0, padx=10, pady=20)
        # CREAMOS EL TAG DE CENTRADO
        self.txt.tag_configure("center", justify='center')
        self.txt.pack(pady=10)
        
        self.df, self.d_ia, self.stats = cargar_y_analizar()
        self.mostrar_inicio()

        ctrl = tk.Frame(root, bg="#0F0F0F")
        ctrl.pack(pady=20)
        tk.Label(ctrl, text="CANTIDAD DE APUESTAS:", bg="#0F0F0F", fg="white", font=("Consolas", 10)).grid(row=0, column=0, padx=10)
        self.ent = tk.Entry(ctrl, width=5, justify="center", font=("Consolas", 16), bg="#333", fg="white", borderwidth=0)
        self.ent.insert(0, "5")
        self.ent.grid(row=0, column=1)
        
        tk.Button(root, text="[ EJECUTAR ANÁLISIS ]", font=("Consolas", 12, "bold"), bg="#00FF41", fg="black", command=self.go, cursor="hand2", padx=20).pack(pady=10)

    def mostrar_inicio(self):
        self.txt.delete(1.0, tk.END)
        if self.df is not None:
            texto = (f"ESTADO: CONECTADO - {len(self.df)} SORTEOS\n"
                     f"NÚMEROS MÁS FRECUENTES: {self.stats['calientes']}\n"
                     f"NÚMEROS MENOS FRECUENTES: {self.stats['frios']}\n"
                     f"{'='*60}\n\n")
            self.txt.insert(tk.END, texto)
            self.txt.tag_add("center", "1.0", "end")
        else:
            self.txt.insert(tk.END, "ERROR: No se encontró el archivo 'historico_limpio.csv'", "center")

    def go(self):
        if self.df is None: return
        try:
            n = int(self.ent.get())
            self.txt.delete(6.0, tk.END) # Mantener cabecera
            for i in range(n):
                c, r, s = generar_ia_inteligente(self.df, self.d_ia)
                s_nums = "  ".join([f"{x:02d}" for x in c])
                res = f"JUGADA {i+1:02d} | {s_nums} | R:{r} (Σ {s})\n"
                self.txt.insert(tk.END, res)
            
            self.txt.insert(tk.END, f"\n\n--- ANÁLISIS FINALIZADO ---")
            # APLICAMOS CENTRADO A TODO EL CONTENIDO
            self.txt.tag_add("center", "1.0", "end")
        except: pass

if __name__ == "__main__":
    root = tk.Tk()
    app = AppPro(root)
    root.mainloop()