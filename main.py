from db import crear_tablas, insertar_cliente, insertar_ticket, insertar_tipo_incidente, insertar_empleado, insertar_contacto_empleado
from json_loader import cargar_datos_json
from data_processor import obtener_datos_generico, obtener_datos_agrupacion
def main():
    # Crear tablas si no existen
    crear_tablas()

    # Cargar los datos del archivo JSON
    data = cargar_datos_json()

    
    for ticket in data['tickets_emitidos']:  # Itera sobre la lista de tickets
        id_ticket = insertar_ticket(ticket['cliente'], ticket['fecha_apertura'], 
                                ticket['fecha_cierre'], ticket['es_mantenimiento'], 
                                ticket['satisfaccion_cliente'], ticket['tipo_incidencia'])
    
        # Verificar si el ticket tiene contactos con empleados
        if 'contactos_con_empleados' in ticket:
            for contacto in ticket['contactos_con_empleados']:
                insertar_contacto_empleado(id_ticket, contacto['id_emp'], contacto['fecha'], contacto['tiempo'])

    
    for cliente in data["clientes"]:
        insertar_cliente(cliente["id_cli"], cliente["nombre"], cliente["telefono"], cliente["provincia"])

    # Insertar Tipos de Incidentes
    for tipo in data["tipos_incidentes"]:
        insertar_tipo_incidente(tipo["id_cli"], tipo["nombre"])
        
    for empleado in data["empleados"]:
        insertar_empleado(empleado["id_emp"], empleado["nombre"], empleado["nivel"], empleado["fecha_contrato"])
    
    # Consultar y obtener los datos en un DataFrame
    df = obtener_datos_generico()
    print("Datos genéricos:")
    for columna in df.columns:
        print(f"{columna}: {df[columna].values[0]}")
    
    df_agrupados = obtener_datos_agrupacion()
    print("\nDatos de agrupación:")
    for tipo in df_agrupados:
        print(f"\nDe tipo {tipo}:\n")
        print(df_agrupados[tipo])


if __name__ == "__main__":
    main()
