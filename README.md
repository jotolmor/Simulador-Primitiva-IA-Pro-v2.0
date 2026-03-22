# 🎰 Simulador Primitiva IA Pro v2.0

Este software avanzado utiliza **Machine Learning** y **filtros de exclusión estadística** para generar combinaciones de lotería basadas en el histórico real (1986-2026).

## 🚀 Nuevas Funciones de Inteligencia

### 1. El Algoritmo de Clustering (K-Means)
La IA divide los 49 números en 6 "familias" según su frecuencia. El programa elige un representante de cada familia, garantizando que tu apuesta tenga números "Calientes" (frecuentes) y "Fríos" (que están por salir), evitando jugadas descompensadas.

### 2. La Regla de la Suma (Σ)
Estadísticamente, el **75% de los sorteos ganadores** tienen una suma total de sus 6 números entre **130 y 210**. El simulador descarta automáticamente cualquier combinación que se salga de este rango de probabilidad.



[Image of the bell curve normal distribution]


### 3. Filtro de Paridad (NUEVO)
Es extremadamente raro (menos del 2% de los casos) que una combinación ganadora esté formada solo por números pares o solo por impares. 
- **Optimización**: El simulador ahora obliga a que cada apuesta tenga una mezcla equilibrada (ej. 3 pares y 3 impares, o 4 y 2). Esto elimina miles de combinaciones "feas" que casi nunca salen en el bombo real.



## 🛠️ Instalación Rápida
1. Instala Python (marca "Add to PATH").
2. Pon `super_creador.py` y `historico_limpio.csv` en la misma carpeta.
3. Ejecuta el script. Se instalarán automáticamente las librerías necesarias (`pandas`, `scikit-learn`, `openpyxl`).

## 📁 Uso
- Introduce la cantidad de apuestas.
- El sistema te mostrará la combinación, el Reintegro (R), la Suma (Σ) y la distribución de Pares/Impares (P/I).