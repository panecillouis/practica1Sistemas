from db import crear_tablas, insertar_cliente, insertar_ticket, insertar_tipo_incidente, insertar_empleado
from json_loader import cargar_datos_json
from data_processor import obtener_datos

def main():
    # Crear tablas si no existen
    crear_tablas()

    # Cargar los datos del archivo JSON
    data = cargar_datos_json()


     # Insertar los datos en la base de datos   
    for ticket in data["tickets_emitidos"]:
        insertar_ticket(ticket["cliente"], ticket["fecha_apertura"], ticket["fecha_cierre"],
                    ticket["es_mantenimiento"], ticket["satisfaccion_cliente"], ticket["tipo_incidencia"])
    for cliente in data["clientes"]:
        insertar_cliente(cliente["id_cli"], cliente["nombre"], cliente["telefono"], cliente["provincia"])

    # Insertar Tipos de Incidentes
    for tipo in data["tipos_incidentes"]:
        insertar_tipo_incidente(tipo["id_cli"], tipo["nombre"])
        
    for empleado in data["empleados"]:
        insertar_empleado(empleado["id_emp"], empleado["nombre"], empleado["nivel"], empleado["fecha_contrato"])
    # Consultar y obtener los datos en un DataFrame
    df = obtener_datos()
    print(df)

if __name__ == "__main__":
    main()
