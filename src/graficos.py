import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import seaborn as sns

def graficar_media_duracion(df, return_fig=False): 
    # Crear el gráfico de barras
    
    fig = plt.figure(figsize=(8, 6))
    plt.bar(df['es_mantenimiento'], df['avg_duracion'], color=['skyblue', 'orange'])

    # Etiquetas y título
    plt.xlabel('Tipo de Incidencia')
    plt.ylabel('Media de Duración (días)')
    plt.title('Media de Duración de Incidencias de Mantenimiento vs No Mantenimiento')

    # Mostrar el gráfico
    if return_fig:
        return fig
    else:
        # Mostrar o guardar el gráfico
        plt.savefig('graficar_media_duracion.png')
        plt.close(fig)



def grafico_boxplot_incidente(df_agrupados, return_fig=False):

    # Asegurarse de que los datos agrupados contengan la columna de tiempos de resolución
    if 'mediana' not in df_agrupados['tipo_incidencia'].columns:
        raise ValueError("Los datos agrupados no contienen la columna 'mediana' para los tiempos de resolución.")
    
    # Extraer los datos necesarios (en este caso la mediana del tiempo trabajado)
    df = df_agrupados['tipo_incidencia']
    
    # Configurar el gráfico
    fig = plt.figure(figsize=(10, 6))
    
    # Dibujar el boxplot usando seaborn
    sns.boxplot(x=df.index, y=df['mediana'], palette='Set2')
    
    # Calcular los percentiles 5% y 90%
    percentil_5 = df['mediana'].quantile(0.05)
    percentil_90 = df['mediana'].quantile(0.90)
    
    # Añadir líneas horizontales para los percentiles 5% y 90%
    plt.axhline(percentil_5, color='red', linestyle='--', label=f'Percentil 5%: {percentil_5:.2f}')
    plt.axhline(percentil_90, color='blue', linestyle='--', label=f'Percentil 90%: {percentil_90:.2f}')
    
    # Títulos y etiquetas
    plt.title('Boxplot de Tiempos de Resolución por Tipo de Incidente')
    plt.xlabel('Tipo de Incidente')
    plt.ylabel('Tiempo de Resolución (horas)')
    plt.legend()
    
    if return_fig:
        return fig
    else:
        # Mostrar o guardar el gráfico
        plt.savefig('grafico_boxplot_incidente.png')
        plt.close(fig)

def mostrar_clientes_criticos(df_agrupados, return_fig=False):
    # Agrupar por 'nombre_cliente' y sumar las incidencias
    df_clientes = df_agrupados['nombre']
    
    # Ordenar los clientes por el número de incidencias en orden descendente
    df_clientes_sorted = df_clientes.sort_values(by='num_incidencias', ascending=False)
    
    # Seleccionar los 5 clientes con más incidencias
    top_5_clientes = df_clientes_sorted.head(5)

    
    # Extraer los datos para la gráfica
    clientes = top_5_clientes['nombre']
    incidencias = top_5_clientes['num_incidencias']
        
    # Crear la gráfica de barras
    fig = plt.figure(figsize=(10, 5))
    plt.barh(clientes, incidencias, color='skyblue')
    plt.xlabel('Número de Incidencias')
    plt.ylabel('Cliente')
    plt.title('Top 5 Clientes con Más Incidencias')
    plt.gca().invert_yaxis()  # Para que el cliente con más incidencias esté en la parte superior
  
    
    if return_fig:
        return fig
    else:
        # Mostrar o guardar el gráfico
        plt.savefig('mostrar_clientes_criticos.png')
        plt.close(fig)

def mostrar_empleados_actuaciones(df_agrupados, return_fig=False):
    # Extraer los datos necesarios
    df_empleados = df_agrupados['nombre']
    
    # Ordenar los empleados por el número de actuaciones en orden descendente
    df_empleados_sorted = df_empleados.sort_values(by='num_contactos', ascending=False)

    # Extraer los datos para la gráfica
    empleados = df_empleados_sorted['nombre']
    actuaciones = df_empleados_sorted['num_contactos']
    
    # Crear la gráfica de barras
    fig = plt.figure(figsize=(10, 5))
    plt.bar(empleados, actuaciones, color='lightcoral')
    plt.xlabel('Empleado')
    plt.ylabel('Número de Actuaciones')
    plt.title('Número de Actuaciones por Empleado')
    plt.xticks(rotation=45)
    if return_fig:
        return fig
    else:
        # Mostrar o guardar el gráfico
        plt.savefig('mostrar_empleados_actuaciones.png')
        plt.close(fig)

def mostrar_actuaciones_por_dia(df_agrupados, return_fig=False):

    # Asegurarse de que la columna de fecha está en formato datetime
    df_agrupados_fecha_cierre = pd.to_datetime(df_agrupados['fecha_cierre']['fecha_cierre'], format="%Y-%m-%d", errors='coerce')
    
    # Extraer el día de la semana (nombre del día)
    df_agrupados_dia_de_la_semana = df_agrupados_fecha_cierre.dt.day_name()
    
    # Extraer num_contactos por dia
    df_agrupados_num_contactos = df_agrupados['fecha_cierre']['num_contactos']

    df_agrupados_full_info = pd.concat([df_agrupados_fecha_cierre, df_agrupados_dia_de_la_semana,df_agrupados_num_contactos], axis=1)
    
    df_agrupados_full_info.columns = ['fecha_cierre', 'dia_de_la_semana','num_contactos']

    resultados = {}

    for index, row in df_agrupados_full_info.iterrows():
        dia = row['dia_de_la_semana']  # Obtener el día de la semana
        num_contactos = row['num_contactos']  # Obtener el número de contactos
        
        # Si el día no está en el diccionario, lo inicializamos con 0
        if dia not in resultados:
            resultados[dia] = 0
        
        # Sumar el número de contactos al día correspondiente
        resultados[dia] += num_contactos

    # Añadir el viernes con un valor de 0 si no está presente
    resultados['Friday'] = 0
    orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    resultados_ordenados = {dia: resultados[dia] for dia in orden_dias if dia in resultados}

    # Crear la gráfica de barras
    fig = plt.figure(figsize=(10, 6))
    plt.bar(resultados_ordenados.keys(), resultados_ordenados.values(), color='lightgreen')
    plt.xlabel('Día de la Semana')
    plt.ylabel('Número de Actuaciones')
    plt.title('Total de Actuaciones por Día de la Semana')
    plt.xticks(rotation=45)  # Rotar las etiquetas del eje x para mejor visualización
    if return_fig:
        return fig
    else:
        # Mostrar o guardar el gráfico
        plt.savefig('mostrar_actuaciones_por_dia.png')
        plt.close(fig)