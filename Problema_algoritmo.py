import random
import math

# Datos iniciales
conferencias = [
    {"nombre": "Conferencia 1", "duracion": 1.5, "horarioPreferido": "Mañana", "asientosDisponibles": 100},
    {"nombre": "Conferencia 2", "duracion": 1.0, "horarioPreferido": "Tarde", "asientosDisponibles": 80},
    {"nombre": "Conferencia 3", "duracion": 2.0, "horarioPreferido": "Noche", "asientosDisponibles": 120},
]
salas = {"Sala 1": 100, "Sala 2": 80, "Sala 3": 120}
horarios = ["Mañana", "Tarde", "Noche"]

# Funciones
def calculo_asistencia(programacion):
    return sum(min(salas[conf['sala']], conf['conferencia']['asientosDisponibles']) for conf in programacion)

def generar_programacion():
    return [
        {"conferencia": conf, "sala": random.choice(list(salas)), "horario": conf['horarioPreferido'], "asistentes": 0}
        for conf in conferencias
    ]

def optimizar_programacion(temperatura_inicial, enfriamiento):
    programacion_actual = generar_programacion()
    asistencia_actual = mejor_asistencia = calculo_asistencia(programacion_actual)
    mejor_programacion = programacion_actual[:]
    temperatura = temperatura_inicial

    while temperatura > 1:
        i, j = random.sample(range(len(conferencias)), 2)
        programacion_actual[i]["horario"], programacion_actual[j]["horario"] = programacion_actual[j]["horario"], programacion_actual[i]["horario"]
        nueva_asistencia = calculo_asistencia(programacion_actual)

        if (diferencia := nueva_asistencia - asistencia_actual) > 0 or random.random() < math.exp(diferencia / temperatura):
            asistencia_actual = nueva_asistencia
            if asistencia_actual > mejor_asistencia:
                mejor_programacion, mejor_asistencia = programacion_actual[:], asistencia_actual
        else:
            programacion_actual[i]["horario"], programacion_actual[j]["horario"] = programacion_actual[j]["horario"], programacion_actual[i]["horario"]

        temperatura *= enfriamiento

    return mejor_programacion

# Ejecución y presentación de resultados
def imprimir_tabla(programacion):
    encabezados = ["Conferencia", "Duración (h)", "Horario Pref.", "Asientos Disp.", "Sala Asignada", "Horario Asignado"]
    linea_separadora = "+".join(["-" * (len(encabezado) + 2) for encabezado in encabezados])

    print(linea_separadora)
    print("| " + " | ".join(encabezados) + " |")
    print(linea_separadora)

    for conf in programacion:
        conf_datos = conf['conferencia']
        fila = [
            conf_datos['nombre'],
            str(conf_datos['duracion']),
            conf_datos['horarioPreferido'],
            str(conf_datos['asientosDisponibles']),
            conf['sala'],
            conf['horario']
        ]
        print("| " + " | ".join([str(item).ljust(len(encabezados[i])) for i, item in enumerate(fila)]) + " |")
        print(linea_separadora)

temperatura_inicial = 1000
enfriamiento = 0.98
programacion_optima = optimizar_programacion(temperatura_inicial, enfriamiento)
imprimir_tabla(programacion_optima)
print("Asistencia total óptima:", calculo_asistencia(programacion_optima))

