import sqlite3
import pandas as pd

def obtener_datos():
    conn = sqlite3.connect('sistema_etl.db')
    query = '''
    SELECT t.id_ticket, t.fecha_apertura, t.fecha_cierre, t.es_mantenimiento, 
           t.satisfaccion_cliente, t.tipo_incidencia, c.nombre_cliente
    FROM Tickets t
    JOIN Clientes c ON t.cliente_id = c.id_cliente
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
