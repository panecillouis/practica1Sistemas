import sqlite3
import pandas as pd

def obtener_datos_generico():
    conn = sqlite3.connect('sistema_etl.db')
    
    # Número total de muestras (tickets)
    query_total_muestras = """
    SELECT COUNT(*) FROM Tickets;
    """
    total_muestras = pd.read_sql(query_total_muestras, conn).iloc[0, 0]
    
    # Media y desviación estándar del total de incidentes con valoración >= 5
    query_incidentes_valorados = """
    SELECT COUNT(*) as total FROM Tickets WHERE satisfaccion_cliente >= 5;
    """
    incidentes_valorados = pd.read_sql(query_incidentes_valorados, conn)['total'].values[0]
    
    # Media y desviación estándar de incidentes por cliente
    query_incidentes_cliente = """
    SELECT cliente_id, COUNT(*) as total FROM Tickets GROUP BY cliente_id;
    """
    df_incidentes_cliente = pd.read_sql(query_incidentes_cliente, conn)
    media_incidentes_cliente = df_incidentes_cliente['total'].mean()
    std_incidentes_cliente = df_incidentes_cliente['total'].std()
    
    # Media y desviación estándar de horas trabajadas por incidente
    query_horas_incidente = """
    SELECT id_ticket, SUM(tiempo_trabajado) as total_horas FROM Contactos_Empleados_Tickets GROUP BY id_ticket;
    """
    df_horas_incidente = pd.read_sql(query_horas_incidente, conn)
    media_horas_incidente = df_horas_incidente['total_horas'].mean()
    std_horas_incidente = df_horas_incidente['total_horas'].std()
    
    # Valor mínimo y máximo de horas trabajadas por empleados
    query_horas_empleados = """
    SELECT id_empleado, SUM(tiempo_trabajado) as total_horas FROM Contactos_Empleados_Tickets GROUP BY id_empleado;
    """
    df_horas_empleados = pd.read_sql(query_horas_empleados, conn)
    min_horas_empleado = df_horas_empleados['total_horas'].min()
    max_horas_empleado = df_horas_empleados['total_horas'].max()
    
    # Valor mínimo y máximo del tiempo entre apertura y cierre de incidentes
    query_tiempo_incidentes = """
    SELECT id_ticket, 
           (julianday(fecha_cierre) - julianday(fecha_apertura)) * 24 AS tiempo_total
    FROM Tickets;
    """
    df_tiempo_incidentes = pd.read_sql(query_tiempo_incidentes, conn)
    min_tiempo_incidente = df_tiempo_incidentes['tiempo_total'].min()
    max_tiempo_incidente = df_tiempo_incidentes['tiempo_total'].max()
    
    # Valor mínimo y máximo del número de incidentes atendidos por empleado
    query_incidentes_empleado = """
    SELECT id_empleado, COUNT(DISTINCT id_ticket) as total FROM Contactos_Empleados_Tickets GROUP BY id_empleado;
    """
    df_incidentes_empleado = pd.read_sql(query_incidentes_empleado, conn)
    min_incidentes_empleado = df_incidentes_empleado['total'].min()
    max_incidentes_empleado = df_incidentes_empleado['total'].max()
    
    conn.close()
    
    # Crear DataFrame con los resultados
    datos = {
        "Total Muestras": [total_muestras],
        "Total Incidentes Valorados >=5": [incidentes_valorados],
        "Media Incidentes por Cliente": [media_incidentes_cliente],
        "Desviación Incidentes por Cliente": [std_incidentes_cliente],
        "Media Horas por Incidente": [media_horas_incidente],
        "Desviación Horas por Incidente": [std_horas_incidente],
        "Min Horas por Empleado": [min_horas_empleado],
        "Max Horas por Empleado": [max_horas_empleado],
        "Min Tiempo Incidente": [min_tiempo_incidente],
        "Max Tiempo Incidente": [max_tiempo_incidente],
        "Min Incidentes por Empleado": [min_incidentes_empleado],
        "Max Incidentes por Empleado": [max_incidentes_empleado]
    }
    
    df_resultados = pd.DataFrame(datos)
    return df_resultados


import sqlite3
import pandas as pd

def obtener_datos_agrupacion():
    conn = sqlite3.connect('sistema_etl.db')

    query = """
    SELECT 
            e.id_empleado,
            e.nombre,
            t.id_ticket,
            ce.id_contacto,
            ce.tiempo_trabajado,
            e.nivel,
            c.nombre_cliente,
            t.fecha_cierre, 
            t.fecha_apertura,
            t.tipo_incidencia
     FROM 
            Empleados e
     JOIN 
            Contactos_Empleados_Tickets ce ON e.id_empleado = ce.id_empleado
     JOIN 
            Tickets t ON ce.id_ticket = t.id_ticket
     JOIN 
            Clientes c ON t.cliente_id = c.id_cliente
     WHERE 
            t.tipo_incidencia = (SELECT id_tipo FROM Tipos_Incidentes WHERE nombre = 'Fraude');
     """


    df = pd.read_sql(query, conn)
    conn.close()
    tipo = ['nombre', 'nivel', 'nombre_cliente', 'tipo_incidencia', 'fecha_apertura','fecha_cierre']
    agrupacion = {}
    for t in tipo:
       agrupacion_tipo = df.groupby(t).agg(
              num_incidencias=('id_ticket', 'count'),
              num_contactos=('id_contacto', 'count'),
              mediana=('tiempo_trabajado', 'median'),
              media=('tiempo_trabajado', 'mean'),
              varianza=('tiempo_trabajado', 'var'),
              max=('tiempo_trabajado', 'max'),
              min=('tiempo_trabajado', 'min')
       ).reset_index()
       agrupacion[t] = agrupacion_tipo
    return agrupacion


def obtener_datos_mantenimiento():
    conn = sqlite3.connect('sistema_etl.db')

    # Consulta SQL para obtener la cantidad de incidentes y la duración calculada (diferencia entre fecha_cierre y fecha_apertura)
    query = """
    SELECT 
        t.es_mantenimiento,
        COUNT(t.id_ticket) AS num_incidencias,
        AVG(JULIANDAY(t.fecha_cierre) - JULIANDAY(t.fecha_apertura)) AS avg_duracion
    FROM 
        Tickets t
    JOIN 
        Contactos_Empleados_Tickets ce ON t.id_ticket = ce.id_ticket
    GROUP BY 
        t.es_mantenimiento;
    """

    df = pd.read_sql(query, conn)
    conn.close()

    # Cambiar los valores de es_mantenimiento a etiquetas legibles
    df['es_mantenimiento'] = df['es_mantenimiento'].map({0: 'No Mantenimiento', 1: 'Mantenimiento'})

    return df
