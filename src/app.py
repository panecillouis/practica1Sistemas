from flask import Flask, render_template
import base64
import io
import matplotlib.pyplot as plt
from db import *
from json_loader import cargar_datos_json
from data_processor import *
import graficos
import matplotlib.pyplot as plt

app = Flask(__name__)

# Función para convertir un gráfico de matplotlib a una imagen base64
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.getbuffer()).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/estadisticas')
def estadisticas():
    # Obtener datos genéricos
    df = obtener_datos_generico()
    datos_genericos = {}
    for columna in df.columns:
        datos_genericos[columna] = df[columna].values[0]
    
    return render_template('estadisticas.html', datos=datos_genericos)

@app.route('/agrupaciones')
def agrupaciones():
    # Obtener datos agrupados
    df_agrupados = obtener_datos_agrupacion()
    return render_template('agrupaciones.html', datos_agrupados=df_agrupados)

@app.route('/graficos')
def visualizaciones():
    # Obtener datos necesarios para los gráficos
    df_mantenimiento = obtener_datos_mantenimiento()
    df_agrupados = obtener_datos_agrupacion()
    
    # Generar los gráficos y convertirlos a base64
    fig_media_duracion = graficos.graficar_media_duracion(df_mantenimiento, return_fig=True)
    img_media_duracion = fig_to_base64(fig_media_duracion)
    
    fig_boxplot = graficos.grafico_boxplot_incidente(df_agrupados, return_fig=True)
    img_boxplot = fig_to_base64(fig_boxplot)
    
    fig_clientes_criticos = graficos.mostrar_clientes_criticos(df_agrupados, return_fig=True)
    img_clientes_criticos = fig_to_base64(fig_clientes_criticos)
    
    fig_actuaciones_empleados = graficos.mostrar_empleados_actuaciones(df_agrupados, return_fig=True)
    img_actuaciones_empleados = fig_to_base64(fig_actuaciones_empleados)
    
    fig_actuaciones_dia = graficos.mostrar_actuaciones_por_dia(df_agrupados, return_fig=True)
    img_actuaciones_dia = fig_to_base64(fig_actuaciones_dia)
    
    return render_template('graficos.html', 
                          img_media_duracion=img_media_duracion,
                          img_boxplot=img_boxplot,
                          img_clientes_criticos=img_clientes_criticos,
                          img_actuaciones_empleados=img_actuaciones_empleados,
                          img_actuaciones_dia=img_actuaciones_dia)

@app.route('/inicializar')
def inicializar_db():
    # Crear tablas si no existen
    crear_tablas()
    
    # Cargar los datos del archivo JSON
    data = cargar_datos_json()
    
    # Insertar datos en la base de datos
    for ticket in data['tickets_emitidos']:
        id_ticket = insertar_ticket(ticket['cliente'], ticket['fecha_apertura'], 
                                ticket['fecha_cierre'], ticket['es_mantenimiento'], 
                                ticket['satisfaccion_cliente'], ticket['tipo_incidencia'])
    
        if 'contactos_con_empleados' in ticket:
            for contacto in ticket['contactos_con_empleados']:
                insertar_contacto_empleado(id_ticket, contacto['id_emp'], contacto['fecha'], contacto['tiempo'])
    
    for cliente in data["clientes"]:
        insertar_cliente(cliente["id_cli"], cliente["nombre"], cliente["telefono"], cliente["provincia"])

    for tipo in data["tipos_incidentes"]:
        insertar_tipo_incidente(tipo["id_cli"], tipo["nombre"])
        
    for empleado in data["empleados"]:
        insertar_empleado(empleado["id_emp"], empleado["nombre"], empleado["nivel"], empleado["fecha_contrato"])
    
    mensaje = "Base de datos inicializada correctamente."
    return render_template("inicializacion.html", mensaje=mensaje)

if __name__ == '__main__':
    app.run(debug=False)