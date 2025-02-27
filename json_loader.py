import json

def cargar_datos_json():
    with open('datos.json', 'r') as file:
        data = json.load(file)
    return data
