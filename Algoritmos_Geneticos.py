import random
import string

# Parámetros del algoritmo genético
target = "HELLO WORLD"
population_size = 100
mutation_rate = 0.01
max_generations = 1000

def generate_random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + " ") for _ in range(length))

def calculate_fitness(text):
    return sum(1 for a, b in zip(text, target) if a == b)

def select_parents(population):
    # Selección de padres por torneo
    tournament_size = 5
    selected_parents = []
    for _ in range(population_size):
        tournament = random.sample(population, tournament_size)
        selected_parents.append(max(tournament, key=calculate_fitness))
    return selected_parents

def crossover(parent1, parent2):
    # Operador de cruce (crossover)
    crossover_point = random.randint(1, len(target) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def mutate(text):
    # Operación de mutación
    mutated_text = list(text)
    for i in range(len(mutated_text)):
        if random.random() < mutation_rate:
            mutated_text[i] = random.choice(string.ascii_uppercase + " ")
    return ''.join(mutated_text)

# Inicialización de la población
population = [generate_random_string(len(target)) for _ in range(population_size)]

for generation in range(max_generations):
    # Evaluar la aptitud de cada individuo en la población
    fitness_scores = [calculate_fitness(individual) for individual in population]

    # Comprobar si alguna cadena coincide con el objetivo
    best_fitness = max(fitness_scores)
    best_individual = population[fitness_scores.index(best_fitness)]
    
    if best_fitness == len(target):
        print(f"Generación {generation}: Encontrada la cadena: {best_individual}")
        break

    # Mostrar el mejor individuo de cada generación
    print(f"Generación {generation}: {best_individual} (Aptitud: {best_fitness}/{len(target)})")

    # Seleccionar padres
    parents = select_parents(population)

    # Generar una nueva población cruzando y mutando
    new_population = []
    while len(new_population) < population_size:
        parent1, parent2 = random.choices(parents, k=2)
        child = crossover(parent1, parent2)
        child = mutate(child)
        new_population.append(child)
    
    population = new_population

# Si no se encuentra la cadena objetivo después de todas las generaciones
if best_fitness < len(target):
    print("No se encontró la cadena 'HELLO WORLD' después de", max_generations, "generaciones.")
