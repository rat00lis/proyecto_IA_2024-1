import os
import matplotlib.pyplot as plt
import numpy as np  # Importar numpy

# Asegurarse de que el directorio de resultados existe
results_dir = './results'
os.makedirs(results_dir, exist_ok=True)

# Datos del método genético, Montecarlo 50 y 100 rollouts
# Datos del método genético
genetico_data = {
    128: 42,
    64: 25,
    32: 9,
    512: 2,
    256: 21,
    16: 1,
    1024: 0,
    2048: 0
}

# Datos del método Montecarlo para 50 rollouts
montecarlo_50 = {
    2048: 18,
    1024: 55,
    512: 26,
    256: 1,
    16: 0,
    32: 0,
    64: 0,
    128: 0
}

# Datos del método Montecarlo para 100 rollouts
montecarlo_100 = {
    2048: 30,
    1024: 57,
    512: 13,
    256: 0,
    16: 0,
    32: 0,
    64: 0,
    128: 0
}

# Lista de métodos y sus datos
metodos = [
    ("Genetico", genetico_data),
    ("Montecarlo 50 Rollouts", montecarlo_50),
    ("Montecarlo 100 Rollouts", montecarlo_100)
]

# Generar un gráfico para cada método
for nombre_metodo, datos in metodos:
    # Ordenar los datos por "Max Cell Value"
    datos_ordenados = dict(sorted(datos.items()))
    
    fig = plt.figure(figsize=(10, 6))
    
    # Generar posiciones equidistantes para las barras
    posiciones = np.arange(len(datos_ordenados))
    
    plt.bar(posiciones, datos_ordenados.values(), width=0.8)  # Usar posiciones para las barras
    plt.title(f'Frecuencia de Valores Máximos de Celdas - {nombre_metodo}')
    plt.xlabel('Valor Máximo de Celda')
    plt.ylabel('Frecuencia')
    
    # Establecer las etiquetas del eje X manualmente
    plt.xticks(posiciones, datos_ordenados.keys())
    
    # Guardar gráfico
    plt.savefig(f'{results_dir}/grafico_{nombre_metodo.replace(" ", "_")}.png')
    plt.close()